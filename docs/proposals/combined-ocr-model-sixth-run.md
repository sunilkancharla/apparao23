# Proposed combined-06 offline evaluation

**Status: approved for bounded preparation and disconnected user-run execution.** Prepared 2026-11-14 (Asia/Calcutta), after state-coordination commit `92f3b67`. The user explicitly approved this package and committing its five proposal documents. Later preparation source/results commits and runtime adoption retain their separate gates.

## Purpose and fixed experiment

Run the original [combined CPU-only matrix](combined-ocr-model-trial.md) once with the committed [monitor repair](../benchmarks/combined-monitor-cadence-repair.md) and [state coordination repair](../benchmarks/combined-state-coordination-repair.md). The latter passed60combined/OCR synthetic tests; native behavior remains unvalidated. Owned writers/combined OCR meter reads now share a short lock, and unchanged descendant observations skip writes. Actual access denials still stop immediately. The historical combined-05 locking handle and combined-03 lost reading remain unresolved.

Reuse the exact cached [combined-05 package](combined-ocr-model-fifth-run.md#purpose-and-fixed-scope): existing project environment/interpreter, Ollama0.40.16, pinned Nomic and two Qwen candidates, both evaluated English OCR engines and manual-04 wheel/language assets, synthetic M02/M03/M04 and frozen T10/T11A corpus/cases/evidence/gold. Rehash against verified receipts; stop on missing/mismatched bytes. No installs, downloads, rendering, new documents/fixtures, orientation correction, replacement models, tuning, cloud grader, global/PATH or product-scope change.

| Role | Candidate | Manifest SHA-256 |
|---|---|---|
| Embeddings | nomic-embed-text:v1.5 | `0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f` |
| Chat A | qwen2.5:1.5b-instruct-q4_K_M | `65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b` |
| Chat B | qwen3:1.7b-q4_K_M | `8f68893c685c3ddff2aa3fffce2aa60a30bb2da65ca488b61fff134a4d1730e7` |

Retain CPU-only/four model threads/context2048/batch64/output192tokens, temperature0.2/top_p0.9/top_k20/repeat_penalty1/seed42; Qwen3 think=false. Nomic remains768dimensions/truncate=false with existing prefix contract. Keep exact OCR settings, one OCR worker and one inference request, at most Nomic plus one chat model resident, keep_alive600seconds and explicit unload on model switch. No controlled cold-cache or calibrated confidence claim.

Schedule remains four OCR deadline/memory controls, eight four-passage corpus embeddings and36chat attempts with36query embeddings. For each chat model, use C01/C03/C08 twice in each baseline/Tesserocr/RapidOCR condition. The24overlapping OCR workers cycle M02/M03/M04. Measure actual intersection; missing overlap stops without retry. OCR remains a separate pressure workload, not chat evidence or proof of a document-to-answer application. Failed/incomplete attempts stay recorded.

## Proposed shared allocation and unchanged limits

| Boundary | Limit |
|---|---|
| Total process starts/attempts | 160 shared across inspection/initialization, regressions/negative controls, tools/Git, server/controller, OCR, native descendants, reporting and cleanup |
| Category ceilings | Preparation48; controller16; OCR28; supervisor/extra descendants36; report16; protected cleanup16 |
| API attempts | 128 loopback requests total, including failures, polling, readiness/residency and unload |
| Active preparation/execution | 30minutes connected preparation; one75-minute disconnected execution epoch including controls/startup/switching/cleanup; human/host approval waits excluded |
| Operation deadlines | Chat90s; embedding/ordinary HTTP60s; OCR30s; deadline sentinel1s |
| Memory | Aggregate job8GiB; OCR worker1.5GiB; monitored controller512MiB; free physicalRAM at least4GiB |
| Monitor | Desired100ms start cadence subtracting work; hard250ms for start/reading gaps, collection/TCP/storage durations and full iteration |
| Added disk | Total512MiB including rawOCR32MiB and answers8MiB |
| Install/download | Zero |

Timing equality remains accepted; invalid or excessive intervals stop. Software checks cannot guarantee interrupting a stalled system call at precisely250ms. Kernel memory caps remain independently enforced. No retries, scheduling privileges, new watchdog, timing/permission change or relaxed storage/ownership boundary.

Before approved preparation commands, create the shared ledger or explicitly preallocate its initial inspection/initialization commands. Reserve failed and successful launches, tools, full combined/OCR fake regressions and negative controls in the same fresh allocation; reconcile native descendants without double-counting roots. No category borrowing, exhausted epoch reset, cleanup-reserve use for normal work or automatic extension. Report actual reservations and elapsed time before handoff.

Link **15 prior records**: the twelve already linked by combined-05, plus its stopped meter (last persisted52/160,eightAPI), the state-write investigation budget (29/32starts,466.578s) and the state-coordination repair budget (32/40starts,604.971s). Preserve initial/final hashes and counters; failed combined-05 persistence prevents treating its last saved counts as complete attempted-transition accounting. Do not repair, reset, mutate, reseal or rerun any old allocation. New `data/t11/combined-06/` is proposed only.

## Ordered tasks and evidence

All tasks are tracked in root [TODO](../../TODO.md). Package approval is recorded; tasks proceed in dependency order.

| ID | Prerequisite and task | Acceptance/evidence |
|---|---|---|
| T11-C6-1 | After approval, establish fresh shared ledger and baseline | Counted initialization; fifteen prior hashes/counters and committed repair state verified; cached inventory only; stop on drift/budget failure |
| T11-C6-2 | After C6-1, update explicit routing/seal inventory test-first | Only06 accepted; old01–05/no-ID/traversal/worker commands refused. Red then green full combined/OCR fake suites/Ruff; seal includes the standalone OCR contract test alongside already sealed source/tests. No repair-policy changes |
| T11-C6-3 | After C6-2, perform cached static preparation and independent readiness checks | Rehash exact source/runtime/models/assets/fixtures/evidence/interpreter and15prior records; parse PowerShell, check links/diff/time/counters. No connected native OCR/model imports/inference/render/download. Report actual readiness before issuing a runnable handoff |
| T11-C6-4 | After C6-3, user disconnects every external link and attests OFFLINE | User launches the sealed standalone runner, noREADYprompt. Owned loopback service, CPU/residency, four controls and fixed matrix share all ceilings; retain timing/state diagnostic packets and every attempt |
| T11-C6-5 | After execution starts, stop/complete and verify owned teardown | Zero active owned children, process reaped/listener released before explicit safe reconnect. Preserve temporary/failed state; no retry/reset/reseal; uncertain cleanup means remain offline |
| T11-C6-6 | After verified teardown and user reconnection, review sanitized results | Actual persisted/attempt counters, timing/overlap/latency/memory and missing coverage reported. Local semantic review if answers exist; valid identifiers alone do not prove support. Update factual docs and request source/results commit approval |

Source scope is the existing `combined_trial.py` and `test_combined_trial.py` for routing, old-command guards and adding `test_ocr_trial.py` to the static seal inventory. No changes to the committed coordination/cadence/OCR hook policies are included. Use an ignored standard-library resource-bounded bootstrap to run both fake suites inside the shared allocation. Update existing handoff/proposal, README/PLAN/TODO/checkpoint and factual reports as needed. Runtime assets, generated documents/receipts and private content remain ignored and uncommitted.

## Offline boundary and risks

Retain **manual physical disconnection without filesystem confinement**: native components have the user's Windows account access. Disconnect Wi-Fi/Ethernet/tethering/every external link before OFFLINE and remain disconnected through verified teardown and safe-to-reconnect message. Codex will not start the native trial while connected. Use only the owned127.0.0.1:11434service; refuse unrelated listeners and never terminate by port alone.

Before starting, close editor/viewer tabs or live watchers on the new trial's state files and preserve instructions locally. This reduces possible external open handles; it is not proof the IDE caused the historical error and not a guarantee against external locking. Do not alter protections, permissions or run elevated. Raw OCR/images/documents/prompts/evidence/vectors/answers/model logs/private-path receipts stay local; inspect only sanitized scalar reports/hashes/counters in the assistant session.

Stop on reconnect/egress/download, identity drift, GPU use, residency/overlap failure, unknown ownership/accounting, resource/timing/deadline/storage/access failure, exhaustion or uncertain cleanup. The repair cannot prevent every external-reader denial or guarantee scheduling under load. No further limit adjustment/retry is approved. Actual physical16GB performance remains unproven if detected hardware differs; the Windows11/16GB/no-dedicated-GPU target is unchanged.

## Approval requested

Approve or amend this exact fresh160-start/128-API package with unchanged artifacts/experiment/limits, bounded routing/seal preparation and disconnected user-run execution. Package approval also covers sanitized result documentation, not an additional repair, further native trial, product implementation, runtime adoption or stage transition. The five proposal documents may be explicitly approved for commit in the same reply; later preparation source/results commits retain their separate gate. No runnable command will be issued before readiness checks succeed.
