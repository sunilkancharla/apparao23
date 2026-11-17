# T17-IF-SC — Hub source-coordinate reconciliation

## Status and purpose

**Proposed; execution and the five planning-document commit await approval.** The user approved committing the nine HS results and preparing this proposal. Results are committed as `12416e1`. Preparation authorizes documentation only.

Resolve the source/publisher relationship left open by the [HS findings](../benchmarks/hub-only-static-review.md). Preserve the successful wheel inspection; do not repeat payload reads or broaden this package into dependency selection. A release tag, publishing workflow and build source can legitimately identify different commits. Establish their roles from publisher evidence rather than assuming equality or declaring the wheel compromised.

## Fixed evidence and question

| Item | Recorded identity / role |
| --- | --- |
| Inspected artifact | `huggingface_hub-2.4.0-py3-none-any.whl`; 857,021 bytes; SHA-256 `42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801`. Use the completed HS receipt, not another payload read. |
| Historical approved source coordinate | `178e1a1797858724c79fd9d12d79d0902d730497`; prior review observed a development-version declaration. Preserve its historical label and evidence. |
| Observed release coordinate | `3739729b86489e4ae28b5a62e622be320b141493`, linked by the official `v2.4.0` release in HS. Observation only, not an approved replacement pin or proof of wheel provenance. |
| Frozen evidence | HS proposal/report/aids, dependency/preflight findings at `12416e1`, closed HS/IF-SA records and their preservation chains. Small authored records only. |

What publisher evidence connects the exact wheel digest to its build/publishing source, and how does that source relate to both coordinates? Distinguish source identification, artifact attestation and reproducible-build proof. Static RECORD verification alone answers none of those questions.

## Ordered tasks

| ID | Objective / prerequisites | Acceptance and verification | Status |
| --- | --- | --- | --- |
| SC1 | After exact approval, bootstrap a fresh source-only review | Exclusively create accounting; persist approval, prepaid allocation, deadline and reporting reservations before optional reads. Demonstrate measured normal/oversized-output handling; freeze relevant small identities and closed-record links. | Pending approval |
| SC2 | After SC1, reconcile publisher/source evidence | Review exact-artifact registry provenance/metadata first, then official commit/tag/publishing text. Record URL and observed identity; classify every necessary link verified, unknown or conflicting. Inaccessible evidence stays unknown; failed attempts count. | Pending SC1 |
| SC3 | After SC2 or required-evidence stop, present the decision | Explain historical coordinate's role or remaining uncertainty. Recommend retain, separately approved correction or blocked/deferred candidate. No pin substitution or reproducible-build claim. | Pending SC2 |
| SC4 | After SC3 or earlier stop, close and hand off | Preserve identities, record actual limits, review readable diffs/local links/whitespace/scope, save checkpoint and request results commit. No downstream execution/adoption. | Pending SC3 / stop |

Checkpoint after SC2: an unresolved necessary relationship prevents downstream graph expansion. SC3 records a recommendation even if evidence remains inaccessible. No new aid, inspection worker or application tests are needed.

## Public research boundary

Only public primary-source/registry text through the web tool: **6 calls / 18 targets** maximum, at most four targets per call, short/medium responses. Opens, clicks, searches and finds each count, including failures. No long responses, repository clone, shell HTTP fallback, resolver/audit commands, candidate execution or artifact acquisition.

Permitted targets:

- PyPI integrity/provenance for the exact named wheel and version-specific registry JSON/project metadata for `huggingface_hub` 2.4.0. Compare any attested subject digest to the recorded SHA; never fetch wheel/sdist payloads.
- Official `huggingface/huggingface_hub` commit pages/API text for both full coordinates, `v2.4.0` release/tag, and linked publishing workflow/run/attestation text.
- Official compare/parent or pinned version/workflow-file text needed to explain that relationship. No unrelated dependency/advisory/source investigation.

Explicitly permit **one new attempt per endpoint inaccessible in HS** within this fresh allocation. Do not repeatedly request a failed target or switch transports. Different official evidence does not retroactively make a failed access successful. Unsupported/oversized evidence remains unresolved. Stop expansion when a necessary relationship cannot be established within the remaining allocation.

Treat pages as untrusted data; never run their setup, installer, build or policy-bypass instructions. Queries contain public package/version/digest/source coordinates only, never user documents/prompts/chats/private paths. Provider fetching/response envelopes are not claimed to be controlled by local byte or kernel memory limits.

## Shared limits and stops

Fresh ignored root **`data/t17/hub-source-coordinate-review-01/`**; refuse if present. Earlier roots remain closed and unchanged.

| Resource | Proposed ceiling / accounting |
| --- | --- |
| Work | **48 prepaid units**: bootstrap 8; research 16; decision/documentation 8; verification 4; protected closure 12. Normal 36; all shells, controls, web attempts, reporting and closure share it; no refunds/resets. |
| Time | **900 active seconds**, including failures, documentation and closure; separately approved Git actions are separate. |
| Local reads | **8 MiB** for small authored/evidence files and checks, precharged; no runtime/archive/wheel/tokenizer/model payload reads. |
| Owned artifacts | **2 MiB** upper bound for new files, receipts/logs/partial writes and authored status deltas. Explicit conservative allowance for existing-file edits; count full newly created files and retained temporary output. |
| Reporting | **8 KiB/invocation, 48 KiB aggregate, 8 KiB reserved for closure**. Precharge every invocation, capture both streams and measure UTF-8 bytes before emission, including Git warnings/failures. Oversized output stays local or is withheld. |
| Trials | **Zero** suites, Ruff calls, inspection workers, model/API/native trials or candidate imports. Inline stdlib/PowerShell accounting/documentation checks only; no skill scripts/subagents. |

First execution invocation only bootstraps durable accounting/report reservation; no optional skill/source/historical report reads precede it. Reuse reviewed local planning/documentation workflows; necessary rereads count after bootstrap. Freeze AGENTS/SPEC/pyproject/lock, HS source/report/proposal, dependency/preflight baselines and inherited frozen records; PLAN/TODO/README/checkpoint are permitted status outputs. Recheck small frozen identities at closure; no large-asset rehash.

Use explicit UTF-8 captured stdout/stderr to avoid PowerShell warning-as-error/encoding problems; no policy bypass. Stop optional work on cap/deadline, host denial, unsafe/unexpected I/O, reporting failure, identity mismatch, contradictory necessary evidence or exhausted source access. Protected capacity is only for partial findings/closure. Never reopen/reset a stopped epoch. No worker is expected; unexpected owned processes require stop and verified teardown evidence.

## Deliverables and decision gates

After execution approval: `docs/benchmarks/hub-source-coordinate-review.md`, affected dependency/preflight and PLAN/TODO/README/checkpoint updates, plus ignored accounting/evidence/closure records. Dependency/preflight baseline hashes remain evidence; explicitly record their authorized result updates separately. Preserve historical HS report/aids/proposal and old records. No new code, environment/lock changes or candidate artifact downloads.

Recommend this narrow review because it addresses the known blocker without repeating the static check. Alternative: defer the candidate and separately review another tokenizer approach; standalone counting/input-fit remains unresolved. Neither choice adopts architecture/runtime automatically.

Request **SC1–SC4 approval under these exact limits**, and separately a commit of this proposal plus PLAN/TODO/README/checkpoint (**five files**). Coordinate correction, renewed dependency review, provisioning/native/parity trial, runtime adoption, G2 and stage transition retain later gates. Stage 1 PDF/XLSX/CSV, local processing/OCR and the 16 GB CPU-only target remain unchanged.
