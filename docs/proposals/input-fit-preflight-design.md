## Latest AS outcome — source display stopped review before implementation

[AS findings](../benchmarks/wheel-artifact-review.md) record a source-display truncation during AS1; planning commit `b466a78`. No aid implementation, Job trial, metadata/payload acquisition or input-fit result occurred. A corrected host reporting path needs review before another bounded execution allocation. Prior probe evidence and source/metadata/native/licence/offline/parity/G2 gates remain unchanged. The metadata-only timing deferral is unchanged.

## Latest MR readiness — gaps remain

[MR evidence](../benchmarks/hub-metadata-dependency-review.md) records partial dependency/artifact/advisory findings. Native/pinned metadata/notices/offline gaps prevent installation readiness. Build-source mapping remains open for adoption under approved metadata-only timing deferral. No input-fit execution/adoption approved.

## Latest AR timing decision — approved for metadata review only

[AR findings](../benchmarks/stable-tokenizer-alternatives.md) record the user's2026-11-17 approval to defer build-source mapping only before metadata/notices/advisory/dependency review, retaining the gap for adoption. Next-package preparation is approved; its execution and source-dependent implementation/runtime adoption remain gated. No input-fit or tokenizer adoption is authorized.

## Latest source gate — epoch 03

Publisher origin is identified for the exact Hub artifact; build-source mapping remains open. [Current evidence](../benchmarks/hub-source-coordinate-review.md) preserves this distinction. No input-fit implementation, source-pin substitution or runtime adoption is authorized by this finding. Earlier entries below are historical.

# T17-IF — exact input-fit preflight design

## Evidence update — IF-SV conditional validation reference

[SV source review](../benchmarks/standalone-tokenizer-validation-design.md), approved proposal `68a878c`, identifies a directly owned exact bundled runner as a credible temporary reference for standalone counting. Shared source token helpers support the [staged trial design](standalone-tokenizer-parity-trial-design.md); installed artifacts, actual rendering/model parity, context/output/EOS and production identity binding remain unverified. No runtime count endpoint, custom build, dependency installation or trial adopted. Existing exact admission/R01/settings remain unchanged.

## Evidence update — IF-QC requires integration direction

[IF-QC source review](../benchmarks/input-fit-oracle-review-continuation.md), approved proposal `fa670fa`, identifies internal runtime token operations but no complete independently verifiable ownership/render/count/context/output contract for the present external controller. Dependency expansion skipped. A proposed owned-runtime bridge versus external handoff comparison needs a separate user decision; no runtime modification, installation or adapter adoption is implied. Existing exact-admission requirements and provisional settings remain unchanged.

## Evidence update — IF-P static data acquisition completed

[IF-P findings](../benchmarks/input-fit-remaining-assets.md), approved proposal `2533f27`, identify all ten remaining publisher data files with exact observed SHA256/size and matching Git blobs. Earlier artifacts were preserved, not reloaded. This closes the missing-file acquisition task only: no tokenizer/model execution, trustworthy counting oracle, runtime/native/dependency adoption or proof of input/output headroom. This contract, provisional limits and G2 boundary remain unchanged.

## Evidence update — IF-N partial static review

[IF-N findings](../benchmarks/input-fit-tokenizer-static-review.md), approved proposal commit `b8ebed3`, verify two wheel identities/RECORD metadata and oneQwen asset's observed SHA256/Git identity. A durable-accounting PermissionError stopped acquisition; no retry. Ten remaining assets, source/native/graph trust and actual rendering/token-count/usable-context/output reservation remain unverified. No candidate code was loaded and no preflight adapter is adopted; provisional limits unchanged.

## Evidence update — IF-M partial manifest and parity requirements

Approved proposal commit `6b67433` produced a [metadata review](../benchmarks/input-fit-tokenizer-manifest-review.md) and [validation matrix](input-fit-tokenizer-parity-validation.md). Historical publisher asset listings and candidate registry hashes are recorded, but Hub release/source-version reconciliation, exact acquisition bytes/graph/payload trust and a trustworthy runtime oracle remain blockers. No executable trial, dependency/runtime adoption or admission proof; this contract and provisional limits remain unchanged.

## Evidence update — IF-L comparison prepared

