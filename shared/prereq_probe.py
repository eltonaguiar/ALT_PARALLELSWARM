#!/usr/bin/env python3
"""
prereq_probe.py — "can I even do this task?" gate.

An agent that cannot browse must say so BEFORE spending its budget, so the
orchestrator can hand it a backup plan or move the task elsewhere.

Writes PREREQ.md with PASS/FAIL per capability plus the consequence.
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def check_http() -> tuple[bool, str]:
    try:
        t0 = time.time()
        r = urllib.request.urlopen(urllib.request.Request("https://example.com", headers={"User-Agent": UA}), timeout=12)
        return r.status == 200, f"HTTP {r.status} in {round(time.time()-t0,1)}s"
    except Exception as e:
        return False, f"{type(e).__name__}: {str(e)[:80]}"


def check_playwright() -> tuple[bool, str]:
    try:
        import playwright
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True, args=["--no-sandbox"])
            pg = b.new_page()
            pg.set_content("<html><body><h1 id=x>render-check</h1></body></html>")
            ok = pg.inner_text("#x").strip() == "render-check"
            v = b.version
            b.close()
        return ok, f"chromium {v}"
    except Exception as e:
        return False, f"{type(e).__name__}: {str(e)[:100]}"


def check_js() -> tuple[bool, str]:
    """Does JS execute? (matters: many doc sites are SPAs)"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True, args=["--no-sandbox"])
            pg = b.new_page()
            pg.set_content("<html><body><div id=o>before</div><script>document.getElementById('o').innerText='after'</script></body></html>")
            pg.wait_for_timeout(300)
            got = pg.inner_text("#o").strip()
            b.close()
        return got == "after", f"js output={got!r}"
    except Exception as e:
        return False, f"{type(e).__name__}: {str(e)[:80]}"


def check_search() -> tuple[bool, str]:
    """Can we reach a search engine that returns relevant results?"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
            ctx = b.new_context(user_agent=UA, locale="en-US", viewport={"width": 1366, "height": 900})
            pg = ctx.new_page()
            pg.goto("https://www.startpage.com/sp/search?query=servicenow+discovery+documentation",
                    wait_until="domcontentloaded", timeout=40000)
            pg.wait_for_timeout(2000)
            links = pg.eval_on_selector_all("a[href^='http']", "els=>els.map(e=>e.href)")
            b.close()
        hits = [x for x in links if "servicenow.com" in x]
        return len(hits) >= 2, f"{len(hits)} servicenow.com results"
    except Exception as e:
        return False, f"{type(e).__name__}: {str(e)[:80]}"


def check_context(base_url: str, model: str, api_key: str) -> tuple[str, int]:
    """Ask Ollama for the model's context length; else report unknown."""
    try:
        host = base_url.rstrip("/").replace("/v1", "")
        req = urllib.request.Request(host + "/api/show", data=json.dumps({"model": model}).encode(),
                                     headers={"Content-Type": "application/json"})
        d = json.loads(urllib.request.urlopen(req, timeout=20).read().decode())
        info = d.get("model_info") or {}
        for k, v in info.items():
            if k.endswith(".context_length") and isinstance(v, int):
                return f"{model} (ollama)", v
        return f"{model} (ollama, size not reported)", 0
    except Exception:
        pass
    known = {"deepseek-v4-flash": 128000, "gpt-oss-120b": 131072, "grok-4.5": 256000}
    for k, v in known.items():
        if k in model:
            return f"{model} (api, assumed)", v
    return f"{model} (unknown)", 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="directory to write PREREQ.md into")
    ap.add_argument("--agent", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--base-url", default="http://localhost:11434/v1")
    ap.add_argument("--api-key", default="")
    ap.add_argument("--skip-search-check", action="store_true")
    args = ap.parse_args()

    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    rows = []
    ok, detail = check_http();      rows.append(("Outbound HTTP", ok, detail))
    ok, detail = check_playwright(); rows.append(("Playwright + Chromium", ok, detail))
    ok, detail = check_js();        rows.append(("JavaScript rendering", ok, detail))
    if args.skip_search_check:
        rows.append(("Web search reachable", True, "skipped (assumed OK)"))
    else:
        ok, detail = check_search(); rows.append(("Web search reachable", ok, detail))
    ctx_name, ctx_len = check_context(args.base_url, args.model, args.api_key)
    rows.append(("Context window", ctx_len >= 32000, f"{ctx_name}: {ctx_len or 'unknown'} tokens"))

    can_browse = all(ok for name, ok, _ in rows if name != "Context window") and rows[4][1]
    lines = [f"# Pre-requisite check — {args.agent}", "",
             f"Model: `{args.model}`", f"Base URL: `{args.base_url}`", "",
             "| capability | pass | evidence |", "|---|---|---|"]
    for name, ok, detail in rows:
        lines.append(f"| {name} | {'YES' if ok else 'NO'} | {detail} |")
    lines += ["", "## Verdict", ""]
    if can_browse and ctx_len >= 32000:
        lines.append("**CAN proceed with independent web research.** Browsing tools reachable and context is adequate.")
    elif can_browse:
        lines.append("**PARTIAL.** Can browse, but context window is small — research must be done in short, "
                     "summarised passes; expect to drop detail. Backup plan: request a summarisation sub-agent.")
    else:
        lines.append("**CANNOT browse independently.** Per instructions, this agent must (a) state the blocker "
                     "here, (b) write a backup request in `02_CLARIFICATIONS/`, and (c) fall back to "
                     "answering from supplied evidence rather than pretending to research.")
    lines += ["", "## Backup plan if blocked", "",
              "- Ask the orchestrator for a pre-fetched evidence digest (another agent's research output).",
              "- Restrict output to structure/planning work that needs no live sources.",
              "- Never fabricate URLs; mark unsourced claims as UNVERIFIED.", ""]
    (out / "PREREQ.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"agent": args.agent, "can_browse": can_browse, "context": ctx_len,
                      "checks": {n: ok for n, ok, _ in rows}}))


if __name__ == "__main__":
    main()
