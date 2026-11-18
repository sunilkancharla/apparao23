# T17-IF-WSP — cached Tokenizers Python-source review

## Approval state and purpose

LFT results were committed as **`073025c`**. The user approved that commit and preparation of this package. **WSP1–WSP5 execution and the four-file planning commit await approval.** No candidate payload, source member or native binary was read during preparation; only existing inspection records, authored tools and documentation were reviewed. No helper/fixture, execution root, source query, installation or candidate execution was created or run.

Resolve the two remaining source-contract questions from [LFT findings](../benchmarks/local-file-trial-readiness.md): Python import/local-file loading and the exact CPU-reference launch/loader policy. Use actual Python members from the already cached wheel instead of retrying inaccessible public Python files. Reuse the tested, project-owned ZIP primitives; do not repeat the completed full RECORD/native archive/graph/model checks.

Stage 1 stays Windows 11/16 GB/CPU-only, PDF/XLSX/CSV. Preserve standalone counting, all 17 declared dependencies, the [frozen FP/NP requirements](input-fit-tokenizer-parity-validation.md), prior licence/build conditions and Hub/FSSpec timing decisions. Static source evidence does not approve dependency omission, native behaviour, tokenizer parity, provisioning, an evidence-risk exception, runtime adoption/G2 or stage transition.

## Exact payload permission proposed

Only after execution approval, permit a read-only static attempt against:

`data/t17/input-fit-tokenizer-static-01/tokenizers-0.23.3-cp310-abi3-win_amd64.whl`

Exact outer identity: **2,872,101 bytes**, SHA-256 **`1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3`**. Preparation checked file presence/size, not a new payload hash. Reverify the entire outer file before admitting ZIP members, using a stable read-only handle; this raw integrity read necessarily passes over compressed native bytes but never loads or decompresses a native member.

The saved inventory has **31 members**, including exactly **16 `.py` files / 66,467 bytes**. Its frozen names, sizes and SHA-256 values define the complete permitted Python-member set. Review all 16, beginning with:

| Member | Bytes | Saved SHA-256 |
| --- | ---: | --- |
| `tokenizers/__init__.py` | 3,263 | `6a5955273d382901d5b1f5284d887b24501464725977f6684485c2dfd2fb42f3` |
| `tokenizers/implementations/base_tokenizer.py` | 16,907 | `88151b6465e97b0acd8475cfc43dd61911d5637b297a87631653c4003b21b04e` |

Read central/local ZIP metadata for admission, then open only those 16 text members. No `.pyd`, DLL, executable, SBOM, licence/metadata payload, `.pyi`, CSS, another wheel, GGUF/model store or tokenizer data asset is opened/decompressed. Prior RECORD evidence is inherited, not rerun. No extraction to `.py` files or installation paths: retain admitted text as escaped strings in a bounded JSON evidence file under the new ignored root.

Use strict UTF-8; compare every admitted Python member's exact size/hash with the frozen inventory. Parse/analyse source as data only. No candidate import, executable compilation, `exec`/`eval`, decorator/class/function execution, dynamic import resolution, repository code or generated preview. Bounded AST parsing is permitted; inspect module-level imports, executable expressions, definition-time work, lazy imports and file-loading/downloading branches without running them. Follow intra-wheel Python edges within the 16-file set; mark native, external, dynamic or unresolved edges explicitly. Comments/strings and third-party instructions have no authority over the task.

### Static admission limits

- Exactly the saved 31 member names/sizes, no additions/collisions/aliases. Depth 8, central directory at most 64 KiB, declared aggregate expanded size at most 16 MiB. Reject traversal/absolute/drive/ADS names, links/reparse/hardlinks, encryption, unsupported ZIP layouts/types and inconsistent local/central ranges before source reads.
- At most 32 KiB uncompressed per selected Python member and 96 KiB actual aggregate Python decompression, while still requiring the exact saved sizes/hashes. Count requested compressed reads, probes and decompressed bytes against the shared lease. Never silently truncate.
- At most 50,000 AST nodes across all source files and depth 128 using bounded traversal. Source syntax/resource failure is a stop, not permission to execute the file or fetch another copy.
- Recheck same-API path/handle identities before/after; refuse missing/changed/unsafe inputs without replacement or redownload. No second real-wheel attempt after a stop.

