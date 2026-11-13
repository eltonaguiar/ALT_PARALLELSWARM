# Evidence excerpts

Short verbatim excerpts from the ServiceNow Brazil documentation retrieved on
2026-11-13. Full topic list and API URLs: `SOURCES.md` / `topics.json`.

> These are technical-documentation quotations used for traceability. They are not
> reproduced in full; the reader should use the API URLs to inspect the source.

## Discovery model and phases

> "Discovery is an automated process that continuously scans and identifies all the
> components within the IT infrastructure. It plays a crucial role in maintaining an
> accurate and up-to-date CMDB 360 with the information it finds."
>
> — *Discovery* (`discovery-root`)

> "The phases of horizontal discovery are: ... Scanning ... Classification ...
> Identification ... Exploration."
>
> — *Exploring Discovery* (`discovery-get-started`)

> "Identifiers accurately determine the identity of the device to avoid the creation of
> duplicate CIs. This identification step only takes place for the Configuration item
> type of discovery, not for the other types of discovery."
>
> — *Discovery identifiers* (`discovery-identifiers`)

> "When you use patterns for Discovery, the identity probe isn't used. Discovery uses the
> appropriate identifier rules based on the CI type that you're trying to discover as
> specified in the pattern operations."
>
> — *How Discovery identifiers work* (`discovery-identifiers-how`)

> "Serial numbers are necessary for accurate asset tracking. ... do not configure
> sensors or patterns to modify the serial number syntax, such as adding a custom prefix.
> Non-standard serial numbers can lead to inaccurate asset tracking."
>
> — *Discovery identifiers* (`discovery-identifiers`)

## IRE and reconciliation

> "IRE prevents duplicate CIs by uniquely identifying CIs. IRE reconciles CI attributes
> by allowing only authoritative data sources to write to CMDB."
>
> — *Identification and Reconciliation Engine (IRE)* (`ire-engine`)

> "Reconciliation is required only for update operations, when the identification
> process identifies a CI in the CMDB that matches an incoming CI in the payload. When
> IRE inserts a new CI, reconciliation is not applied."
>
> — *Components and process of Identification and Reconciliation* (`ire-components-process`)

> "If `glide.identification_engine.skip_duplicates` is true, and the number of duplicate
> CIs is less than the threshold specified by
> `glide.identification_engine.skip_duplicates.threshold`, then the oldest of the
> duplicate CIs is picked as a match and gets updated. That oldest duplicate CI also
> becomes the main CI ... The rest of the duplicate CIs are tagged as duplicates by
> setting their `duplicate_of` attribute to the appropriate main CI."
>
> — *Detecting duplicate CIs* (`detect-duplicate-ci`)

> "If `glide.identification_engine.skip_duplicates` is false, then matching of duplicate
> CIs fails with an error, and none of the duplicate CIs are updated. ... In either case,
> de-duplication tasks are always created."
>
> — *Detecting duplicate CIs* (`detect-duplicate-ci`)

## Data source rules

> "When IRE processes an insert operation that is prohibited by an IRE data source rule,
> the insert operation fails. ... `INSERT_NOT_ALLOWED_FOR_SOURCE`"
>
> — *Create an IRE data source rule* (`ire-data-source-rule`)

> "IRE data source rules have no impact when dynamic reconciliation rules are in effect."
>
> — *Create an IRE data source rule* (`ire-data-source-rule`)

## CI Class Manager

> "To access the CI Class Manager, navigate to `All > Configuration > CI Class Manager`.
> In general, the `sn_cmdb_admin` role has full access to all sections of the CI Class
> Manager and the `sn_cmdb_editor` user role has read access only."
>
> — *CI Class Manager* (`ci-class-manager`)

> "The class for which you create a dependent relationship rule, must have a dependent
> identification rule."
>
> — *Create dependent relationship rules* (`dependent-relationship-rules`)

## Deletion strategies and schedules

> "Deletion strategies are available only with patterns, not probes/sensors."
>
> — *CI deletion strategies for pattern discovery* (`discovery-deletion-strategy`)

> "On Demand ... Doesn't run on a schedule. Select Discover now to run Discovery. This is
> the default option."
>
> — *Run options for discovery schedules* (`run-options`)

## Source lookup

Each excerpt maps to a row in `topics.json`; use the `api_url` field to retrieve the
full topic. Canonical reader URLs for the major pages are listed at the end of
`SOURCES.md`.
