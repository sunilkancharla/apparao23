# Proposed combined-04 offline evaluation

**Status: approved for bounded preparation and the disconnected user-run trial.** Prepared 2026-11-14 (Asia/Calcutta), after commit `28844cb`. The user explicitly approved "Agents.md and commit and the next plan", approving this exact package and the five proposal documents' commit. Runtime adoption and later source/results commits retain separate gates. Preparation evidence and actual counters will be recorded before handoff.

## Purpose and evidence

Repeat the unchanged [combined experiment](combined-ocr-model-trial.md) once under a fresh allocation, using the [repaired resource diagnostics](../benchmarks/combined-resource-diagnostic.md). Combined-03 passed four safety controls but stopped during corpus embedding; its failing reading was lost. Its [exact historical trigger remains unknown](../benchmarks/combined-ocr-model-third-stop.md). The repair passed 28 fake tests; this does not prove combined native feasibility.

The next run either produces the planned measurements or preserves a specific resource-guard failure with its scalar readings and limits. The 0.25-second sampling-gap stop remains binding. It may stop the new run again; no automatic retry, polling-policy adjustment or threshold relaxation is authorized. If the run stops elsewhere, report that boundary without claiming a resource diagnosis.

## Frozen scope

Use only existing project-local Ollama 0.40.16, the pinned models below, the existing exact OCR evaluation inventory/English assets from manual-04, synthetic M02/M03/M04 images and frozen T10/T11A case/evidence/gold packets. Rehash all bytes against existing receipts. Missing or drifted assets stop preparation; there is no installation, download, new fixture rendering, model substitution, orientation correction or new document processing. Existing interpreter and package identities must match the earlier sealed inventory; do not change global installations or PATH.

| Role | Candidate | Manifest SHA-256 |
|---|---|---|
| Embeddings | nomic-embed-text:v1.5 | `0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f` |
| Chat A | qwen2.5:1.5b-instruct-q4_K_M | `65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b` |
| Chat B | qwen3:1.7b-q4_K_M | `8f68893c685c3ddff2aa3fffce2aa60a30bb2da65ca488b61fff134a4d1730e7` |