The [source review](../benchmarks/input-fit-adapter-source-review.md) and [adapter comparison](input-fit-adapter-comparison.md), under approved proposal commit `0a3a709`, distinguish public rendering from exact counting, special-token policies and owned internal operations. A standalone tokenizer candidate has registry provenance metadata, but asset/GGUF/rendering parity and output/EOS accounting remain unproved. Conditional direction recommendation awaits user decision; no adapter, dependency or runtime is adopted and this contract/provisional limits remain unchanged.

## Evidence update — IF-K completed

The [IF-K inspection](../benchmarks/metadata-identity-correction-results.md), approved under proposal commit `c4dff2d`, now verifies all nine selected public metadata files. Qwen has separate system/template layers with role/message/tool-related fields and im-start/im-end markers; Nomic parameters declare num_ctx8192. These facts inform an adapter-design comparison but do not prove actual rendering, prefix/tokenizer/special-token parity, effective context or192-token output reservation. Provisional settings and this draft contract remain unchanged; no adapter/internal-runner/model execution is adopted. Earlier IF-S incomplete-layer evidence below is historical where superseded by IF-K verification.

## Status and purpose

Draft for review, prepared after approval to commit the R1-W findings and proceed. Findings are committed as `197eb6e`. This document makes the proposed admission contract and next static investigation concrete; it does not select a tokenizer, grant internal-runner access or authorize implementation/inference. The [R1-W report](../benchmarks/public-source-web-review.md) is the evidence base. No additional public research was performed here; its closed allocation remains unchanged.

The intended user behavior is simple: before requesting an answer, establish that the question and the evidence actually supplied fit, with room left for the answer. If that cannot be established, explain the limitation instead of silently losing evidence. This supplements the provisional [R01 packing contract](../retrieval-design.md); it does not change its limits or reopen settled user decisions.

## Proposed admission contract

### 1. Freeze the request and identity

Capture the selected conversation/reference revision, extraction/index generation and supplied citation manifest. Build one immutable request containing mandatory policy/current question and complete optional history/evidence units. Freeze the model manifest, weight/config/template identity, runtime/runner identity, tokenizer policy, rendering path and effective context. A tag or unrelated tokenizer's vocabulary size is insufficient.

Count and generate from the same frozen request and settings. Any content, template, model, runner or context change invalidates admission. Rebuild and recount only within a separately defined finite attempt budget; never reuse an old successful result after a source-selection change. Recheck publication revisions using the already proposed transactional rule in [contracts](../contracts.md).

Use transient request identities/digests only for comparison inside the owned operation; this proposal adds no retained prompt log or content-bearing history snapshot. Diagnostic reports contain opaque operation IDs, counts, component versions and safe failure categories, not rendered prompts, token IDs or quotations.

### 2. Count the effective input, not a proxy

The adapter must count the exact rendered/tokenized sequence that the pinned runtime will consume, including role delimiters, policy, question, retained history, evidence labels/citations, assistant-generation prefix and applicable special tokens. It must identify the renderer/native-template path and special-token policy rather than assume the two are interchangeable. JSON byte length and rendered token length are separate measurements.

The result must report exact input tokens, effective context, identity binding, template/tokenizer policy version and whether any input was dropped or rewritten. Missing/unknown fields or an unverified identity yield unavailable, never a successful estimate. Do not infer fit from a response's evaluated count, a trailing marker, empty output or a byte/token ratio.

The proposed acceptance inequality is:

`exact input tokens + reserved output tokens + verified additional runtime overhead <= effective context tokens`

The provisional output ceiling remains **192 tokens**, and requested context remains **2,048 tokens**. Effective context is the verified usable context for the actual selected runner/model, not merely the requested value. Do not double-count template/special tokens already included in exact input. Conversely, do not assume additional overhead is zero: its meaning and bound must be established against the same execution path. Equality is acceptable only once the runner's reserved-slot/termination semantics have been verified. Output-budget/EOS accounting remains a validation item; no arbitrary safety margin or enlarged context is adopted here.

### 3. Reduce optional content in the approved order

Enforce the unchanged provisional byte guards as well as token admission: current question512 UTF-8 bytes, history at most two complete pairs/500 bytes, evidence2,000 bytes, whole serialized model input3,000 bytes and chunks at most800 bytes/top5. The exact serializer and its included delimiters/escaping must be frozen in the design; individual maxima are not additive allowances.

On a known overflow, discard the oldest complete history pair first, then the lowest-ranked complete evidence unit, preserving source-aware fragments/anchors. Re-render and recount after each change. With at most two history pairs and five evidence units, initial admission plus at most seven removals gives a proposed maximum of **eight candidate evaluations**. This is a deterministic future packing bound, not permission for eight inference calls. No retries of an unavailable adapter or background regeneration loop are proposed.

