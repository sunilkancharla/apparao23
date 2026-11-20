# T17-IF-QC — counting reference needs an integration decision

## Outcome — 2026-11-16

Approved [continuation](../proposals/input-fit-oracle-review-continuation.md), proposal commit `fa670fa`. Corrected bootstrap persisted UTC clock,64prepaid units, research counters and a conservative reporting reservation before inspection/output. Thirty prior identities were frozen before research. **A complete trustworthy counting reference remains unestablished for the present external-controller design.** This is a bounded source-review verdict, not proof that Ollama can never support one.

Research ended at **five calls/twenty targets**, including two404source paths. Six calls/twenty-four targets were reserved and not refunded. No remaining call was used after the decision; conditional dependency review was skipped. No downloads outside public web-text retrieval, installation, candidate import, service/model/API/inference or runtime modification. G2/application gates remain open.

## Pinned evidence and unresolved contract

All source references below use Ollama `v0.40.16`. Source observations do not verify the cached executable's bundled native implementation or exact model parity.

| Evidence | Observation | Consequence |
|---|---|---|
| [llm/server.go](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/llm/server.go), `LlamaServer`, `NewLlamaServer` |Internal interface includes tokenization, PID/port and context operations; requested context may be clamped |Internal capability is not an external controller contract |
| [llm/llama_server.go](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/llm/llama_server.go), `tokenize`, `Tokenize`, `completionPromptForRequest` |Internal tokenization accepts a special-token flag; exposed Go method passes false, while completion preparation can pass true |Counting policy must match effective generation, including any BOS handling |
| Same source, `startLlamaServer`, `GetPort` |Ollama owns a child and its selected loopback port |No validated handoff to this project's Python controller was established |
| Same source, `Embedding` |Embedding response supplies usage/count observations after evaluation |Useful later validation evidence, insufficient pre-admission proof |
| [server/routes.go](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/server/routes.go), route registration and `DebugRenderOnly` branches |Reviewed public routes lack a registered token-count interface; debug branches return rendered text/image count |Rendered text alone does not establish token IDs, count, usable context or reserved answer space |
| Same source, embedding `adjustTokenLimit` / `inputTokensAndContext` |Embedding admission adjusts context using model metadata and boundary tokens |Separate prefix/normalization/special-token parity remains necessary |
| [server/prompt.go](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/server/prompt.go), `chatPrompt` |Optional truncation uses rendered input and the tokenizer to choose retained messages |The app must preserve selected evidence/history and separately prove answer headroom |

The literal debug JSON key was absent from routes.go; checking the typed `DebugRenderOnly` field confirmed the behavior. This was a lookup distinction, not evidence that debug rendering disappeared. Two former runner paths returned404; neither was retried or replaced by a different runtime version. Medium web responses sometimes expanded into extensive source context; no long response was requested or raw source echoed through shell reporting. Web-provider envelopes were explicitly outside the controlled-stdout byte claim.

Unresolved requirements for a later counting integration: a trusted runtime-to-controller ownership/lifetime handoff; exact effective rendered token sequence for the fixed chat branch and separate embedding branch; identity binding to the actual cached weights/config/template/native runtime; effective context and192output/EOS accounting; no silent truncation/context shift or count-to-generation drift. None was assigned an invented default. Post-generation counts and standalone-tokenizer agreement do not close these gaps.

## Alternatives requiring a user decision

| Direction | Benefit | Cost / remaining proof |
|---|---|---|
| **A. Design a narrow counting bridge inside an owned, pinned Ollama build** |Can bind rendering/tokenization/context and subsequent generation to the same internal model ownership |Requires an explicitly approved runtime change/build, provenance/license/native review and maintenance. No ready implementation or safety guarantee claimed |
| B. Design an external Windows ownership handoff to the existing owned child |Could preserve the current executable |No trusted handoff is established; it must avoid arbitrary port/log scanning and prove PID/birth/socket/model lifetime. Private-protocol and token-policy gaps remain |
| C. Reconsider the exact admission architecture/requirement |Could enable a different approach |Needs a concrete alternative and explicit architecture/requirement approval; byte caps or post-generation counts cannot silently replace exact admission |

**Recommend A for the next bounded design comparison**, because it makes the missing contract explicit at the point that already owns the model. This recommends design only, not selecting a fork, installing tools, compiling, modifying Ollama, changing its version or adopting a bridge. Compare B before committing to a build; if neither has acceptable maintenance/resource cost, return C to the user. Do not continue standalone-tokenizer dependency expansion until this direction is resolved.

A future design must retain all existing parity negatives: special-token/Unicode/delimiter cases, independent effective-runtime token reference, separate Nomic prefixes/CLS/SEP, below/equal/above capacity with output reservation, identity/restart drift, truncation/shift refusal and cancellation/source-publication checks. The frozen [parity design](../proposals/input-fit-tokenizer-parity-validation.md) remains unchanged. No native parity trial was prepared or authorized here.

## Task closure and evidence limits

- **QC1 completed:** Accounting before output;30entry preservation hashes; no full inspection dump. DateTimeOffset UTC used.
- **QC2 completed as bounded review, unresolved:** Source-cited contract gaps and alternatives established within five calls/twenty targets. No independent reference approved or empirically validated.
- **QC3 skipped by the approved decision rule:** Dependency/native/advisory/provenance gaps remain unchanged.
- **QC4 completed as decision handoff:** Findings/status/checkpoint and final preservation/link/diff/accounting receipts saved; separate findings commit approval required.

Controlled shell output uses4096-byte conservative reservations before emission, measured summaries and captured native checks. Initial4096reservation also covers the approved proposal Git output; later Git actions remain separate. After research and verification, an optional diff-display command had a PowerShell quoting error before its body/precharge ran. No file/research action ran in that command. Its short parser diagnostic was not measured/precharged by that invocation; an additional4096conservative reservation was recorded during closure. This is a reporting-order deviation, despite no observed byte-cap overrun; do not claim complete reporting-policy compliance. Optional work ended without rerunning that display; the complete readable tracked diff had already been saved locally. No helper/process/model teardown was needed. Existing closed epochs were not reopened or modified. No routine tests/Ruff for this documentation-only review; final check counts/time/artifact/reporting totals live in `data/t17/input-fit-oracle-review-02/closeout.json`. Units retain full64reservation, including unused/protected capacity; no refunds.

All software/data remain local except public-source web retrieval. The unchanged Windows11/16GB CPU-only target, PDF/XLSX/CSV/OCR/privacy requirements, provisional2,048context/192output/R01 limits, chart deferral and stage boundary remain binding. No runtime adoption or usable application capability is claimed.
