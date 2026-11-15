# T12-D — MATCH permission correction and remaining comparison

**Status: approved for T12-D1–D6, its exact execution boundary and five planning documents' commit.** User answered "I do approve both" to the explicit package/boundary and commit request. Results are committed as `4146d7c`. Fresh runtime-03 meter reserves12preparation starts and fully debits the first300-second external work block before initialization/review/Git. No successor source/staged assets/native work yet. Complete covered steps without repeated task-start approvals. Later source/results commits and runtime adoption retain separate gates; requested-decision wording below is historical.

## Objective and fixed scope

The [runtime-02 result](../benchmarks/sqlite-vec-runtime-followup-results.md) exposed a missing permission: the approved query uses MATCH, but the function allowlist omitted `match`. Correct that single permission, demonstrate authorization of the complete fixed SQL statement before another handoff, and evaluate the remaining B recovery/paired-search coverage. Preserve every previous allocation, source, seal, asset and receipt unchanged; unused old allowances do not fund this package.

Proposed fresh identities:

- Ignored run: `data/t12/sqlite-vec-runtime-03/`, run ID `sqlite-vec-runtime-03`.
- Ignored staging: `.venv/.cache/sqlite-vec-review/part-d-01/`.
- At most three new authored evaluation files: `tests/evals/spikes/sqlite_vec_match_trial.py`, `test_sqlite_vec_match_trial.py`, `sqlite-vec-match.json`.

Derive from the reviewed followup harness; limit changes to fresh identities, the `match` permission, the declared remaining-work schedule, preparation bookkeeping below and necessary tests. No product code, parser, model, frontend, dependency or architecture adoption. Reuse trusted helpers without editing them or invoking old entry points. Review the successor diff and unchanged native adapter/query/worker-launch logic explicitly.

## Architecture and dependency review before implementation

Retain the reviewed SQLite baseline A, sqlite-vec B cosine query, scoped eligible-rowid selection, `k=eligible_count`, complete candidates before deterministic top5 and transactional mapping. Do not optimize/change SQL, drop scope checks or switch algorithms. Keep version/hash/original-file/readiness checks and all authorizer restrictions. The only newly approved function would be **`match`**; no unknown-function fallback or disabling the authorizer. If another permission/query/native requirement appears, stop and record it.

Use the [original exact artifact table](sqlite-vec-runtime-comparison.md) and [accepted companion-notice policy](../decisions.md). Cache-only sqlite_vec-0.1.9-py3-none-win_amd64.whl remains292804bytes/SHA256 `4a28dc12fa4b53d7b1dced22da2488fade444e96b5d16fd2d698cd670675cf32`; DLL289280bytes/SHA256 `fcf98662a7ad9dce394b96a88f91032047823831b951c76636787c312a6476e6`. Preserve the same1068-byte MIT and10931-byte Apache texts and their original pinned hashes. Recheck existing Python3.14.6 executable/DLL identities and SQLite3.50.4; drift stops preparation.

Stage only DLL/notices at the new project-venv cache root after verifying exact bytes and safe ancestors. No Python-distribution installation, wrapper/NumPy import, dependency/lock update, PATH/global/service change, build, download or new public research. Static notice omission and binary/source-provenance limitations remain visible. Exact versions/bytes do not imply native safety or final storage adoption.

## Test-first authorization contract

First demonstrate the omitted callback with actual stdlib SQLite, a controlled in-memory table matching the fixed query's columns, and a harmless Python-registered `match` stub. Run the exact parameterized SELECT shape through the real authorizer while recording its function callbacks. The regression must fail with the old function set, then pass when only `match` is added. Register the stub only in tests; never substitute it for native search in the offline trial.

Check missing/wrong stub/schema setup explicitly so a test setup failure cannot masquerade as the original denial. Assert callback names and query completion with the corrected contract. Retain denied ATTACH/DETACH, unknown functions, SQL extension loading, optional filesystem/static-pointer functions and unsafe PRAGMAs. Keep inherited loading-finally, scoped ties/candidate completeness, frozen float32/idempotence, version/reference, time/epoch/reuse and owned-loop/cleanup regressions.

This tests SQLite authorization and statement shape, **not vec0 planning/filtering/distance/recovery correctness**. The subsequent disconnected trial must still establish those properties. Do not claim a fake worker schedule exercised native SQL.

## Proposed remaining native schedule

1. Run the same deadline and memory sentinels for the new owned boundary:2workers.
2. Run B's four real crash boundaries with a separate counted reopen/search worker after each:8workers. Preserve before/after commit, original-file-before-commit and commit-before-cleanup cases, exact counts, integrity/FK checks, scoped recovered retrieval and marker reconciliation.
3. Run fresh paired A/B measurements for32and1000vectors in that fixed order:4workers. Each size retains768float32 components, seed12001+size,12queries,four passes,top5,1e-6tolerance and independent exhaustive rankings. Require vector/query hashes matching the selected earlier fixtures. Retain excluded closer rows, cutoff ties, empty/short scopes, version/original validation and shared-library controls.

Total **14owned workers plus2launcher/controller reservations =16planned worker-category starts**. The four A crash/reopen pairs already completed in runtime-02 are carried forward as historical evidence and are not repeated in this package. This scope reduction is explicit: new A workers supply paired performance/reference and scoped controls, not fresh A crash coverage. Old10000-row timeout remains closed; no10000-row trial. Report cache/order bias and no product latency threshold unless separately agreed.

Measure native load, insertion, query samples, single-vector rebuild, reopen/integrity, deletion, footprint and memory only where actually observed. Stop at the first unsupported permission/query, failure or resource boundary. No automatic retries, microtrials outside the meter, partial schedule advertised as complete, or speedup claim before both paired measurements exist.

