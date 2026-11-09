"""Befehlszeile:

  python -m cine plan     episodes/zombie_ep01.yaml            Szenenplan + Prompts anzeigen (kostenlos)
  python -m cine estimate episodes/zombie_ep01.yaml --video replicate   Kosten schätzen, Freigabe-Code
  python -m cine approve  episodes/zombie_ep01.yaml --video replicate --code ABC123 --max-usd 8
  python -m cine run      episodes/zombie_ep01.yaml [--video mock|manual|replicate]
  python -m cine redo     episodes/zombie_ep01.yaml --scene s04  [--video …]
  python -m cine status   [produktion]
  python -m cine serve                                         Dashboard im Browser
"""
from __future__ import annotations

import argparse
import json
import sys

from . import cost
from .config import load_config, load_env_file
from .dashboard import serve, write_dashboards
from .episode import load_episode
from .pipeline import production_id, redo_scene, run_production, save_prompts, write_plan
from .providers import get_video
from .providers.base import Ctx
from .stages import prompts
from .state import PRODUCTIONS, Production
from .util import read_json, setup_logging


def _overrides(a) -> dict:
    o: dict = {"providers": {}}
    for k in ("video", "image", "sfx", "vision"):
        v = getattr(a, k, None)
        if v:
            o["providers"]["vision_qc" if k == "vision" else k] = v
    if getattr(a, "video", None) in ("replicate",) and not getattr(a, "image", None):
        o["providers"]["image"] = "replicate"
    if getattr(a, "video", None) == "manual" and not getattr(a, "image", None):
        o["providers"]["image"] = "manual"
    if getattr(a, "resolution", None):
        o["render"] = {"resolution": a.resolution}
    if getattr(a, "aspect", None):
        o.setdefault("render", {})["aspect"] = a.aspect
    return o


def main(argv=None) -> int:
    load_env_file()
    setup_logging()
    ap = argparse.ArgumentParser(prog="cine", description="KI-Kinopipeline")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, episode=True):
        if episode:
            p.add_argument("episode")
        p.add_argument("--video", choices=["mock", "manual", "replicate"])
        p.add_argument("--image", choices=["mock", "manual", "replicate"])
        p.add_argument("--sfx", choices=["procedural", "elevenlabs"])
        p.add_argument("--vision", choices=["none", "gemini"])
        p.add_argument("--resolution", choices=["360p", "720p", "1080p"])
        p.add_argument("--aspect", choices=["9:16", "16:9"])
        p.add_argument("--id", help="Produktions-ID (Standard: <episode>_<videoanbieter>)")

    for name in ("plan", "estimate", "run"):
        common(sub.add_parser(name))
    p = sub.add_parser("approve")
    common(p)
    p.add_argument("--code", required=True)
    p.add_argument("--max-usd", type=float, required=True)
    p = sub.add_parser("redo")
    common(p)
    p.add_argument("--scene", required=True)
    p = sub.add_parser("status")
    p.add_argument("production", nargs="?")
    p = sub.add_parser("serve")
    p.add_argument("--port", type=int, default=8765)
    a = ap.parse_args(argv)

    if a.cmd == "serve":
        serve(a.port)
        return 0
    if a.cmd == "status":
        if a.production:
            st = read_json(PRODUCTIONS / a.production / "state.json", {})
            print(json.dumps({k: st.get(k) for k in ("id", "status", "current", "spend_usd")}, ensure_ascii=False, indent=1))
        else:
            for d in sorted(PRODUCTIONS.glob("*/state.json")):
                st = read_json(d, {})
                print(f"{st.get('id'):40} {st.get('status'):22} {st.get('spend_usd', 0):6.2f} $  {st.get('current', '')}")
        print(write_dashboards())
        return 0

    ep = load_episode(a.episode)
    over = _overrides(a)
    cfg = load_config(ep.settings, over)
    pid = a.id or production_id(ep, cfg)

    if a.cmd == "plan":
        prod = Production(pid)
        plan = write_plan(ep, prod, cfg)
        ctx = Ctx(cfg, prod, None, 0, 0)
        ps = prompts.build_all(ep, get_video(cfg["providers"]["video"], ctx))
        save_prompts(prod, ps)
        print((prod.dir / "plan.md").read_text(encoding="utf-8"))
        first = ep.scenes[0].id
        print(f"--- Prompt {first} ---\n{ps[first]['prompt']}\n")
        print(f"Alle Prompts: {prod.dir / 'prompts'}")
        return 0
    if a.cmd == "estimate":
        prod = Production(pid)
        est = cost.estimate(ep, cfg)
        cost.save_estimate(prod, est)
        print(cost.format_estimate(est))
        return 0
    if a.cmd == "approve":
        prod = Production(pid)
        est = cost.estimate(ep, cfg)
        cost.save_estimate(prod, est)
        appr = cost.approve(prod, a.code, a.max_usd)
        print(f"Freigegeben: bis {appr['max_usd']:.2f} USD für {pid} (Code {appr['code']})")
        return 0
    if a.cmd == "redo":
        res = redo_scene(a.episode, a.scene, over, pid)
    else:
        res = run_production(a.episode, over, pid)
    print(json.dumps({k: v for k, v in res.items() if k != "estimate"}, ensure_ascii=False, indent=1, default=str))
    if res["status"] == "wartet auf Freigabe":
        print("\n" + cost.format_estimate(res["estimate"]))
    return 0 if res["status"] in ("fertig", "wartet auf Clips", "wartet auf Freigabe") else 2


if __name__ == "__main__":
    sys.exit(main())
