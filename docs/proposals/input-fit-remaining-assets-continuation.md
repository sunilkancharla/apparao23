# T17-IF-P — diagnostic-enabled remaining-asset continuation

## Status and purpose

Proposed; execution awaits approval. IF-O source/findings are committed as `a13e8b2`. The user approved preparing this continuation. [IF-N findings](../benchmarks/input-fit-tokenizer-static-review.md) verified two wheels and one Qwen asset before a bookkeeping PermissionError; [IF-O findings](../benchmarks/receipt-persistence-investigation.md) reproduced a controlled replacement failure but did not establish the old cause.

Acquire and statically identify only the ten missing public data files in a **new** allocation, with operation-level bookkeeping diagnostics and bounded scalar reporting. This is a new attempt under a newly approved package, not reopening or retrying any closed command. No installation, candidate imports, model/API/inference call, runtime adoption or application implementation. G2 stays open.

## Exact files and identity policy

| Publisher / full revision | Only permitted payload filenames |
|---|---|
| `Qwen/Qwen2.5-1.5B-Instruct` / `5fee7c4ed634dc66c6e318c8ac2897b8b9154536` |`tokenizer_config.json`, `vocab.json`, `merges.txt`, `config.json`, `LICENSE` |
| `nomic-ai/nomic-embed-text-v1.5` / `541c5a6fadb4da793505a2bb4d3ee910de7f39ea` |`tokenizer.json`, `tokenizer_config.json`, `special_tokens_map.json`, `vocab.txt`, `config.json` |

Do not redownload the two wheels or Qwen's already acquired tokenizer.json. Hash-check those three existing files solely to preserve/relate their identities; do not inspect wheel contents again, parse/load the existing tokenizer or copy them into the new root. Retain all old receipts/pending files unchanged. No additional assets, weights, archive, transitive dependency or alternative revision is authorized.

Carry forward IF-N's explicit data-only acquisition policy: retrieve the exact revision/filename pairs, verify publisher-declared exact size and Git/LFS identity where available, and compute local SHA256. Missing publisher SHA256 remains `publisher_digest_unavailable`; a first-observed hash is not independent attestation. Complete filenames/byte hashes do not establish model-store equivalence, native safety, license completeness or tokenizer parity. Stop on missing/mismatched metadata rather than choosing another snapshot.

## Ordered tasks and acceptance

| ID | Objective / prerequisite | Acceptance and evidence | Status |
|---|---|---|---|
| IF-P1 |After approval, freeze old evidence and new shared accounting |Clock/full reservations, fixed schedule and preservation identities durable before optional work; old epochs unchanged |Pending approval |
| IF-P2 |After P1, implement a small diagnostic wrapper test-first |Per-stage bookkeeping telemetry, strict remaining-file/transport/reporting caps, passing tests/lint/format and caught mutation; no candidate execution |Pending P1 |
| IF-P3 |After P2, one supervised continuation worker |Up to ten exact payloads identified or honest partial stop, per-operation/error/HTTP journals, verified process teardown; no retry |Pending P2 |
| IF-P4 |After P3 or bounded stop, review and close |Combined reference manifest distinguishes earlier/new observations, preserves old files, records limits/deviations/gaps and requests separate source/results commit |Pending P3 |

Potential new authored files: `tests/evals/spikes/remaining_asset_review.py` and `test_remaining_asset_review.py` only. Do not edit the frozen IF-N/IF-O aids or the prior parity design. Use local incremental/test-driven/security/review/documentation workflows; no skill scripts/subagents or application source changes.

## Reuse and bookkeeping diagnostic boundary

The reviewed IF-N aid may be imported **only as locally authored Python evaluation code**, after verifying its recorded SHA256 `47f1d2c8202d96cbd07c4ff7d1f899c6130423d7935a73aa2cff20b1bd3d4f5c` and reviewing import side effects. Its main guard must remain inactive. Reuse bounded byte/identity/DNS/HTTP primitives as appropriate; never call its old main/acquire/controller or use its default RUN/WHEELS schedule. This permission does not allow importing any downloaded wheel/tokenizer or third-party candidate code.

Use an isolated module instance with an explicitly stricter URL policy and a new-root Budget subclass/wrapper. Every inherited operation must obey this package's lower request/body/output caps, not merely the older larger constants. Tests must prove the narrower policy applies inside redirect handling, precharge and output writes. Do not fork the entire old downloader or dynamically extract/eval source. IF-O is a read-only diagnostic design reference; no old synthetic probe or Windows handle API is needed here.

The new bookkeeping writer preserves the same exclusive-pending/JSON-write/flush/fsync/close/replace semantics, adding before/success/failure packets for each operation. Capture exception class/errno/winerror and approved basenames only. Do not log arbitrary error strings, absolute paths, configuration/template/vocabulary text or candidate outputs. Preserve failed pending/old target bytes and conservative reservations. No retry/backoff, unique-temporary strategy, permission change, forced overwrite or pending-file deletion is introduced.

Use a bounded independent append-only operation journal which does not invoke the writer under test. A reporting failure stops optional work; it must not authorize another transport or a successful-precharge claim. A failed/missing precharge prevents opening its HTTP request. The CLI must be fixed to the fresh root and refuse a previous claim/closed allocation. No old data-root fallback.