Never truncate the question, mandatory policy, a table value or quotation to force admission. Record retrieved versus supplied/omitted evidence separately. If mandatory content cannot fit, return a clear limit result. If no usable evidence remains, abstain without generation. If only part of a multi-source question can be supported, preserve the existing partial-answer/missing-evidence disclosure rule; fitting one source does not prove completeness.

### 4. Fail closed and check publication

Proposed internal outcomes are `FIT`, `TOO_LARGE`, `FIT_UNAVAILABLE`, `IDENTITY_CHANGED`, `SOURCE_CHANGED` and `CANCELLED`. Only `FIT` may proceed to generation. These are design labels, not newly implemented/public API codes.

Use `truncate=false` and `shift=false` as proposed defense-in-depth settings only after exact pinned behavior is validated. They do not replace counting or output reservation. A runtime error, unexpected truncation, identity drift or timeout must not publish a successful answer. A response stopped by the output limit is incomplete under R01. Publication still requires the existing atomic current-reference/generation check; a successful preflight does not resolve a later deletion race or establish semantic support.

## Adapter alternatives and decision gate

| Alternative | Potential benefit | Review cost / remaining evidence |
|---|---|---|
| Public supported count-only interface |Smallest coupling if one exists for the pinned version |R1-W did not establish one. No invented `/api/tokenize` endpoint or assumed zero-output-token semantics. |
| Exact local rendering plus matching tokenizer |Can count before generation and bind to the cached model |Requires a reviewed tokenizer artifact/implementation, exact special-token parity and a method to reproduce the actual runtime rendering path. No dependency selected. |
| Owned runner's internal template/tokenizer operations |Could use the same loaded model's tokenizer without another model package |Internal port/protocol coupling, process/address ownership, lifetime races, authentication/exposure, native loading and resource costs must be reviewed. No port scanning, arbitrary service attachment or direct internal call authorized. |
| Runtime modification/wrapper exposing a checked operation |Could return rendering/count/context together |Changes the evaluated runtime/build/provenance and expands maintenance/security work; do not hide this inside a helper. |
| Byte bounds plus truncation refusal |Useful resource guards |Not an exact input-count/output-reservation method; insufficient alone for the unchanged gate. |

**Recommendation:** inspect the cached public metadata and existing sealed source/provisioning inventories first, then compare the matching-tokenizer and owned-runner options in a concrete adapter decision. Prefer the smallest change that can prove parity. Keep the gate unresolved if neither option can do so. This draft does not authorize either option or imply a final architecture choice.

Embedding admission is separate: freeze Nomic's own identity/tokenizer/context, include the final `search_query:` or `search_document:` prefix and preserve `truncate=false`/768 dimensions. Chat token counts cannot validate an embedding request. No model/template/prefix change is proposed.

## Test-first acceptance specification for later implementation

These cases are specifications only; no tests were created or run for this draft.

| Case | Required result / evidence |
|---|---|
| Exact fit, one token over, effective context below requested |Correct boundary result with the verified output/overhead accounting; never rely on byte size alone |
| Short byte string with many tokens; escaped/non-ASCII content; special-token-like text |Same actual rendered token stream as the selected path; untrusted strings cannot bypass policy |
| History/evidence overflow |Oldest complete history then lowest-ranked complete evidence removed; no partial values/anchors; no more than eight candidates |
| Missing adapter, malformed count, timeout or identity drift |No generation; visible unavailable/changed result; no automatic fallback or retry |
| Same bytes but changed source revision; deletion between count and save |Admission invalidated or atomic publication rejected under the existing source-change contract |
| Mandatory content too large / no evidence / one required source omitted |Clear limit/abstention/partial-support outcome as applicable; no unsupported complete answer |
| Runtime defaults truncate or shift; output limit reached |Explicit safeguard behavior validated; incomplete output never reported as a complete success |
| Nomic prefixed boundary and model mismatch |Independent embedding check; reject wrong identity/prefix/context policy |

Routine implementation tests must fake the adapter/runtime and prove no generation on rejection. A later separately approved synthetic integration must establish actual template/special-token parity, context/output boundaries, no silent truncation, worker ownership/teardown, no runtime downloads/external traffic and measured CPU-only latency/memory. Neither fake success nor this design demonstrates those properties.

## Proposed next package: IF-S static artifact and adapter review

