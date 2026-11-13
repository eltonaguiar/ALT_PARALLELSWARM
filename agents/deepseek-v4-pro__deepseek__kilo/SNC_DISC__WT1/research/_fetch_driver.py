#!/usr/bin/env python3
"""Direct search->fetch->digest driver (no LLM loop). Used by deepseek-v4-pro
(Kilo native) to pull real evidence for the SNC_DISC_RESEARCH reference.

Reuses the proven retrieval + Playwright-rendered extraction from
shared/research_harness.py, but the "model" is me reading the digest directly.
"""
from __future__ import annotations
import sys, json, time
from pathlib import Path

SHARED = Path("/home/eaguiar2015/ALT_PARALLELSWARM/shared")
sys.path.insert(0, str(SHARED))
import research_harness as rh  # noqa: E402

QUERIES = [
    ("discovery_phases_order",
     "ServiceNow Discovery phases order of operations scan classify identify explore patterns"),
    ("discovery_properties_config",
     "ServiceNow Discovery properties configuration options MID server schedules credential"),
    ("ci_class_manager_identification",
     "ServiceNow CI Class Manager identification rules configuration"),
    ("ci_class_manager_reconciliation",
     "ServiceNow CI Class Manager reconciliation rules configuration"),
    ("ire_engine",
     "ServiceNow Identification and Reconciliation Engine IRE data source rules"),
    ("ire_data_source_rules",
     "ServiceNow IRE data source rules which data source can update which field"),
    ("avoid_duplicate_ci",
     "ServiceNow Discovery avoid duplicate CIs identification reconciliation rules"),
    ("insert_vs_update_cmdb",
     "ServiceNow Discovery insert new CI versus update existing CI CMDB behavior"),
    ("data_refresh_rules",
     "ServiceNow CMDB data refresh rules staleness identification engine"),
    ("mid_server_horizontal",
     "ServiceNow horizontal discovery pattern MID server probes sensors"),
]

OUT = Path(__file__).resolve().parent
ts = time.strftime("%Y%m%d_%H%M%S")

for slug, q in QUERIES:
    print(f"\n===== {slug} =====", flush=True)
    try:
        results = rh.ddg(q, 8)
    except Exception as e:
        print(f"SEARCH_ERROR {e}", flush=True)
        results = []
    if not results:
        print("NO RESULTS", flush=True)
        (OUT / f"{ts}_{slug}.md").write_text(f"# {slug}\n\nNO RESULTS for: {q}\n")
        continue
    picked = results[:4]
    blocks, cites = [], []
    for r in picked:
        txt = rh.page_text(r["url"])
        if len(txt) < 300:
            continue
        paras = rh.extract(txt, q, max_paras=5) or [txt[:500]]
        cites.append(r["url"])
        blocks.append(f"SOURCE: {r['url']}\nTITLE: {r['title']}\n" +
                      "\n".join(f"  - {p}" for p in paras))
        if len(blocks) >= 3:
            break
    body = "\n\n".join(blocks) if blocks else f"could not extract text from:\n" + \
        "\n".join("- " + r["url"] for r in picked)
    doc = f"# {slug}\n\nquery: {q}\n\n## Evidence ({len(blocks)} sources)\n\n{body}\n\n## All search hits\n\n" + \
        "\n".join(f"- [{r['title']}]({r['url']}) score={r.get('score',0)}" for r in results)
    (OUT / f"{ts}_{slug}.md").write_text(doc)
    print(f"  sources={len(cites)} chars={len(doc)}", flush=True)

print("\nDONE", flush=True)
