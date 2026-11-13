# Detecting duplicate CIs

- Source: https://www.servicenow.com/docs/r/zurich/servicenow-platform/configuration-management-database-cmdb/id-detect-dup-ci.html
- Release: Zurich
- Map: platcap

---

# Detecting duplicate CIs

When IRE identification process detects duplicate CIs, it groups each set of duplicate CIs into a de-duplication task for review and remediation. A large number of duplicate CIs might be due to weak identification rules. You
 can configure the identification engine to reconcile duplicate CIs.

During Identification and Reconciliation Engine (IRE) processes, handling of duplicate CIs is determined by the properties
glide.identification_engine.skip_duplicates
(set to true by default) and
glide.identification_engine.skip_duplicates.threshold
(set to 5 by default), and on the number of duplicate CIs that are detected. You can configure these properties so duplicate CIs are automatically
 reconciled, skipping duplication.

- If glide.identification_engine.skip_duplicates is true, and the number of duplicate CIs is less than the threshold specified by glide.identification_engine.skip_duplicates.threshold , then the oldest of the duplicate CIs is picked as a match and gets updated. That oldest duplicate CI also becomes the main CI for
 that set of duplicate CIs. The rest of the duplicate CIs are tagged as duplicates by setting their duplicate_of attribute to the appropriate main CI. During matching, IRE filters out any CI that is
 tagged as duplicate of any CI.
- If glide.identification_engine.skip_duplicates is false, then matching
 of duplicate CIs fails with an error, and none of the duplicate CIs are updated.
Also, the
glide.duplicate_ci_remediator.max.cis
property determines de-duplication processing for a large number of duplicate CIs. For more information, see the 'Large number of duplicate CIs' section in the
Duplicate CIs remediation
topic.

In either case, de-duplication tasks are always created.

Note:
For a duplicate CI, if any of the CI's attributes, other than
duplicate_of
, is updated by IRE processing, then the CI is no longer
 considered a duplicate CI. In that situation, the value of
duplicate_of
is
 cleared in the CI.
For more information about these properties, see
Properties
.

## Remediating de-duplication tasks

For information about reviewing and remediating de-duplicate tasks, and how the main CI is used, see
Duplicate CIs remediation
.
