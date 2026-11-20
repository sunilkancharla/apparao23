# T17-IF-SV — standalone tokenizer validation design

## Status and question

Proposed; package execution and five-document proposal commit await approval. The user approved standalone direction C in the [integration comparison](input-fit-counting-integration-comparison.md), committed `aae897e`. Production counting should remain separate from Ollama if exact compatibility can be demonstrated. No dependency/runtime adoption, installation or native execution follows from direction approval.

**New, specific question:** can the exact unmodified native runner bundled with the pinned Ollama release serve as a temporary, directly owned validation reference, without a new production counting endpoint or custom build? Existing evidence shows Ollama internally launching a native runner and using its tokenization interface; it does not establish direct-launch compatibility, packaged provenance or complete effective-generation parity. Investigate those gaps instead of repeating the public-API search already closed in IF-QC.

This is a source/document-only package. It must yield a concrete validation design or an explicit blocked verdict, not a native trial. No binaries/models/tokenizer assets are acquired, inspected locally, launched or loaded here.

## Fixed evidence and research boundaries

Use Ollama `v0.40.16`, the previously identified chat/embedding models and publisher tokenizer revisions, existing Tokenizers0.23.3/Hub2.4.0 findings, [IF-QC evidence](../benchmarks/input-fit-oracle-review-continuation.md) and the frozen [parity contract](input-fit-tokenizer-parity-validation.md). No version substitution or reopening closed epochs. Keep the standalone graph/native/license/source-release gaps visible; this package does not close them or select additional dependencies.

Read pinned primary runtime source, its build/package configuration and exactly referenced native source revisions. Upstream moving main/master documentation cannot prove the bundled binary's behavior. A missing pinned native revision/build mapping is a blocker, not permission to pick a newer upstream runner. Public repository/release metadata only through web tools; no payload downloads, raw HTTP fallback, registry resolution command or source archive.

Investigate these questions in order:

1. Identify the packaged native-runner source/build mapping and supported direct-launch/tokenization operations for that exact runtime. Separate source intent, release provenance and future local binary identity verification. Do not claim they are interchangeable.
2. Specify a directly owned test-reference lifecycle: exact binary/model identities, explicit loopback binding/port ownership, isolated approved state, no attach/scan/log scraping, no automatic model fetch and bounded teardown. This would be a future evaluation tool, not replacing Ollama for production generation or counting.
3. Trace tokenization through the selected real chat/embedding generation paths. Specify reference observations for exact effective rendering/preprocessing/special-token policy, normalization, Nomic prefixes and context/output/EOS. An accessible `/tokenize` endpoint alone is insufficient. Do not claim a full token sequence if the actual path exposes only counts.
4. Determine whether a future synthetic trial can validate the standalone adapter against the same effective native implementation without concurrent heavy workloads or an unbounded second model load. Frozen byte identities do not automatically solve count/generation drift; state the binding checks and remaining proof. Keep resource limits as proposed validation targets, not tested capacity.

## Ordered tasks and acceptance

| ID | Objective / prerequisite | Acceptance and evidence | Status |
|---|---|---|---|
| IF-SV1 |After approval, bootstrap before inspection/output |Exclusive fresh root, UTC clock/full accounting/research/reporting reservations and frozen hashes durable first |Pending approval |
| IF-SV2 |After SV1, establish reference feasibility |Pinned file/symbol/revision evidence for direct reference provenance, launch/ownership and effective token path, or explicit missing-link verdict |Pending SV1 |
| IF-SV3 |Only if SV2 supports a credible route, specify later trial |Named artifact-verification prerequisites, standalone dependency gates, synthetic cases/negative controls, shared resource/call/teardown boundaries and acceptance matrix; no trial execution |Pending SV2 |
| IF-SV4 |After SV2 stop or SV3, close |Feasible/blocked/unknown report, unchanged prior identities, links/diff/accounting/checkpoint and user decision; separate findings commit |Pending SV2/SV3 |

