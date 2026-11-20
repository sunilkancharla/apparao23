# Approved fake-only live storage repair

**Date:** 2026-11-14 (Asia/Calcutta). User approved a24-start/10-active-minute fake-worker-only repair and committing the reviewed fixes/diagnostic notes. No new offline native allocation, model/OCR run, installation, download or adoption was approved or performed.

## Change and boundary

The combined runner now uses a separate `live_tree_bytes` counter. It skips descendant entries that have already disappeared after enumeration; those entries no longer occupy storage at inspection time. It also tolerates an enumerated child directory disappearing before traversal. It does not catch permission denial, other I/O failures, missing required roots or errors outside the run tree. Root directory type/link attributes are checked before/after traversal, and replacement of the root during a scan is refused.

The512-MiB combined run,32-MiB raw and8-MiB answer caps are unchanged. Existing reparse-point checks remain, with explicit symbolic-link rejection. Directory-to-file changes stop rather than silently continuing. The original strict static/isolation helper is unchanged. The new counter remains a sampled storage observation, not a kernel-enforced disk quota, atomic whole-tree snapshot or filesystem sandbox. Files created after a directory listing can enter the next sample; observed over-cap storage still stops.

Reporting improvements from the preceding [diagnostic](combined-storage-diagnostic.md) remain: public error codes/area/category/project-source location, exact filenames in a private ignored receipt only, no raw path in observer stop messages. The exact historical combined-02 missing filename remains unknown.

## Test-first verification

New live-count tests first failed (24 total, four errors). After implementation, **24 stdlib/fake tests passed in1.262s**; Ruff passed after correcting an import separator. The controlled atomic replacement and file deletion cases run against both counters: the strict helper still raises the original FileNotFoundError, while the live combined scan succeeds. Fake threads are joined and bounded event waits prevent hanging tests.

Additional positive/negative checks cover exact stable byte totals, cap overflow, missing/non-directory required roots, required root deletion during traversal, vanished child directories, permission errors, outside-tree missing errors and reparse-marked entries. The existing deadline, accounting, overlap, CPU/residency, endpoint, privacy and ownership regressions remain passing. No actual large file, unsafe link, inference engine or model server was started by these checks.

Evidence: ignored `data/t11/storage-repair-01/` contains the linked budget, failing/passing checks and Ruff output. Conservative reservations22/24 include final docs/Git closeout, leaving two cleanup slots. Execution remained inside10active minutes, with zero OCR/model roots, API calls, downloads or installation. The stopped combined-02 meter's hash is unchanged; neither stopped ledger/seal was reset or resealed. Earlier diagnostic evidence remains separate at20/24 starts.

## Commit and next gate

The user approved committing the reviewed deadline repair, failure reports, sanitized diagnostics, live-counter repair, regressions and affected progress/handoff documentation. Only those source/docs belong in the scoped commit; runtime data, receipts, assets, sample documents and unrelated reference files stay excluded.

Both combined native runs remain stopped. Do not run their commands. A fresh bounded continuation must be proposed and approved before preparing/resealing a new offline handoff. Native overlap/resource behavior and remaining T09/T11/G2 quality/adoption gates remain unproven; fake success is not a combined feasibility result.
