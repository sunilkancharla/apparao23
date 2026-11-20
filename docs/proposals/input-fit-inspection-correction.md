# T17-IF-R — bounded metadata inspection correction

## Status and objective

Proposed, awaiting approval. The [partial IF-S findings](../benchmarks/input-fit-static-review.md) are committed as `f1b62d4`. Its allocation is closed and remains unchanged. The exact cause of its stalled PowerShell is unproven; this proposal addresses the observed missing completion/session handling and bounds the path inspection without claiming a diagnosed root cause.

Deliver a small, test-first standard-library inspection aid and its tests, then permit **one** fresh read of the two pinned public model manifests and their seven declared non-weight layers if all controls pass. Save verified metadata or an honest partial stop. Do not load models, choose a tokenizer, access a runner endpoint or implement application functionality.

## Allowed source and artifacts

At most two new authored files: `tests/evals/spikes/input_fit_metadata.py` and `tests/evals/spikes/test_input_fit_metadata.py`. Keep the controller, bounded reader and its command dispatch in the single cohesive aid; avoid new launcher frameworks or changes to historical helpers. Use the already available base `F:/Python/Python314/python.exe` with `-I -S -B`; project Ruff may check the two files. No packages/imports from the evaluated application/native dependencies or global environment changes.

The only real inspection root is the existing project-owned `data/ollama/models`. Copy exact manifest/layer identities from the committed IF-S report, not a mutable model tag. The worker may read the two manifests and the nine-file total inventory comprising those manifests plus Qwen config/system/template/license and Nomic config/parameters/license. Their declared combined metadata size is26,739bytes. No model weights, GGUF parsing, tokenizer instantiation, other models or saved user content may be read. Existing license files are read as data only; this does not certify bundled native notices.

## Required correction and acceptance

1. **Finite checked paths:** derive a bounded ancestor list, with no repeated parent mutation/while-until-root loop. Reject non-progress, excessive depth, traversal/outside-root, unexpected type or reparse/link ancestors. Check before opening and compare file identity/stat before and after reading. Fixed expected digests and size are mandatory. These checks do not establish race-free filesystem confinement; refuse any observed instability.
2. **Bounded input and progress:** read at most64KiB+1 per file, reject >64KiB, and enforce1MiB aggregate metadata reads including failed attempts. Count actual read bytes conservatively even on error. Persist a content-free per-file started/completed/refused status, hash/length and sanitized error type before moving to another file. Keep extracted public config/template findings local and separate from progress. No model/prompt text in ordinary logs.
3. **Owned process and complete results:** retain every execution result field, including exit/session identifiers when tools yield. Use an explicit argument vector and `shell=False` for one owned base-Python metadata child; it must contain no spawn/network/service code. Retain its process handle. After successful creation, use a30-second communication deadline; on timeout kill that exact child and verify reap within5seconds. Process-creation delay itself is not claimed covered by that communication timer. Bound captured output to64KiB by limiting worker output to a small checked result; persist detailed findings to the owned run directory instead. Keep controller launch/result/cleanup state durable; never infer exit from empty output.
4. **No automatic retry:** controls and lint must pass before the single real metadata attempt. A guard failure, timeout, unknown child state, output/persistence error or exhausted shared budget stops the package. Do not rerun an old command, weaken a limit, attach by process name/port, scan all host processes or fetch missing assets. If cleanup cannot be verified, report that uncertainty and stop dependent work.

This is a connected public-metadata/standard-library investigation, with no filesystem or outbound confinement claim. There is no new kernel RAM cap: fixed read/output ceilings limit intended buffers but do not measure/enforce whole-process RAM. No candidate native code runs. This narrow boundary requires approval; prior model trials do not authorize a general connected native execution policy.

## Test-first and review requirements