Stop source expansion once a necessary direct-reference/provenance link is unsupported. Return the exact missing evidence and alternatives; do not use remaining budget to investigate custom builds or install unrelated tokenizer packages. A source-supported design still requires separate exact-artifact review/provisioning and native parity approval.

## Required future validation matrix — design only

Preserve FP01–08/NP01–08 in the frozen parity design. Cover chat versus embedding separately; ASCII/Unicode/whitespace/delimiter and explicit special-token input; exact system/history/evidence/citation/assistant-prefix sequence; Nomic query/document prefixes/CLS/SEP; below/equal/above context with192output reservation; effective context clamp, truncation/shift, mismatch/unavailable/restart/drift/cancellation/replay/source-publication failures. No percentage tolerance for an exact-count adapter. Independent effective-runtime reference is mandatory; post-generation usage alone or two standalone implementations agreeing is insufficient.

Test-first fake admission/packing/identity/error checks precede a separately approved native trial. Installed/native footprint, offline behavior and RAM/latency remain unmeasured. A future trial package must name exact verified artifacts and budgets before any installation/import/API/model call. No automatic custom-build fallback or weakened byte-estimate admission.

## Shared package limits — after approval only

Fresh ignored root `data/t17/standalone-validation-design-01/`; refuse if present. **64prepaid conservative units:48normal/16protected**: initialization8, source review20, design/reporting/closeout20, protected16. Include all shells/wrappers/interpreters/negative/check/report/cleanup operations, no refunds/resets. Separately approved Git actions are outside the epoch.

**1,200active seconds /2MiB new artifacts; eight web calls /twenty-four targets**, maximum four targets/call, short/medium responses. Charge each failed/cache-miss target and every search/open/find/click before dispatch. No native process, helper/test creation, fixture generation, local model/binary inspection or hashing, candidate imports/install/download/build/global/PATH changes. No application tests/Ruff for documentation-only work.

First invocation must create and flush full accounting/reporting records before optional inspection or controlled stdout. Use literal PowerShell, DateTimeOffset UTC, explicit scalar projection and ReadAllText. Use simple single-quoted status messages; do not construct optional diff-display commands with nested quote/newline interpolation. Capture native warnings/stderr and report checked summaries. **8KiB/invocation /64KiB aggregate controlled output,8KiB protected reserve**, measured including newline and precharged durably. Keep an explicit conservative allowance for bootstrap/Git/error output; any output escaping precharge is a deviation, not retrospective compliance. Web/provider envelopes are opaque, separately limited by call/target/response settings; record excessive responses honestly. No filesystem/outbound confinement or kernel RAM-cap claim.

Freeze AGENTS/SPEC/pyproject/lock, the integration comparison, IF-L comparison, frozen parity design, IF-N/O/P source/test pairs and findings, IF-Q/QC findings and each named old final meter/closeout; IF-N pending/stopped meter, IF-P combined manifest and IF-QC preservation/research/reporting evidence. Existing IF-QC reporting charges are in meter.json, not a fabricated per-call journal. Preserve transitive links, no model asset copies/weight hashes. Reverify direct identities at closure. Unexpected I/O/host denial/report failure, identity conflict, cap/deadline or unsupported necessary link stops optional work; protected capacity is closure only.

## Deliverables and approval

After approval, author `docs/benchmarks/standalone-tokenizer-validation-design.md`, a trial design only if credible, local preservation/research/accounting receipts and affected dependency/preflight/PLAN/TODO/README/checkpoint updates. Leave frozen earlier reports/parity unchanged. No executable handoff, runtime adoption or G2/application implementation. Keep unchanged16GB CPU-only/PDF-XLSX-CSV/OCR/privacy/provisional2,048context192output/R01 and chart deferral.

Requested: approve IF-SV1–SV4 within these exact source/design limits and separately commit this proposal plus PLAN/TODO/README/checkpoint (five files). Necessary routine steps inside the approved package need no further task-start permission. Later findings commits, installation/native execution/build/adoption remain gated.
