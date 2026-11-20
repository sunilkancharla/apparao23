# T17-IF-LFC — local-file tokenizer comparison

## Status and conclusion

ALN results were committed as **`fc0d8f5`**. The user approved that commit and preparation of this comparison. This document uses retained evidence only: no public query, new execution root, candidate payload read, installation, import, model call or application implementation. The approved conditional standalone-tokenizer direction is preserved.

**Local-file loading and dependency removal are different decisions.** The saved inspection of the exact Tokenizers 0.23.3 Windows wheel declares `huggingface-hub>=0.16.4,<3.0` as a base requirement. Calling only a local-file loader does not remove that requirement. This is already established by the [static findings](../benchmarks/standalone-tokenizer-static-verification.md); another source-search package is unnecessary to establish that restriction.

The retained [RRC dependency review](../benchmarks/remaining-artifact-readiness-continuation.md) includes HF-Xet in the selected Hub 2.4.0 Windows closure. A locally unused download feature is not permission to omit a declared dependency. No claim is made that a local-file API imports or executes every installed dependency; that call path remains unverified here.

## Options

| Option | What changes | Dependency consequence | Evidence / decision needed |
| --- | --- | --- | --- |
| **A — local-file loading with the complete declared dependency set** | Counting would read only pre-acquired, identity-checked local tokenizer assets; Ollama remains responsible for generation/embeddings | Retain required Hub/HF-Xet and other applicable dependencies for the selected baseline; no package-footprint reduction established | Exact loader/import/offline behaviour, native compatibility, notices/build gaps and runtime parity remain unverified. Recommended for preparation of a trial-only proposal, not installation or adoption. |
| B — same wheel, omit Hub/HF-Xet because their features are unused | Force an incomplete installation or alter dependency metadata | Conflicts with the retained declared graph; feature non-use does not establish a supported dependency-free distribution | Not recommended or authorized. No `--no-deps`, metadata editing, stub modules, repackaging or import-error suppression is proposed. |
| C — a different publisher-supported release/distribution | Investigate whether another exact official artifact has a smaller valid required graph and suitable local-file behaviour | Reduction is possible only if its actual metadata/implementation demonstrates it; no such candidate was established here | Requires a separate bounded candidate/artifact review and user decision. No downgrade, fork, new package or source pin is selected by this comparison. |
| D — retain the hold | No tokenizer candidate provisioned | Existing environment remains as recorded | Avoids unresolved execution exposure but delays parity/input-fit work and the CSV flow. It does not solve exact counting. |

**Recommendation:** choose A for **preparation of a concrete trial-only proposal**, while keeping unconditional installation/runtime adoption on hold. The smaller design is a local-only loading boundary, not a promise of a smaller installed dependency graph. Option C is appropriate only if reducing installed dependencies is a stronger priority than retaining the current research baseline; that priority has not been decided.

The current baseline observations remain Tokenizers **0.23.3**, Hub **2.4.0** and HF-Xet **1.8.0**, with their existing saved artifact identities. They are not newly approved defaults. Repeated older-release searches without a specific candidate/benefit are not recommended. The existing Python/project constraints and applicable full graph must still be reconciled before any installation proposal.

## Proposed local-only boundary, not an implemented API

The future loader would accept configured local paths to approved tokenizer assets, verify their identities and fail clearly on a missing/mismatched asset. It would not accept a repository/model identifier, remote URL, dynamic code, automatic download or cloud fallback. Its public and native import/load paths still require source and later runtime validation; this document does not claim that an API already meets this contract.

Loading a tokenizer is only one part of exact input counting. Keep the [approved counting direction](input-fit-counting-integration-comparison.md), [frozen parity requirements](input-fit-tokenizer-parity-validation.md) and [staged trial design](standalone-tokenizer-parity-trial-design.md):

