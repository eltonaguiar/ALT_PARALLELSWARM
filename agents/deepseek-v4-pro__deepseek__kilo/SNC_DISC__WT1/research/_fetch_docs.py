import sys, time
from pathlib import Path
sys.path.insert(0, "/home/eaguiar2015/ALT_PARALLELSWARM/shared")
import research_harness as rh

DOCS = [
 ("ire_engine", "https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ire.html", "IRE concepts data source precedence timestamps identification reconciliation"),
 ("reconciliation_principles", "https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_ReconciliationRulesPrinciples.html", "reconciliation rules principles priority data source precedence authorization"),
 ("ire_data_source_rule", "https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-ire-data-source-rule.html", "create IRE data source rule allowed fields order"),
 ("identification_rules", "https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_IdentificationRules.html", "identification rules criteria priority entry"),
 ("discovery_properties", "https://www.servicenow.com/docs/r/it-operations-management/discovery/r_DiscoveryProperties.html", "discovery properties configuration options"),
]
ts = time.strftime("%Y%m%d_%H%M%S")
OUT = Path(".")
for slug, url, q in DOCS:
    txt = rh.page_text(url)
    print(f"===== {slug}: {len(txt)} chars =====", flush=True)
    paras = rh.extract(txt, q, max_paras=12) if len(txt) > 300 else []
    body = "\n".join(f"  - {p}" for p in paras) if paras else txt[:3000]
    (OUT / f"{ts}_DOC_{slug}.md").write_text(
        f"# DOC {slug}\n\nURL: {url}\nquery: {q}\n\n## Extracted\n\n{body}\n")
    print(body[:800], flush=True)
print("DONE", flush=True)
