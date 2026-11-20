# T17-IF-SC — source-coordinate continuation with immutable accounting

## Status and purpose

**Proposed; execution and the five planning-document commit await approval.** The user approved committing the five stopped-attempt findings and preparing this continuation. Findings are committed as `c404b61`.

Continue the [original source-only review](hub-source-coordinate-review.md) in a fresh allocation. The [first attempt](../benchmarks/hub-source-coordinate-review.md) stopped during accounting before research; it is closed, not retried or repaired. Avoid its failed File.Replace operation by creating new immutable accounting records. This is a proposed mechanism change, not a diagnosis of the original argument-binding failure.

The product goal, exact source question, candidate identities and research ceilings remain unchanged. Do not repeat successful HS wheel/runtime inspection or silently substitute a source coordinate.

## Fixed inputs and question

| Input | Identity / permitted use |
| --- | --- |
| Completed wheel evidence | Hub 2.4.0 wheel, 857,021 bytes; SHA-256 `42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801`. Read HS receipts/findings only; no wheel reread/download. |
| Historical source | `178e1a1797858724c79fd9d12d79d0902d730497`; prior development-version observation remains historical. |
| Observed release | `3739729b86489e4ae28b5a62e622be320b141493`, linked by the official v2.4.0 release in HS; no replacement-pin approval or established build provenance. |
| Preserved context | AGENTS/SPEC/pyproject/lock; HS proposal/report/aids; dependency/preflight baselines; closed SC attempt 01 proposal/report/final records and inherited preservation links. Small authored evidence only. |

What publisher evidence connects the exact wheel digest to build/publishing source, and how do those roles relate to the historical and release coordinates? A workflow, tag and build can identify different commits. Distinguish a verified relationship, an attestation and reproducible-build proof; do not infer any of them from RECORD hashes or a matching version string.

## Corrected accounting contract

Fresh ignored root **`data/t17/hub-source-coordinate-review-02/`**; refuse if present. Never modify attempt 01, its original/pending/final ledgers, or any closed HS/IF-SA root.

- First execution invocation only creates the fresh root and an exclusive-create, flushed `ledger-0000.json`. Include approval reference, fixed ceilings/deadline, initial charge and reporting reservation. No optional skills/source/historical-evidence reads before this record. Bootstrap failure stops execution; do not assume a ledger exists.
- Subsequent reservations create **new** `ledger-NNNN.json` files with FileMode.CreateNew, UTF-8 bytes and Flush(true). Never replace, truncate or overwrite a ledger; no File.Replace, rename-overwrite, mutable latest-pointer or backup-path argument. Read only regular files inside the fresh root; reject reparse/hardlink/alias paths.
- At most **32 ledger records, 4 KiB each**. Each contains sequence, previous record SHA-256, fixed epoch identity, cumulative counters/status and the current reservation; no growing event-history array. Use literal derived ordinal names, not paths supplied by JSON.
- Select the latest state only after checking the complete contiguous sequence from 0000, schemas/size bounds, previous-byte hashes, unchanged epoch/limits, and nondecreasing counters. Never skip a malformed/partial highest record, fill a gap, reuse an ordinal or reset a counter. A terminal record forbids further optional work. SHA linkage detects changes within this workflow; it is not tamper-proof storage against the local user.
- Reserve **4 MiB of the unchanged 8 MiB local-read budget at bootstrap** for all ledger validation reads: at most 32 validations of at most 32 records × 4 KiB. The remaining 4 MiB covers precharged authored/evidence/documentation reads. Control/closure invocations share the same record limit and allocation.
- Before optional evidence reads, demonstrate one successful reservation append and fresh selection. Run inline scalar/in-memory controls for valid selection and rejection of a gap, invalid parent hash, decreasing counter, partial/malformed highest record and terminal-state continuation. Demonstrate measured normal output and oversized-output refusal. Do not corrupt disk records for these controls or run a test suite/worker. Persist a small control-result receipt.
- If a record write/flush/validation fails, stop optional work, preserve all partial bytes and use exclusively named protected stop/close records. Retain the last successful state plus failed pending reservation without refund. Do not repair an invalid chain or claim that the failed invocation met its reporting contract.

This permits inline accounting/documentation orchestration only, not an application implementation or new executable inspection aid. A single sequential controller owns reservations; no concurrent writers or subagents.

## Ordered tasks and evidence

