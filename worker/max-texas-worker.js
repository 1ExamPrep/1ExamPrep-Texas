// Max, the Texas exam advisor for passyourtexascontractorexam.com. Cloudflare Worker "1exam-texas".
// Paste this whole file into the Cloudflare Worker editor (Workers & Pages > 1exam-texas > Edit code), replacing everything, then Deploy.
// Needs one binding: Settings > Bindings > Add > Workers AI, variable name AI.
// Products and facts are read from the site itself (shared/kb/products.json and shared/kb/texas.json), so a site build updates Max.

const DEFAULTS = {
  ALLOWED_ORIGINS: "https://passyourtexascontractorexam.com,https://www.passyourtexascontractorexam.com,https://1examprep.github.io",
  SITE_BASE: "https://passyourtexascontractorexam.com/",
  AI_MODEL: "@cf/google/gemma-4-26b-a4b-it",
  AI_BACKUP_MODEL: "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
  DEBUG_KEY: "tx-6c41e9b2f07d"
};

const TTL_MS = 60 * 60 * 1000;
const memo = new Map();

// ---------- loading the site's knowledge ----------
async function loadJson(url) {
  const hit = memo.get(url);
  if (hit && Date.now() - hit.at < hit.ttl) return hit.data;
  let data = null;
  try {
    const res = await fetch(url, { cf: { cacheTtl: 3600, cacheEverything: true } });
    if (res.ok) data = await res.json();
  } catch {}
  memo.set(url, { at: Date.now(), data, ttl: data ? TTL_MS : 60 * 1000 });
  return data;
}
function siteBase(raw, origin) {
  try {
    const u = new URL(raw), o = new URL(origin);
    if (u.protocol !== "https:" || u.host !== o.host) return null;
    return u.origin + u.pathname.replace(/[^/]*$/, "");
  } catch { return null; }
}

// ---------- understanding what people typed ----------
function lev(a, b) {
  if (a === b) return 0;
  if (Math.abs(a.length - b.length) > 2) return 9;
  const d = [];
  for (let i = 0; i <= a.length; i++) d[i] = [i];
  for (let j = 1; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++) {
    d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
  }
  return d[a.length][b.length];
}
const FIX_WORDS = ["journeyman", "master", "electrician", "electrical", "plumber", "plumbing", "refrigeration", "technician", "wireman", "lineman",
  "inspector", "industrial", "maintenance", "appliance", "license", "requirements", "experience", "enforcement", "contractor", "residential"];
