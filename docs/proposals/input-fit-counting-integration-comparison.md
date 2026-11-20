# T17-IF-CD — standalone counting and runtime integration comparison

## Status and evidence

The user approved the recommended standalone direction C and committing this comparison on 2026-11-16. This approves preparing the exact validation-design package, not runtime/dependency adoption, installation, a build or a trial. The comparison follows [IF-QC findings](../benchmarks/input-fit-oracle-review-continuation.md), committed `17e0e70`. Existing pinned evidence only: no additional web research, runtime allocation, code, installation, compilation, candidate import or model call.

The unresolved problem is obtaining an exact input count that matches the model state used for generation, together with its available context. A separate matching tokenizer can perform normal application counting; it does not inherently require replacing Ollama or using its internal tokenizer on every request. Ollama v0.40.16 has internal operations, but an independent validation reference and external ownership contract were not established. Acquired standalone assets alone do not prove generation special-token parity or answer headroom. The existing [preflight contract](input-fit-preflight-design.md) and frozen [parity design](input-fit-tokenizer-parity-validation.md) remain binding.

**User clarification:** the user asked why a separate tokenizer should not be used for future development. It remains a valid option and must not disappear merely because its validation oracle is unresolved. Distinguish the app's production counter from the independent reference needed to validate it. No direction, dependency or weaker admission rule is adopted by this clarification.

## Standalone route C — keep runtime counting modular

Use the pinned matching standalone tokenizer against the exact effective rendered input, with the verified model-specific preprocessing/special-token policy. Keep Ollama for generation and embeddings. Benefits: a reusable counting boundary, fake-testable packing logic and no inherent custom Ollama build for normal counting. A future model change still requires matching assets/policy and renewed validation; a tokenizer is not model-independent.

Current blockers: complete dependency/native/provenance/offline review, exact publisher-to-cached-model parity, rendering equivalence, independent actual-runtime validation and context/output semantics. Separate downloaded files do not close those gaps. A one-time bounded runtime reference may validate a standalone counter without becoming its per-request production dependency, but that reference and the frozen drift/identity requirements must first be demonstrated. No such trial or reference is ready here.

**Revised recommendation after the user's question: retain C as the preferred production direction, conditional on the existing exact-parity/admission gates.** First design the smallest independent validation route; investigate A/B only to the extent needed to obtain that reference or if C proves unsuitable. Do not commit to maintaining a custom runtime build merely to count tokens. This returns to the conditional standalone direction in [IF-L](input-fit-adapter-comparison.md), rather than silently selecting a different architecture.

## Comparison

| Criterion | A — narrow bridge in owned Ollama build | B — external Windows ownership handoff |
|---|---|---|
| Proposed integration |Private app-to-runtime bridge around the internal model/render/count/generate path |Controller obtains verified ownership information for the exact existing runtime child and its private operations |
| Existing evidence |Internal runtime interface has tokenization, context, PID/port and generation operations |Runtime owns a loopback child/port internally; no validated external handoff was established |
| Model lifetime |Design can require one retained model lease across admission and generation |Must prove child/socket identity and additionally bind the correct loaded model/options for the whole operation |
| Prompt fidelity |Can count after runtime rendering and generation-specific preprocessing |Must establish equivalence across separate public rendering/private tokenization/generation paths |
| Special tokens / context |Needs explicit mapping of each selected chat/embedding branch and output/EOS policy |Needs the same mapping; knowing a port or generic token count is insufficient |
| Local privacy |Private loopback interface, bounded transient state and no payload logs are proposed requirements |Same privacy requirements; process inspection must stay restricted to owned processes |
| Build and maintenance |New custom binary, reproducible Windows build, native provenance/notices/security review and update maintenance |Could preserve the current binary; private protocol and Windows ownership integration still need maintenance |
| New dependencies |Not determined; build toolchain/native inputs must be evaluated before provisioning |Not determined; no Windows inspection package is selected or authorized |
| Failure behavior |Unavailable on lease/identity/context mismatch; generation cannot reuse stale admission |Unavailable on ambiguous ownership, socket/PID reuse, model reload or policy uncertainty |
| Current readiness |Conceptual route; no build/API feasibility or resource evidence |Conceptual route; no trusted handoff or model-lifetime evidence |

A puts the missing count-to-generation contract beside the component already controlling the model. Its build/maintenance cost is material; do not describe it as a trivial endpoint or an already compatible patch. B remains an alternative if a constrained handoff can satisfy the same contract without process/port scanning or weakening identity checks. These are possible reference/integration mechanisms, not prerequisites already proven necessary for C. No claim that any route is impossible, secure, faster or lower-memory has been demonstrated.

