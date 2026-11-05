# Runde 4 (2026-11-05): ALLE deutschen Sprecher (de-DE/de-AT/de-CH) + alle Multilingual-Stimmen mit demselben deutschen Text
# fuer die Serie "Roundhead Island" (Alex will Stimme wie im FC-Asche-Video bzw. Auswahl aller deutschen Sprecher).
import asyncio, edge_tts, os, json
os.makedirs("output/voices", exist_ok=True)
for f in os.listdir("output/voices"): os.remove(os.path.join("output/voices", f))
TXT = "Tag eins: Ich habe gerade mein eigenes Land gegründet. Willkommen auf Roundhead Island! Und für jeden Like kommen zehn Euro in die Kasse."
async def main():
    vs = await edge_tts.list_voices()
    sel = [v for v in vs if v["Locale"].startswith("de-") or "Multilingual" in v["ShortName"]]
    info = []
    for v in sel:
        n = v["ShortName"]
        try:
            await edge_tts.Communicate(TXT, n, rate="+10%").save(f"output/voices/{n}.mp3"); ok = True
        except Exception as e:
            ok = False
        info.append({"name": n, "gender": v.get("Gender"), "locale": v["Locale"], "ok": ok,
                     "personalities": v.get("VoiceTag", {}).get("VoicePersonalities"), "categories": v.get("VoiceTag", {}).get("ContentCategories")})
    json.dump(info, open("output/voices/voices.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(info, indent=1, ensure_ascii=False))
asyncio.run(main())
