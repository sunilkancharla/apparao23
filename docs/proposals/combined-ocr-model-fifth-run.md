# Proposed combined-05 offline evaluation

**Status: approved for bounded preparation and disconnected user-run execution.** Prepared 2026-11-14 (Asia/Calcutta), after monitoring-repair commit `0b345d5`. The user explicitly approved this package and committing its five proposal documents. Later preparation source/results commits retain their separate gate; no model/OCR adoption is approved.

## Purpose and fixed scope

Run the original bounded CPU-only [combined experiment](combined-ocr-model-trial.md) once with the committed [monitor cadence repair](../benchmarks/combined-monitor-cadence-repair.md). Combined-04 stopped because its recorded loop-start interval was 259.0546 ms against a 250-ms ceiling. The repaired loop accounts for check work before waiting and additionally checks actual collection/reading/scan intervals. Its 34 fake tests passed, but native timing under inference load remains unverified. The new run may still stop; this proposal does not promise completion or relax any timing/resource limit.

Reuse the exact cached artifacts and settings in the [combined-04 frozen package](combined-ocr-model-fourth-run.md#frozen-scope): project-local Python/environment, Ollama 0.40.16, pinned Nomic and two Qwen chat models, both English OCR engines and their manual-04 wheel/language inventory, synthetic M02/M03/M04 and the frozen T10/T11A corpus/questions/evidence/gold. Rehash against prior verified receipts; stop on missing/drifted bytes. No downloads, installs, new samples, rendering, orientation repair, tuning, replacement models, global/PATH changes or product ingestion.

| Role | Candidate | Manifest SHA-256 |
|---|---|---|
| Embeddings | nomic-embed-text:v1.5 | `0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f` |
| Chat A | qwen2.5:1.5b-instruct-q4_K_M | `65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b` |
| Chat B | qwen3:1.7b-q4_K_M | `8f68893c685c3ddff2aa3fffce2aa60a30bb2da65ca488b61fff134a4d1730e7` |

Retain CPU-only inference with four model threads, context2048, batch64, output192 tokens, temperature0.2/top_p0.9/top_k20/repeat_penalty1/seed42 and Qwen3 think=false. Nomic remains768 dimensions/truncate=false with existing prefix contract. Retain exact OCR settings, one OCR worker and one inference request, at most Nomic plus one chat model resident, keep_alive600 seconds and explicit unload on chat-model switch. No latency or quality threshold is invented.

Schedule: four OCR deadline/memory controls; eight four-passage corpus embedding calls; then36 scored chat attempts with36 query embeddings (C01/C03/C08 twice for each baseline/Tesserocr/RapidOCR condition per chat model). The24 overlapping OCR workers cycle M02/M03/M04. Preserve failed attempts and actual overlap timestamps. OCR is a separate pressure workload, not answer evidence. Missing actual overlap stops without retry. No controlled cold-cache claim.

## Proposed shared allocation and unchanged stop limits

| Boundary | Limit |
|---|---|
| All process starts/attempts | 160 shared across initialization/inspection, tests/negative controls, tools/Git, server/controller, OCR, native descendants, reporting and cleanup |
| Category ceilings | Preparation48; controller16; OCR28; supervisor/extra descendants36; report16; protected cleanup16 |
| Loopback API attempts | 128, including failed calls, polling, readiness/residency and unload |
| Active connected preparation | 30 minutes; human/host approval waits excluded |
| Active disconnected execution | One75-minute epoch, including startup/controls/model switching/cleanup; never reset |
| Operation deadlines | Chat90s; embedding/ordinary HTTP60s; OCR30s; deadline sentinel1s |
| Memory | Aggregate job8GiB; OCR worker1.5GiB; monitored controller512MiB; physical freeRAM at least4GiB |
| Monitor timing | Desired100ms start cadence after subtracting work; hard250ms for loop-start gap, completed-reading gap, collection/TCP/storage durations and full iteration |
| Added disk | Total512MiB, including raw OCR32MiB and answers8MiB |
| Downloads/installations | Zero |

Timing boundaries preserve exact-equality acceptance and refuse invalid intervals. Software checks cannot interrupt an unresponsive system call at precisely250ms; report this limitation alongside independently enforced kernel memory caps. No new watchdog, monitor thread, scheduling privilege or relaxed boundary is included.

Before any approved preparation command, create the new shared ledger or make an explicit initial reservation covering its inspection/initialization commands. Charge all actual/failed attempts, conservatively reserve tool launches and reconcile native descendants without double counting roots. No category borrowing, cleanup-reserve consumption by normal work, silent extension or automatic retry. Report actual reservations and elapsed time at readiness, not historical values.

Hash-link the ten prior records already linked by combined-04, plus its stopped meter (**60/160, seven API attempts**) and the completed `monitor-cadence-repair-01/budget.json` (**24/32 starts,335.938active seconds**): twelve prior records in total. Verify their initial and final hashes/counters unchanged. Preserve every earlier source epoch, seal and stopped/consumed allocation. Do not modify/reset/reseal old records or run their commands. A new `data/t11/combined-05/` allocation is proposed, not currently created.

## Ordered tasks and evidence

Tasks are tracked in root [TODO](../../TODO.md); package approval is recorded and tasks proceed in dependency order.

| ID | Objective and prerequisite | Acceptance/verification |
|---|---|---|
| T11-C5-1 | After approval, establish fresh shared allocation | Prior twelve records/hash/counter snapshot and current committed baseline verified; counted initialization and cached inventory; stop on drift or exhausted resources |
| T11-C5-2 | After C5-1, update explicit run routing using test-first development | Failing then passing selection/CLI/lazy-worker tests; only combined-05 accepted; old01–04/no-ID/traversal calls refused. Full combined fake suite/Ruff preserve timing, memory, ownership, privacy and cleanup contracts |
| T11-C5-3 | After C5-2, prepare and independently verify static seal | Exact cached source/model/OCR/fixture/evidence/interpreter hashes, prior-record immutability, PowerShell syntax, document links and diff verified inside preparation allocation. No connected native OCR/model imports or inference; report actual counters before handoff |
| T11-C5-4 | After C5-3, user disconnects and attests OFFLINE | Only the user starts the sealed standalone runner; no READY prompt. Owned loopback service, CPU/residency, four controls and unchanged matrix share all caps. Save timing/resource diagnostics and all failed attempts |
| T11-C5-5 | After execution starts, complete or stop and verify cleanup | Durable sanitized failure packet where possible; zero active owned children, owned process reaped and port released before explicit safe reconnect. Otherwise remain disconnected; never terminate unrelated services |
| T11-C5-6 | After verified teardown/reconnection, review sanitized result | Report counters/timings/overlap/latency/memory and missing coverage. If answers exist, prepare local semantic review; identifiers alone do not establish support. Update factual docs and request separate reviewed source/results commit approval |

Source scope is the existing three combined evaluation scripts, only as necessary for run routing and its tests. The committed cadence repair is retained without further policy changes. Update existing handoff/proposal, README/PLAN/TODO/checkpoint and authored benchmark reports as needed. Runtime assets, generated receipts, prompts/evidence/answers/OCR/vectors and review pages remain ignored and uncommitted.

## Execution boundary, risks and approval

Retain the explicitly disclosed synthetic-only **manual disconnection without filesystem confinement**: native code has the user's Windows account access. Disconnect Wi-Fi, Ethernet, tethering and every external link before OFFLINE; remain disconnected through verified teardown and the safe-to-reconnect message. Codex will not start the native trial while connected. Bind the owned service only to127.0.0.1:11434; refuse unrelated listeners and never kill by port alone. No cloud fallback or remote grader. Only sanitized scalar status/counters/hashes/metrics may be reviewed in the assistant session; raw inputs/outputs and private exact-path receipts stay local.

Stop on reconnect/egress/download, identity drift, GPU activity, residency/overlap failure, ownership/accounting uncertainty, memory/timing/deadline/storage boundary, exhausted allowance or uncertain cleanup. No retry or limit adjustment. The new timing checks are stricter than historical loop-start-only measurements and may expose other slow phases. A completed run still does not establish strict performance on a physical16-GB host if this computer differs, semantic correctness, broader OCR acceptance, runtime adoption or Stage1 completion.

The user approved this exact package and the five proposal documents' commit (`79a2dea`). This covers the fresh160-start/128-API allocation, fixed experiment/artifacts, unchanged safety limits, necessary bounded selector/test/static preparation, disconnected user-run execution and sanitized results documentation. Later preparation source/results commits, timing-policy changes, further native trials, product implementation and Stage2 transition remain separate gates.

## Completed static preparation

[Preparation evidence](../benchmarks/combined-ocr-model-fifth-preparation.md) records34passing fake tests in1.774s, Ruff and final independent rehash of151sealed identities/12unchanged prior records. PowerShell syntax passed. Readiness199.696elapsed seconds,36/160reservations (28preparation/eightreport),zeroAPI/native attempts,offline epoch unset. The [new handoff](combined-ocr-model-handoff.md) is ready for the already approved disconnected user-run step. New preparation source/documentation commit approval remains pending.
