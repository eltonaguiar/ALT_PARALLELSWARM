#!/usr/bin/env python3
"""
Harness v3 — "wrapper does the browsing".

The model gets ONE research primitive:
    research(query) -> server-side: search, pick authoritative sources, fetch,
                       extract only the paragraphs that match the query, return a
                       compact digest with citations.

Then answer(text). No page dumps, no link-following, no 6-tool juggling.
Hypothesis: a weak model can produce grounded research if the wrapper absorbs
retrieval + extraction, which is what it is bad at.
"""
from __future__ import annotations
import argparse, base64, json, re, sys, time, urllib.parse, urllib.request, html
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
BASE_KEY = ""
_CACHE: dict[str, str] = {}

AUTHORITY = [  # (regex, weight) — authority of the SOURCE, not of the answer
    (r"support\.servicenow\.com", 5),
    (r"servicenow\.com/community", 4),
    (r"servicenow\.com/docs", 3),
    (r"developer\.servicenow\.com", 2),
    (r"servicenow\.com", 1),
]


def _ddg_http(query: str, n: int = 8):
    body = urllib.parse.urlencode({"q": query}).encode()
    req = urllib.request.Request("https://html.duckduckgo.com/html/", data=body,
                                 headers={"User-Agent": UA,
                                          "Content-Type": "application/x-www-form-urlencoded"})
    raw = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")
    anchors = list(re.finditer(r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', raw, re.S))
    snips = list(re.finditer(r'class="result__snippet"[^>]*>(.*?)</a>', raw, re.S))
    out, seen = [], set()
    for i, a in enumerate(anchors):
        href = html.unescape(a.group(1))
        if "uddg=" in href:
            m = re.search(r"uddg=([^&]+)", href)
            if m:
                href = urllib.parse.unquote(m.group(1))
        if href in seen:
            continue
        seen.add(href)
        title = html.unescape(re.sub(r"<[^>]+>", "", a.group(2))).strip()
        snip = html.unescape(re.sub(r"<[^>]+>", "", snips[i].group(1))).strip() if i < len(snips) else ""
        out.append({"title": title, "url": href, "snippet": snip})
        if len(out) >= n:
            break
    return out


def _engine_browser(engine: str, query: str, n: int = 8):
    """Search via a real browser context. HTTP endpoints serve degraded/blocked results."""
    from playwright.sync_api import sync_playwright
    urls = {
        "startpage": "https://www.startpage.com/sp/search?query=" + urllib.parse.quote(query),
        "brave": "https://search.brave.com/search?q=" + urllib.parse.quote(query),
    }
    skip = ("startpage.com", "brave.com", "google.com", "bing.com", "duckduckgo.com", "javascript:")
    out, seen = [], set()
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        ctx = b.new_context(user_agent=UA, locale="en-US", viewport={"width": 1366, "height": 900})
        pg = ctx.new_page()
        pg.goto(urls[engine], wait_until="domcontentloaded", timeout=45000)
        pg.wait_for_timeout(2500)
        anchors = pg.eval_on_selector_all(
            "a[href^='http']",
            "els=>els.map(e=>[e.innerText.trim().slice(0,120), e.href])")
        b.close()
    for text, href in anchors:
        if not href or any(s in href for s in skip) or href in seen:
            continue
        if len(text) < 8:
            continue
        seen.add(href)
        out.append({"title": text.replace("\n", " ")[:90], "url": href, "snippet": ""})
        if len(out) >= n:
            break
    return out


def ddg(query: str, n: int = 8):
    """Search with backend fallback: DuckDuckGo HTTP -> Startpage -> Brave (browser)."""
    results = []
    try:
        results = _ddg_http(query, n)
    except Exception:
        results = []
    for engine in ("startpage", "brave"):
        if len(results) >= 4:
            break
        try:
            alt = _engine_browser(engine, query, n)
            if len(alt) > len(results):
                results = alt
        except Exception:
            continue
    for r in results:
        r["score"] = max([w for pat, w in AUTHORITY if re.search(pat, r["url"])] or [0])
    results.sort(key=lambda r: -r["score"])
    return results[:n]


def _strip(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h[1-6]>|</li>|</tr>", "\n", raw)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    txt = re.sub(r"[ \t\xa0]+", " ", txt)
    return re.sub(r"\n\s*\n+", "\n", txt).strip()


def page_text(url: str) -> str:
    if url in _CACHE:
        return _CACHE[url]
    text = ""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
        text = _strip(urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace"))
    except Exception:
        text = ""
    if len(text) < 900:
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                b = p.chromium.launch(headless=True, args=["--no-sandbox"])
                ctx = b.new_context(user_agent=UA, locale="en-US")
                pg = ctx.new_page()
                pg.goto(url, wait_until="domcontentloaded", timeout=45000)
                pg.wait_for_timeout(1800)
                for f in pg.frames:
                    for label in ("Accept and Proceed", "Accept All", "I Accept", "Accept"):
                        try:
                            loc = f.get_by_role("button", name=label)
                            if loc.count():
                                loc.first.click(timeout=1500)
                                break
                        except Exception:
                            pass
                best = ""
                for f in pg.frames:
                    try:
                        x = f.inner_text("body")
                    except Exception:
                        continue
                    if len(x) > len(best):
                        best = x
                b.close()
                text = best if len(best) > len(text) else text
        except Exception:
            pass
    _CACHE[url] = text
    return text


STOP = set("the a an of and or for to in on with what which how why when does do is are was were "
           "between difference explain walk through step steps about into from by as at".split())

def extract(text: str, query: str, max_paras: int = 7) -> list[str]:
    terms = [t for t in re.findall(r"[a-z0-9]{4,}", query.lower()) if t not in STOP]
    paras = [p.strip() for p in text.split("\n") if 60 < len(p.strip()) < 1400]
    scored = []
    for p in paras:
        low = p.lower()
        hits = sum(1 for t in terms if t in low)
        if hits:
            scored.append((hits, len(p), p))
    scored.sort(key=lambda x: (-x[0], x[1]))
    seen, out = set(), []
    for _, _, p in scored:
        key = p[:80]
        if key in seen:
            continue
        seen.add(key)
        out.append(p[:500])
        if len(out) >= max_paras:
            break
    return out


def research(query: str, focus: str = "") -> str:
    try:
        results = ddg(query, 8)
    except Exception as e:
        return f"RESEARCH_ERROR: search failed ({type(e).__name__})"
    if not results:
        return "RESEARCH_EMPTY: no results for that query"
    q = (query + " " + focus).strip()
    picked = results[:4]
    fetched = list(ThreadPoolExecutor(max_workers=4).map(lambda r: page_text(r["url"]), picked))
    blocks, cites = [], []
    for r, txt in zip(picked, fetched):
        if len(txt) < 400:
            continue
        paras = extract(txt, q)
        if not paras:
            paras = [txt[:400]]
        cites.append(r["url"])
        blocks.append(f"SOURCE: {r['url']}\nTITLE: {r['title']}\n" +
                      "\n".join(f"  - {p}" for p in paras[:4]))
        if len(blocks) >= 3:
            break
    if not blocks:
        return ("RESEARCH_EMPTY: found results but could not extract readable text "
                "(sites may be JS-blocked). Try rephrasing the query.")
    digest = "\n\n".join(blocks)
    return f"EVIDENCE ({len(blocks)} sources):\n\n{digest[:4200]}"


def llm(base_url, model, messages, tools=None, timeout=240):
    payload = {"model": model, "messages": messages, "temperature": 0.1, "stream": False}
    if tools:
        payload["tools"] = tools
    req = urllib.request.Request(base_url.rstrip("/") + "/chat/completions",
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + (BASE_KEY or "ollama")})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


SYSTEM = """You are a research analyst. You have no reliable memory, so all facts must come from research().

Workflow:
1. Call research() with a focused query. Read the evidence digest it returns.
2. If the evidence does not cover part of the question, call research() again with a different query.
3. To finish, call answer() with a well-organised answer that cites the source URLs from the evidence.

Never invent URLs, rule names, or facts that are not in the evidence.
"""

TOOLS = [
    {"type": "function", "function": {
        "name": "research",
        "description": ("Search the web and return extracted evidence paragraphs with their source URLs. "
                        "The wrapper does the browsing; you only read the digest."),
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string", "description": "what to research"}},
            "required": ["query"]}}},
    {"type": "function", "function": {
        "name": "docs_search",
        "description": ("Search ServiceNow's OWN documentation directly (bypasses web search and bot walls). "
                        "Use this first for anything about ServiceNow configuration."),
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string", "description": "what to look up in ServiceNow docs"}},
            "required": ["query"]}}},
    {"type": "function", "function": {
        "name": "answer", "description": "Final answer citing the URLs used.",
        "parameters": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}}},
]


