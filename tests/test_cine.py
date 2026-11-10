"""Tests der Kino-Pipeline. Laufen komplett kostenlos und offline (pytest -q tests/)."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from cine import cost
from cine.config import load_config
from cine.episode import EpisodeError, load_episode
from cine.pipeline import redo_scene, run_production
from cine.providers.base import ClipRequest, Ctx
from cine.providers.replicate import ReplicateVideo
from cine.stages import prompts, qc
from cine.state import Production

REPO = Path(__file__).resolve().parent.parent
EP1 = REPO / "episodes" / "zombie_ep01.yaml"
FREE = {"providers": {"video": "mock", "image": "mock", "sfx": "procedural", "vision_qc": "none"},
        "render": {"resolution": "360p"}}


@pytest.fixture()
def short_ep(tmp_path) -> Path:
    """Episode 1 auf drei kurze Szenen gekürzt – schnell, aber gleiche Struktur."""
    d = yaml.safe_load(EP1.read_text(encoding="utf-8"))
    d["id"] = "test_ep"
    d["scenes"] = d["scenes"][:3]
    for s, dur in zip(d["scenes"], (3, 4, 4)):
        s["duration"] = dur
        s["cues"] = [c for c in s.get("cues", []) if c["t"] <= dur]
    p = tmp_path / "test_ep.yaml"
    p.write_text(yaml.safe_dump(d, allow_unicode=True), encoding="utf-8")
    return p


def _ff(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *map(str, args)], check=True)


# --- Episode / Prompts --------------------------------------------------------------

def test_episode1_is_valid_and_60s():
    ep = load_episode(EP1)
    assert ep.total_duration == 60
    assert [s.beat for s in ep.scenes] == ["hook", "orientation", "threat", "escalation", "flight", "twist",
                                          "cliffhanger"]
    assert ep.scenes[0].duration <= 3, "Hook muss in den ersten Sekunden sitzen"


def test_episode_validation_catches_missing_fields(tmp_path):
    d = yaml.safe_load(EP1.read_text(encoding="utf-8"))
    del d["scenes"][1]["lighting"]
    p = tmp_path / "bad.yaml"
    p.write_text(yaml.safe_dump(d), encoding="utf-8")
    with pytest.raises(EpisodeError, match="lighting"):
        load_episode(p)


def test_prompts_contain_every_required_aspect():
    ep = load_episode(EP1)

    class V:
        supports_first_frame = True
        supports_references = True

    ps = prompts.build_all(ep, V())
    for s in ep.scenes:
        t = ps[s.id]["prompt"]
        for key in ("Scene:", "Time:", "Weather:", "Lighting:", "Camera:", "Movement:", "Visible:", "Zombies:",
                    "Action:", "Mood:", "Audio:", "Continuity:", "first-person POV"):
            assert key in t, f"{s.id}: {key} fehlt"
        assert ".." not in t
    assert not ps["s01"]["uses_first_frame"] and ps["s01"]["uses_refs"]
    assert all(ps[s.id]["uses_first_frame"] for s in ep.scenes[1:])
    assert "third-person" in ps["s01"]["negative"]


# --- Kosten / Freigabe ----------------------------------------------------------------

def test_estimate_paid_and_free():
    ep = load_episode(EP1)
    free = cost.estimate(ep, load_config(ep.settings, FREE))
    assert free["basis_usd"] == 0 and not free["kostenpflichtig"]
    paid = cost.estimate(ep, load_config(ep.settings, {"providers": {"video": "replicate", "image": "replicate"}}))
    assert paid["kostenpflichtig"]
    assert paid["basis_usd"] == pytest.approx(60 * 0.07 + 3 * 0.04, abs=0.01)
    assert paid["worst_case_usd"] > paid["mit_reserve_usd"] > paid["basis_usd"]
    assert len(paid["code"]) == 6


def test_paid_run_stops_before_spending_without_approval(short_ep, tmp_path, monkeypatch):
    monkeypatch.setenv("REPLICATE_API_TOKEN", "test-not-used")

    def boom(*a, **k):
        raise AssertionError("Es darf kein API-Aufruf passieren")

    monkeypatch.setattr("cine.providers.replicate.run_prediction", boom)
    res = run_production(short_ep, {"providers": {"video": "replicate", "image": "replicate"}}, base=tmp_path)
    assert res["status"] == "wartet auf Freigabe"
    assert Production("test_ep_replicate", base=tmp_path).data["spend_usd"] == 0


def test_guard_blocks_wrong_code_changed_plan_and_budget(short_ep, tmp_path):
    ep = load_episode(short_ep)
    cfg = load_config(ep.settings, {"providers": {"video": "replicate", "image": "replicate"}})
    prod = Production("g", base=tmp_path)
    est = cost.estimate(ep, cfg)
    cost.save_estimate(prod, est)
    with pytest.raises(cost.PaymentNotApproved):
        cost.approve(prod, "XXXXXX", 5)
    cost.approve(prod, est["code"], 1.0)
    guard = cost.CostGuard(prod, est["plan_hash"])
    guard.check(0.5, "ok")
    with pytest.raises(cost.PaymentNotApproved, match="Budget"):
        guard.check(1.5, "zu teuer")
    guard.commit(0.8, "verbraucht")
    with pytest.raises(cost.PaymentNotApproved):
        guard.check(0.5, "Rest reicht nicht")
    with pytest.raises(cost.PaymentNotApproved, match="geändert"):
        cost.CostGuard(prod, "anderer-plan").check(0.1, "x")


def test_replicate_provider_charges_only_after_guard(tmp_path, monkeypatch):
    """Mit Freigabe: richtige Eingaben, Kosten werden verbucht (API gemockt)."""
    monkeypatch.setenv("REPLICATE_API_TOKEN", "t")
    cfg = load_config({}, {"providers": {"video": "replicate"}})
    prod = Production("r", base=tmp_path)
    (prod.dir / "approval.json").write_text('{"plan_hash":"h","max_usd":5}')
    guard = cost.CostGuard(prod, "h")
    seen = {}

    def fake_run(model, inp, timeout_s=0):
        seen.update(model=model, inp=inp)
        return {"id": "p1", "status": "succeeded", "output": "https://example/x.mp4"}

    def fake_dl(url, out):
        _ff("-f", "lavfi", "-i", "color=c=gray:s=360x640:d=4", out)

    monkeypatch.setattr("cine.providers.replicate.run_prediction", fake_run)
    monkeypatch.setattr("cine.providers.replicate._download", fake_dl)
    img = tmp_path / "f.jpg"
    _ff("-f", "lavfi", "-i", "color=c=red:s=64x64", "-frames:v", "1", img)
    v = ReplicateVideo(Ctx(cfg, prod, guard, 720, 1280))
    meta = v.generate(ClipRequest("s02", "p", "n", 4, first_frame=img), tmp_path / "o.mp4")
    assert seen["model"] == "google/gemini-omni-1.2-flash"
    assert seen["inp"]["duration"] == 4 and seen["inp"]["aspect_ratio"] == "9:16"
    assert seen["inp"]["image"].startswith("data:image/jpeg;base64,") and "reference_images" not in seen["inp"]
    assert meta["usd"] == pytest.approx(0.28)
    assert prod.data["spend_usd"] == pytest.approx(0.28)


# --- Qualitätskontrolle ---------------------------------------------------------------

QCFG = load_config()["qc"]


def test_qc_flags_black_and_frozen_clip(tmp_path):
    clip = tmp_path / "black.mp4"
    _ff("-f", "lavfi", "-i", "color=c=black:s=360x640:d=4:r=24", "-pix_fmt", "yuv420p", clip)
    r = qc.check_clip(clip, 4, 360, 640, QCFG)
    assert not r["checks"]["schwarzbilder"] and not r["checks"]["eingefroren"]
    assert r["score"] < QCFG["min_scene_score"]


def test_qc_flags_hard_cut_inside_pov_clip(tmp_path):
    a, b, clip = tmp_path / "a.mp4", tmp_path / "b.mp4", tmp_path / "cut.mp4"
    _ff("-f", "lavfi", "-i", "testsrc2=s=360x640:d=2:r=24", "-pix_fmt", "yuv420p", a)
    _ff("-f", "lavfi", "-i", "mandelbrot=s=360x640:r=24", "-t", "2", "-pix_fmt", "yuv420p", b)
    _ff("-i", a, "-i", b, "-filter_complex", "[0:v][1:v]concat=n=2:v=1[v]", "-map", "[v]", clip)
    r = qc.check_clip(clip, 4, 360, 640, QCFG)
    assert not r["checks"]["pov_ohne_schnitt"], r["metrics"]


def test_qc_flags_wrong_aspect_and_short_clip(tmp_path):
    clip = tmp_path / "wide.mp4"
    _ff("-f", "lavfi", "-i", "testsrc2=s=640x360:d=2:r=24", "-pix_fmt", "yuv420p", clip)
    r = qc.check_clip(clip, 6, 360, 640, QCFG)
    assert not r["checks"]["seitenverhaeltnis"] and not r["checks"]["dauer"]


# --- Ende-zu-Ende (kostenlos) -----------------------------------------------------------

def test_end_to_end_mock_resume_and_redo(short_ep, tmp_path):
    res = run_production(short_ep, FREE, base=tmp_path)
    assert res["status"] == "fertig", res
    prod = Production("test_ep_mock", base=tmp_path)
    final = Path(res["video"])
    info = qc.media_info(final)
    assert info["duration"] == pytest.approx(11, abs=0.2)
    assert (info["width"], info["height"]) == (360, 640) and info["has_audio"]
    assert res["qc"]["issues"] == [], res["qc"]
    assert (prod.dir / "output" / "bericht.md").exists()
    assert (prod.dir / "dashboard.html").exists() and (tmp_path / "index.html").exists()
    # Fortsetzen: nichts wird neu generiert
    mt = {s: (prod.dir / "clips" / f"{s}.mp4").stat().st_mtime for s in ("s01", "s02", "s03")}
    run_production(short_ep, FREE, base=tmp_path)
    assert mt == {s: (prod.dir / "clips" / f"{s}.mp4").stat().st_mtime for s in mt}
    # Nur Szene s02 neu
    res2 = redo_scene(short_ep, "s02", FREE, base=tmp_path)
    assert res2["status"] == "fertig"
    after = {s: (prod.dir / "clips" / f"{s}.mp4").stat().st_mtime for s in mt}
    assert after["s01"] == mt["s01"] and after["s03"] == mt["s03"] and after["s02"] != mt["s02"]


def test_manual_free_path_handoff_then_ingest(short_ep, tmp_path):
    over = {"providers": {"video": "manual", "image": "mock", "sfx": "procedural", "vision_qc": "none"},
            "render": {"resolution": "360p"}}
    res = run_production(short_ep, over, base=tmp_path)
    assert res["status"] == "wartet auf Clips"
    prod = Production("test_ep_manual", base=tmp_path)
    card = prod.dir / "handoff" / "s01.md"
    assert card.exists() and "Prompt" in card.read_text(encoding="utf-8")
    # Nutzer legt Clips ab (hier simuliert mit Mock-Clips)
    mock = run_production(short_ep, FREE, base=tmp_path / "m")
    for s in ("s01", "s02", "s03"):
        shutil.copy2(tmp_path / "m" / "test_ep_mock" / "clips" / f"{s}.mp4", prod.dir / "inbox" / f"{s}.mp4")
        run_production(short_ep, over, base=tmp_path)  # Szene für Szene, wie im echten Ablauf
    res = run_production(short_ep, over, base=tmp_path)
    assert res["status"] == "fertig", res
    assert mock["status"] == "fertig"
    # Startbild der Folgeszene stammt aus dem Ende der Vorszene
    assert (prod.dir / "handoff" / "s02_startbild.jpg").exists()


def test_qc_flags_nearly_black_clip(tmp_path):
    """Fast schwarzes Bild mit kleinem hellem Fleck (früherer Platzhalter) darf nicht durchkommen."""
    clip = tmp_path / "dark.mp4"
    _ff("-f", "lavfi", "-i", "color=c=0x0c0e12:s=360x640:d=4:r=24", "-vf", "noise=alls=20:allf=t",
        "-pix_fmt", "yuv420p", clip)
    r = qc.check_clip(clip, 4, 360, 640, QCFG)
    assert not r["checks"]["helligkeit"]
    assert r["score"] < QCFG["min_scene_score"]
