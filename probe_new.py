import asyncio, sys, platform, uuid, json, datetime
import aiohttp, ssl, certifi
from edge_tts.drm import DRM
from edge_tts.constants import TRUSTED_CLIENT_TOKEN
res=[]
def note(s):
    res.append(s); print(s, flush=True)
note("OS="+platform.platform())
def ts():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)")
def cfg():
    return (f"X-Timestamp:{ts()}\r\nContent-Type:application/json; charset=utf-8\r\nPath:speech.config\r\n\r\n"
      '{"context":{"synthesis":{"audio":{"metadataoptions":{"sentenceBoundaryEnabled":"false","wordBoundaryEnabled":"true"},"outputFormat":"audio-24khz-48kbitrate-mono-mp3"}}}}\r\n')
def ssml(rid):
    s=("<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'><voice name='en-US-AndrewMultilingualNeural'>"
       "<prosody pitch='+0Hz' rate='+0%' volume='+0%'>This is a short test of the voice.</prosody></voice></speak>")
    return f"X-RequestId:{rid}\r\nContent-Type:application/ssml+xml\r\nX-Timestamp:{ts()}Z\r\nPath:ssml\r\n\r\n{s}"
async def attempt(name, url_tpl, ver, origin, extra):
    rid=uuid.uuid4().hex
    url=url_tpl.format(tok=TRUSTED_CLIENT_TOKEN, cid=rid, gec=DRM.generate_sec_ms_gec(), ver=ver)
    ua=f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver.split('-')[1].split('.')[0]}.0.0.0 Safari/537.36 Edg/{ver.split('-')[1].split('.')[0]}.0.0.0"
    h={"Pragma":"no-cache","Cache-Control":"no-cache","User-Agent":ua,"Accept-Encoding":"gzip, deflate, br, zstd","Accept-Language":"en-US,en;q=0.9"}
    if origin: h["Origin"]=origin
    h.update(extra)
    h["Cookie"]="muid="+DRM.generate_muid()+";"
    try:
        async with aiohttp.ClientSession() as s:
            async with s.ws_connect(url, headers=h, compress=15, timeout=20, ssl=ssl.create_default_context(cafile=certifi.where())) as ws:
                await ws.send_str(cfg()); await ws.send_str(ssml(rid))
                n=0
                async for m in ws:
                    if m.type==aiohttp.WSMsgType.BINARY: n+=len(m.data)
                    elif m.type==aiohttp.WSMsgType.TEXT and "Path:turn.end" in m.data: break
                    elif m.type in (aiohttp.WSMsgType.CLOSED,aiohttp.WSMsgType.ERROR): break
                note(f"{name} OK bytes={n}")
    except aiohttp.WSServerHandshakeError as e:
        note(f"{name} HS {e.status}")
    except Exception as e:
        note(f"{name} ERR {type(e).__name__} {str(e)[:80]}")
async def main():
    old="wss://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1?TrustedClientToken={tok}&ConnectionId={cid}&Sec-MS-GEC={gec}&Sec-MS-GEC-Version={ver}"
    new="wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1?Ocp-Apim-Subscription-Key={tok}&ConnectionId={cid}&Sec-MS-GEC={gec}&Sec-MS-GEC-Version={ver}"
    new2="wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1?TrustedClientToken={tok}&ConnectionId={cid}&Sec-MS-GEC={gec}&Sec-MS-GEC-Version={ver}"
    ext="chrome-extension://jdiccldimpdaibmpdkjnbmckianbfold"
    for ver in ["1-155.0.3745.0","1-143.0.3650.75","1-140.0.3485.14"]:
        for nm,u in [("new",new),("new2",new2)]:
            for on,o in [("ext",ext),("none",None),("edge","https://edge.microsoft.com")]:
                await attempt(f"{nm}/{ver[2:5]}/{on}",u,ver,o,{})
    await attempt("old/155",old,"1-155.0.3745.0",ext,{})
asyncio.run(main())
note("fertig")
msg=" | ".join(res).replace("\n"," ")
print(f"::notice title=TTS-Neu {sys.platform}::{msg}")
