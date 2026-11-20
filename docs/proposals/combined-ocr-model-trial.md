# T11 proposal: bounded combined OCR/model pressure evaluation

**Status: explicitly approved for bounded implementation, user-run offline testing and committing reviewed changes.** Prepared 2026-11-14 (Asia/Calcutta), after results commit `94f3e46`. The user subsequently replied "yes i approve this" to the implementation/offline-testing/scoped-commit request. This authorizes the exact package below; native execution remains the disconnected user-run step. No installation/download or runtime adoption is included. This is a feasibility subset of T11; it does not close T09's quality gaps or all Stage 1 acceptance.

## Question and scope

Can the existing CPU-only models coexist with an OCR worker while producing the same fixed-evidence answers, within a conservative resource envelope for the Windows 11/16-GB target? Compare sequential operation with measured OCR/chat overlap. Use both evaluated OCR engines as candidates; do not select one based on this proposal. Preserve the user's positive visual assessment of rotated text alongside unchanged automated M08 mismatches; no rotation repair, rescore or new asset is included here.

Use synthetic OCR fixtures and the already authored T10/T11A fixed corpus/questions only. No `sample_files`, real documents, uploads, product UI, persistent index, cloud grader, global changes, Windows isolation experiments or new dependencies. OCR text is not fed to the chat benchmark: it remains a separate stress workload. Fixed evidence isolates pressure effects and does not demonstrate an extraction-to-answer application.

## Frozen artifacts and settings

Rehash existing project-local Ollama 0.40.16 executable/all required model layers against the verified T10/T11A receipts before loading. No mutable-tag refresh, network research, pulls, downloads, replacement assets or installation. Missing/mismatched bytes stop readiness. Use existing project `.venv`, exact OCR pins and the 16-wheel/three-English-asset inventory from manual-04; no changed language/model/font or classifier. Source/config/artifact/fixture/evidence hashes must be frozen before the first native launch.

| Role | Existing candidate | Manifest SHA-256 |
|---|---|---|
| Embeddings | nomic-embed-text:v1.5 | `0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f` |
| Chat A | qwen2.5:1.5b-instruct-q4_K_M | `65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b` |
| Chat B | qwen3:1.7b-q4_K_M | `8f68893c685c3ddff2aa3fffce2aa60a30bb2da65ca488b61fff134a4d1730e7` |

Exact layer/version identities and licensing records remain those in [embeddings](../benchmarks/embeddings.md), [chat models](../benchmarks/chat-models.md), and the approved OCR inventory; this is not a license/adoption change. Do not include the review-only 3B candidate or substitute other models. Qwen3's tag is not a measured parameter-count/memory guarantee.

Retain T11A options: CPU/zero VRAM, four model threads, context 2048, batch 64, maximum output 192 tokens, temperature 0.2, top_p 0.9, top_k 20, repeat_penalty 1, seed 42. Qwen3 uses `think=false`; Qwen2.5 retains its non-thinking template. Preserve the authored system contract/schema and case evidence; no tuning after observing results. Nomic uses the previously tested 2048 context, full 768 dimensions, truncate=false and existing query/document prefix contract. OCR remains one thread per backend/session where configured, one worker, exact cached paths, 300 DPI/12 MP and classifier/download refusal unchanged.

Propose project-owned loopback server only, `127.0.0.1:11434`, with trust_env=false/no redirects; do not attach to or terminate an existing service. One inference request at a time, at most two resident models (Nomic and one chat candidate); use `keep_alive=600` seconds for embedding/chat requests and explicit unload before chat-model switch. Verify residency/CPU state rather than assuming keep-alive succeeded. If runtime evicts a required resident model, retain an incomplete coexistence result and stop; do not silently alter settings to make it fit.

## Ordered tasks and frozen schedule

| ID | Objective and prerequisite | Acceptance/evidence |
|---|---|---|
| T11-P1 | After approval, inspect existing supervisors and establish shared budgets/ownership before adapting evaluation code | Test-first fake cases cover combined process/API counting, overlap accounting, memory/deadline stops, missing assets, drift, disconnect and teardown. No OCR/model imports during connected preparation; at most three authored evaluation/test files, plus affected docs. |
| T11-P2 | Rehash assets and freeze evidence/fixtures/settings, then seal one fresh standalone offline handoff | New linked ledger under `data/t11/combined-01/`, no old counter reset. Reuse verified manual-04 synthetic inputs read-only; verify their manifest hashes. No new fixture rendering or fonts. Fixture-copy metadata must preserve source identity and page provenance. |
| T11-P3 | User disconnects/attests; start only owned server/controller, run bounded positive/stop controls | Verify loopback ownership, CPU/residency, aggregate memory and >=4 GiB free RAM. Four direct OCR sentinel roots: deadline/memory once per engine, using existing synthetic sentinels, not full reexecution of old controls. Failure stops, with teardown evidence. |
| T11-P4 | Execute the fixed baseline/overlap matrix below | Exactly 36 scored chat attempts, 44 embedding attempts and 24 OCR comparison roots. Every failed/interrupted attempt remains in the denominator; no retries or order changes. Save per-request/worker timestamps and actual overlap. |
| T11-P5 | Stop/unload/reap owned processes, verify listener release, then user reconnects | Teardown true, empty owned-child list, no owned listener; do not kill unrelated processes by port alone. Otherwise user remains disconnected. |
| T11-P6 | Review sanitized metrics and prepare local answer review | Distinguish automated schema/citation-ID checks from semantic correctness. Raw answers, OCR, vectors and prompts remain local. Report failed/missing cases and resource limits; update README/TODO/checkpoint. Ask separately before results commit/adoption. |

