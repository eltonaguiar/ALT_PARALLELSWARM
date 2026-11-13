# 03 — CI Class Manager: Bread-crumbs

The **CI Class Manager** is the central UI for viewing/editing CMDB class definitions,
IRE settings, CMDB Health, and some Service Mapping definitions.

## Access
- Navigate: `All > Configuration > CI Class Manager`
  (direct: `cmdb_ci_class_manager.do`).
- Roles: `sn_cmdb_admin` = full access; `sn_cmdb_editor` / `itil` = read access.
- Does **not** manage non-CMDB tables.

## Screen layout
1. Open **CI Class Manager**.
2. Click **Hierarchy** to expand the **CI Classes** tree.
3. Select a class → the **class navigation bar** appears with these tabs.

## Class navigation bar (what each tab controls)

| Tab | Purpose | Key actions |
|-----|---------|-------------|
| **Class Info → Basic Info** | Class metadata | View/edit display name, table name, description, icon; extensible / principal class flags. Table name is read-only after creation. |
| **Attributes** | Table columns | View/add/edit attributes. **Set `Identification = true`** on an attribute to make it a CI identifier. Use the **Added** tab → *Insert new column*. |
| **Identification and Reconciliation** | IRE rules for the class | View/create/delete identification rules, inclusion rules, reconciliation & data-refresh rules. |
| **Dependent Relationships** | Hosting/containment rules | Define which relationships are required for identification (dependency rules). |
| **Suggested Relationships** | Relationship suggestions | Diagram of suggested relationships; add/delete via *New*. Used by the CI relationship editor. |
| **All Relationship Rules** | Combined view | Suggested + dependent relationships in one diagram. |
| **Health** | CMDB Health | Configure health properties, scorecards, rules/settings per class. |
| **CI List** | Class CIs | List/create/delete CIs of this class. |

## Creating / extending a class (wizard)
1. `All > Configuration > CI Class Manager` → **Hierarchy** → select parent class.
2. **Add Child Class** (only if the parent is extendable).
3. **Provide Basic Info**: Display name, Table name (auto `u_cmdb_ci...`), Description, Icon, Extensible, Principal Class → **Next**.
4. **Add Attributes**: `+` add columns; set `Identification=true` for identifiers → **Next**.
5. **Set Identification Rule**: review the **derived** rule + **Identifier Entries**; use **Replace** to customize.
6. **Dependencies**: **Add dependency** (appears only if dependent identification rules exist).
7. **Add Reconciliation Rules**: add **Reconciliation Rules** and **Data Refresh Rules**.
8. **Add Suggested Relationships**: review diagram; **New** to add one (select Relationship + Target Class).
9. **Done**.

## Adding a suggested relationship (quick path)
- In CI Class Manager: select class → **Suggested Relationships** → **New** → choose Relationship + Target Class → **Save**.
- Or `All > Configuration > Relationships > Suggested Relationships` → **New**.
- Fields: **Base class**, **Relationship**, **Dependent class**. Example: Oracle *Is Hosted On* Linux Server.
- Removing a suggested relationship does **not** affect relationships already created/updated by Discovery.

## Creating/editing a CI relationship (from a CI)
- Open the CI form → **Related Items** → **Add CI relationship** (+).
- **Use suggested relationship**: pick relationship type → pick CIs → `+` to add.
- Filters: hide CI / user / group relationships (stored in `ci_manage_relationships_filter_hint.*`).
- Or clear *Use suggested relationship* and use **Downstream/Upstream Relationships**.

## Where the IRE-related bread-crumbs land
- **Identification rules** (identifier entries): Regular / Lookup / Hybrid — see doc 04.
- **Reconciliation rules** live in tables `cmdb_reconciliation_definition` (static) and
  `cmdb_dynamic_reconciliation_definition` (dynamic); **data refresh** uses `cmdb_datasource_last_update`.
- **Deduplication allowed classes**: `cmdb_duplicate_lookup_related_allowed_class`.

## Sources
- CI Class Manager landing — servicenow.com/docs (ci-class-manager-landing-page)
- View/edit class definitions — servicenow.com/docs (t_ViewTableDefinitions)
- Create a CI class — servicenow.com/docs (t_CreateCIType)
- Add a suggested relationship — servicenow.com/docs (t_AddANewSuggestedRelationship)
- Create/edit a CI relationship — servicenow.com/docs (t_CreateCIRelationship)