- Count the exact effective rendered input with the correct model-specific preprocessing, assistant prefix and special-token policy. Chat and embedding prefixes/normalization/boundary rules require separate checks.
- Preserve the existing context/output/headroom, packing, identity/drift and fail-closed rules. Local files, byte estimates or post-generation usage alone cannot establish correct preflight admission.
- Validate against the exact retained Ollama/native reference identities and compatibility overlays; no arbitrary upstream binary, private-port discovery, custom runtime build or newly invented model default.
- Preserve Windows 11/16 GB/CPU-only, one heavy workload at a time, the approved validation targets and owned-process teardown. Source design is not evidence of memory fit, speed, offline operation or parity.

The existing staged design remains a draft, not a runnable trial allocation. Any loader adapter or controller implementation must use test-first synthetic controls and review before a separately approved native run.

## Remaining evidence and the next approval

The [ALN findings](../benchmarks/artifact-licence-notice-review.md) clarify Apache-2.0 source terms and verify the retained HF-Xet notice text. They do not establish complete bundled native/vendor notices or an independently reproduced wheel/build-source mapping. Hub/FSSpec source conditions retain their approved metadata-only timing deferral. None is waived by using local files.

If A is selected, prepare **one concrete trial-only proposal** that:

1. Names the exact candidate artifacts, complete required graph, existing local assets and source/API prerequisites. Distinguishes satisfied prerequisites from the precise unresolved evidence.
2. States any requested trial-specific residual-risk exception in plain terms: what is missing, which exact installation/native actions it would permit, and what remains blocked before adoption. Approval of this comparison or of proposal preparation is not that exception.
3. Defines project-venv-only provisioning with `uv`, no global/PATH changes, no startup downloads, synthetic local-only inputs, actual host/execution privacy boundary, shared budgets, owned teardown, stop conditions and complete response/report capture. Carry the ALN reporting-reserve failure into the controller design; do not merely copy the previous allowance and claim enforcement.
4. Carries every required parity/negative/regression case, exact-runtime reference and resource check into one shared allocation. Do not repeat completed archive/graph/source reviews unless a changed input or unresolved prerequisite justifies it.
5. Ends with measured evidence and a separate runtime-adoption/G2 decision. Neither a successful trial nor trial-only acceptance automatically adopts the component or advances the stage.

That proposal may conclude that execution is not yet supportable; it must not manufacture readiness to obtain approval. No runnable handoff, acquisition, dependency modification, source query or trial is authorized now. If the user prefers C or D, record that direction before dependent preparation. No new runtime limits, retention behaviour or product scope are set here.

## Work completed under this documentation approval

| ID | Objective / prerequisite | Acceptance / evidence | Status |
| --- | --- | --- | --- |
| LFC1 | Inspect retained artifact, dependency and counting evidence after ALN commit | Mandatory Hub requirement distinguished from features/imports; old results remain read-only | Completed: saved metadata/static/RRC/ALN reports |
| LFC2 | Compare supported local-file baseline, unsupported omission, alternative artifact and hold after LFC1 | Benefits, costs and unknowns explicit; no dependency-removal or offline claim | Completed: options table |
| LFC3 | Preserve counting/validation contract and define next proposal requirements after LFC2 | Local-only boundary, exact-runtime parity and named residual gaps retained; no executable trial permission | Completed as design documentation |
| LFC4 | Review comparison and obtain next direction after LFC3 | Four-document consistency/identity/link/whitespace/diff/index checks; user chooses next preparation and separately approves commit | Documentation ready; user decision/commit pending |

Only this comparison, PLAN, TODO and README change. No ADR accepts a new architecture because no new architecture is adopted. Historical reports/proposals/roots, AGENTS/SPEC/project/lock, evaluation source/manifests, historical checkpoints and unrelated user files remain unchanged. No session-checkpoint file is created.

**Requested decision:** approve the four-file comparison commit and preparation of option A's exact trial-only proposal, or choose C/D. This is a documentation/next-package decision; it does not approve installation, a licence-risk exception, native execution, runtime adoption or a stage transition.