## Transport, data and output limits

The worker may make at most **40HTTP transactions including redirects**, shared across the two pinned tree-metadata requests and ten payloads. Maximum2validated redirects per logical fetch. HTTPS host is **huggingface.co only**, with exact pinned tree/resolve/resolve-cache paths and reviewed public redirect-query fields. No arbitrary host/port/credentials/secret queries/proxy inheritance; reject private/reserved DNS results and retain the known DNS check/use limitation. Default verified TLS, identity content encoding, bounded streaming reads, no alternate transport or automatic failed-request retry. No optional web research or registry/wheel request in this package.

Payload cap **4MiB/file /8MiB aggregate**. Metadata cap **1MiB/body /4MiB aggregate** including charged redirect/error bodies/probes. Precharge exact reported sizes plus overflow probes before fetch, without refunds; stop if unknown size cannot be safely reserved within caps. Every received byte/error/redirect and every failed attempt belongs to the same shared accounting. New local artifacts, journals, partial files, fixtures and reports together at most **16MiB**; no full-body duplicate staging. Hash/size/Git/LFS mismatch stops the worker before publishing that asset as verified.

**Reporting correction after IF-O:** controlled reporting stdout at most **16KiB per invocation /128KiB aggregate**, including tests/lint/diagnostics/closeout, with16KiB of the aggregate reserved for protected closure. Measure UTF-8 text before emitting it, persist cumulative reporting charge and refuse oversize optional output. Project-file output and reporting stdout are separate counters. Select scalar properties explicitly; use plain text reads such as `[IO.File]::ReadAllText`, never serialize Get-Content provider objects or arbitrary Process/file objects. Do not print full remote responses, vocabularies, templates or raw journals. Tool-provider envelopes/internal output are opaque and are not claimed kernel-enforced; document any unaccounted output honestly.

## Tests and one connected execution boundary

Meaningful failing tests first, then the smallest wrapper. Cover all write-stage/error/diagnostic failures, successful precharge before transport, no retry, exact ten-file/version/host rejection, redirect restrictions, lower inherited caps, malformed/size/hash/Git/LFS metadata, response encoding, partial files, reparse/traversal refusal, old-root/closed-claim refusal and bounded scalar reporting including provider-object refusal. Include a mutation of an admission/error/cap guard. At most **six focused suite invocations** and **four Ruff invocations**, reserving final lint/format checks before optional refinements. Fake tests use injected transports and synthetic bytes only.

After fake checks pass, one isolated stdlib continuation worker, supervised with retained Process/birth identity, at most300seconds plus30seconds teardown;10-second request timeout. Account for controller/console descendants and record observed teardown. No subprocess candidate/service or OS file-lock experiment. Connected public-data/static-only boundary; **no filesystem/outbound confinement or kernel RAM-cap claim**. Host permission requirements remain distinct from project approval; no policy bypass, global environment/PATH change or package installation.

## Shared accounting and stopping rules

After approval only, create ignored `data/t17/input-fit-assets-remaining-01/`. **112prepaid conservative units:96normal/16protected**: initialization8, helper/tests48, acquisition16, review12, close12, protected16. Include wrappers/shells/interpreters/test/lint/mutation/negative/control/HTTP/report/cleanup operations in the same blocks. Separately approved Git actions are outside this epoch. Reserve all ceilings before optional work; no refunds or exhausted-epoch reset. One actual continuation worker only.

**1,800active seconds /16MiB local artifacts**, with the separate reporting/HTTP caps above. Preserve AGENTS/SPEC/pyproject/lock; frozen IF-N/IF-O aid/test sources, their findings, prior parity design, final meters/closeouts and old stopped/pending/manifest/inspection/identity/process/research receipts. Hash-check the three earlier payloads at entry/closure without parsing/loading. Preserve the linked older evidence through its existing manifests. Do not update a document that is in the preservation manifest; put new findings in the current report/status references.

Stop optional execution at the first applicable cap, host denial, unexpected I/O error, reporting failure, publisher/path/hash mismatch, invalid metadata, deadline or uncertain teardown. Preserve operation/error diagnostics where possible. Protected capacity is solely for preservation/partial closeout, never more downloads/tests. No repair/retry/reseal of stopped runs. A failed attempt requires another explicit decision, not a silent fresh command.

## Deliverables and approval request

After approval, deliver `docs/benchmarks/input-fit-remaining-assets.md`, local per-asset/HTTP/operation/reporting/teardown/combined-reference manifests, the two reviewed aids and affected dependency/preflight/PLAN/TODO/README/checkpoint updates. Keep successful earlier identities distinct from new observations, and exact-byte acquisition distinct from publisher attestation/runtime suitability. Full graph/native notices/advisories, source-to-release provenance, disconnected runtime and exact rendering/token/output-headroom parity remain separate unresolved gates.

Requested now: approve IF-P1–P4, including this explicit locally authored-module reuse, diagnostic-only writer change, connected ten-file acquisition and limits, and separately commit the five proposal/status documents. Routine ordered work is covered by that one approval. Later source/results commits, installation/native parity/runtime adoption and stage transitions retain separate gates.