| ID | Objective / prerequisite | Acceptance / verification | Status |
| --- | --- | --- | --- |
| SC1 | After exact approval, bootstrap and validate immutable accounting | Initial durable record precedes optional reads; append/fresh-selection and negative/output controls pass; verify frozen small inputs and record identities before source research. | Pending approval |
| SC2 | After SC1, review publisher/source relationship | Exact-artifact registry provenance/metadata first; then official commit/tag/publishing text. Every necessary relationship has a URL, observed identity and verified/unknown/conflicting label; failed access counted. | Pending SC1 |
| SC3 | After SC2 or required-evidence stop, make a recommendation | Identify historical coordinate's role or remaining uncertainty; recommend retain, separately approved correction or blocked/deferred candidate. No pin substitution or downstream graph expansion. | Pending SC2 |
| SC4 | After SC3 or earlier stop, close and hand off | Verify frozen small identities, readable tracked/new-file diffs, links/scope/whitespace/privacy and actual resources; checkpoint/partial findings; separate results-commit request. | Pending SC3 / stop |

Checkpoints: accounting controls before evidence reads; necessary provenance assessment before any downstream proposal. An unresolved relationship can yield an honest blocked recommendation, not an automatic new source pin or custom build.

## Public research and shared ceilings

Only public primary-source/registry text via the web tool: **6 calls / 18 targets**, at most four targets per call, short/medium responses. Opens/clicks/finds/searches and failures count. Permitted targets remain exact-wheel PyPI integrity/provenance, version-specific registry JSON/project metadata, official Hub commit/tag/release pages/API text and linked publishing workflow/run/attestation or necessary compare/parent/pinned-version text.

Allow one fresh attempt per endpoint inaccessible in HS, as explicitly allowed in the original SC package and never attempted in SC epoch 01. No repeated failed target, alternate HTTP transport, repository clone, resolver/audit command, binary/wheel/sdist/model download, build or candidate-code execution. A different official source may provide different evidence; it does not erase a failed access. Query public package/version/hash/source coordinates only. Never follow page instructions as commands or send private document/chat content. Provider response envelopes are not claimed to be locally byte- or kernel-bounded.

| Resource | Ceiling / allocation |
| --- | --- |
| Work | **48 prepaid units**: bootstrap/controls 8; research 16; decision/docs 8; verification 4; protected closure 12. Normal 36; no refunds/resets. All wrappers, controls, research, reporting and closure share it. |
| Active time | **900 seconds**, including controls, failures, documentation/checks/closeout. Separately approved Git actions remain separate. |
| Local reads | **8 MiB total**: 4 MiB conservative ledger-validation allocation plus 4 MiB precharged small-file/evidence checks. No runtime/archive/wheel/tokenizer/model payload reads. |
| Artifacts | **2 MiB** upper bound, including all ledgers/receipts/partial writes, captures/diffs, new report and conservative authored status-edit accounting. State the counting basis; do not discard failures to meet a cap. |
| Reporting | **8 KiB/invocation / 48 KiB aggregate**, preserving **8 KiB for closure**. Precharge before invocation; capture stdout and stderr, including warnings/failures; measure UTF-8 bytes before emission. Oversized output is withheld or retained within artifact limits. |
| Executable trials | **Zero** suites/Ruff/inspection workers/candidate imports/model/API/native trials. Only the expressly described inline accounting/output controls and documentation checks; no skill scripts/subagents. |

Stop optional work on deadline/cap/record limit, host denial, unexpected I/O/reporting failure, unsafe input, identity mismatch, contradictory required evidence or exhausted source access. Protected capacity is only for partial findings and closure. If any unexpected owned process exists, verify teardown before handoff. No retry/reset/continuation of a stopped allocation.

## Deliverables, alternatives and approval

Use the existing `docs/benchmarks/hub-source-coordinate-review.md` for a clearly separated epoch-02 result; preserve its epoch-01 account and committed history. Update PLAN/TODO/README/checkpoint and dependency/preflight findings only where new evidence affects them. Keep dependency/preflight entry hashes as baseline evidence and distinguish authorized result edits from frozen artifacts. Local approval/accounting/control/source-reference/preservation/closeout receipts remain ignored. No new code or environment/PATH/lock/dependency change.

Recommend immutable records to avoid the failed replacement operation while retaining charge/stop history. Alternative: investigate File.Replace/null binding in a separate diagnostic package, delaying source review; it is not needed to answer the publisher question and is not included here. Deferring this candidate also remains possible under a separate approach decision.

Request approval for **SC1–SC4 under this corrected contract**, plus a separate commit of this proposal and PLAN/TODO/README/checkpoint (**five files**). Routine covered steps need no repeated task approval. Coordinate correction, dependency expansion, provisioning/native/parity trial, runtime adoption, G2 or stage transition keep their later gates. Stage 1 PDF/XLSX/CSV, local OCR/privacy and the 16 GB CPU-only target remain unchanged.