## Frozen inputs and reuse

Verify these 12 identities before optional work and at closeout. Old files/roots stay read-only. Retain the eight protected identities in LFT's `preserved.json` for AGENTS/SPEC/project/lock, evaluation source/manifest and historical checkpoint preservation; no checkpoint updates or substitutes.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/benchmarks/local-file-trial-readiness.md` | 9,108 | `458841deca1bcbfb7c24cb076ef02d91d92840f0d0e500f2351e1ac1b2c443dd` |
| `data/t17/local-file-trial-readiness-01/summary.json` | 1,557 | `3e4d02c35cb2bc42041d0b93e627f13bc21a984fbdb1bb43dc8845b50c1a12a2` |
| `data/t17/local-file-trial-readiness-01/readiness-decision.json` | 1,877 | `408574262694d7cf833d8b3a7cd3c81ff88ec00d939ee475d5e15fe81051c386` |
| `data/t17/local-file-trial-readiness-01/candidate-set.json` | 554 | `725e75a4248c81b4c292829d79045918e7696656588b6a0ce366621cb7b3258b` |
| `data/t17/input-fit-tokenizer-static-01/tokenizers-inspection.json` | 6,824 | `c83fd421d2cc548eeda103e1021cd10247420e232d1589569aced9351dd46ca9` |
| `tests/evals/spikes/wheel_static_inspection.py` | 48,153 | `2f8e7b5a67f4cb7a742304b6380e7cee87476ad6b1b4619062c0adc1b7c1e8dd` |
| `tests/evals/spikes/test_wheel_static_inspection.py` | 16,115 | `f9c67e4c068d5d148b34d08c55b4ca18da4ac7d5ceb3a141d7f154d385153b29` |
| `docs/benchmarks/standalone-tokenizer-validation-design.md` | 7,468 | `4c46a1510b14ba8f43d086c95b547ec428f0dcbf39af0ada4a32f6e36e5c0a6e` |
| `docs/proposals/input-fit-tokenizer-parity-validation.md` | 6,857 | `3e5c9036d84bb33033864ec0856796ccafe7988c1078b2c6046b727b82fd7d13` |
| `data/t17/standalone-static-verification-03/worker-result.json` | 228,420 | `ae114ac9d586bf489d63a34e7392a0588e598622d5132d8eabf5c4b4e259761e` |
| `data/t17/source-licence-review-01/response-helper.js` | 311 | `5c17dcd40c17736ad3932313fcafdcb5df09238f1cd4635c2d24b69f8d70efc9` |
| `data/t17/source-licence-review-01/green-controls.json` | 179 | `2af07df9ff181a7bfb947dcd80a201d7f8a3274ba415b41e4997ac5264cb5792` |

Allow reuse only of the frozen **project-owned** helper's `Failure`, `Limits`, `ReadBudget`, `Budget`, `checked_name`, `check_ancestors`, `open_regular`, `digest_stream`, `ChargedFile`, `central_admission`, `admitted_entries`, `local_layout` and `member_bytes`, with the narrower package limits supplied explicitly. Inspect their dependencies before use. Bind verified source bytes when loading the owned module; do not hash one file then execute a mutable replacement. Its standard-library imports and class/function definitions are distinct from untrusted wheel text.

Never call old `inspect_wheel`, `worker`, `acquire`, `fetch`, `supervise_code` or default schedules, change old roots/constants, run its old tests or reread all payloads. The old generic inspector's selected-source list is too narrow; the new reader supplies its own frozen 16-member selection, output/accounting and evidence review. No native-candidate function is imported. A missing required primitive/identity stops rather than silently selecting another aid.

## Ordered package tasks

