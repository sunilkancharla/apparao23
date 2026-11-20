# T17-IF-M — exact tokenizer parity validation requirements

## State

Design delivered under approved IF-M, proposal commit `6b67433`. [Manifest findings](../benchmarks/input-fit-tokenizer-manifest-review.md) are partial: Hub source/release reconciliation, exact asset/distribution bytes and dependency graph remain unresolved. **This is not an executable trial package or permission to acquire/install/load anything.** Standalone direction approval is conditional on the proof below; G2 remains open.

## Prerequisites before proposing execution

1. Reconcile Hub2.4.0's advertised publishing commit with its2.4.0.dev0 source version and final wheel dependency metadata. Freeze a complete compatible graph and exact Windows regular-Python3.14 artifacts. Any alternative version, dependency omission or vendor modification requires an explicit decision.
2. Freeze publisher revisions, minimum asset names, exact sizes and independently verified SHA256 values. Review wheel payload/RECORD, source-to-build provenance, native libraries/crates, licenses/notices and reachable advisories. Specify bounded acquisition and how downloaded bytes are verified before parsing/loading. Current registry hashes/listing sizes are insufficient clearance.
3. Specify local-only loading/import behavior and data directory, with no Hub/network fetch, telemetry, repository code or source build. Measure footprint separately; wheel size is not installed size or RAM.
4. Establish a trustworthy token/rendering oracle for the selected cached GGUF and actual runtime generation/embedding branch. Debug-rendered text, returned counts after generation or two standalone tokenizers agreeing do not by themselves establish admission correctness. If no oracle can be justified, report unavailable and request a direction decision; no internal port scanning/fork fallback.
5. Prepare one explicit synthetic-only execution package with exact owned executable/model/asset/source digests, request settings, endpoints/process ownership and teardown, finite positive/negative/control counts, one shared meter and time/memory/output limits. No script-policy bypass or arbitrary endpoint attachment. No executable permit is created by these requirements.

## Test-first fake contract matrix

| ID | Case | Required invariant / evidence |
|---|---|---|
| FP01 |Missing/malformed count, context, overhead, or identity |Admission unavailable; no invented zero/margin or generation fallback |
| FP02 |Immutable source/request identity |Same selected-source generation, model, weights, config, template, runtime, tokenizer, rendering settings and context held across render/count/generate/publication |
| FP03 |Optional-content packing |At most8candidate packings; remove oldest complete history pairs then lowest-ranked evidence; preserve mandatory policy/question and disclose omissions |
| FP04 |Mandatory overflow / eight candidates exhausted |Clear refusal/qualification without inference retry or hidden truncation |
| FP05 |Below/equal/above capacity |Use input+192output+verified additional overhead<=effective context; equality needs independently proven reserved-slot/EOS semantics |
| FP06 |Source/runtime/model/tokenizer drift and restart |Invalidate admission; stale count cannot authorize a changed request or source publication |
| FP07 |Cancellation, timeout and malformed oracle result |Stop owned work, bound cleanup and preserve accurate status; no answer publication after cancellation |
| FP08 |Unsupported tools/media and unrelated references |Reject unsupported rendering branches and preserve retrieval scope; no silent path switch |

Use injected deterministic fake boundaries and meaningful failing tests first. Include a mutation proving rejection/identity/reservation guards matter. These tests verify the contract, not native tokenizer parity or feasibility.

## Later native parity matrix — execution not authorized

| ID | Synthetic cases | Required oracle and pass condition |
|---|---|---|
| NP01 |ASCII, Unicode, combining marks, emoji, CR/LF, tabs, leading/trailing whitespace |Pinned standalone and trusted cached-model tokenizer agree on exact IDs/counts for the same effective text/policy; no tolerance percentage |
| NP02 |Chat delimiter strings as untrusted question/evidence content |Special-token interpretation matches actual generation; literal marker text cannot bypass source/policy boundaries |
| NP03 |Missing/explicit system, one user turn, complete history pairs, evidence/citation labels |Runtime rendering equals actual consumed sequence including mandatory system and assistant prefix; publisher Jinja template not substituted |
| NP04 |Automatic special tokens on/off, BOS/EOS and generation branch |Document exact branch/policy/extra slots without double counting; branch mismatch blocks adoption |
| NP05 |Nomic mixed case, whitespace, search_query/search_document prefixes, CLS/SEP |Separate embedding oracle validates normalization, prefix and special-token accounting against actual embedding input; no chat-tokenizer reuse |
| NP06 |Just below, exactly at and above usable capacity, mandatory overflow |No silent truncation/context shift; independently verified192-output/termination reservation and effective-context clamp semantics |
| NP07 |Identity/source change, unload/reload, cancellation and unavailable oracle |Fail closed before generation/publication; same owned runtime lifetime and selected-source generation verified |
| NP08 |Disconnected cold/warm loading and complete answer path |No required external traffic or asset fetch; record loading/count/render/whole-answer latency, total owned memory and available RAM |

Every native oracle/negative/control/generation/cleanup call must have an explicit count in the later shared budget. This matrix deliberately does not invent an API or call count before the oracle/interface is established. No weight reload or eight-inference interpretation of the packing limit.

## Unchanged targets and publication gate

Provisional2,048context/192output and R01 byte caps remain unchanged. Original Windows11/16GB/CPU-only target, one heavy job,30-second warm complete answer,90-second hard answer,8GiB owned total and4GiB available remain validation goals. Record exact assets/settings, cold/warm samples and complete-process memory pressure; disconnected behavior and strict target feasibility require actual evidence. Do not convert a metadata review or a larger-RAM result into target acceptance.

Adoption requires all prerequisite/contract/native parity cases plus documented exceptions decided by the user. Any mismatch, missing oracle, cleanup uncertainty or resource/privacy failure blocks adoption. Review findings and exact dependency/runtime choice separately before G2/application implementation. Results commits and stage transitions retain their explicit gates.