Retain all [original settings](combined-ocr-model-trial.md#frozen-artifacts-and-settings): CPU only, four model threads, context 2048, batch 64, 192 output tokens, temperature 0.2, top_p 0.9, top_k 20, repeat_penalty 1, seed 42; Qwen3 think=false. Nomic retains 768 dimensions, truncate=false and the verified prefix contract. OCR retains its exact cached configuration and one-thread settings where configured. Keep one inference request and at most one OCR worker active, with at most Nomic plus one chat model resident. Keep-alive remains 600 seconds, with explicit unload on model switch.

The schedule remains four OCR deadline/memory controls, eight corpus embedding calls, and 36 chat attempts with 36 query embedding calls: per chat model, C01/C03/C08 twice in each baseline/Tesserocr/RapidOCR condition. The 24 overlapping OCR workers cycle M02/M03/M04. Measure actual chat/OCR intersection; no overlap means incomplete and stop, not retry. OCR output remains a separate pressure workload, not chat input or proof of a working document-to-answer application.

## Proposed shared allocation

| Boundary | Unchanged limit |
|---|---|
| All process starts/attempts | 160, including preparation shells/tools, fake tests, negative controls, controller, native descendants, reporting and cleanup |
| Categories | Preparation 48; controller/server 16; OCR/sentinels 28; supervisor/extra descendants 36; reporting/Git 16; protected cleanup 16 |
| Loopback API attempts | 128 total, including errors, polling, controls/readiness and unload calls |
| Active connected preparation | 30 minutes; human approval waits excluded |
| Active offline execution | One 75-minute epoch including startup, controls, measurements and cleanup; no reset |
| Per-operation deadlines | Chat 90 s; embedding/ordinary HTTP 60 s; ordinary OCR 30 s; deadline sentinel 1 s |
| Aggregate job memory | 8 GiB, with owned-private/peak-job sampled checks retained |
| OCR worker/controller | 1.5 GiB OCR worker cap; 512 MiB monitored controller private-memory stop |
| Physical headroom/sampling | At least 4 GiB free physical RAM; sampling gap at most 0.25 s |
| Added disk | 512 MiB total, including raw OCR at most 32 MiB and answers at most 8 MiB |
| Downloads/installations | Zero |

Before any post-approval preparation commands, establish the fresh shared ledger or an explicit preallocated reservation covering its creation and inspection commands. Reserve before launches; charge failed attempts and extra descendants without double counting roots. Preparation, all regressions and negative controls share this allocation. Preserve cleanup reserves; no category borrowing or extension. Report actual preparation consumption before the user-run handoff rather than copying historical reservations. Keep all earlier native and fake epochs closed.

Hash-link the prior combined-01, combined-02 and combined-03 ledgers (75/160 and five API calls; 51/160 and five; 56/160 and eight respectively), both storage diagnostic/repair allocations (20/24 and 22/24), resource diagnostic allocation and its completion receipt (24/24), and the prior OCR, embedding and chat records. Record exact paths, hashes and counters in the new seal. Do not reset, rerun, reseal or mutate any stopped/consumed allocation.

## Ordered preparation and execution

These tasks are tracked in root [TODO](../../TODO.md); the package is approved and execution follows their dependency order.

| ID | Objective and prerequisite | Acceptance and verification |
|---|---|---|
| T11-C4-1 | After package approval, establish the shared allocation and inspect the committed baseline | Fresh unstarted combined-04 ledger with prior hashes/counters; immutable prior records; counted preparation commands and unchanged exact inventory. Stop on drift or insufficient allocation. |
| T11-C4-2 | After C4-1, change explicit run selection using test-first development | A failing selector/CLI/lazy-worker regression, then all fake contracts and Ruff pass. Only combined-04 is selectable; old/no-ID commands cannot redirect. Resource receipt/privacy/write-failure controls, shared deadlines and existing stop controls remain covered. |
| T11-C4-3 | After C4-2, perform static cached preparation and seal the user handoff | Verify source/model/asset/fixture/evidence hashes, all prior records, PowerShell syntax and document links. No connected native OCR/model imports, inference, rendering, install or download. Review source diff and actual counters; stop before handoff on any failure. |
| T11-C4-4 | After C4-3, user disconnects every external link and explicitly attests OFFLINE | Only the user launches the new sealed runner; no READY prompt. Owned loopback server, CPU/residency and four sentinel controls verified before the unchanged matrix; each attempt consumes the shared ledger. Stay disconnected through cleanup. |
| T11-C4-5 | After C4-4 starts, complete or stop and verify owned teardown | Preserve every partial attempt. On resource failure retain guard names/readings/limits before shutdown where disk permits, and include the packet in the final summary. Verify zero owned workers, server reaped and listener released; otherwise remain offline. Never terminate unrelated processes. |
| T11-C4-6 | After verified teardown and user reconnection, review sanitized evidence | Report status, all counters, overlap, latency/memory and limitations; prepare local-only semantic review if results exist. Update README/TODO/checkpoint and request approval for the reviewed source/results commit. No adoption or task/stage transition. |

Likely source changes are limited to the three existing evaluation scripts: `combined_trial.py`, `combined_native.py` only if routing requires it, and `test_combined_trial.py`. Documentation changes use the existing proposal/handoff, README, PLAN/TODO, checkpoint and factual benchmark reports. Runtime receipts remain under ignored `data/t11/combined-04/`. No product code or new dependency is included.

## Privacy, stop conditions and unresolved decisions

The user-run synthetic-only trial accepts **no filesystem confinement**: native components have the user's Windows account access. All external links must remain physically disconnected until verified teardown and the explicit safe-to-reconnect message. Use only an owned loopback service at 127.0.0.1:11434; refuse an occupied unrelated listener. No cloud fallback or external grader. Documents, images, prompts, vectors, raw answers/OCR and private exact-path error receipts remain local and are not printed into tools or committed. Review only sanitized counters/statuses, hashes and scalar resource measurements in the assistant session.

Stop on reconnect, unexpected egress/download, identity drift, GPU use, residency/overlap failure, ownership or accounting uncertainty, resource/deadline/storage boundary, exhausted allowance or cleanup uncertainty. Preserve evidence without retries. A receipt-write failure also stops; durable storage cannot be guaranteed on disk failure. Sampled storage checks are not kernel disk quotas. Strict performance on a physical 16-GB host remains unproven if detected hardware differs; the approved Windows 11/16-GB/no-dedicated-GPU target does not change.

The user approved this exact fresh package, including its limits and the disconnected/no-filesystem-confinement arrangement. A future sampling-policy change, model/OCR adoption, production latency/quality budgets, rotated-output resolution, broader OCR/grounding acceptance and remaining Stage 1 architecture decisions stay separately gated. This trial does not resolve them automatically.

Package approval authorizes the necessary bounded selector changes, fake verification, static preparation, disconnected user-run trial and sanitized results documentation. The accompanying explicit commit approval covers the five proposal documents only. Later source/results commits, limit relaxation, additional trials and Stage 2 transition remain separate gates.

## Completed static preparation

Proposal documents committed as `473d24a`. [Preparation evidence](../benchmarks/combined-ocr-model-fourth-preparation.md) records test-first selector changes, 28 passing fake contracts (2.150 s), passing Ruff/PowerShell syntax and final rehash of 149 sealed identities with ten prior records unchanged. Final preparation check: 250.468 s, 36/160 reservations (28 preparation/eight reporting), zero API/native attempts, offline epoch unset. The [new handoff](combined-ocr-model-handoff.md) is ready for the already approved disconnected user-run step. New preparation source/documentation commit remains gated.