## Proposed integrated bridge contract — only if that route is selected

The following describes A's stronger integrated mechanism. It is not a new requirement to put standalone counting inside Ollama. C must instead satisfy the existing frozen count/generation identity and parity contract through a demonstrated adapter design.

1. **Prepare:** accept only the approved text-only shape and selected model. Freeze evidence/request identity, actual model/runtime/template/config/tokenizer identities, effective context and generation settings. Acquire an exclusive or otherwise verified model lease. Reject cloud models, tools/media, unsupported branches and unknown policy.
2. **Measure:** use the effective rendered input after generation-specific preprocessing, including assistant prefix and actual special-token policy. Return exact input count, proven additional overhead/output reservation and effective context. Separate Nomic query/document prefix/normalization/CLS/SEP handling from chat. Token IDs/rendered prompts need not leave the runtime for normal application use.
3. **Admit:** apply the unchanged `input +192output + verified additional overhead <= effective context` rule. Equality is accepted only with verified reserved-slot/EOS semantics. Unknown fields are unavailable, never zero. Up to eight packing candidates are permitted; none initiates inference. Do not silently truncate evidence/history or shift context.
4. **Generate:** use a short-lived, one-use opaque admission handle bound to the exact prepared request and retained lease. Revalidate identities/settings and consume the handle atomically before inference; reject changed requests, replay, reload, expired/cancelled state or lost ownership. No output publication from a failed/stale admission. Proposed mechanism needs feasibility review; it is not a selected API or approved retention rule.
5. **Release:** cancellation, completion and failures release the lease/temporary state within a bounded cleanup deadline. Define lease lifetime, outstanding-state cap and crash behavior during the next design review; do not invent default values. Preserve90-second hard-answer target and source-publication checks. No durable prompt/token cache, telemetry or payload logs.

For either route, the browser must not access internal counting/runner operations. Existing app trust boundaries remain: localhost, validated host/origin, authenticated app-to-owned-runtime communication, bounded parsing and no arbitrary attachment. New endpoint authentication, capability expiry and resource limits need a concrete review before adoption; the bridge is not authorization to open an unauthenticated control interface.

## Why B needs more than a PID/port lookup

A retained process identity and verified socket owner can be necessary evidence but do not identify the loaded weights, renderer, special-token policy or future generation branch. A model reload or runner replacement must invalidate admission. B needs an explicit trusted handoff and a demonstrated way to keep those facts stable across public/private operations. Arbitrary port probing, scraping untrusted logs, attaching to an unrelated Ollama or treating post-generation counts as preflight proof remains excluded. No process inspection or private endpoint access was performed for this comparison.

## Decisions and smallest next work

The user must choose whether to retain standalone counting with validation design first (C, recommended), investigate a custom owned runtime build (A), investigate an external handoff first (B), or request another proposal. None approves a build, trial or installation. No requirement is silently relaxed to use byte counts, token estimates or returned usage as exact admission.

If C is chosen, prepare a bounded validation-design package that first identifies an independent effective-runtime reference and proves how it can validate the standalone counter without requiring a new production counting endpoint. Keep prior artifact findings and unresolved dependencies visible; do not install before that route is credible. If A is chosen, inspect pinned runtime scheduler/lease and generation integration points, Windows build inputs and upstream/native provenance. If B is chosen, inspect the trusted handoff/model-lifetime mechanism first; stop if it needs a runtime change. Prepare the exact package after direction choice, before research/execution. No approach may waive the existing parity requirements.

| Task | Objective / prerequisite | Acceptance / verification | Status |
|---|---|---|---|
| IF-CD1 |Compare standalone C and A/B from existing evidence |Production counting distinguished from validation reference; ownership/fidelity/build/privacy/resource uncertainty explicit |Completed as document review |
| IF-CD2 |Define common proposed contract |Prepare/measure/admit/generate/release, replay/drift/failure boundaries and unresolved limits documented |Completed as draft, not adopted |
| IF-CD3 |Obtain direction decision after CD1/2 |User approved recommended C on2026-11-16; exact follow-up package to be prepared for separate approval |Direction approved; no runtime adoption |

Later implementation must be test-first, with fake admission/lease/replay/identity/cancellation controls before any separately approved native parity trial. Preserve all prior parity cases and exact-artifact/resource/offline/teardown gates. Do not infer native compatibility or performance from source design. G2 remains open; no CSV product code or stage transition authorized. Existing16GB CPU-only/PDF-XLSX-CSV/OCR/privacy/provisional settings and chart deferral remain unchanged.
