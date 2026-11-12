// =====================================================================
// Roundhead Island LIVE – Server
//  * liest Likes / Geschenke / Follows / Chat aus dem TikTok-LIVE (tiktok-live-connector, inoffiziell)
//  * schickt sie per WebSocket an das Spiel (game.html)
//  * Kommentator "Buergermeister Sam": Antworten per lokaler KI (Ollama), Stimme per edge-tts (Andrew)
// Start:  node server.js            -> echtes Live (TikTok-Name aus config.json)
//         node server.js --sim      -> Test mit Fake-Zuschauern (ohne TikTok), KI + Stimme laufen echt
// Dann im Browser / in TikTok LIVE Studio:  http://localhost:8787/live/game.html
// Keine Passwoerter / Schluessel noetig. Laeuft komplett lokal und kostenlos.
// =====================================================================
const http = require('http'), fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const { WebSocketServer } = require('ws');
const CFG = Object.assign({ tiktokUser: '', port: 8787, ollamaUrl: 'http://127.0.0.1:11434', ollamaModel: 'qwen2.5:7b', voice: 'en-US-AndrewMultilingualNeural', rate: '+8%', python: process.platform === 'win32' ? 'python' : 'python3' },
  fs.existsSync(path.join(__dirname, 'config.json')) ? JSON.parse(fs.readFileSync(path.join(__dirname, 'config.json'), 'utf8')) : {});
const SIM = process.argv.includes('--sim');
const ROOT = path.join(__dirname, '..');                   // mg/  (damit ../lib und fonts gefunden werden)
const TTS_DIR = path.join(__dirname, 'tts'); fs.mkdirSync(TTS_DIR, { recursive: true });
const log = (...a) => console.log(new Date().toLocaleTimeString('de-DE'), ...a);

// ---------------- Webserver + WebSocket ----------------
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.json': 'application/json', '.mp3': 'audio/mpeg', '.otf': 'font/otf', '.ttf': 'font/ttf', '.png': 'image/png', '.jpg': 'image/jpeg' };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]); if (p === '/') p = '/live/game.html';
  const f = p.startsWith('/tts/') ? path.join(TTS_DIR, path.basename(p)) : path.join(ROOT, path.normalize(p).replace(/^(\.\.[\/\\])+/, ''));
  if (!f.startsWith(ROOT) && !f.startsWith(TTS_DIR)) { res.writeHead(403); return res.end() }
  fs.readFile(f, (e, d) => { if (e) { res.writeHead(404); return res.end('nicht gefunden') } res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' }); res.end(d) });
});
const wss = new WebSocketServer({ server, path: '/ws' });
let GAME = {};                                               // letzter Spielstand vom Spiel
wss.on('connection', s => { log('Spiel verbunden'); s.on('message', m => { try { const e = JSON.parse(m); if (e.type === 'state') GAME = e.state } catch (x) { } }) });
const send = e => { const s = JSON.stringify(e); wss.clients.forEach(c => c.readyState === 1 && c.send(s)) };
server.listen(CFG.port, () => log(`Spiel: http://localhost:${CFG.port}/live/game.html`));

