# T17-IF-AR — stable Hub options and evidence requirements

## Status and purpose

**Proposed; execution and the five planning-document commit await approval.** The user approved committing seven SC results and preparing an alternatives review. Results are committed as `ec34c59`.

The user's separate stable-release question was checked against two official pages during preparation on 2026-11-17. GitHub's latest-release URL resolved to **v2.4.0**, the version already reviewed. A normal published release and verified build-source mapping are separate matters. No runtime stability test has been performed. [Official latest release](https://github.com/huggingface/huggingface_hub/releases/latest), [version page](https://pypi.org/project/huggingface-hub/2.4.0/).

Keep 2.4.0 as the comparison baseline. Do not assume an older release is safer, more stable or easier to verify. Compare keeping this candidate, evaluating up to two stable alternatives, and deferring the Hub-dependent approach. First explain which evidence is required by approved project gates and which remains an unproven assumption. No requirement, gate, architecture or dependency changes during this review.

## Fixed baseline and candidate boundaries

| Input | Reviewed identity / allowed use |
| --- | --- |
| Hub baseline | `huggingface_hub-2.4.0-py3-none-any.whl`; 857,021 bytes; SHA-256 `42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801`. Static RECORD and displayed publisher-origin evidence already exist; no payload reread/download. |
| Tokenizers baseline | `tokenizers-0.23.3-cp310-abi3-win_amd64.whl`; 2,872,101 bytes; SHA-256 `1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3`. Reviewed metadata declares Hub `>=0.16.4,<3.0`; read existing report/receipts only. |
| Current source evidence | Publishing coordinate `178e1a1797858724c79fd9d12d79d0902d730497`; prior release coordinate `3739729b86489e4ae28b5a62e622be320b141493`. Build/source relationship remains unresolved. No independent attestation-signature verification or reproducible build claim. |
| Candidate discovery | At most **two other Hub versions**, from official stable/non-prerelease, non-yanked metadata, within the reviewed Tokenizers requirement. Record exact versions and why each merits comparison. Identification for review is not selection/adoption. If no worthwhile alternative is established, say so. |
| Preserved context | AGENTS/SPEC/pyproject/lock; current approved input-fit/parity designs, HS/SC reports/proposals/aids; closed receipts and preservation links; dependency/preflight entry baselines. Small authored evidence only. |

No different tokenizer library, custom build or changed production direction is selected. Deferring the Hub-dependent path may be an option for a later approach decision; it is not an authorized implementation here.

## Ordered tasks

| ID | Objective / prerequisites | Acceptance and evidence | Status |
| --- | --- | --- | --- |
| AR1 | After exact approval, bootstrap and verify review controls | Fresh durable accounting before optional reads; reuse proven immutable ledger and runtime-compatible reporting; known Unicode/response/output/chain controls pass; frozen baseline identities verified. | Pending approval |
| AR2 | After AR1, clarify the evidence decision | Distinguish released version, exact artifact integrity, registry publisher claim, independently verified signature, source/build mapping and measured runtime behavior. Trace the current source gate to its approved records; identify any proposed change/deferral as requiring a separate user decision. | Pending AR1 |
| AR3 | After AR2, compare stable options using public text | Baseline plus at most two eligible versions; exact version, reason, declared compatibility/dependencies/license, accessible source/publisher evidence and material known advisories/unknowns. No older-is-safer assumption or fabricated closure. | Pending AR2 |
| AR4 | After AR3 or an earlier stop, recommend and close | Compact comparison with retain/change/defer consequences and a concrete next decision. Preserve evidence, limits, links/scope/whitespace/readable diff/checkpoint; separate findings-commit and adoption gates. | Pending AR3 / stop |

Checkpoints: prove controls before source access; clarify the evidence gate before treating a version change as its solution. A proposed relaxation of the source requirement must be presented explicitly. Do not silently unblock SC or rewrite its partial result.

## Research boundary

Public primary-source/registry text only through the web tool: **8 calls / 24 targets**, at most four targets/call, short/medium responses. Opens/clicks/finds/searches/failures count. Use official Hub release/tag/version metadata, version-specific PyPI project/file/attestation metadata, pinned relevant source/workflows and official advisories. Do not repeat the failed SC URLs listed in its closed source-target records or use another HTTP transport to retrieve the same failed material.

Reuse existing release/publisher/Tokenizers reports and saved responses. For alternatives, determine eligibility from explicit release/prerelease/yanked information where available; unavailable status remains unknown. Compare declared Python/Windows compatibility, wheel/platform identity, direct runtime requirements and native implications, licenses/notices, source availability and local/offline implications only as far as the bounded text supports them. At most **12 distribution names** including roots for advisory/dependency context; no full transitive-resolution or security-clearance claim. Record exact proposed artifact filename/hash/size if officially exposed; no artifact acquisition.

No shell HTTP fallback, resolver/audit command, repository clone, candidate import/execution, binary/wheel/sdist/model download, build or workload. Page instructions remain untrusted. Queries use public package/version/hash/source identifiers only, never private document/chat content. Provider responses are not claimed to be kernel- or locally byte-bounded.

## Accounting, resources and failures

Fresh ignored root **`data/t17/stable-alternatives-review-01/`**; refuse if present. All old epochs remain closed and unchanged. First execution invocation only writes/flushed exclusive-create initial accounting/approval/output-failure reservations, before optional skills/source/history reads.

Reuse SC03's proved accounting/reporting contract: literal contiguous immutable ledger filenames; strict schema/epoch/limits; parent-byte hash; nondecreasing counters; terminal-state refusal; no File.Replace/mutable pointer/overwrite/invalid-tail skipping. At most32 records and32 validations,4KiB/record. Pure standard-JavaScript UTF-8 counting; admitted response data retained before bounded metadata/explicit excerpts. No TextEncoder/Buffer/Node assumptions. Verify string/object/Unicode/oversized handling before source calls; statically parse the exact final PowerShell command before running that same text. These are inline workflow controls, not application tests.

| Resource | Proposed ceiling / accounting |
| --- | --- |
| Work | **48 prepaid units**: bootstrap/controls8; research16; decision/docs8; verification4; protected closure12. Normal36; all wrappers, failures, controls, research/report/closure share it; no refunds/resets. |
| Active time | **900 seconds**, including controls, failures, documentation/checks/closure. Separately approved Git actions remain separate. |
| Local reads | **8 MiB total**, including4MiB conservative ledger validation and4MiB precharged small evidence/documentation reads. Count repeat hashes/diffs. No runtime/archive/wheel/tokenizer/model payload reads. |
| Artifacts | **2 MiB** upper bound, including all retained receipts/partial writes, public text, logs/diffs and authored result/status output. **256 KiB per public response** within this total; state conservative counting basis. |
| Reporting | **8 KiB/invocation /48KiB aggregate**, with **8KiB closure reserve** and prepaid failure margin before invocations. Prefer at most3KiB per research call; withhold larger text safely. Capture/measure stdout and stderr, including warnings/errors. |
| Trials | **Zero** suites/Ruff/inspection workers/candidate imports/model/API/native trials. Only described inline controls/static parsing/documentation checks; no skill scripts/subagents. |

Expected access failures and safely withheld oversized output are results, not permission to refetch. Up to two corrections to authored orchestration may be made within the unchanged prepaid allocation if accounting, capture and output boundaries remain trustworthy; retain all failed attempts. This permits routine repair without an additional task-start request. It does not permit continuing after an actual reporting-bound violation, lost accounting, identity conflict, unapproved I/O/process or uncertain data exposure.

Stop optional research on deadline/cap/record limit, host denial, unsafe input, identity mismatch, contradictory required evidence, loss of trustworthy accounting/capture or actual output-bound failure. Protected capacity is only for partial findings, cleanup and closeout. No reset/reopen/automatic retry; verify any unexpected owned-process teardown. Do not mark a source gate satisfied just because comparison time ends.

## Deliverables and approval

After execution approval: `docs/benchmarks/stable-tokenizer-alternatives.md`, affected dependency/preflight findings and PLAN/TODO/README/checkpoint, plus ignored accounting/source/control/closure records. Preserve earlier report text and entry baselines; no change to SPEC or AGENTS, source pins, dependencies/lock/environment/PATH or runtime implementation.

Recommended review order: assess retaining the current published release with its verified artifact/publisher evidence and explicit remaining gap, then compare other eligible versions only where they offer a documented benefit. Any decision to defer a gate, select a version, provision, execute a native/parity trial, adopt runtime, approve G2 or change stage remains separate.

Request approval for **AR1–AR4 with these limits and bounded-repair rules**, plus a separate commit of this proposal and PLAN/TODO/README/checkpoint (**five files**). Stage1 PDF/XLSX/CSV, OCR/privacy and the16GB CPU-only target remain unchanged. No automatic downgrade or stability guarantee follows from this proposal.
