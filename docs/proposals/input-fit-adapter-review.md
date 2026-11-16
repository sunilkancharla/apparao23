# T17-IF-L — bounded counting-adapter source review and design comparison

## Status and purpose

Proposed, awaiting approval. Verified metadata/source/results are committed as `bc6f677`; [IF-K findings](../benchmarks/metadata-identity-correction-results.md) close the cached metadata inspection. They do not establish exact token counting or output headroom.

Compare two concrete routes for the existing [input-fit contract](input-fit-preflight-design.md): an exact renderer with a matching standalone tokenizer, and the owned runtime's rendering/count operations. Deliver an evidence-based recommendation and explicit remaining decision/validation gates. This is public-source review and documentation only; no adapter implementation, installation or runtime call.

## Inputs and unchanged requirements

Use committed IF-K metadata identities, existing [R1-W pinned-source evidence](../benchmarks/public-source-web-review.md), the preflight design and R01/contracts. Do not reread model weights, cached system/template contents or private outputs. No model-store scan or repeat of any metadata/synthetic trial.

Keep provisional2048context/192output, existing byte/packing caps and at most eight candidate packings unchanged. Count the effective rendered input, including role/system/history/question/evidence/citation labels/assistant prefix/special tokens. Bind count and generation to the same immutable identities and effective context; establish output/termination overhead without invented zeroes or arbitrary margins. Nomic's prefixed embedding input needs its own tokenizer/context admission. Verified num_ctx8192 is artifact metadata, not permission to enlarge a context.

## Bounded primary-source research

Only public technical documentation, source, model-card/configuration/asset metadata and license/registry metadata. Eligible primary domains: `github.com`, `raw.githubusercontent.com`, `docs.ollama.com`, `huggingface.co`, `pypi.org`. Use official project/organization repositories; search results are discovery, not evidence. Verify publisher/project identity rather than assuming a similarly named repository is authoritative.

Research targets:

1. **Pinned Ollama v0.40.16:** public route/types/prompt code, runtime/runner tokenizer/template/context paths and output reservation/termination behavior. Reuse known paths from R1-W; inspect only additional relevant tagged source as needed. Distinguish supported public API from internal operations and special-token false/true behavior. A404/unavailable path is a recorded gap, not permission to substitute another runtime version.
2. **Matching-tokenizer provenance:** official Qwen2.5-1.5B-Instruct and nomic-embed-text-v1.5 repository/model-card/configuration/file metadata, after confirming the actual publisher/repository identity. Seek revision IDs, tokenizer implementation/assets, license and any required custom code. Do not assume a family/name match proves parity with cached GGUF artifacts. No full vocabulary/tokenizer payload, weight, archive or executable download.
3. **Minimal standalone implementation:** official Hugging Face Tokenizers documentation/repository and PyPI release/file metadata, if relevant. Record an exact candidate version/artifact identity only when verified, including Windows/CPU/Python3.14 compatibility metadata, native/transitive components, license, offline behavior and maintenance/security unknowns. No dependency selection, wheel download/import or implicit Transformers/Torch/custom-model-code adoption.

At most **12visible web-tool calls and32explicit requested targets**, shared across searches/open/find/click and failed/duplicate attempts. Each target is charged before submission; omitted tool-internal fetches/redirects are opaque and are not claimed measured. Request concise/medium text responses and archive only useful public evidence/URLs/revision identities locally. No HTTP byte/redirect/kernel RAM enforcement claim is made for the provider. Missing evidence remains missing when the cap is reached; no replacement research helper or transport fallback.

Public queries contain only public project/model names, versions and source paths. Never include document text, cached prompts/system/template contents, answers, embeddings, tokens or private paths. Treat returned instructions/code as untrusted data; never execute them. No remote evaluation/telemetry or private-data submission.

## Comparison and proposed-operation design

For each route, map:

