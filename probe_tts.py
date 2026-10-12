import asyncio, sys, platform, os, urllib.request, ssl, time
res = []
def note(s):
    res.append(s); print(s, flush=True)
note(f"OS={platform.platform()}")
try:
    import edge_tts
    note("edge_tts version " + getattr(edge_tts, "__version__", "?"))
except Exception as e:
    note("import fehler " + repr(e)); 
async def go():
    c = edge_tts.Communicate("This is a short test of the voice.", "en-US-AndrewMultilingualNeural")
    n = 0
    async for ch in c.stream():
        if ch["type"] == "audio": n += len(ch["data"])
    return n
for i in range(2):
    try:
        n = asyncio.run(go()); note(f"EDGE OK bytes={n}"); break
    except Exception as e:
        note(f"EDGE FEHLER {type(e).__name__}: {str(e)[:300]}"); time.sleep(3)
try:
    r = urllib.request.urlopen("https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/voices/list?trustedclienttoken=6A5AA1D4EAFF4E9FB37E23D68491D6F4", timeout=20)
    note(f"VOICELIST HTTP {r.status}")
except Exception as e:
    note(f"VOICELIST FEHLER {type(e).__name__}: {str(e)[:200]}")
msg = " | ".join(res).replace("\n", " ")
print(f"::notice title=TTS-Probe {sys.platform}::{msg}")