Use mocked paths/stat/open/process/clock boundaries and small temporary synthetic metadata, maximum32files/128KiB generated control data inside the fresh ignored run root. Cover drive roots, trailing separators, case handling, excessive ancestry and non-progress; traversal/reparse/outside-root; changed identity, wrong digest/size, oversized and cumulative reads; per-file receipt write failure; malformed/empty child output, nonzero exit, timeout, kill/reap failure and exactly-one-attempt admission. Prove invalid inputs do not reach the real reader and failed/unknown cleanup does not produce success. No real timeout child or negative-control subprocess is authorized: mock those boundaries.

Initial regression must fail meaningfully before implementation. Run focused fake tests and Ruff, then mutate one admission/timeout or path-refusal condition in a temporary/in-memory copy and verify its test fails; restore without changing sealed live bytes. Report the exact commands/results rather than inventing a passing suite. No tests of actual model token counts are included.

## Ordered package

| ID | Objective / prerequisite | Acceptance and verification | Status |
|---|---|---|---|
| IF-R1 |After approval, freeze previous hashes and fresh shared accounting; review the two aid designs |Prior IF-S/R1-W ledgers and selected source/spec/lock identities preserved; manifest/clock persisted before optional work |Pending approval |
| IF-R2 |After R1, implement the finite reader/controller test first |Expected red, passing focused fake tests/Ruff and caught targeted mutation; no real metadata child yet |Pending R1 |
| IF-R3 |After R2, seal aid/interpreter/expected identities and execute one real metadata attempt |Per-file hash/size/progress evidence or partial stop; full result retained; owned child exit/reap verified |Pending R2 |
| IF-R4 |After R3 or bounded stop, review metadata/adapter implications and close |Dated findings, links/diff/preservation/elapsed/output accounting, incomplete input-fit claims retained and separate commit request |Pending R3 |

## Shared limits

- Fresh ignored root **`data/t17/input-fit-inspection-01/`**, created only after approval. Preserve the old run/meter; no reset or retry.
- **80 prepaid conservative local execution units:64normal/16protected** across orchestration, tools, shells, test/lint/mutation interpreters, controller, its one direct child, reviews and cleanup. Manifest: initialization8, test authoring4, red6, implementation4, green/lint8, correction/mutation8, one real attempt8, report4, review8, close6, protected16. No phase refund; stop if a required block cannot cover its remaining steps. Git closeouts are separately authorized actions outside this fresh investigation epoch.
- **1,200 active seconds**, including tool waits, tests, authoring and reporting; **2MiB total new authored files, receipts/findings and control fixtures**. Clock and full reservation manifest persisted before optional preparation. Persist conservative charged time across interruptions; human approval waits before starting excluded.
- At most **one actual metadata child**, one at a time; base Python only, no venv redirector, no descendant spawning. The launch/tool/controller/child all consume the same reserved block. No actual extra discovery/timeout child. Per-child timing as above; watchdog/process ownership integration is not a candidate/model adoption.
- Per-file64KiB, total1MiB metadata,64KiB child output,32synthetic files/128KiB control data. No new web calls/downloads/installs/native library/model/parser/OCR/extension/service/API/inference or weight reads. No larger contexts, replacement models, runtime changes or optional tools.
- Exhaustion or a missing prerequisite uses protected capacity only for termination, preservation and partial reporting/closure. Do not continue research/implementation with protected slots. There is no permission for a second real attempt, fallback runtime or later inference trial.

## Deliverables and decisions

After approval, author the two aids and `docs/benchmarks/input-fit-inspection-results.md`; update affected dependency/design cross-references only where actual evidence warrants them, plus PLAN/TODO/README/checkpoint. Expected metadata findings should distinguish verified bytes, declared values, source inference and unverified runtime behavior. Config/template reads alone cannot prove special-token parity, exact pre-generation counting, context/output reservation or representative CPU-only acceptance. Native trust, notices/advisory gaps and G2 remain open.

Request approval of this exact IF-R package and separately of the five proposal/status documents' commit. One package approval covers all authorized corrections/tests/read/review steps without repeated per-step permission. Later source/results commits, adapter selection, new dependencies/internal-runner access, native validation and application implementation retain separate gates.