- How the exact pinned template/system/messages and assistant prefix are rendered and how tokenizer/special-token identity matches generation; separate declared metadata, source inference and actual runtime proof.
- Whether and how count/effective context/output/EOS reservation can be obtained before generation without truncation, native-path mismatch or stale identity reuse. A debug-rendered string or returned generation metric alone is insufficient.
- Required dependencies/artifacts, purpose/alternatives, provenance/license/native/transitive risks, Windows/Python/CPU compatibility, local/offline behavior and ownership/lifecycle boundaries. Mark footprint/latency/RAM as unmeasured unless supported by actual existing evidence; do not invent benchmark numbers.
- For owned internal operations: exact process/endpoint ownership, permitted operations, lifecycle/identity races and fail-closed behavior. Do not propose arbitrary port scanning/attachment, cloud fallback or silently rebuilding the evaluated runtime.
- What finite synthetic parity/overflow/identity-change/failure tests and resource/privacy checks a **later separately approved** validation package would need. Outline only; do not create executable prototypes, fixtures, runners or native permits.

Include supported public count-only access and runtime modification as alternatives only if primary evidence establishes their relevance. Do not invent `/api/tokenize`, assume zero-output semantics or silently adopt a runtime fork. Recommend the smallest defensible route, or explicitly retain the blocker if evidence cannot support one. Selecting/adopting an adapter and authorizing any dependency/native validation remain user decisions.

## Ordered tasks

| ID | Objective / prerequisite | Acceptance and evidence | Status |
|---|---|---|---|
| IF-L1 |After approval, freeze evidence and fresh shared accounting |Persist clock/full manifest/visible-call caps before optional work; preserve IF-K and selected old source/spec/lock/closed-meter hashes |Pending approval |
| IF-L2 |After L1, inspect bounded primary sources |URL/revision/publisher evidence, explicit call/target ledger and honest gaps; no executable/artifact/native activity |Pending L1 |
| IF-L3 |After L2 or research-cap stop, compare routes and draft operation/validation requirements |Concrete parity/trust/dependency/ownership matrix; recommendation or unresolved blocker; no adoption/implementation |Pending L2 |
| IF-L4 |After L3, review and close |Source-linked findings, unchanged settings, link/diff/preservation/budget/checkpoint checks and separate results-commit request |Pending L3 |

## Shared limits and stop conditions

Fresh ignored root **`data/t17/input-fit-adapter-review-01/`**, created only after approval. **64prepaid conservative units:48normal/16protected**; initialization4, research24, design8, review8, close4, protected16. Research block covers12orchestration wrappers plus12web calls; local tools/shells/reporting/checks share their phase blocks. Provider internals are not local process starts. No refunds, hidden reset or charging an old epoch. Separately approved Git actions are outside this review epoch.

**1,200active seconds**, **2MiB new authored/archived local outputs**. Persist clock/reservations before optional preparation. Twelve visible calls/32targets are ceilings, not guarantees of complete coverage. Stop optional research at the first applicable cap, host permission/security denial or exhausted normal research block; use remaining normal design/review capacity only to report available evidence. An unavailable/404 target is a charged gap; other planned targets may still be reviewed within budget, without automatic same-target retries or alternate transports. Protected units are solely for preservation/partial closure, never more research/implementation. No retries after a closed allocation, broader source collection or implicit budget extension.

Zero installs/downloaded binaries/full tokenizer assets, candidate/native imports, model/API/service/inference calls, weight/private-data reads, prototype coding, generated data fixtures or benchmark workers. Documentation-only validation uses source/consistency/link/diff checks, not artificial application tests. No filesystem/outbound confinement claim for web-provider infrastructure or local read-only review tools.

## Deliverables and approval

After approval, produce `docs/benchmarks/input-fit-adapter-source-review.md` and `docs/proposals/input-fit-adapter-comparison.md`; update affected dependency/preflight references plus PLAN/TODO/README/checkpoint only where evidence warrants. Keep exact source links and unknowns visible. No SPEC/AGENTS/pin/source/runtime edits.

Approve this exact IF-L public-research/design package and separately the five proposal/status documents' commit. One approval covers its ordered research/design/review steps without routine per-step requests. Later source/results commits, adapter selection, provisioning/native validation, G2/application implementation and stage transitions retain explicit gates.