// ---------------- Filter ----------------
const BAD = /(hurensohn|fick|nazi|hitler|nutte|schlampe|wichser|spast|behindert|kys|kill yourself|suizid|selbstmord|nigg|porn|sex)/i;
const clean = s => String(s || '').replace(/https?:\/\/\S+/g, '').replace(/[^\p{L}\p{N}\s.,!?'’\-:;()€%]/gu, '').replace(/\s+/g, ' ').trim();
const nick = u => clean(u).slice(0, 20) || 'Gast';

// ---------------- Stimme (edge-tts, Andrew) ----------------
let ttsN = 0;
function tts(text) {
  return new Promise(res => {
    const f = `say_${Date.now()}_${ttsN++ % 50}.mp3`, out = path.join(TTS_DIR, f);
    const spoken = text.replace(/[_.]+(?=\w)/g, ' ').replace(/(\d+)/g, ' $1 ');   // Nutzernamen sprechbar machen
    const p = spawn(CFG.python, ['-m', 'edge_tts', '--voice', CFG.voice, '--rate', CFG.rate, '--text', spoken, '--write-media', out]);
    let done = false; const fin = ok => { if (!done) { done = true; res(ok && fs.existsSync(out) ? '/tts/' + f : null) } };
    p.on('close', c => fin(c === 0)); p.on('error', () => fin(false)); setTimeout(() => { p.kill(); fin(false) }, 15000);
  });
}
// alte Audiodateien aufraeumen
setInterval(() => { for (const f of fs.readdirSync(TTS_DIR)) { const p = path.join(TTS_DIR, f); if (Date.now() - fs.statSync(p).mtimeMs > 120000) fs.unlinkSync(p) } }, 60000);

// ---------------- KI (Ollama, lokal) ----------------
const SYSTEM = `Du bist "Bürgermeister Sam", der fröhliche Moderator eines TikTok-LIVE-Spiels namens "Roundhead Island".
Die Zuschauer bauen gemeinsam eine Insel: Doppelt tippen gibt Likes (Likes füllen die Stadt-Ziele, z. B. Brunnen, Leuchtturm, Riesenrad),
Folgen gibt ein eigenes Haus auf der Insel, Geschenke lassen das eigene Haus wachsen (bis zur Luxus-Villa). Wer "wo bin ich" schreibt, bekommt einen Pfeil zu seinem Haus.
Regeln: Antworte IMMER auf Deutsch, in höchstens 2 kurzen Sätzen (max. 25 Wörter), locker, witzig und freundlich, wie ein Moderator.
Sprich die Person mit ihrem Namen an. Keine Emojis, keine Hashtags, keine Links. Erfinde keine Zahlen – nutze nur den Spielstand.
Rede nicht über Politik, Religion, echte Personen, Gewalt, Sex oder Drogen; bei so etwas lenkst du freundlich zurück zur Insel.
Gib keine persönlichen Daten preis und frag nicht danach. Wenn jemand fies ist, ignorierst du es und bleibst nett.`;
async function llm(user, extra = '') {
  try {
    const r = await fetch(CFG.ollamaUrl + '/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: CFG.ollamaModel, stream: false, options: { temperature: .8, num_predict: 70 },
        messages: [{ role: 'system', content: SYSTEM + '\nSpielstand gerade: ' + JSON.stringify(GAME) + extra }, { role: 'user', content: user }] }) });
    const j = await r.json(); let t = clean(j.message && j.message.content);
    t = t.split(/(?<=[.!?])\s+/).slice(0, 2).join(' ').slice(0, 220);
    return t && !BAD.test(t) ? t : null;
  } catch (e) { return null }
}
// ---------------- Kommentator ----------------
const pickT = a => a[Math.floor(Math.random() * a.length)];
const TPL = {
  join: n => pickT([`Willkommen auf Roundhead Island, ${n}!`, `Hey ${n}, schön dass ihr da seid!`, `${n} – willkommen auf der Insel!`]),
  follow: n => pickT([`${n}, danke fürs Folgen! Dein eigenes Haus steht schon!`, `Neuer Einwohner: ${n}! Willkommen in deinem neuen Haus!`]),
  gift: (n, g) => pickT([`Wow, danke ${n} für ${g}! Dein Haus wächst!`, `${n}, du Legende! Danke für ${g}!`]),
  idle: () => pickT(['Doppelt tippen für Likes, dann bauen wir das nächste Wahrzeichen!', 'Folgen bringt dir ein eigenes Haus auf der Insel!', 'Schreibt „wo bin ich“, dann zeige ich euch euer Haus!', 'Geschenke lassen euer Haus wachsen, bis zur Luxus-Villa!'])
};
const Q = [];                  // Warteschlange {prio, make: async () => text}
let busyUntil = 0, lastSpoke = Date.now(), joinBuf = [], giftBuf = new Map();
function queue(prio, make) { if (Q.length > 6) Q.sort((a, b) => b.prio - a.prio).splice(5); Q.push({ prio, make, t: Date.now() }) }
async function loop() {
  const now = Date.now();
  if (now > busyUntil && Q.length) {
    Q.sort((a, b) => b.prio - a.prio || a.t - b.t); const job = Q.shift();
    if (now - job.t < 25000) {
      const text = await job.make();
      if (text) { const url = await tts(text); const dur = Math.max(2, text.length * .068); send({ type: 'say', text, url, dur }); busyUntil = Date.now() + dur * 1000 + 600; lastSpoke = Date.now(); log('SAM:', text) }
    }
  }
  // Beitritte sammeln (max. alle 20 s eine Begruessung fuer mehrere Namen)
  if (joinBuf.length && now - (loop.lastJoin || 0) > 20000) { const ns = joinBuf.splice(0, 3); joinBuf = []; loop.lastJoin = now; queue(1, async () => TPL.join(ns.join(', ').replace(/, ([^,]*)$/, ' und $1'))) }
  // Geschenke sammeln (pro Person zusammenfassen)
  for (const [n, g] of giftBuf) if (now - g.t > 2500) { giftBuf.delete(n); queue(3, async () => (await llm(`${n} hat gerade ${g.count}x ${g.gift} geschenkt. Bedanke dich kurz und sag, dass das Haus wächst.`)) || TPL.gift(n, g.gift)) }
  // Stille fuellen
  if (now - lastSpoke > 35000 && !Q.length && now > busyUntil) { lastSpoke = now; queue(0, async () => (await llm('Sag einen kurzen, lustigen Satz zur Insel und motiviere zum Liken, Folgen oder Fragen-Stellen.')) || TPL.idle()) }
  setTimeout(loop, 300);
}
loop();
function onEvent(e) {
  send(e);
  const n = nick(e.user);
  if (e.type === 'join') joinBuf.push(n);
  else if (e.type === 'follow') queue(2, async () => TPL.follow(n));
  else if (e.type === 'gift') { const g = giftBuf.get(n) || { gift: clean(e.gift) || 'das Geschenk', count: 0 }; g.count += e.repeat || 1; g.t = Date.now(); giftBuf.set(n, g) }
  else if (e.type === 'chat') {
    const txt = clean(e.text); if (!txt || BAD.test(txt) || BAD.test(n)) return;
    const isQ = /\?|wo bin ich|sam\b|bürgermeister|wie |was |wann |warum |kann ich|darf ich/i.test(txt);
    if (isQ) queue(2, async () => (await llm(`${n} schreibt im Chat: "${txt}". Antworte direkt.`)) || null);
  }
}
// ---------------- TikTok LIVE ----------------
async function tiktok() {
  if (!CFG.tiktokUser) { log('Kein TikTok-Name in config.json (tiktokUser) – nur Spiel/Kommentator laufen.'); return }
  let TL; try { TL = require('tiktok-live-connector') } catch (e) { log('tiktok-live-connector fehlt: npm install'); return }
  const Conn = TL.TikTokLiveConnection || TL.WebcastPushConnection;
  const c = new Conn(CFG.tiktokUser.replace(/^@/, ''));
  const on = (names, fn) => names.forEach(n => { try { c.on(n, fn) } catch (x) { } });
  const nm = d => (d.user && (d.user.nickname || d.user.uniqueId)) || d.nickname || d.uniqueId || 'Gast';
  on(['member'], d => onEvent({ type: 'join', user: nm(d) }));
  on(['like'], d => onEvent({ type: 'like', user: nm(d), count: d.likeCount || 1 }));
  on(['follow'], d => onEvent({ type: 'follow', user: nm(d) }));
  on(['chat'], d => onEvent({ type: 'chat', user: nm(d), text: d.comment || '' }));
  on(['gift'], d => { if (d.giftType === 1 && !d.repeatEnd) return;   // Combo-Geschenke erst am Ende zaehlen
    const gd = d.giftDetails || d.gift || {}; onEvent({ type: 'gift', user: nm(d), gift: d.giftName || gd.giftName || gd.name || 'Geschenk', diamonds: d.diamondCount || gd.diamondCount || 1, repeat: d.repeatCount || 1 }) });
  on(['streamEnd'], () => log('LIVE beendet.'));
  on(['disconnected'], () => { log('Verbindung weg – neuer Versuch in 15 s'); setTimeout(tiktok, 15000) });
  try { await c.connect(); log('Mit TikTok-LIVE von @' + CFG.tiktokUser + ' verbunden.') } catch (e) { log('TikTok-Verbindung fehlgeschlagen (ist das LIVE gestartet?):', e.message || e); setTimeout(tiktok, 20000) }
}
// ---------------- Simulation ----------------
if (SIM) {
  const N = ['lena.k', 'maxi_07', 'Jonas_HD', 'mia.lol', 'Luca.ftw', 'emil2009', 'sophie_xo', 'Noah.gg', 'paulinchen', 'Finn_der_Erste'];
  const C = ['wo bin ich', 'hallo sam', 'wie viel likes haben wir?', 'was bauen wir als nächstes?', 'kann ich bürgermeister werden?', 'warum ist mein haus so klein?'];
  setInterval(() => { const r = Math.random(), u = pickT(N);
    if (r < .25) onEvent({ type: 'join', user: u }); else if (r < .75) onEvent({ type: 'like', user: u, count: 1 + Math.floor(Math.random() * 10) });
    else if (r < .85) onEvent({ type: 'chat', user: u, text: pickT(C) }); else if (r < .9) onEvent({ type: 'follow', user: u }); else onEvent({ type: 'gift', user: u, gift: pickT(['Rose', 'Finger Heart', 'Donut']), diamonds: 5, repeat: 1 }) }, 700);
  log('SIMULATION läuft (Fake-Zuschauer).');
} else tiktok();