## Shared limits and preparation across session pauses

Request a **new96-start allocation**, additional to closed runtime-02's70/96history and other retained ledgers. Categories remain preparation24,tests16,workers32,reporting16,protected cleanup8. Count/pre-reserve every shell/tool/Git/test/control/controller/worker/native descendant attempt, including failures; no category borrowing. Link runtime-02's13prior records plus its meter,summary,readiness,seal and three authored followup files:20prior records. Seal exact new sources/contracts/fixtures/assets/interpreter/helpers and all linked identities after review; report the actual seal count, not a predicted count.

Limits stay30active preparation minutes, one45-minute disconnected native epoch,120seconds per worker,2GiB aggregate owned job,512MiB sampled controller private memory, at least4GiB available RAM, controller plus at most one worker,100ms target/300ms hard completed-reading/collection/full-iteration boundary,512MiB outputs plus1MiB staged assets, and zero downloads/API/model/OCR calls. The target stays Windows11/16GB/CPU-only; observations on the actual host do not prove physical16GB acceptance.

To prevent another uncertain external reporting segment, **pre-debit bounded external preparation blocks before work**, with fixed duration/deadline/identity recorded. Each block is at most300seconds; enforce expiry before continuing commands, retain the full conservative debit on interruption, and never refund it based on inferred idle time or file timestamps. A resumed session may start a new block only after verifying the previous block's charged record, stopped owned work, unchanged identities and sufficient original remaining allowance. Human waiting after a stopped block consumes no new block. No reset of counters or native epochs.

Internal code-owned staging/check segments retain monotonic measurements and fixed process/watchdog limits; charge them conservatively in addition to external reservations where applicable. An unexplained internal open segment or uncertain owned process still stops—this proposal does not authorize clearing arbitrary markers or another timestamp-based exception. Persist a checkpoint/end-of-block status at each work milestone. After final reviewed readiness, no active external timer may remain across the user handoff. Include bounded final documentation/Git work in the preparation allowance before freezing it. If these accounting controls cannot be implemented within the narrow scope or allowance, stop for review rather than widening the task.

## Native execution boundary

The native DLL retains the user's Windows account access: this synthetic trial has **no filesystem confinement**. Approval must explicitly include that fresh boundary. Use no real documents. User physically disconnects Wi-Fi/Ethernet/tethering/every external link before running the standalone launcher and attests OFFLINE. Remain disconnected through verified owned teardown and the safe reconnect message. Kernel jobs and the SQL authorizer do not prove native file/network containment.

Connected work is limited to fake/stdlib tests, exact cached-byte staging and static review. No candidate DLL loading, model/OCR/server work or performance workers while connected. No runnable handoff until independent readiness and the preserved closed-run checks pass. Source/asset drift, wrong identity/version/scope, unsupported query/function, accounting/resource/epoch failure, reconnect or uncertain cleanup stops without retry/reset/reseal. No firewall/policy/permissions workaround.

## Ordered tasks, prerequisites and acceptance

| ID | Objective and prerequisite | Acceptance / verification |
|---|---|---|
| T12-D1 | Exact package approval; design/dependency/accounting review before code | Fresh roots absent;20prior hashes, exact cached assets/interpreter and fixed single-function/schedule changes recorded; charged preparation block/process reservations durable |
| T12-D2 | D1; positive-query authorization regression first | Old allowlist meaningfully refuses MATCH; actual stdlib callbacks and exact fixed statement pass only with match added; dangerous-function/attachment/PRAGMA denials preserved |
| T12-D3 | D2; minimal successor and bounded pause accounting | At most3new evaluation files, focused/inherited tests and Ruff pass; diff confirms only declared changes; prepaid interruption/resume/exhaustion and no-native-epoch-renewal controls verified |
| T12-D4 | D3; staging and independent readiness | Exact DLL/notices, regenerated selected fixtures, full source/interpreter/prior seal and launcher syntax verified; positive SQL gate plus delayed-handoff fake check honest; counters/time/block closure and zero connected load evidence saved |
| T12-D5 | D4; one user-operated disconnected remaining trial |14owned-worker schedule or truthful partial stop; B recovery/query/paired results only as observed; actual owned teardown and safe reconnect; no retry |
| T12-D6 | Verified cleanup/reconnection; results/review | Sanitized metrics/counters and prior hashes checked; factual report/README/PLAN/TODO/checkpoint, readable diff and separate source/results commit request; no adoption inferred |

Work sequentially, save checkpoints after D1, tests/review and readiness/results. Read verified local incremental-implementation, test-driven-development, security-and-hardening and code-review-and-quality skills before their relevant steps; documentation-and-adrs for closeout. This proposal uses planning-and-task-breakdown with existing root PLAN/TODO. Optional developer tools are unnecessary here: SkillSpector remains deferred, MarkItDown outcome unchanged, UI UX Pro Max retains its separate pre-frontend gate. No installation/evaluation of unrelated tools.

Create preparation/results reports and a standalone handoff only when evidence exists. Final storage adoption, T16/T17/G2, larger-scale capacity, physical16GB validation and product retention/derived-storage decisions remain open. Scope and Stage1 formats do not change.

**Decision requested:** approve T12-D1–D6, including the additional96-start allocation, only-match permission change, explicit remaining14-worker schedule, prepaid bounded preparation blocks, exact cached DLL/notices staging and fresh manual disconnected execution without filesystem confinement. Separately approve committing these five planning documents. One package approval covers necessary covered edits/tests/staging/handoff, not subsequent source/results commits, extra permissions or adoption.
