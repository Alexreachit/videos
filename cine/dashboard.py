"""Statusübersicht als HTML (productions/index.html + productions/<id>/dashboard.html).

`python -m cine serve` startet zusätzlich einen kleinen lokalen Server
(http://localhost:8765), über den man kostenlose Läufe starten kann.
Kostenpflichtige Läufe sind dort bewusst NICHT startbar – die brauchen die
Freigabe über `approve` bzw. den GitHub-Workflow.
"""
from __future__ import annotations

import html
import json
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .state import PRODUCTIONS
from .util import read_json

CSS = """
:root{--bg:#0e1013;--card:#171a1f;--ink:#e8e6e3;--mut:#8b9099;--ok:#4caf7a;--warn:#e0a63a;--bad:#e05a4f;--line:#262a31}
@media (prefers-color-scheme: light){:root:not([data-theme=dark]){--bg:#f4f3f0;--card:#fff;--ink:#1b1c1e;--mut:#666b73;--line:#e2e0db}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,sans-serif}
main{max-width:1100px;margin:0 auto;padding:24px 16px}h1{font-size:24px;margin:0 0 4px}h2{font-size:17px;margin:28px 0 10px}
.mut{color:var(--mut)}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}.k{font-size:12px;color:var(--mut);text-transform:uppercase;letter-spacing:.04em}
.v{font-size:22px;font-weight:650}table{width:100%;border-collapse:collapse}td,th{padding:8px 6px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{font-size:12px;color:var(--mut);font-weight:600}.pill{display:inline-block;padding:1px 8px;border-radius:99px;font-size:12px;border:1px solid var(--line)}
.ok{color:var(--ok)}.warn{color:var(--warn)}.bad{color:var(--bad)}img.sheet{width:150px;border-radius:6px;display:block}
.wrap{overflow-x:auto}video{max-width:320px;width:100%;border-radius:10px;background:#000}
button{background:var(--ink);color:var(--bg);border:0;border-radius:8px;padding:8px 14px;font-weight:600;cursor:pointer}
select{padding:7px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink)}
"""


def _e(x) -> str:
    return html.escape(str(x))


def _score_cls(s) -> str:
    return "ok" if s >= 70 else ("warn" if s >= 50 else "bad")


def production_html(pdir: Path) -> str:
    st = read_json(pdir / "state.json", {})
    est = read_json(pdir / "estimate.json", {}) or {}
    appr = read_json(pdir / "approval.json", {}) or {}
    plan = read_json(pdir / "plan.json", {}) or {}
    scenes = plan.get("scenes", [])
    rows = []
    for sc in scenes:
        sid = sc["id"]
        s = st.get("scenes", {}).get(sid, {})
        clip, q = s.get("clips", {}), s.get("qc_clips", {})
        score = q.get("score")
        sheet = q.get("sheet")
        rows.append(
            f"<tr><td><b>{_e(sid)}</b><div class=mut>{_e(sc['beat'])} · {sc['duration']}s</div></td>"
            f"<td>{_e(clip.get('status', '–'))}<div class=mut>{_e(clip.get('model', clip.get('provider', '')))}"
            f"{' · Versuch ' + str(clip.get('attempt')) if clip.get('attempt') else ''}</div></td>"
            f"<td>{f'<span class={_score_cls(score)}>{score}</span>' if score is not None else '–'}</td>"
            f"<td>{'<br>'.join(_e(i) for i in q.get('issues', [])) or _e(clip.get('note', ''))}</td>"
            f"<td>{f'<img class=sheet src={_e(sheet)}>' if sheet else ''}</td></tr>")
    fin = st.get("steps", {}).get("qc_final", {})
    out = pdir / "output"
    videos = sorted(out.glob("*.mp4")) if out.exists() else []
    ev = "".join(f"<tr><td class=mut>{time.strftime('%d.%m. %H:%M', time.localtime(e['ts']))}</td>"
                 f"<td class={'warn' if e['level'] != 'info' else ''}>{_e(e['msg'])}</td></tr>"
                 for e in reversed(st.get("events", [])[-25:]))
    prov = plan.get("providers", {})
    return f"""<!doctype html><html lang=de><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>{_e(plan.get('title', st.get('id', 'Produktion')))}</title><style>{CSS}</style></head><body><main>
<p class=mut><a href="../index.html" style="color:inherit">← alle Produktionen</a></p>
<h1>{_e(plan.get('title', st.get('id')))}</h1><div class=mut>{_e(st.get('id'))} · Stand {time.strftime('%d.%m.%Y %H:%M', time.localtime(st.get('updated', time.time())))}</div>
<h2>Status</h2><div class=grid>
<div class=card><div class=k>Status</div><div class=v>{_e(st.get('status', '–'))}</div><div class=mut>{_e(st.get('current', ''))}</div></div>
<div class=card><div class=k>Ausgegeben</div><div class=v>{st.get('spend_usd', 0):.2f} $</div><div class=mut>freigegeben: {appr.get('max_usd', 0):.2f} $</div></div>
<div class=card><div class=k>Schätzung</div><div class=v>{est.get('basis_usd', 0):.2f} $</div><div class=mut>mit Reserve {est.get('mit_reserve_usd', 0):.2f} $</div></div>
<div class=card><div class=k>Gesamt-QC</div><div class=v>{fin.get('score', '–')}</div><div class=mut>{_e('; '.join(fin.get('issues', [])) or '')}</div></div>
</div>
<h2>Modelle</h2><div class=card>Video: <b>{_e(prov.get('video'))}</b> · Bilder: <b>{_e(prov.get('image'))}</b> · Sound: <b>{_e(prov.get('sfx'))}</b> · KI-Prüfung: <b>{_e(prov.get('vision_qc'))}</b></div>
<h2>Szenen</h2><div class="card wrap"><table><tr><th>Szene</th><th>Clip</th><th>QC</th><th>Hinweise</th><th>Kontaktblatt</th></tr>{''.join(rows)}</table></div>
<h2>Fertige Videos</h2><div class=card>{''.join(f'<p><video controls src="output/{_e(v.name)}"></video><br><a href="output/{_e(v.name)}">{_e(v.name)}</a></p>' for v in videos) or '<span class=mut>noch keins</span>'}</div>
<h2>Protokoll</h2><div class="card wrap"><table>{ev}</table></div>
</main></body></html>"""


