# v3 run

model: nvidia/nemotron-3.5-super-vl-120b-a12b
elapsed: 57.3s
research_calls: 4
error: None

## Question
How do you configure ServiceNow to avoid duplicate CIs and to control whether an existing CI is updated versus a new CI inserted into the CMDB?

## Answer
# Configuring ServiceNow to Prevent Duplicate CIs and Control Update-vs-Insert Behavior

## Core Mechanism: The Identification and Reconciliation Engine (IRE)

ServiceNow uses the **Identification and Reconciliation Engine (IRE)** as a centralized framework to decide whether an incoming CI payload should **update an existing CI** or **insert a new CI** into the CMDB. The IRE handles both creation of new CIs and updates to existing ones, and it helps maintain CMDB integrity when multiple data sources feed configuration data【https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB1064718】.

## 1. Configure Identification Rules (the update-vs-insert decision)

Identification Rules are the primary control for determining whether a CI already exists. When a new CI is introduced, the IRE checks the CI Identification Rules for that CI class:

- **If a match is found** → ServiceNow updates the existing CI record with the new information.
- **If no match is found** → a new CI record is created in the appropriate CI class【https://www.servicenow.com/community/cmdb-articles/elevating-cmdb-data-quality-with-well-defined-ci-identification/ta-p/2857355】.

### How to configure them
- Go to **Configuration > CI Class Manager** to see and edit the identification rules that apply to a specific CI class【https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0869861】.
- Ensure **strong identifiers** (for example, Serial Number + Manufacturer, or Name + IP/MAC combinations) are consistently configured for related classes【https://www.servicenow.com/community/cmdb-forum/how-to-avoid-duplicate-ci-creation/m-p/3498456】.
- Identification rules can be priority-based and hierarchical—for example, first check Serial Number, then Name, then IP Address + MAC Address. They can also reference related lists (such as IP Address tables)【https://www.servicenow.com/community/itom-forum/identification-and-reconciliation-rules-versus-coalesce/m-p/986797】.
- **Inclusion rules** can narrow which CIs are included in the identification process (e.g., only CIs with Operational Status = Operational). However, inclusion rules can lead to duplicate CIs if not configured properly【https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB1064718】【https://www.servicenow.com/community/cmdb-articles/elevating-cmdb-data-quality-with-well-defined-ci-identification/ta-p/2857355】.

### Important caveat
Duplicate CIs are identified **in real-time as data is processed by the IRE**, not by a separate daily job. If data is inserted into `cmdb_ci` without going through the IRE (for example, via GlideRecord or the REST API Explorer), the identification rules are bypassed and duplicates can still be created【https://www.servicenow.com/community/in-other-news/duplicate-configuration-items-in-the-servicenow-cmdb/ba-p/2271418】.

## 2. Configure Reconciliation Rules (control which sources may update)

While Identification Rules answer *"Does this CI already exist?"*, Reconciliation Rules answer *"Which data source is allowed to update this CI or its attributes?"*【https://www.servicenow.com/community/cmdb-articles/cmdb-understanding-identification-and-reconciliation-rules-and/ta-p/3520826】.

- Reconciliation rules specify which data sources can update a table or a set of table attributes, and they can be defined at the parent and/or child class level【https://www.servicenow.com/community/cmdb-articles/cmdb-identification-reconciliation/ta-p/2301712】.
- Best practice: ensure there is a reconciliation rule in place for **each data source authorized to update CIs** in the CMDB【https://www.servicenow.com/community/cmdb-articles/cmdb-identification-reconciliation/ta-p/2301712】.
- Together, Identification and Reconciliation rules help prevent duplication, reconcile CI attributes, reclassify CIs, and allow only authoritative data sources to update CI records【https://www.servicenow.com/community/cmdb-articles/cmdb-identification-reconciliation/ta-p/2301712】.

## 3. Use IRE for every data source (best practice)

To avoid duplicates, route all CMDB population through the IRE:

- **Discovery**: Use IRE for Discovery data so CIs are matched against existing records before insertion【https://www.servicenow.com/community/cmdb-forum/how-to-avoid-duplicate-ci-creation/m-p/3498456】.
- **Import Sets / Transform Maps**: Use Identification and Reconciliation for import sets as well【https://www.servicenow.com/community/itom-forum/identification-and-reconciliation-rules-versus-coalesce/m-p/986797】.
- **Service Graph Connectors**: These rely on the IRE's priority-based matching system rather than traditional coalesce fields【https://www.servicenow.com/community/itom-articles/how-to-verify-identification-rules-for-service-graph-connectors/ta-p/3417132】.
- **REST API / direct inserts**: Avoid inserting CIs via GlideRecord or raw REST API calls outside the IRE, because those mechanisms do not check identification rules【https://www.servicenow.com/community/in-other-news/duplicate-configuration-items-in-the-servicenow-cmdb/ba-p/2271418】.

## 4. Coalesce fields (simpler, legacy alternative)

In transform maps, a **coalesce field** can be used to match on a single unique field (e.g., Serial Number) to decide update vs. insert. However, Identification and Reconciliation rules are more powerful because they support complex, multi-criteria, priority-based matching across related tables【https://www.servicenow.com/community/itom-forum/identification-and-reconciliation-rules-versus-coalesce/m-p/986797】. For CMDB data, the IRE is strongly recommended over relying solely on coalesce fields.

## 5. Detect and remediate existing duplicates

- The **CMDB Health Dashboard** runs a scheduled job called **Correctness Score Calculation** (available under CMDB Health Preferences). It scans `cmdb_ci` records against their class's CI Identification Rules; records identified as duplicates are assigned to a de-duplication task and marked as "duplicate"【https://www.servicenow.com/community/in-other-news/duplicate-configuration-items-in-the-servicenow-cmdb/ba-p/2271418】.
- Starting with the **New York release**, the `cmdb_ci` table includes a **Duplicate Of** field. When the IRE inserts a CI detected as a duplicate of two or more existing CIs, the duplicate CI references the earliest-created CI in this field【https://www.servicenow.com/community/in-other-news/duplicate-configuration-items-in-the-servicenow-cmdb/ba-p/2271418】.

## Summary Checklist

| Goal | Configuration Action |
|------|---------------------|
| Prevent duplicate CIs | Define strong, consistent Identification Rules per CI class in CI Class Manager; route all sources through IRE |
| Update existing CI instead of inserting | Ensure incoming data matches an active Identification Rule; use Reconciliation Rules to authorize the updating source |
| Control which source wins | Set up Reconciliation Rules per data source and attribute |
| Catch duplicates already in CMDB | Run CMDB Health / Correctness Score Calculation; review de-duplication tasks and the Duplicate Of field |

**Key sources:** ServiceNow KB0869861, KB1064718; ServiceNow Community articles on CI Identification Rules, CMDB Identification & Reconciliation, and duplicate CI identification.

## Transcript
```
[0] research(ServiceNow CMDB avoid duplicate CIs identification reconciliation update vs insert coalesc) -> 2266c
[0] research(ServiceNow CI identification rules configure duplicate CI prevention CMDB) -> 4161c
[1] research(ServiceNow CMDB identification rules configuration coalesce field update existing CI inser) -> 3710c
[1] research(ServiceNow reconciliation rules configure update vs insert CI CMDB identification) -> 2394c
[2] no tool call: # Configuring ServiceNow to Prevent Duplicate CIs and Control Update-vs-Insert Behavior

## Core Mechanism: The Identification and Reconciliation Engi
[3] answer()
```