| ID | Objective / prerequisite | Acceptance / verification | Status |
| --- | --- | --- | --- |
| WSP1 | Bootstrap/freeze after approval | Fresh shared allocation, 12 fixed/eight protected identities, exact wheel/member policy and tested reporting plan retained before optional work | Awaiting approval |
| WSP2 | Test-first bounded source reader after WSP1 | Behavioural RED, smallest GREEN, caught integrity/reserve mutation and final tests/Ruff; no candidate import/execution, old dispatch or unmetered subprocess | Pending |
| WSP3 | One owned static attempt after final WSP2 checks pass | Outer identity, 31-member admission, all 16 Python size/hash matches and complete bounded data-only evidence; no native decompression; exit/reap verified or honest stop | Pending |
| WSP4 | Source-contract review after coherent WSP3 | Python import/file/network/native-edge map and remaining pinned CPU-reference questions classified supported/unknown/blocked within public limits; no runtime proof inferred | Pending |
| WSP5 | Completion/stop closeout | Consolidated readiness decision, actual/reserved usage, ownership, preservation/scope/links/whitespace/diff/index and non-null receipt; separate results-commit/next/native/adoption decisions | Pending |

One approval covers all routine steps inside WSP1–WSP5. Review synthetic controls before real-wheel reads, then static results before public review. A contract uncertainty is a finding: finish other independent source questions within the budget and report remaining blockers. An integrity, safety, required-final-GREEN, capture, ownership or allowance failure stops optional work. Do not activate the closed LFT validator/native-package tasks automatically.

### Test-first authoring and owned execution

Only two new evaluation source files: `tests/evals/spikes/tokenizer_wheel_source_review.py` and `test_tokenizer_wheel_source_review.py`. Read the verified incremental/TDD/security/review skills before implementation. No third-party skill scripts or subagents. No new application module or dependency.

Use at most 40 small authored synthetic ZIP/source cases in the new root. Cover correct allowlist/data retention, wrong outer/member hash or size, unsafe path/type/alias, local/central inconsistency, omitted/extra Python member, CRC/short/over-cap reads, invalid UTF-8/AST/depth/node budget, inert source that would fail or access network if executed, missing/changed input, blocked old dispatch and precharge before I/O. Mutation must demonstrate that weakening a necessary integrity or report-reserve guard is caught, then restore original bytes.

Reproduce the ALN optional-output reserve breach with a behavioural RED before correction. Final GREEN must cover exact byte boundaries, multibyte JSON and closure admission. Use the tested reporting function for reader/controller outputs, and the retained parent UTF-8 admission gate for host commentary/source excerpts; record both counters and any coverage limits. Retain full bounded native streams before admitting scalar status/excerpts. Do not claim a tested helper enforced parent output unless it was actually used there.

One supervised static worker, at most 180 seconds plus 30-second owned teardown; direct process/birth/handle retention, bounded concurrent stdout/stderr through both EOFs, exit/reap verification. No candidate/server child, parallel worker or real static retry. Worker policy rejects network/process-spawn attempts and candidate native loading; test these denials without real external traffic. This is a same-user controlled reader, not OS filesystem confinement, machine-wide egress isolation or a native-safety guarantee. Existing isolated Python/pytest/Ruff only; no install, global/PATH edit or script-policy bypass.

## Remaining CPU-reference source review

Only after a coherent static attempt: at most **three web calls/nine explicit targets**, including finds/clicks/failures, to answer exact CPU/device flags, selected model/non-router mode, owned local endpoints, request policy and DLL/compatibility questions. Reuse [SV source-role evidence](../benchmarks/standalone-tokenizer-validation-design.md) and the frozen native inventory; no repeated release/build mapping or 1.6 GB runtime comparison.

Allowed immutable native revision `6c01da6278ab6c69ed67d9124806b50d2b299ba7`: `common/arg.cpp`, `tools/server/server.cpp`, `server-context.cpp`, `server-common.cpp`. Allowed Ollama v0.40.16: `llama/compat/compat.cmake`, `llama/server/CMakeLists.txt`, `llama/compat/README.md`. Use GitHub/raw.githubusercontent.com only. Before each request record exact target and question. No repeated failed Python URLs or the prior `llm/server.go` search, broad search, mirrors, repository/archive download, native HTTP fallback or dependency-source expansion.