def write_dashboards(base: Path | None = None, server: bool = False) -> Path:
    base = base or PRODUCTIONS
    base.mkdir(parents=True, exist_ok=True)
    items = []
    for d in sorted(p for p in base.iterdir() if (p / "state.json").exists()):
        (d / "dashboard.html").write_text(production_html(d), encoding="utf-8")
        st = read_json(d / "state.json", {})
        plan = read_json(d / "plan.json", {}) or {}
        items.append(f"<tr><td><a href='{_e(d.name)}/dashboard.html'>{_e(plan.get('title', d.name))}</a>"
                     f"<div class=mut>{_e(d.name)}</div></td><td>{_e(st.get('status'))}</td>"
                     f"<td>{st.get('spend_usd', 0):.2f} $</td></tr>")
    eps = sorted((Path(__file__).resolve().parent.parent / "episodes").glob("*.yaml"))
    start = ""
    if server:
        opts = "".join(f"<option>{_e(e.name)}</option>" for e in eps)
        start = f"""<h2>Neue Produktion (kostenlos)</h2><div class=card><form method=post action=/start>
<select name=episode>{opts}</select> <select name=video><option value=mock>Testlauf (Platzhalter)</option>
<option value=manual>Gratis-Weg (Prompt-Karten / eigene Clips)</option></select> <button>Starten</button></form>
<p class=mut>Kostenpflichtige Läufe: erst <code>estimate</code>, dann <code>approve</code> (oder GitHub-Workflow mit Freigabe-Code).</p></div>"""
    (base / "index.html").write_text(f"""<!doctype html><html lang=de><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Kino-Pipeline</title><style>{CSS}</style>
{'<meta http-equiv=refresh content=10>' if server else ''}</head><body><main><h1>Kino-Pipeline</h1>
<div class=mut>Produktionen</div>{start}<h2>Übersicht</h2><div class=card><table><tr><th>Produktion</th><th>Status</th><th>Kosten</th></tr>
{''.join(items) or '<tr><td class=mut>noch keine</td></tr>'}</table></div></main></body></html>""", encoding="utf-8")
    return base / "index.html"


def serve(port: int = 8765) -> None:
    from urllib.parse import parse_qs

    from .pipeline import run_production

    base = PRODUCTIONS
    write_dashboards(base, server=True)

    class H(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(base), **kw)

        def do_GET(self):
            write_dashboards(base, server=True)
            return super().do_GET()

        def do_POST(self):
            if self.path != "/start":
                self.send_error(404)
                return
            q = parse_qs(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode())
            ep = q.get("episode", [""])[0]
            video = q.get("video", ["mock"])[0]
            if video not in ("mock", "manual"):
                self.send_error(403, "Nur kostenlose Läufe über das Dashboard")
                return
            ep_path = Path(__file__).resolve().parent.parent / "episodes" / Path(ep).name
            over = {"providers": {"video": video, "image": video, "sfx": "procedural", "vision_qc": "none"}}
            threading.Thread(target=run_production, args=(ep_path,), kwargs={"overrides": over}, daemon=True).start()
            self.send_response(303)
            self.send_header("Location", "/index.html")
            self.end_headers()

        def log_message(self, *a):
            pass

    print(f"Dashboard: http://localhost:{port}/index.html  (Strg+C beendet)")
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()


if __name__ == "__main__":
    print(json.dumps(str(write_dashboards())))
