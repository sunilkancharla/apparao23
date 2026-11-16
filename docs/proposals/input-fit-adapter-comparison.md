# T17-IF-L — counting-adapter comparison and proposed validation contract

## Recommendation and approval boundary

**Prefer investigating runtime-rendered text with a pinned matching standalone tokenizer.** This avoids independently recreating the cached Go template while keeping internal runner ports out of the proposed application interface. It remains conditional on exact token/special-token parity with the evaluated generation path. Neither route is selected/adopted, installed or executed by this document. [Primary-source evidence and candidate identities](../benchmarks/input-fit-adapter-source-review.md).

The existing [input-fit design](input-fit-preflight-design.md) remains binding: unchanged provisional2048context/192output, R01 byte limits, frozen count/generation identities, bounded optional-content removal, separate Nomic admission and fail-closed unknowns. No user requirement or context budget changes are proposed.

## Concrete route comparison

| Dimension | Runtime-rendered text + matching standalone tokenizer | Owned runtime internal operations |
|---|---|---|
| Rendering |Obtain the exact text through the verified owned-runtime rendering path; do not substitute a repository Jinja template or handwritten role concatenation |Use the selected runtime's own renderer/template operations, with explicit branch identity |
| Tokenization |Pin tokenizer implementation/assets and prove normalization/special-token/token-ID parity with the selected cached model |Reuse the loaded model's tokenizer, but count with the exact generation special-token policy; internal Tokenize alone is insufficient |
| Interface |Existing rendering behavior remains a debug/version-coupled interface; it is not a count-only API or proven load-free call |Requires a new trusted controller-to-runner endpoint handoff; no demonstrated external integration currently exists |
| Dependencies |Native tokenizer extension, hub transitive dependency and two model-specific asset sets; none approved |No additional standalone tokenizer necessarily needed, but existing runtime/native trust and tighter private-protocol coupling remain |
| Identity/lifetime |Freeze runtime/model/template/serializer/tokenizer/context/settings between render/count/generate |Also hold the same owned child/socket lifetime; any reload/rebind/runner change invalidates admission |
| CPU/RAM/disk |Registry wheel size is metadata only; installed/transitive/assets footprint and contention are unmeasured |Loaded-runtime cost and count/render overhead are unmeasured; no lower-RAM claim |
| Offline/privacy |Pinned local files only; prohibit runtime hub fetching/telemetry; verify behavior |Only identity-verified loopback operations; prohibit cloud/management forwarding and arbitrary attachment |
| Current blocker |Exact asset/GGUF and renderer/generation parity unproved |Endpoint ownership/access plus renderer/special-token parity unproved |

Supported public count-only access remains unestablished. Runtime modification is a separate build/provenance/maintenance choice; it is not an implied fallback. Byte caps/truncation errors and returned post-generation counts remain useful safeguards/observations rather than admission proof.

## Proposed operation boundary — design only

1. Freeze selected-source revision, evidence manifest, complete message units, model/weight/config/template/runtime identities, rendering branch/settings, tokenizer implementation/assets and effective context. Accept only the already allowed text-only request shape; reject unsupported tools/media rather than silently taking another rendering path.
2. Render using that frozen request and obtain the exact effective sequence, including mandatory system policy and assistant prefix. Keep rendered text transient/local. A debug string must be shown equivalent to what generation consumes; otherwise return unavailable.
3. Count with the verified matching tokenizer/special-token policy. Return count, usable context, proven additional overhead/termination accounting and the same identity bundle. Do not log rendered prompts/token IDs or treat missing values as zero.
4. Apply `input +192output + verified additional overhead <= effective context`, avoiding double counting. Equality requires reserved-slot/EOS proof. At most eight existing packing candidates; oldest complete history first, then lowest-ranked evidence. Unknown count/identity/ownership is unavailable, not permission for another adapter or inference retry.
5. Revalidate the unchanged bundle and selected-source generation before generation/publication. Explicit truncation/shift defenses require tested pinned behavior. Preserve abstention, partial-evidence disclosure, cancellation,90-second hard-answer target and current-source publication rules.

For embeddings, freeze the correct Nomic tokenizer/normalization/special tokens and final prefixed query/document input separately; do not use chat counts, omit prefix tokens, or adopt8192as a new application limit.

## Later validation requirements — no execution authorized

Any future package must first name exact asset revisions/digests, binary/native/transitive artifacts/licenses/advisories, local-only loading APIs and permitted operations. It must set a fresh shared budget for all positive/negative/cleanup work, with host/process/resource/privacy boundaries and stop rules before any install or model call.

Use test-first fake admission/packing/identity/error controls before a separately approved synthetic native parity trial. Include ASCII/Unicode/whitespace, chat delimiters embedded as untrusted text, missing/explicit system text, complete history pairs, evidence/citation labels, assistant prefix, same rendered bytes under different special-token policies, and Nomic case/prefix/CLS/SEP behavior. Counts/token IDs must agree with the proven effective generation/embedding path, not merely another tokenizer's own output. Any mismatch blocks adoption; no percentage tolerance for an exact-count adapter.

Boundary cases must cover just-below/equal/above effective capacity with output/EOS reservations, no truncation/shift, mandatory overflow, multi-source omission, eight-candidate exhaustion, malformed/unavailable results, source/runtime/model/template/tokenizer changes, cancellation and restart/reload. If the internal route is later selected, add owned-process birth/socket identity, port reuse, lifetime handoff and cleanup uncertainty; never use global scans or user-supplied endpoint attachment as proof.

Measure cold/warm render/count/whole-answer latency and owned app/Ollama/native total memory/free headroom on the unchanged16GB CPU-only target. Existing one-heavy-job/30-second warm/90-second hard/8GiB-owned/4GiB-free targets remain acceptance goals, not results. Separately verify disconnected local operation with zero asset fetches/required external traffic. No new benchmark numbers are asserted here.

## Decisions requested after review

Accept the standalone-tokenizer direction **for preparing an exact artifact/dependency/parity package**, or choose the internal route and require its ownership handoff design first. A direction decision does not approve Tokenizers0.23.3, its hub dependency/assets, installation, runtime calls, native trials or G2. The identified candidate/version and gaps remain in the linked evidence report. Results-document commit approval is separate.
