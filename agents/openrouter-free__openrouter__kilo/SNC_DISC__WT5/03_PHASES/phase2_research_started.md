# Phase 2 — research_started

2026-11-13T08:52Z

Agent `openrouter-free__openrouter__kilo` Phase 2 research in progress.
Pass 2 of 3: CI Class Manager bread crumbs, identification & reconciliation rules, duplicate/insert-update behavior.

**Evidence sources:**
- KB0869861: How to troubleshoot duplicate CMDB CI records (full IRE logic: identification → reconciliation → insert/update flow)
- KB0755747: Discovery doesn't update operational status of retired CIs when rediscovered (CMDB lifecycle)
- Support portal KB articles on CI Class Manager and identification rules
- developer.servicenow.com docs on Discovery properties

**Current progress:**
- IRE payload processing: validate → loop identification rules → query CMDB → CI found? Yes: reconciliation rules → update/No: create → No more rules → create
- Identification rules: Derived (inherited from parent), Independent (serial number only), Correlation ID first matching criteria
- CI Class Manager: Configuration > CI Class Manager — view per-class identification rules
- Inclusion rules: Configuration > Identification/Reconciliation > Identification Inclusion Rules — avoid "Class" condition on parent tables
- Duplicate prevention: glide.discovery.multi_page_serial_mode = true for multipage payloads
- Reconciliation: Does source have permission? Inclusion rules? ACLs? Business rules?