function fixTypos(text) {
  return String(text || "").replace(/[A-Za-z]{5,}/g, (w) => {
    const l = w.toLowerCase();
    if (FIX_WORDS.includes(l)) return w;
    if (/^jour/.test(l) || l === "jman") return "journeyman";
    for (const f of FIX_WORDS) if (lev(l, f) <= (f.length >= 7 ? 2 : 1)) return f;
    return w;
  });
}
function norm(text) { return " " + fixTypos(text).toLowerCase().replace(/a\/c/g, "ac").replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ") + " "; }
function guessTrade(t) {
  if (/ (electric\w*|wireman|lineman|nec) /.test(t)) return "electrical";
  if (/ (plumb\w*|tsbpe) /.test(t)) return "plumbing";
  if (/ (hvac|ac|air condition\w*|refrigerat\w*|acr|heating) /.test(t)) return "acr";
  return null;
}
function guessLicense(text, licenses, trade) {
  const t = norm(text);
  let best = null, len = 0;
  for (const l of licenses) for (const a of l.a || []) {
    const p = " " + a.toLowerCase().replace(/a\/c/g, "ac").replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim() + " ";
    if (p.length > len && t.includes(p)) { best = l.s; len = p.length; }
  }
  if (best) return best;
  const tr = guessTrade(t) || trade;
  const j = / journeyman /.test(t), m = / master /.test(t);
  if (tr === "electrical") return m ? "master-electrician" : j ? "journeyman-electrician" : null;
  if (tr === "plumbing") return m ? "master-plumber" : j ? "journeyman-plumber" : null;
  if (tr === "acr") return / class a /.test(t) ? "environmental-air-class-a" : / class b /.test(t) ? "environmental-air-class-b" : null;
  return null;
}
function isQuestion(text) {
  const t = norm(text);
  return /\?/.test(text) || /^ (how|what|when|where|why|who|which|is|are|can|could|do|does|did|should|will|would|if) /.test(t) ||
    / (how many|how much|how long|do i need|requirements?|qualif\w*|hours|years|open book|closed book|allowed|pass\w* score|renew\w*|fee|fees|cost) /.test(t);
}
function wantsProducts(text) {
  return / (buy|order|recommend|suggest|which package|what package|which one should|what should i (get|buy)|show me|cheapest|best package|price|prices|in stock) /.test(norm(text));
}

// ---------- picking facts ----------
const KB_STOP = new Set("a an the and or of to in on for is are am be do does did i im my me we you your it its this that what which who how when where why can could would should will with from at by as about if so get need want exam test license licence texas".split(" "));
const SYN = {
  year: ["experience", "years", "hours"], years: ["experience", "hours"], experience: ["years", "hours"], hours: ["experience", "years"],
  book: ["books", "reference", "open", "allowed"], books: ["reference", "open", "allowed"], bring: ["allowed", "open", "tabs"], tabs: ["tabs", "publisher", "nec"],
  open: ["open", "closed", "allowed"], closed: ["closed", "open"], pass: ["passing", "score"], score: ["passing"], questions: ["items", "minutes"],
  long: ["minutes", "time"], time: ["minutes"], fee: ["fees", "cost", "costs"], cost: ["fee", "fees", "costs"], price: ["prices", "runs"],
  renew: ["renewal", "continuing", "education"], apply: ["application", "tdlr", "tsbpe"], who: ["tdlr", "tsbpe", "issues"], code: ["nec", "ipc", "upc", "imc"]
};
function toks(text) { return norm(text).trim().split(" ").filter((w) => w.length > 1 && !KB_STOP.has(w)); }
function pickFacts(pieces, question, slots, max = 4, maxChars = 3200) {
  const base = toks(question);
  if (!base.length) return [];
  const words = new Map();
  for (const w of base) { words.set(w, 2); for (const x of SYN[w] || []) if (!words.has(x)) words.set(x, 1); }
  const df = new Map();
  const docs = pieces.map((p) => {
    p._k = p._k || new Set((p.k || "").split(" ")); p._h = p._h || new Set((p.kh || "").split(" "));
    for (const w of words.keys()) if (p._k.has(w)) df.set(w, (df.get(w) || 0) + 1);
    return p;
  });
  const N = docs.length;
  const scored = docs.map((p) => {
    let sc = 0;
    for (const [w, wt] of words) if (p._k.has(w)) sc += wt * Math.log(1 + N / (df.get(w) || 1)) * (p._h.has(w) ? 2.5 : 1);
    if (slots.license && p.c === slots.license) sc *= 1.35;
    else if (slots.license && p.c && p.c !== slots.license) sc *= 0.4;
    if (slots.group && p.g === slots.group) sc *= 1.3;
    else if (slots.group && p.g && p.g !== slots.group) sc *= 0.6;
    if (p.h.startsWith("Q:")) sc *= 1.4;
    if (p.h.startsWith("About ")) sc *= 0.75;
    return { p, sc };
  }).filter((x) => x.sc > 0).sort((a, b) => b.sc - a.sc);
  const out = []; let used = 0;
  for (const { p } of scored) {
    if (out.length >= max) break;
    if (used + p.t.length > maxChars && out.length) continue;
    out.push(p); used += p.t.length;
  }
  return out;
}

// ---------- products ----------
function candidatesFor(items, slots, limit = 10) {
  const all = items.filter((p) => p.c === slots.license && p.a);
  let pool = all.filter((p) => p.cur && p.rg === "Texas");
  if (!pool.length) pool = all.filter((p) => p.cur);
  if (!pool.length) pool = all;
  if (slots.max_price) { const under = pool.filter((p) => p.p <= slots.max_price * 1.05); if (under.length) pool = under; }
  return pool.sort((a, b) => b.r - a.r || a.p - b.p).slice(0, limit);  // the AI sees the whole list and picks
}
const WHY = { "the-1-package": "Exam prep, books, the application and business setup in one.", "ultimate-rental": "Highlighted rental books, the online course and live training.",
  "ultimate-combo": "The full study set plus timed online practice exams.", "highlighted-tabbed": "The books already highlighted, ready for the exam room.",
  "online-course": "Timed practice you can do on your phone.", "book-package": "The reference books the exam is written to.", "rental-package": "The books on rental plus the online course." };
function defaultPicks(cands, want, wantMap, bestList) {
  if (!cands.length) return [];
  const types = (wantMap || {})[want] || [];
  const wantHits = types.length ? cands.filter((p) => types.includes(p.ty)) : [];
  let value = null;
  for (const t of bestList || []) { value = cands.find((p) => p.ty === t); if (value) break; }
  const top = want === "cheapest" ? cands.slice().sort((a, b) => a.p - b.p)[0] : (wantHits[0] || value || cands[0]);
  const alt = cands.filter((p) => p.id !== top.id).sort((a, b) => a.p - b.p)[0];
  return [top, alt].filter(Boolean).map((p) => ({ id: p.id, why: WHY[p.ty] || "" }));
}

// ---------- the AI ----------
const PROMPT = `You are Max, the exam advisor on {BRAND}, a store selling exam prep for Texas trade licenses: TDLR electrician licenses (journeyman, master, residential wireman, maintenance, sign, lineman, industrial, residential appliance installer), TSBPE plumbing licenses, TDLR air conditioning and refrigeration contractor and technician exams, San Antonio and Dallas city exams, the Texas code enforcement officer exam, and ICC and NASCLA national exams. Orders ship from {FUL}. Phone: {PHONE}.
You are an AI assistant. Never claim to be a human; if someone asks, say plainly you're the site's AI advisor and offer the phone number for a real person.

How you talk:
- Like a friendly, experienced Texas tradesman who now helps people get licensed. Warm, relaxed, plain English, a bit of encouragement. Contractions are fine.
- React to what they actually said before moving on.
- Ask about their situation when it helps you recommend: when is the exam, first try or a retake, do they already own the books, do they like studying online or on paper, budget.
- One question at a time. Never list several questions at once. Never sound like a form.
- Answer questions about licensing and the exam using the "Facts" section when it is given. Use its numbers and names exactly, in your own plain words.
- Key Texas rules you can always rely on: Texas electrical exams use the 2026 NEC since September 1, 2026, are open book, and PSI only allows the NEC publisher's permanent tabs. Texas plumbing written exams are closed book and run by Pearson VUE for TSBPE. A/C contractor exams are open book with PSI. Texas has no state general contractor license.
- If the facts do not cover the question, say honestly that the board decides and suggest checking with TDLR or TSBPE or calling us. Never guess numbers, fees or rules.
- If you want to send two separate chat messages, separate them with \\n\\n inside the reply string. Keep each one short, 1 to 3 sentences. Total under 90 words.
- No markdown, no bullet lists, no dashes used as punctuation, at most one emoji.

Decide what to do this turn:
- "chat": answer a question or respond to small talk.
- "ask": you need to know which license they are going for before products can be shown.
- "search": the license is known and it is a good moment to show products. Your reply then introduces your picks in a sentence or two, because the products appear right under it.

When a "Products for this customer" list is given and you choose "search", pick the best 1 to 3 from it by exact id: one clear top pick tied to what they told you, plus one cheaper or more complete alternative if it helps. Each "why" is one short plain reason under 18 words. Never pick anything that is not in the list.

Also give 2 or 3 short quick replies the customer might tap next, in their voice, under 6 words each.

Respond with ONLY this JSON:
{"reply":"...","slots":{"license":null,"want":null,"max_price":null},"action":"chat","picks":[{"id":"...","why":"..."}],"suggestions":["..."]}
"picks" is an empty list unless action is "search". license is one of these slugs or null: {SLUGS}. want is one of everything, books, online, cheapest or null.
Lines like [Shown: ...] in your earlier messages are products the customer already saw.`;

function parseModelJson(text) {
  if (!text) return null;
  if (typeof text === "object") return text;
  text = String(text);
  const s = text.indexOf("{"), e = text.lastIndexOf("}");
  if (s === -1) return null;
  const raw = e > s ? text.slice(s, e + 1) : text.slice(s);
  try { return JSON.parse(raw); } catch {}
  try { return JSON.parse(raw.replace(/\n/g, "\\n").replace(/\r/g, "")); } catch {}
  const m = raw.match(/"reply"\s*:\s*"((?:[^"\\]|\\.)*)"/s);
  return m ? { reply: m[1].replace(/\\n/g, "\n").replace(/\\"/g, '"') } : null;
}
const THINKING = /gemma-4|qwen3|nemotron|gpt-oss|deepseek-r1|kimi/i;
function replyText(r) { const t = r?.response ?? r?.choices?.[0]?.message?.content ?? r?.result?.response ?? ""; return typeof t === "string" || (t && typeof t === "object") ? t : ""; }
async function runModel(env, system, history, slots, maxTokens) {
  const known = Object.keys(slots).filter((k) => slots[k]).length ? "\n\nKnown so far: " + JSON.stringify(slots) : "";
  const messages = [{ role: "system", content: system + known }, ...history];
  const opts = { messages, max_tokens: maxTokens, temperature: 0.3 };
  if (THINKING.test(env.AI_MODEL)) opts.chat_template_kwargs = { enable_thinking: false };
  let text = replyText(await env.AI.run(env.AI_MODEL, opts));
  if (!text || (typeof text === "string" && !text.trim())) text = replyText(await env.AI.run(env.AI_BACKUP_MODEL, { messages, max_tokens: maxTokens, temperature: 0.3 }));
  return parseModelJson(text);
}
function trimHistory(messages, max = 10) {
  if (!Array.isArray(messages)) return [];
  return messages.filter((m) => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string").slice(-max).map((m) => ({ role: m.role, content: m.content.slice(0, 800) }));
}
function cleanSuggestions(list) { return Array.isArray(list) ? list.filter((x) => typeof x === "string" && x.trim()).map((x) => x.trim().slice(0, 40)).slice(0, 3) : []; }

async function chat({ env, history, slots, site, origin }) {
  const base = siteBase(site.base || "", origin);
  if (!base) return { status: 400, body: { error: "Bad site address" } };
  const [catalog, kb] = await Promise.all([loadJson(base + "shared/kb/products.json"), loadJson(base + "shared/kb/texas.json")]);
  const items = catalog?.items || [], licenses = catalog?.licenses || [], wantMap = catalog?.want || {};
  const known = new Set(licenses.map((l) => l.s));
  const lastUser = history.filter((m) => m.role === "user").slice(-1)[0]?.content || "";
  const allUser = history.filter((m) => m.role === "user").map((m) => m.content).join(" . ");
  slots = { license: known.has(slots.license) ? slots.license : null, want: slots.want || null, trade: slots.trade || null, max_price: Number(slots.max_price) || null };
  const said = guessLicense(lastUser, licenses, slots.trade) || (!slots.license && guessLicense(allUser, licenses, slots.trade));
  if (said) slots.license = said;
  const tl = norm(lastUser);
  // a question about another trade than the license chosen earlier: follow the question
  const qTrade = guessTrade(tl), curLic = licenses.find((l) => l.s === slots.license);
  if (!said && qTrade && curLic && curLic.g !== qTrade) { slots.license = null; slots.trade = qTrade; }
  if (/ (cheap\w*|lowest|budget|least expensive) /.test(tl)) slots.want = "cheapest";
  else if (/ (online|on my phone|course) /.test(tl)) slots.want = "online";
  else if (/ (everything|all in one|complete|best chance) /.test(tl)) slots.want = "everything";
  else if (/ (books?|code book|paper) /.test(tl) && wantsProducts(lastUser)) slots.want = "books";
  const group = (licenses.find((l) => l.s === slots.license) || {}).g || guessTrade(norm(lastUser)) || (slots.trade !== "other" && slots.trade) || guessTrade(norm(allUser));
  const asking = isQuestion(lastUser) && !wantsProducts(lastUser);
  const facts = pickFacts(kb?.pieces || [], lastUser + " " + allUser.slice(-300), { license: slots.license, group });
  const factText = facts.length ? "\n\nFacts from our pages (answer from these when they fit):\n" + facts.map((p, i) => `[${i + 1}] ${p.h.replace(/^Q: /, "Question: ")}\n${p.t}`).join("\n\n") : "";
  const cands = slots.license ? candidatesFor(items, slots) : [];
  const list = cands.length && !asking ? "\n\nProducts for this customer:\n" + cands.map((p) => `- id: ${p.id} | ${p.cn} | ${p.tn} | ${p.rg === "Texas" ? "Texas" : "any state"}${p.y ? " " + p.y : ""} | $${p.p.toFixed(2)}`).join("\n") : "";
  const system = PROMPT.replaceAll("{BRAND}", String(site.brand || "our store").slice(0, 80)).replaceAll("{FUL}", String(site.fulfillment || "1 Exam Prep").slice(0, 80))
    .replaceAll("{PHONE}", String(site.phone || "the number in the site header").slice(0, 30)).replace("{SLUGS}", [...known].join(", "));
  const out = await runModel(env, system + factText + (asking ? '\n\nThe customer asked a question. Answer it. Set action to "chat".' : list), history, slots, 700);
  if (out?.slots?.license && known.has(out.slots.license)) slots.license = out.slots.license;
  if (out?.slots?.want && ["everything", "books", "online", "cheapest"].includes(out.slots.want)) slots.want = out.slots.want;
  let reply = typeof out?.reply === "string" && out.reply.trim() ? out.reply.trim() : "";
  if (!reply && facts.length) reply = (facts[0].t.match(/[^.!?]+[.!?]+/g) || [facts[0].t]).slice(0, 2).join(" ").trim();
  const suggestions = cleanSuggestions(out?.suggestions);
  const lic = licenses.find((l) => l.s === slots.license);
  if (lic) slots.trade = ["local", "business", "national", "codes"].includes(lic.g) ? "other" : lic.g;
  const action = asking ? "chat" : out?.action || (slots.license ? "search" : "ask");
  // a question about a known license: answer, then the packages for it
  if (asking && lic) {
    const picks = defaultPicks(candidatesFor(items, slots), slots.want, wantMap, catalog?.best);
    if (picks.length) return { status: 200, body: { reply: (reply || "Good question.") + "\n\nIf you meet the requirements, these are what I'd use for the " + lic.n + " exam:", slots, products: picks, suggestions: ["How are they different?", "I have another question"] } };
  }
  if (action !== "search" || !lic) {
    return { status: 200, body: { reply: reply || "Happy to help. Which Texas license are you going for?", slots, products: [], suggestions: suggestions.length ? suggestions : lic ? ["Show me packages", "Is it open book?"] : ["Journeyman electrician", "Master plumber", "HVAC Class B"] } };
  }
  const pool = candidatesFor(items, slots), byId = new Map(pool.map((p) => [p.id, p]));
  let picks = Array.isArray(out?.picks) ? out.picks.filter((p) => p && byId.has(String(p.id))).slice(0, 3).map((p) => ({ id: String(p.id), why: typeof p.why === "string" ? p.why.slice(0, 140) : "" })) : [];
  if (!picks.length) picks = defaultPicks(pool, slots.want, wantMap, catalog?.best);
  return { status: 200, body: { reply: reply || "Here's what I'd look at for you:", slots, products: picks, suggestions: suggestions.length ? suggestions : ["How do they compare?", "Is it open book?"] } };
}

// ---------- HTTP ----------
function cors(request, env) {
  const origin = request.headers.get("Origin") || "";
  const ok = env.ALLOWED_ORIGINS.split(",").map((s) => s.trim()).includes(origin);
  return { ...(ok ? { "Access-Control-Allow-Origin": origin } : {}), "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type", "Vary": "Origin" };
}
function json(data, status, headers) { return new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json", ...headers } }); }

export default {
  async fetch(request, rawEnv) {
    const env = Object.assign({}, DEFAULTS);
    for (const k of Object.keys(rawEnv || {})) if (rawEnv[k] !== undefined && rawEnv[k] !== "") env[k] = rawEnv[k];
    const h = cors(request, env);
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: h });
    const url = new URL(request.url);
    if (url.pathname === "/health" || url.pathname === "/") return json({ ok: true, name: "Max, Texas exam advisor", ai: !!env.AI }, 200, {});
    if (url.pathname === "/debug" && request.method === "GET") {
      if (url.searchParams.get("key") !== env.DEBUG_KEY) return json({ error: "Not found" }, 404, {});
      if (!env.AI) return json({ error: "No Workers AI binding named AI. Add it under Settings > Bindings." }, 200, {});
      const raws = [];
      const env2 = { ...env, AI: { run: async (m, o) => { const r = await env.AI.run(m, o); raws.push(r?.response ?? r?.choices?.[0]?.message?.content ?? r); return r; } } };
      const history = url.searchParams.getAll("q").map((c, i) => ({ role: i % 2 ? "assistant" : "user", content: c }));
      const slots = { license: url.searchParams.get("license"), want: url.searchParams.get("want"), trade: url.searchParams.get("trade") };
      const origin = new URL(env.SITE_BASE).origin, t0 = Date.now();
      try {
        const out = await chat({ env: env2, history, slots, origin, site: { base: env.SITE_BASE, brand: "Pass Your Texas Contractor Exam", phone: "(877) 775-9400" } });
        return json({ ms: Date.now() - t0, model: env.AI_MODEL, raw: raws, result: out.body }, 200, {});
      } catch (err) { return json({ ms: Date.now() - t0, raw: raws, error: String(err?.message || err) }, 200, {}); }
    }
    if (url.pathname !== "/chat" || request.method !== "POST") return json({ error: "Not found" }, 404, h);
    if (!h["Access-Control-Allow-Origin"]) return json({ error: "Origin not allowed" }, 403, h);
    let body;
    try { body = await request.json(); } catch { return json({ error: "Bad JSON" }, 400, h); }
    const history = trimHistory(body.messages, 10);
    if (!history.length || history[history.length - 1].role !== "user") return json({ error: "Last message must be from the user" }, 400, h);
    const slots = typeof body.slots === "object" && body.slots ? body.slots : {};
    const site = typeof body.site === "object" && body.site ? body.site : {};
    const origin = request.headers.get("Origin") || "";
    try {
      if (!env.AI) throw new Error("No Workers AI binding named AI");
      const out = await chat({ env, history, slots, site, origin });
      return json(out.body, out.status, h);
    } catch (err) {
      console.error("chat error", err?.message || err);
      // still useful without the AI: the right packages for a license we recognised
      try {
        const base = siteBase(site.base || "", origin);
        const catalog = base ? await loadJson(base + "shared/kb/products.json") : null;
        const text = history.filter((m) => m.role === "user").map((m) => m.content).join(" . ");
        const s = { ...slots, license: slots.license || guessLicense(text, catalog?.licenses || [], slots.trade) };
        const picks = s.license ? defaultPicks(candidatesFor(catalog?.items || [], s), s.want, catalog?.want, catalog?.best) : [];
        return json({ reply: picks.length ? "Here are the closest matches I found:" : "Sorry, I'm having trouble right now. You can still tap the buttons or use the regular search.", slots: s, products: picks, degraded: true }, 200, h);
      } catch { return json({ reply: "Sorry, I'm having trouble right now. You can still use the regular search.", slots, products: [], degraded: true }, 200, h); }
    }
  }
};
