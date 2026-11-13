# 02 — Clarifications

These do not block the reference; they would change specific recommendations. Defaults
used are listed so the document remains actionable.

| # | Question | Default assumed | Why it matters |
|---|---|---|---|
| 1 | Which ServiceNow family/patches are in scope? | **Zurich**, English docs. | Dynamic IRE, AI summaries, and some UI labels are patch-sensitive. |
| 2 | Is **CMDB 360 / Multisource CMDB** licensed and enabled? | **No** for static guidance; §5.4 explains the dynamic path separately. | Dynamic reconciliation rules cannot work without it. |
| 3 | Is **Dynamic IRE** already committed for Hardware? | **No assumption**; verify `glide.identification_engine.dynamic_ire_enabled`. | Changes identification behaviour and rule maintenance. |
| 4 | Is **domain separation** enabled? | **No**, but §3.10/§5.4 call out the differences. | Schedules, credentials, and reconciliation scopes differ. |
| 5 | Which non-Discovery sources write CMDB? (SCCM, Intune, AWS, Azure, Qualys, etc.) | **Unknown**; the reference gives a generic authority model. | Data-source rules and reconciliation priorities need the real source list. |
| 6 | What is the scale? (IPs, MID Servers, schedules, domains) | **Pilot-scale examples**; §9 gives large-estate options. | MID clustering, Shazzam batching, and behavior design depend on it. |
| 7 | Are there **custom classes/identifiers** from a pre-Geneva upgrade? | **No**; §3.6 gives the conversion warning. | Legacy identifiers must be converted before `use_cmdb_identifiers=true`. |
| 8 | Is **Service Mapping** in scope? | **Out of scope** except shared IRE/Discovery. | Top-down entry points and traffic-based mapping need separate research. |
| 9 | What is the deletion policy for missing CIs? | **No deletion**; strategies are presented as options. | `Delete`/`Mark as absent` can remove network adapter/IP records. |
| 10 | Is there a sub-production instance for **Identification Simulation**? | **Assumed yes**; §5.9/§8.3 require it. | Rule changes should never be first tested in production. |
| 11 | Are there regulatory constraints on CI retention? | **Unknown**. | Affects delete vs absent vs retired strategies and duplicate remediation. |
| 12 | Which release introduced the instance? (new vs upgraded) | **Unknown**; defaults flagged where they drift. | Four hostname/IP defaults differ between new Zurich and upgraded instances. |

## Blockers

None. These are scoping questions, not missing evidence.

## What I would ask a sibling agent to do

- Pull the equivalent pages for the customer's exact release if it is not Zurich.
- Validate the CI Class Manager paths on a live sub-production instance.
- Provide the customer's source-of-truth matrix per CI class; then reconciliation rules
  can be turned from principles into concrete rows.
