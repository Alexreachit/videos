import asyncio, platform
import edge_tts, edge_tts.communicate as ec
from edge_tts.constants import TRUSTED_CLIENT_TOKEN as TOK
ec.WSS_URL = "wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1?Ocp-Apim-Subscription-Key=" + TOK
res = ["OS=" + platform.platform(), "edge_tts " + getattr(edge_tts, "__version__", "?")]
async def go():
    c = edge_tts.Communicate("This is a short test of the voice, with a few more words.", "en-US-AndrewMultilingualNeural", boundary="WordBoundary")
    a = w = 0
    async for ch in c.stream():
        if ch["type"] == "audio": a += len(ch["data"])
        elif ch["type"] == "WordBoundary": w += 1
    return a, w
try:
    a, w = asyncio.run(go()); res.append(f"PATCH OK audio={a} words={w}")
except Exception as e:
    res.append(f"PATCH FEHLER {type(e).__name__} {str(e)[:150]}")
print("::notice title=TTS-Patch::" + " | ".join(res))
