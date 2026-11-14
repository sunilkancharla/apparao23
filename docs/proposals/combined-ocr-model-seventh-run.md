# Proposed combined-07 offline evaluation

**Status: approved for the exact bounded package and five proposal documents' commit.** On 2026-11-14 the user answered "yes please" to the explicit package/commit request. Prepared after `c47dfda`, which committed the approved 300-ms monitoring change and 61 passing combined/OCR fake contracts. No native execution has started. All older native runs remain closed.

## Purpose and fixed experiment

Run the original [combined CPU-only matrix](combined-ocr-model-trial.md) once with the committed [300-ms policy](../benchmarks/combined-monitor-300ms.md), [work-aware monitor](../benchmarks/combined-monitor-cadence-repair.md) and [owned state coordination](../benchmarks/combined-state-coordination-repair.md). Combined-06 completed 15 answers and nine OCR/chat overlaps before its 287.7155-ms reading gap exceeded its then-approved 250-ms limit. That observed gap fits the new ceiling; completion at 300 ms remains unproven. Neither a timing cause nor the historical external state-file locking process is established.

Reuse the exact cached artifacts/settings of [combined-06](combined-ocr-model-sixth-run.md#purpose-and-fixed-experiment), including its existing interpreter/environment, Ollama 0.40.16, both evaluated English OCR engines/assets, synthetic M02/M03/M04 and frozen T10/T11A corpus/cases/evidence/gold. Hash verification must stop on missing or drifted bytes. No installations, downloads, rendering, new fixtures/documents, orientation correction, tuning, replacement models, cloud grading, global/PATH changes or product adoption.

| Role | Candidate | Manifest SHA-256 |
|---|---|---|
| Embeddings | nomic-embed-text:v1.5 | `0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f` |
| Chat A | qwen2.5:1.5b-instruct-q4_K_M | `65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b` |
| Chat B | qwen3:1.7b-q4_K_M | `8f68893c685c3ddff2aa3fffce2aa60a30bb2da65ca488b61fff134a4d1730e7` |

Retain CPU-only execution, four model threads, context 2048, batch 64, output 192 tokens, temperature 0.2/top_p 0.9/top_k 20/repeat_penalty 1/seed 42; Qwen3 think=false. Nomic retains 768 dimensions, truncate=false and existing prefixes. Keep one OCR worker/one inference request, at most Nomic plus one chat model resident, keep_alive 600 seconds and explicit unload on switching. Preserve exact evaluated OCR settings and local assets. These are exploratory measurements with uncontrolled cache/order, not controlled cold/warm comparisons.

The fixed schedule remains four OCR deadline/memory controls, eight four-passage corpus embeddings and 36 chat attempts with 36 query embeddings. Each chat model uses C01/C03/C08 twice in each baseline/Tesserocr/RapidOCR condition; 24 overlapping OCR workers cycle M02/M03/M04. Measure actual overlap and stop if missing. OCR pressure is separate from chat evidence; it does not demonstrate an end-user scanned-document answer flow. Failed/incomplete/unattempted cases must remain distinct.

## Proposed shared allocation

| Boundary | Limit |
|---|---|
| Process starts/attempts | 160 shared across preparation, inspection/initialization, Git/tools, fake/negative controls, controller/server, OCR, native descendants, reports and cleanup |
| Category ceilings | Preparation 48; controller 16; OCR 28; supervisor/extra descendants 36; report 16; protected cleanup 16 |
| API attempts | 128 loopback attempts, including failures/readiness/residency/polling/unload |
| Active time | 30 minutes connected preparation; one 75-minute disconnected epoch including startup/controls/switching/cleanup; human/host approval waits excluded |
| Operation deadlines | Chat 90 s; embeddings/ordinary HTTP 60 s; OCR 30 s; deadline sentinel 1 s |
| Memory | Aggregate job 8 GiB; OCR worker 1.5 GiB; monitored controller 512 MiB; available physical RAM at least 4 GiB |
| Monitoring | Desired 100-ms cadence subtracting work; hard 300 ms for start/reading gaps, collection/TCP/storage/full iteration and resource sampling gap |
| Added disk | Total 512 MiB, including raw OCR 32 MiB and answers 8 MiB |
| Install/download | Zero |

Timing equality is accepted, excessive/invalid intervals stop, and no further timing extension is allowed. The 300-ms ceiling permits 50 ms more observation delay than older trials; it cannot guarantee a blocked call is interrupted at that instant. Kernel memory caps stay independent. No retries, grace windows, smoothing, new monitor thread, scheduling privileges or permission changes.

Before the first approved preparation command, explicitly reserve its initial inspection/initialization starts or initialize the fresh shared ledger. Count all successful/failed launches, full combined/OCR regressions and negative controls. Reconcile native descendants without double-counting roots. No borrowing categories, reset/extension of exhausted budgets or normal use of protected cleanup starts. Report actual elapsed time/counters before handoff.

Link **18 prior records**: the 15 records already linked by combined-06, plus its closed meter and seal, and closed `data/t11/monitor-300ms-01/budget.json`. Preserve initial/final hashes and counters. Combined-06 remains at 64/160 reservations and 62 API attempts; the policy package closed at 32/32 reservations and 267.056 active seconds. Combined-05's last persisted counters still have their documented completeness caveat. Do not modify any old meter/seal/temp receipt, including to repair its source mismatch. Create only a fresh `data/t11/combined-07/` after approval.

## Ordered tasks and acceptance

| ID | Prerequisite and objective | Acceptance and evidence |
|---|---|---|
| T11-C7-1 | Exact package approval; establish fresh ledger/baseline | Initial commands reserved; 18 prior records and committed 300-ms policy verified; existing cached identities/settings reviewed. Stop on drift or budget failure |
| T11-C7-2 | C7-1; change routing test-first | Only combined-07 accepted. Refuse old 01–06, absent/invalid/traversal IDs and old worker requests; red then green full combined/OCR fake suites, focused Ruff/format. Preserve policy, sealed-source inventory and all other behavior |
| T11-C7-3 | C7-2; prepare cached artifacts and independently verify readiness | Rehash source/runtime/models/assets/fixtures/evidence/interpreter and 18 prior records; include standalone OCR tests in seal, parse PowerShell, check links/diff/budget. No connected native backend imports/inference/render/download. Publish actual readiness before runnable handoff |
| T11-C7-4 | C7-3; user operates the disconnected sealed runner once | User disconnects every external link and attests OFFLINE; owned loopback server, four controls and frozen matrix obey all shared limits. Record attempts/timing/overlap; stop without retry on failure |
| T11-C7-5 | Execution starts; verify teardown on completion or stop | Zero active owned children, process reaped and owned listener released before explicit safe reconnect. Preserve failure/temp receipts; uncertain cleanup means remain disconnected |
| T11-C7-6 | Verified teardown/reconnection; report and review | Inspect sanitized counters/metrics only, preserve missing coverage; request local semantic answer/citation review, update factual docs, request separate preparation/results commit approval |

Source scope: `tests/evals/spikes/combined_trial.py` and `test_combined_trial.py`, limited to new default/run-ID/CLI routing and associated refusal tests. Do not change `combined_native.py`, OCR sources, 300-ms constant/guard semantics, fixtures, models or dependencies. Use the existing reviewed standard-library resource-bounded fake bootstrap within the shared allocation. Documentation scope includes PLAN/TODO/README/checkpoint, this proposal, readiness/results reports and updating the existing handoff only after successful preparation. No runtime/generated/private assets enter Git.

## Offline boundary and stop conditions

This package retains **manual physical disconnection without filesystem confinement**: native components have the user's Windows account file access. Use only the existing synthetic/frozen evidence. Disconnect Wi-Fi, Ethernet, tethering and every external link before OFFLINE; remain disconnected through `TEARDOWN VERIFIED: True` and the explicit safe-to-reconnect message. Codex will not execute native inference while connected. No new READY prompt is needed for unchanged fixtures; no runnable command is provided at the proposal stage.

Before a future start, save instructions locally, close heavy applications and editor/viewer/watchers on the new state files. This reduces possible external handles; it neither identifies the historical cause nor guarantees success. Use ordinary PowerShell without elevation/protection changes. Use only the owned 127.0.0.1:11434 listener; refuse unrelated listeners and never terminate by port alone.

Stop on reconnect/egress/download, identity drift, GPU use, residency/overlap failure, unknown ownership/accounting, resource/timing/deadline/storage/access failure, exhaustion or uncertain teardown. Never retry/reset/reseal the stopped run or silently increase a limit. Raw documents/images/OCR/prompts/evidence/vectors/answers/logs/private error-path receipts remain local; assistant review uses sanitized scalars/hashes/counters only.

## Remaining decisions and approval

Combined-06 S01–S15 semantic review remains pending independently; this proposal neither records acceptance nor scores missing answers. Future completed answers also require local factual/citation review. Windows 11/16 GB/no dedicated GPU remains the target despite detected hardware differences; performance on a physical 16-GB machine, broader OCR quality/rotation, runtime selections/adoption and Stage 1 acceptance remain open.

Approve or amend this exact fresh 160-start/128-API package, including bounded routing/preparation, the 300-ms policy, manual disconnected execution without filesystem confinement and sanitized closeout. The five proposal documents may be separately approved for commit together with the package. Later preparation/results commits, additional repairs, further native runs, runtime adoption and stage transitions retain explicit gates. No scope or limit other than the already approved monitoring ceiling changes.