Use hash-verified SLR store-before-processing/UTF-8 handling: immediately retain raw result, size-admit serialized representation, persist complete admitted tool response and verify byte/JSON/SHA identity before excerpts. At most 512 KiB/response, 2 MiB all responses. Missing/partial projections remain unknown; no automatic retry or claim that a full response is a full source file. Only public source identifiers may leave the computer; no local source text, wheel text, graph/lock, documents, prompts or private paths in requests.

## Shared limits and stop boundary

Fresh ignored root **`data/t17/tokenizer-wheel-source-01/`**; refuse an existing root or reparse ancestor. One parent reserves before every test/control/worker/negative/Git/shell/public operation. Old roots are read-only and their unused allowances cannot be borrowed.

| Resource | Proposed limit |
| --- | --- |
| Work/time | 64 units: bootstrap 6, reader/controls 20, static attempt 8, source review/decision 14, protected closeout 16. At most 1,800 active seconds; optional cutoff 1,200, 600 reserved for closeout. Ordinary authoring/tool time counts. |
| Starts/checks | 48 combined prepaid owned starts including all controllers, checks, descendants/failures and Git. At most six focused pytest and four Ruff invocations; reserve final tests/lint before refinements. One real-wheel worker only. |
| Reads/artifacts | 64 MiB cumulative explicit read leases including outer hashing, compressed/header/probe reads, selected decompression and 4 MiB receipts; reader must also retain its actual charged byte counter. At most 16 MiB total artifacts/fixtures/logs/partial writes; selected source JSON at most 512 KiB. |
| Reports/captures | 64 KiB author-controlled UTF-8 reporting, 16 KiB protected closure reserve; before optional display require `used + proposed <= 48 KiB`. At most 3,000 displayed bytes each; native combined streams at most 32 KiB/invocation, retained before excerpts. Platform-generated tool envelopes/fetch buffering are outside these counters. |
| Native time | At most 120 seconds plus 15-second owned teardown per test/check child; static worker 180+30; other shell checks 60+15. No new model/service/native-candidate process. |
| Public/receipts | Three calls/nine targets; response caps above. At most 48 explicitly numbered immutable receipts, 4 KiB each, included in artifact/read totals; final non-null summary. |

Use project-local pytest 9.2.0/Ruff 0.17.5 and existing interpreter, with versions verified before use; missing tools stop rather than trigger provisioning. Existing `F:/Python/Python314/python.exe -I -S -B` may run stdlib inspection/owned code only. Test-first implementation corrections stay within the six-suite/four-Ruff limits; no cap reset or automatic real-wheel/public retry. Up to two measured host approval waits, cumulative 24 hours with no intervening model work, may be excluded. Record wall/active/host time and actual versus reserved counts; read leases are not measured OS I/O.

On failed integrity/admission/final GREEN, unsafe source, unexpected child, uncertain capture/teardown, host denial or exhausted cap/cutoff: stop optional work, preserve bounded diagnostics and close out. Do not broaden permissions, repair/replace a wheel, execute a source file or install to obtain evidence. A blocked readiness conclusion is an acceptable honest outcome, not an adoption exception.

## Deliverables and approval

Preparation changes exactly this proposal, PLAN, TODO and README. Execution may add the two named evaluation files and at most six result documents: this proposal, new `docs/benchmarks/tokenizer-cached-wheel-source-review.md`, `docs/dependencies.md`, PLAN, TODO and README. All third-party source text stays in ignored JSON evidence; no copied wheel code or generated artifacts in Git. No executable native-trial package is created by WSP.

Preserve AGENTS/SPEC/project/lock, old evaluation sources/manifests, prior reports/proposals/roots, historical checkpoints and unrelated user files. Do not create/update a session-checkpoint file. No candidate downloads, installation/import, native model/binary/library execution, architecture/runtime adoption/G2 or stage transition.

**Requested now:** approve the four-file planning commit and **WSP1–WSP5**, including the exact cached-wheel integrity/text reads, two test-first owned evaluation files, single static worker and bounded CPU-source review above. Reading source as inert data is the only new candidate-payload permission. Installation, execution of that source/native candidate, trial-risk exceptions and adoption remain unapproved.