This exact investigation is **pending approval**. It uses existing local public model manifests/config/template metadata and authored inventories only; no user documents or saved prompt/answer/token output may be read into tools. It changes documentation only.

| ID | Objective and prerequisite | Acceptance / verification | Status |
|---|---|---|---|
| IF-S1 |After approval, freeze source/closed-meter and selected manifest/config/template identities |Fresh accounting/clock; checked owned paths and recorded hashes; safe metadata inventory, no model execution |Pending approval |
| IF-S2 |After S1, trace actual cached Qwen/Nomic rendering and special-token evidence from available metadata |Distinguish observed metadata, source inference and unavailable parity; byte serializer/output/overhead unknowns listed explicitly |Pending S1 |
| IF-S3 |After S2, compare concrete adapter dependencies/trust boundaries and remaining native freshness gaps |Purpose/alternatives/license/provenance/Windows/CPU/offline/resource unknowns; recommend a specific next decision or retain blocker; no silent selection |Pending S2 |
| IF-S4 |After S3 or partial stop, review and close |Dated design/evidence report, task/status updates, links/diff/preservation checks and separate results-commit request |Pending S3 |

Fixed candidates remain Ollama0.40.16/Qwen2.5:1.5b-instruct-q4_K_M/Nomicv1.5 and the exact hashes in the [committed inventory](../dependencies.md). Do not substitute a tag, pull a missing layer or parse native model weight payloads. Limit each JSON/template metadata file to64KiB and total inspected metadata to1MiB; check size before reading and reject unexpected types/links/outside-root targets. Large weights may be checked only against existing recorded hash evidence; no new weight parsing or tokenizer instantiation. Missing or oversized metadata produces a partial result.

Proposed allocation: fresh `data/t17/input-fit-static-01/`, **64 conservative local units** (48normal/16protected), **900 active seconds**, **2MiB combined authored/accounting output**, **zero web calls/downloads/installs/native loads/services/inference/fixture generation/new executable aids**. Prepay initialization8, metadata inspection12, design8, review12, close8 and protected16 before optional checks. Count orchestration/nested tools/shells/inspection executables and checks together. Git closeouts require separate approval and occur outside this investigation allocation. Persist clock/reservations before optional inspection; no refunds/reset/retry. At a limit or missing prerequisite, use protected capacity only for partial findings/preservation/closeout. No filesystem or outbound confinement is claimed for text inspection.

Likely outputs after approval: `docs/benchmarks/input-fit-static-review.md`, focused proposed contract/ADR/dependency cross-references where justified, and PLAN/TODO/README/checkpoint. Keep one detailed evidence report. No application code, tests, new parser/tokenizer, native helper or changed SPEC/AGENTS/lock is included. A native trial must receive its own exact artifacts, workload, privacy boundary and shared API/process/time/memory/disk limits after the adapter decision; do not pre-authorize that unknown package here.

## Review decisions

Review this draft contract and the IF-S investigation package. The settled product scope/resource targets are unchanged. The concrete tokenizer/adapter choice, exact special-token/output overhead and actual runtime privacy/compatibility remain unresolved until evidence supports a decision. Git approval for this five-document draft set is separate from IF-S approval and from later findings commits. G2 and the first CSV application implementation remain gated.

## IF-SA continuation 03 — static progress, runtime gate unchanged

[Findings](../benchmarks/standalone-tokenizer-static-verification.md) verify the archive/all 75 installed files and Tokenizers RECORD. Hub identity matched, but 191 entries exceeded 128; mandatory stop before further graph/source/native/offline review. Static equality does not prove effective runner/DLL loading, source-release provenance, rendering/token-ID parity, context/EOS or output reservation. Frozen parity/trial designs are unchanged; no candidate launch/install/G2. Recommend a separately approved Hub-only continuation.


## HS static evidence — source mapping remains a preflight gate

[HS findings](../benchmarks/hub-only-static-review.md) close the Hub wheel entry/RECORD gap: 191 entries and 190 payload hashes verified, metadata/one license read, no candidate import/execution. Final 18 tests/lint/format and owned-worker teardown passed. Public release source points to 3739729…; approved 178e1a… is not yet linked to release/wheel. Stop retained; no automatic pin correction, dependent graph expansion, native trial or runtime adoption. Static equality does not establish offline behavior, loader/source provenance, standalone/native parity, context/EOS or output headroom. Frozen trial designs remain unchanged.
