# T12-D — completed disconnected storage comparison

## Outcome and evidence

The user ran `sqlite-vec-runtime-03` from preparation commit `e4db995` and reported `completed_pending_review_no_adoption`, receipt persistence, verified teardown and the safe reconnect message. Review of the local sanitized summary and closed meter confirms the full approved schedule: two safety controls, four B crash/reopen pairs and four A/B benchmark workers. No retry, source change, installation, download or additional native execution was performed during this review.

All **37 sealed identities and 20 prior records** were independently rehashed after the run and remain unchanged. Sources, staged assets, interpreter, selected fixtures and prior allocations are preserved. The original readiness receipt describes preparation, not the later execution state. Runtime-03 is now closed; its launcher must not run again.

Evidence remains local in `data/t12/sqlite-vec-runtime-03/summary.json`, `meter.json`, `seal.json`, `inputs.json` and `readiness.json`. Only sanitized metrics and authored source were reviewed; databases, raw vectors and private-path receipts were not opened. See [approved scope](../proposals/sqlite-vec-match-correction.md) and [preparation verification](sqlite-vec-match-preparation.md). Earlier A recovery evidence remains in the [runtime-02 report](sqlite-vec-runtime-followup-results.md).

## Correctness and recovery

The deadline sentinel exited125 as intended; the memory sentinel returned `memory_refused`. All four B recovery workers exited0 with integrity `ok` and recovered scoped-search assertions satisfied:

| Crash boundary | Contents / documents / references / chunks | Reconciliation observations |
|---|---|---|
| Before commit | 1 / 1 / 2 / 1 | No orphan or cleanup marker |
| After commit | 1 / 2 / 3 / 2 | No orphan or cleanup marker |
| Original file before commit | 1 / 1 / 2 / 1 | One orphan marker |
| Commit before cleanup | 2 / 2 / 3 / 2 | One cleanup marker |

These are the prescribed synthetic boundary checks, not proof of recovery from every crash or filesystem failure. Marker observations must not be described as a completed production reconciliation service. Four baseline A recovery pairs passed in runtime-02 and were deliberately not repeated here.

Each of the four benchmark workers completed **48 ranking/distance checks**, totaling **192**. Results matched the independent exhaustive reference, including ordered IDs and distance tolerance1e-6. Paired vector/query hashes match at each size. Both adapters also completed the authored controls for excluded closer rows, deterministic cutoff ties, empty scopes, version rejection, referenced-library deletion refusal and shared ownership after conversation deletion. Frozen-byte identity, reopen/integrity, rebuild and deletion assertions completed. These checks exercise synthetic storage behavior, not document extraction, answer quality or an implemented application.

## Paired search measurements

A is the standard SQLite/Python exhaustive baseline; B uses the exact reviewed sqlite-vec0.1.9 Windows DLL. Both use the same768-component frozen float32 vectors, seed12001+size,12queries, four passes and top5. B retains the approved eligible-rowid filter and `k=eligible_count`, fetching all eligible candidates before deterministic ranking. It also reads and validates eligible vector blobs in Python. These timings measure the complete adapter search, not an isolated native kernel or an optimized bounded top-K index.

| Vectors | Adapter | Median across all48 queries | Maximum query | Four pass medians, ms |
|---|---|---|---|---|
| 32 | A | 21.840 ms | 63.971 ms | 21.523, 38.960, 22.560, 19.791 |
| 32 | B | 9.914 ms | 17.060 ms | 10.145, 9.451, 9.579, 10.501 |
| 1000 | A | 477.963 ms | 656.423 ms | 465.199, 460.101, 498.879, 474.153 |
| 1000 | B | 282.300 ms | 311.013 ms | 282.873, 281.516, 136.388, 285.736 |

The pooled median ratio A/B is approximately2.20 at32vectors and1.69 at1000vectors. These are descriptive ratios for one fixed-order trial, not statistical estimates or guaranteed product speedups. A ran before B at each size; cold filesystem cache was not controlled. First and subsequent passes are shown without claiming rigorously cold/warm measurements. The variability, especially B's third1000-vector pass, remains visible. No product latency threshold was selected.

| Vectors / adapter | Native load, ms | Insert, ms | One-vector rebuild, ms | Reopen + integrity, ms | Delete + integrity, ms | Database bytes before / after deletion |
|---|---|---|---|---|---|---|
| 32 / A | 0 | 17.038 | 1.270 | 6.931 | 33.184 | 176128 / 176128 |
| 32 / B | 11.278 | 30.748 | 11.531 | 18.491 | 24.129 | 3366912 / 3366912 |
| 1000 / A | 0 | 288.289 | 1.288 | 29.153 | 65.573 | 4165632 / 4165632 |
| 1000 / B | 14.449 | 500.566 | 13.103 | 37.339 | 538.883 | 7401472 / 7401472 |

A has no candidate extension-load step. Deletion removed the prescribed references/data but did not shrink either database file; no vacuum or secure-erasure claim follows. B improves measured search latency while increasing footprint and several update costs. At1000vectors its database is about1.78times A's size; at32vectors the fixed overhead is much more prominent. Larger-scale behavior remains unknown; the historical10000-row timeout is closed and was not retried.

## Accounting, resources and boundaries

The terminal meter is closed at **72/96 conservative reservations**: preparation24, tests16, workers16, reporting16, cleanup0. Workers16 comprises14 actual owned workers plus two user launcher/controller reservations. Preparation remains1501.2886612000293 conservative seconds within1800; all five prepaid external blocks remain fully debited and closed. One native epoch and its original45-minute deadline are preserved. Exact final elapsed native duration was not persisted, so none is inferred from file timestamps. No counters or epochs were reset.

Across **512 samples**, minimum available RAM was10684911616bytes, maximum sampled controller private memory19693568bytes, maximum observed job peak53579776bytes and maximum runtime output footprint37986608bytes. Maximum completed-reading gap was0.13617339998017997seconds and maximum collection/full-iteration observation0.056344900047406554seconds, below the approved300ms ceiling. The largest worker result reported33820672bytes sampled private peak and44351488bytes peak working set; these measure different things from aggregate job peak. Staged assets are separately capped and sealed.

The run completed under the authored120-second worker deadlines,2GiB owned-job limit,512MiB controller limit,4GiB minimum headroom and disk/process boundaries without a reported resource stop. Sampled values are observations, not continuous guarantees. The existing interpreter is Python3.14.6 with SQLite3.50.4; the exact wheel/DLL/notices and their licensing/provenance limitations are documented in the approved proposal. No physical16GB-machine acceptance, filesystem confinement or general native-code safety is established. The user manually disconnected every external link; controller network observations are supplementary, not independent proof of all-link isolation. No model/OCR workload was included.

## Review and next decision

T12-D1–D6 are complete as a bounded evaluation and documentation package. The original MATCH authorization defect did not recur. Source/contract hashes and paired fixture identities remain unchanged; no further permission was added. The29-test preparation result remains historical evidence; no tests were repeated for this documentation-only closeout.

Recommend reviewing B as the preferred storage candidate for the next design decision, based on matching synthetic rankings/recovery and lower measured search latency. Compare that benefit with its larger files, update costs, native artifact/notice limitations and remaining scale uncertainty. This recommendation does **not** adopt it. A separate runtime-adoption decision must specify acceptable latency/storage limits and outstanding lifecycle/derived-storage requirements before product implementation. T16 grounding evaluation and T17/G2 remain subsequent gated work; full T12 acceptance, physical16GB validation, end-user functionality and Stage1 acceptance are not declared complete. Results-documentation Git approval remains separate.
