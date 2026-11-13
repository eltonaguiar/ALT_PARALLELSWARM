#!/usr/bin/env python3
"""
docs_api.py — read ServiceNow docs through the khub API the docs SPA itself uses.

Why: docs.servicenow.com redirects headless browsers to an ad tracker and renders
an empty shell, so every scraping path fails. The SPA fetches topic content from

  https://www.servicenow.com/docs/api/khub/maps/<map>/topics/<content_id>/content?target=DESIGNED_READER

which returns the real article HTML with HTTP 200 and no JS.

Discovery: found by teammate agent `deepseek-flash__openrouter__kilo-cli` (their
`research/topics.json`), verified independently here.

Topic index: built from any `research/topics.json` in the repo — no API key, no
search engine, no bot wall.
"""
from __future__ import annotations

import html
import json
import re
import urllib.request
from functools import lru_cache
from pathlib import Path

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "shared" / "state" / "docs_api_cache"
STOP = set("the a an of and or for to in on with what which how why when does do is are was were "
           "between difference explain walk through step steps about into from by as at".split())


@lru_cache(maxsize=1)
def topic_index() -> list[dict]:
    """Collect topics from every topics.json any agent has produced."""
    topics, seen = [], set()
    for p in REPO.glob("agents/*/research/topics.json"):
        try:
            data = json.loads(p.read_text())
        except Exception:
            continue
        if not isinstance(data, list):
            continue
        for t in data:
            url = t.get("api_url")
            if not url or url in seen:
                continue
            seen.add(url)
            topics.append({"key": t.get("key", ""), "title": t.get("title", ""), "api_url": url})
    # also accept a private index outside the repo
    priv = Path.home() / ".alt_parallelswarm_private" / "docs_topic_index.json"
    if priv.exists():
        try:
            for t in json.loads(priv.read_text()):
                url = t.get("api_url")
                if url and url not in seen:
                    seen.add(url)
                    topics.append({"key": t.get("key", ""), "title": t.get("title", ""), "api_url": url})
        except Exception:
            pass
    return topics


def _text(raw_html: str) -> str:
    raw_html = re.sub(r"(?is)<(script|style|nav|footer)[^>]*>.*?</\1>", " ", raw_html)
    raw_html = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h[1-6]>|</li>|</tr>", "\n", raw_html)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw_html))
    txt = re.sub(r"[ \t\xa0]+", " ", txt)
    return re.sub(r"\n\s*\n+", "\n", txt).strip()


def fetch(api_url: str) -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", api_url)[-120:]
    fp = CACHE / f"{slug}.txt"
    if fp.exists():
        return fp.read_text(encoding="utf-8", errors="replace")
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": UA, "Accept": "text/html"})
        raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        txt = _text(raw)
    except Exception as e:
        txt = f"DOCS_API_ERROR: {type(e).__name__}: {str(e)[:120]}"
    fp.write_text(txt, encoding="utf-8")
    return txt


def _api_topics(map_ids: list[str] | None = None) -> list[dict]:
    """Enumerate a docs map's topics through the public khub list endpoint."""
    map_ids = map_ids or ["bsp_DjPRMilbWYHwwVa4zQ"]  # Brazil ITOM bundle (contains Discovery)
    out = []
    for mid in map_ids:
        try:
            req = urllib.request.Request(f"https://www.servicenow.com/docs/api/khub/maps/{mid}/topics",
                                         headers={"User-Agent": UA, "Accept": "application/json"})
            data = json.loads(urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace"))
        except Exception:
            continue
        for t in data if isinstance(data, list) else []:
            url = t.get("contentApiEndpoint") or t.get("api_url")
            if not url:
                continue
            if url.startswith("/"):
                url = "https://www.servicenow.com" + url
            if url.startswith("http"):
                out.append({"key": t.get("id", ""), "title": t.get("title", ""), "api_url": url})
    return out


def refresh_index() -> int:
    """Write a private topic index outside the repo (keeps the repo free of source dumps)."""
    priv = Path.home() / ".alt_parallelswarm_private"
    priv.mkdir(parents=True, exist_ok=True)
    topics = _api_topics()
    if topics:
        (priv / "docs_topic_index.json").write_text(json.dumps(topics), encoding="utf-8")
    return len(topics)


def _content_hits(txt: str, terms: list[str]) -> int:
    low = txt.lower()
    return sum(1 for t in terms if t in low)


def search(query: str, top_n: int = 3, max_chars: int = 4200, scan: int = 6) -> str:
    """Score topics by title first; if that is thin, scan the most plausible topics by content."""
    topics = topic_index()
    if not topics:
        return ("DOCS_API_EMPTY: no topic index found. Run "
                "`python3 shared/docs_api.py --refresh-index` first.")
    terms = [t for t in re.findall(r"[a-z0-9]{3,}", query.lower()) if t not in STOP]

    def title_score(t):
        title = (t["title"] or "").lower()
        hay = title + " " + (t["key"] or "").lower()
        return sum(2 if term in title else (1 if term in hay else 0) for term in terms)

    scored = sorted(((title_score(t), t) for t in topics), key=lambda x: -x[0])
    picks = [t for s, t in scored if s > 0][:top_n]

    if len(picks) < 2:
        # title match insufficient: scan a bounded set of CMDB/Discovery-looking topics
        area_words = ("cmdb", "class", "discover", "identif", "reconcil", "data", "refresh",
                      "source", "propert", "schedule", "health", "ire")
        cands = [t for t in topics
                 if any(w in (t["title"] or "").lower() for w in area_words)][:scan * 2]
        ranked = []
        for t in cands:
            txt = fetch(t["api_url"])
            if txt.startswith("DOCS_API_ERROR"):
                continue
            ranked.append((_content_hits(txt, terms), t, txt))
        ranked.sort(key=lambda x: -x[0])
        picks = [t for h, t, _ in ranked[:top_n] if h > 0] or [t for _, t, _ in ranked[:top_n]]

    if not picks:
        return f"DOCS_API_EMPTY: nothing matched {terms[:5]}. Try different words."

    blocks = []
    for t in picks[:top_n]:
        txt = fetch(t["api_url"])
        if txt.startswith("DOCS_API_ERROR"):
            continue
        paras = [p.strip() for p in txt.split("\n") if 60 < len(p.strip()) < 1200]
        paras.sort(key=lambda p: -sum(1 for x in terms if x in p.lower()))
        blocks.append(f"DOCS_TOPIC: {t['title']}\nSOURCE: {t['api_url']}\n" +
                      "\n".join("  - " + p[:420] for p in (paras[:5] or [txt[:400]])))
    if not blocks:
        return "DOCS_API_EMPTY: matched topics but none could be fetched."
    return "EVIDENCE (ServiceNow docs API):\n\n" + "\n\n".join(blocks)[:max_chars]


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if args and args[0] == "--refresh-index":
        n = refresh_index()
        print(json.dumps({"topics_indexed": n,
                          "path": str(Path.home() / ".alt_parallelswarm_private" / "docs_topic_index.json")}))
    else:
        print(search(" ".join(args) or "discovery identification"))