def _parse_text_tool(content: str):
    """Some small models emit tool calls as text, e.g. answer({"text": "..."}) — accept both."""
    if not content:
        return None
    m = re.search(r'\b(research|answer)\s*\(\s*(\{.*?\})\s*\)', content, re.S)
    if m:
        try:
            return m.group(1), json.loads(m.group(2))
        except Exception:
            pass
    m = re.search(r'\b(research|answer)\s*\(\s*"([^"]{10,})"\s*\)', content, re.S)
    if m:
        return m.group(1), ({"query": m.group(2)} if m.group(1) == "research" else {"text": m.group(2)})
    # bare json object
    m = re.search(r'\{.*\}', content, re.S)
    if m:
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict):
                if "query" in obj:
                    return "research", obj
                if "text" in obj:
                    return "answer", obj
        except Exception:
            pass
    return None


def run(base_url, model, question, rounds, transcript):
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    calls = 0
    for step in range(rounds + 4):
        if calls >= rounds:
            messages.append({"role": "user", "content": "Research budget used up. Call answer() now using the evidence you have."})
        try:
            r = llm(base_url, model, messages, tools=TOOLS)
        except Exception as e:
            transcript.append(f"[{step}] LLM_ERROR {type(e).__name__}")
            return None, f"LLM_ERROR {type(e).__name__}: {str(e)[:120]}", calls
        msg = (r.get("choices") or [{}])[0].get("message") or {}
        tc = msg.get("tool_calls") or []
        content = (msg.get("content") or "").strip()

        if not tc:
            parsed = _parse_text_tool(content)
            if not parsed:
                transcript.append(f"[{step}] no tool call: {content[:150]}")
                messages.append({"role": "assistant", "content": content or "..."})
                messages.append({"role": "user", "content": "Call research() or answer() as a tool."})
                continue
            name, a = parsed
            transcript.append(f"[{step}] text-tool {name}")
            if name == "answer":
                return a.get("text", ""), None, calls
            res = research(a.get("query", ""), a.get("focus", ""))
            calls += 1
            messages.append({"role": "assistant", "content": content[:600]})
            messages.append({"role": "user", "content": "EVIDENCE:\n" + res[:5000]})
            continue

        messages.append({"role": "assistant", "content": content or None, "tool_calls": tc})
        for c in tc:
            name = c["function"]["name"]
            try:
                a = json.loads(c["function"].get("arguments") or "{}")
            except Exception:
                a = {}
            if name == "answer":
                transcript.append(f"[{step}] answer()")
                return a.get("text", ""), None, calls
            if name == "research":
                res = research(a.get("query", ""), a.get("focus", ""))
            elif name == "docs_search":
                try:
                    import docs_api
                    res = docs_api.search(a.get("query", ""))
                except Exception as e:
                    res = f"DOCS_API_ERROR: {type(e).__name__}: {str(e)[:120]}"
            else:
                res = f"ERROR unknown tool {name}"
            calls += 1
            transcript.append(f"[{step}] research({str(a.get('query',''))[:90]}) -> {len(res)}c")
            messages.append({"role": "tool", "tool_call_id": c.get("id", ""), "content": res[:5000]})
    return None, f"MAX_ROUNDS (calls={calls})", calls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen2.5:7b-instruct-q5_K_M")
    ap.add_argument("--base-url", default="http://localhost:11434/v1")
    ap.add_argument("--api-key", default="")
    ap.add_argument("--question", required=True)
    ap.add_argument("--rounds", type=int, default=6)
    ap.add_argument("--out", default="/tmp/weak_browse/v3")
    args = ap.parse_args()
    global BASE_KEY
    BASE_KEY = args.api_key
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    tr: list[str] = []
    t0 = time.time()
    ans, err, calls = run(args.base_url, args.model, args.question, args.rounds, tr)
    elapsed = round(time.time() - t0, 1)
    slug = re.sub(r"[^a-z0-9]+", "_", args.model.lower())[:36]
    (out / f"{ts}_{slug}.md").write_text(
        f"# v3 run\n\nmodel: {args.model}\nelapsed: {elapsed}s\nresearch_calls: {calls}\nerror: {err}\n\n"
        f"## Question\n{args.question}\n\n## Answer\n{ans or '(none)'}\n\n## Transcript\n```\n"
        + "\n".join(tr) + "\n```\n", encoding="utf-8")
    print(json.dumps({"model": args.model, "elapsed_s": elapsed, "research_calls": calls,
                      "error": (err or "")[:100], "answer_chars": len(ans or ""),
                      "answer_head": (ans or "")[:220]}))


if __name__ == "__main__":
    main()
