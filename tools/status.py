"""Pflegt status/agents.json (wird vom lokalen Control Center alle 20 s gelesen).
python tools/status.py work "<Agent>" "<Aufgabe>"   |  done "<Agent>" "<Ergebnis>"  |  log "<Agent>" "<Text>"  |  idle-all"""
import json, sys, time
from pathlib import Path
P = Path(__file__).resolve().parent.parent / "status" / "agents.json"
st = json.loads(P.read_text(encoding="utf-8")) if P.exists() else {"agents": {}, "log": []}
cmd = sys.argv[1]; now = time.time()
def log(a, m): st["log"] = (st.get("log", []) + [{"id": f"{now:.3f}-{a}", "agent": a, "msg": m, "ts": now}])[-60:]
if cmd == "work":
    st["agents"][sys.argv[2]] = {"status": "arbeitet", "task": sys.argv[3], "since": now}; log(sys.argv[2], "startet: " + sys.argv[3])
elif cmd == "done":
    st["agents"][sys.argv[2]] = {"status": "idle", "result": sys.argv[3], "since": now}; log(sys.argv[2], "fertig: " + sys.argv[3])
elif cmd == "log":
    log(sys.argv[2], sys.argv[3])
elif cmd == "idle-all":
    for a in st["agents"].values(): a["status"] = "idle"
st["updated"] = now
P.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")
