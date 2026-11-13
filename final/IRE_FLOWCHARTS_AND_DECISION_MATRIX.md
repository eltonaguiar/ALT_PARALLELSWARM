# IRE Flowcharts & Decision Matrix

## 1. IRE Pipeline Flowchart

```mermaid
flowchart TD
    Payload[Payload Item Arrives] --> FastPath{Fast Path:<br/>source_name + source_native_key<br/>in sys_object_source_info?}
    
    FastPath -->|Yes & skip_sys_object_source_matching=false| UpdatePath[UPDATE Existing CI]
    FastPath -->|No OR skip_sys_object_source_matching=true| IdMatch[Identification Rule Matching]
    
    IdMatch --> Match{Match Found?}
    
    Match -->|Yes| InclusionCheck{Inclusion Rule<br/>Allows This CI?}
    Match -->|No| DSRGate[IRE Data Source Rule Gate]
    
    InclusionCheck -->|Yes| Reconcile[Reconciliation Rules]
    InclusionCheck -->|No| InsertPath[INSERT New CI<br/>⚠️ Potential Duplicate]
    
    Reconcile --> StaticOrDynamic{Static or Dynamic<br/>Reconciliation?}
    
    StaticOrDynamic -->|Static| DataRefresh{Data Refresh Rule<br/>Stale?}
    StaticOrDynamic -->|Dynamic| CMDBWrite[CMDB Write<br/>Dynamic wins]
    
    DataRefresh -->|Not Stale| CMDBWrite[CMDB Write<br/>Static wins]
    DataRefresh -->|Stale & Lower-Priority<br/>Source Authorized| CMDBWrite
    DataRefresh -->|Stale but No Auth| SkipField[Field Skipped]
    
    DSRGate --> DSRBlocked{Insert Not Allowed?}
    DSRBlocked -->|Yes| PartialPayload[Partial Payload Stored<br/>CreateOrUpdateCIEnhanced()]
    DSRBlocked -->|No| InsertCI[INSERT New CI]
    
    CMDBWrite --> Done[Complete]
    InsertCI --> Done
    PartialPayload --> Done
    SkipField --> Done
    InsertPath --> Done
    
    classDef fast fill:#e8f5e9,stroke:#2e7d32
    classDef gate fill:#fff3e0,stroke:#ef6c00
    classDef write fill:#e3f2fd,stroke:#1565c0
    classDef decision fill:#fce4ec,stroke:#c2185b
    
    class FastPath,UpdatePath fast
    class DSRGate,InclusionCheck,DSRBlocked gate
    class CMDBWrite,InsertCI,PartialPayload write
    class Match,StaticOrDynamic,DataRefresh decision
```

## 2. Discovery Source A vs B Decision Matrix Flowchart

```mermaid
flowchart TD
    Start[Discovery Source A or B<br/>payload for cmdb_ci_computer] --> FastPath{Fast Path:<br/>source + native_key<br/>in sys_object_source_info?}
    
    FastPath -->|Yes & skip_sys_object_source_matching=false| UpdateA[UPDATE existing CI<br/>Reconciliation applies]
    FastPath -->|No OR skip=true| Identify[Identification Rule Matching<br/>Hardware Rule entries]
    
    Identify --> Match{Match Found?}
    
    Match -->|Yes| Inclusion{Inclusion Rule<br/>Active record condition<br/>allows this CI?}
    Match -->|No| DSRGate[IRE Data Source Rule<br/>for this Source + Class]
    
    Inclusion -->|Yes| Recon[Reconciliation Rules<br/>Static or Dynamic]
    Inclusion -->|No| InsertPath[INSERT NEW CI<br/>⚠️ Duplicate Risk]
    
    Recon --> ReconType{Reconciliation Type?}
    
    ReconType -->|Static| DataRefresh{Data Refresh Rule<br/>for this Source?}
    ReconType -->|Dynamic| DynamicWin[Dynamic Wins<br/>Value-based via CMDB 360]
    
    DataRefresh -->|No Rule| PriorityCheck{Priority Check:<br/>This Source vs Other}
    DataRefresh -->|Rule Exists| StaleCheck{Field Stale?<br/>(Effective Duration<br/>vs cmdb_datasource_last_update)}
    
    PriorityCheck -->|This Source Higher Priority| UpdateField[Update Field]
    PriorityCheck -->|This Source Lower Priority| EmptyCheck{Field Empty?}
    
    EmptyCheck -->|Yes & override.null=true| UpdateField
    EmptyCheck -->|No| RejectUpdate[Reject Update]
    
    StaleCheck -->|Not Stale| PriorityCheck
    StaleCheck -->|Stale & Lower-Priority<br/>Source Authorized by Recon| UpdateField
    StaleCheck -->|Stale but Not Authorized| RejectUpdate
    
    DSRGate --> DSRBlocked{Insert Not Allowed?}
    DSRBlocked -->|Yes| Partial[Partial Payload<br/>Stored for Merge]
    DSRBlocked -->|No| InsertCI[INSERT New CI]
    
    classDef update fill:#e3f2fd,stroke:#1565c0
    classDef insert fill:#fff3e0,stroke:#ef6c00
    classDef reject fill:#fce4ec,stroke:#c2185b
    classDef gate fill:#f3e5f5,stroke:#7b1fa2
    classDef decision fill:#e8f5e9,stroke:#2e7d32
    
    class UpdateA,UpdateField,DynamicWin update
    class InsertPath,InsertCI,Partial insert
    class RejectUpdate reject
    class DSRGate,Inclusion gate
    class Match,ReconType,DataRefresh,StaleCheck,PriorityCheck,EmptyCheck,DSRBlocked decision
```