For each of the two chat candidates, use existing C01 (answerable), C03 (multi-source/table values) and C08 (empty-evidence refusal), each twice, in this order: baseline with no OCR (6 calls), Tesserocr overlap (6), RapidOCR overlap (6). Total 18 per model, 36 chat calls. Preserve exact previous case/evidence/schema identities; if those identities cannot be reconciled, stop readiness rather than inventing replacements. C08's current evidence remains empty despite any embedding probe.

Before the matrix, embed the frozen 32-document T10 corpus in batches of four (8 calls). Before each chat attempt, issue one existing-contract query embedding (36 calls), checking dimensions/finite values; this is a resource workload, not a new retrieval-quality score. Keep Nomic resident during the matrix. No concurrent embedding/chat inference is claimed.

Each of the 24 overlap calls starts one OCR worker on a fixed cycle M02, M03, M04 repeated in call order. Use the existing immutable gold and readable-case thresholds. Start the worker only while the chat request is in flight; log timestamp intersection, observed loaded-model state and per-process samples. If no real overlap occurs, flag that pair incomplete rather than silently retrying. Model loading/cache state and short OCR durations may limit observable overlap. Do not call baseline runs controlled cold-cache measurements.

## Proposed execution/resource allocation — needs approval

- **160 shared process starts/attempts**, covering preparation shells, tests, direct workers, native server/model descendants, four sentinels, regression/negative controls and closeout. Planned allocation: 48 preparation/tests, 16 controller/server/readiness, 28 OCR/sentinels, 36 supervisor/descendant allowances, 16 reporting/Git shells and 16 protected cleanup. Native child accounting charges real descendants without double counting reserved roots. Stop before exceeding any category/shared boundary; no automatic retries or reset.
- **128 loopback API attempts total**, including the 80 scheduled chat/embedding attempts and up to 48 readiness/model-state/unload/teardown calls. Failed calls and polling consume the same meter; no hidden unlimited health checks.
- **75 minutes active execution**, including controls, startup, model switching and cleanup. Chat hard deadline 90 seconds each, embedding 60 seconds, ordinary OCR 30 seconds, deadline sentinel 1 second. Human offline/fixture-readiness waits are logged separately. Connected preparation is bounded to 30 active minutes, excluding user/host approval waiting.
- **Aggregate owned native/controller memory cap 8 GiB**, OCR worker cap 1.5 GiB, monitored controller private-memory stop 512 MiB, at least 4 GiB available physical RAM. Sample aggregate commit, available RAM and process memory at <=250 ms intervals; report sampled versus kernel-enforced limits accurately. Verify a parent aggregate cap does not inadvertently impose the controller's private-memory threshold on child workers. Counter/limit setup failure stops before model/OCR launch.
- At most one OCR worker plus one chat request; two resident models maximum. CPU only; no change to the approved 16-GB target. Detected host capacity is not altered or presented as a strict 16-GB benchmark: cap owned workloads conservatively and report actual hardware/background pressure. Exact behavior on a physical 16-GB host remains an acceptance limitation if this machine differs.
- **Zero downloaded bytes; 512 MiB new trial disk**, including logs/vectors/local review; raw OCR <=32 MiB and answers <=8 MiB. Existing assets/fixtures are not duplicated without counting added bytes. Stop on drift, GPU activity, reconnect, unexpected egress/download, insufficient resources, unknown ownership, process/API accounting failure, deadline or uncertain cleanup. Preserve partial results and all old ledgers.

These are proposed safety/measurement limits, not adopted product latency/memory budgets. Human-readable latency ratios and quality deltas inform a later decision; no passing latency threshold is silently invented.

## Approval requested and remaining decisions

Approve or amend this exact T11 feasibility package: candidate shortlist, fixed schedule, resource/process/API ceilings, manual disconnected operation without filesystem confinement, and one new bounded implementation/preparation/offline-execution allocation. Approval would cover its necessary test-first helper changes, static preparation and user-run steps; Git commit and runtime adoption remain separate gates. No execution is authorized by approval of the preceding OCR results commit.

Keep the rotated-output discrepancy open for local inspection; orientation correction/retrial needs a separate approved package and unchanged-versus-corrected comparison. Representative real scans/table provenance, remaining grounding/semantic scores, acceptable production latency and G2 adoption stay unresolved. This small combined matrix does not close them, T09 or the entirety of T11.

## Prepared handoff

[Connected preparation evidence](../benchmarks/combined-ocr-model-preparation.md) records 15 passing stdlib/fake contracts and 142 sealed files. [Current offline instructions](combined-ocr-model-handoff.md) use combined-01 only. Historical whole-question-file drift from scope amendments was reconciled through unchanged selected wording/gold and frozen packet identities; both file hashes are retained. No native inference has run in this combined allocation.
