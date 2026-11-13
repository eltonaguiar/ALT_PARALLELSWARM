# v3 run

model: nvidia/nemotron-3.5-super-vl-120b-a12b
elapsed: 23.6s
research_calls: 3
error: None

## Question
What can you configure in the ServiceNow CI Class Manager related to Discovery, identification and reconciliation, and where in the interface are those settings?

## Answer
## What You Can Configure in ServiceNow CI Class Manager

CI Class Manager is the central location for configuring Identification and Reconciliation Engine (IRE) rules and settings. To access it, navigate to **Configuration > CI Class Manager** [1].

### 1. Identification Rules
You can configure identification rules for each CI class, including:
- **Identifier Entries** — choose attributes from the main table, a lookup table, or a combination to uniquely identify CIs
- **Priority** and **Criterion Attributes** for each identifier entry
- These rules control how Discovery matches discovered CIs to existing CIs in the CMDB (e.g., by serial number, name, MAC address, etc.)

**Interface location:** CI Class Manager > your CI class > **Identification Rule** tab [2][3]

### 2. Inclusion Rules (Advanced)
You can configure advanced inclusion rules that restrict which CIs are taken into consideration for identification. For example, you can create a rule specifying that you only want to process CIs with a particular status (e.g., "Operational").

**Interface location:** CI Class Manager > your CI class > **Inclusion Rule (Advanced)** tab [2]

### 3. Reconciliation Rules
You can configure reconciliation rules that control which data sources are allowed to update CI attributes after Discovery has collected data. For each rule you specify:
- **Discovery source** (e.g., ServiceNow Discovery, manual entry, SCCM)
- **Priority** — a higher priority value indicates greater authority over attribute updates

**Interface location:** CI Class Manager > your CI class > **Reconciliation Rules** tab [2][3]

### Summary Table

| Setting | What It Controls | Interface Location |
|---------|-----------------|-------------------|
| Identification Rules | How Discovery matches/identifies CIs | CI Class Manager > class > Identification Rule tab |
| Inclusion Rules (Advanced) | Which CIs are considered for identification | CI Class Manager > class > Inclusion Rule (Advanced) tab |
| Reconciliation Rules | Which data sources can update CI attributes and their priority | CI Class Manager > class > Reconciliation Rules tab |

### Sources
[1] ServiceNow KB1064718 — CMDB Identification and Reconciliation Engine fundamentals: https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB1064718
[2] ServiceNow Community — A Deep Dive into CI Class Manager and IRE: https://www.servicenow.com/community/cmdb-forum/a-deep-dive-into-ci-class-manager-and-ire-servicenow-cmdb/m-p/3486406
[3] ServiceNow Community — CMDB identification and reconciliation discussion: https://www.servicenow.com/community/cmdb-forum/need-help-in-cmdb-ci-class-expansion/td-p/3575528

## Transcript
```
[0] research(ServiceNow CI Class Manager configure Discovery identification reconciliation settings int) -> 1490c
[1] research(ServiceNow CI Class Manager identification rules inclusion rules reconciliation rules conf) -> 2988c
[1] research(ServiceNow CI Class Manager interface tabs Discovery identification reconciliation configu) -> 3935c
[2] answer()
```
