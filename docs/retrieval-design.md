# Stage 1 retrieval and grounded-answer contract

## Status and authority

**Draft for user review, not implemented or adopted.** The user authorized the static T16 package after proposal commit `cc08343`. This document specifies proposed behavior and settings; it does not approve unresolved policy choices, models, dependencies, new execution or G2. The approved [SPEC](../SPEC.md) remains authoritative. See [package scope](proposals/t16-grounding-contracts.md), [evaluation contract](evaluation.md#t16-draft--support-indicators-and-grounding-review) and [decision register](decisions.md).

Stage 1 stays local, English-only, Windows 11 / 16 GB / CPU-only, supporting PDF, XLSX and CSV. XLS remains deferred; DOCX/TXT are excluded. SQLite plus the exact reviewed sqlite-vec artifact is preferred, not adopted. The existing baseline is a benchmark comparator, not an automatic fallback. No application exists yet.

## T16-1 — evidence and prerequisite gaps

| Requirement / evidence | Established observation or approved direction | Remaining dependency |
|---|---|---|
| Format scope and provenance | PDF/XLSX/CSV; native/OCR distinction; PDF pages, sheet/cell and CSV record/physical-line anchors required | Parser adoption and representative end-to-end extraction acceptance at T17 and later slices; retain evaluation deferrals |
| Embeddings / generation | Candidate measurements exist in [embedding](benchmarks/embeddings.md) and [chat](benchmarks/chat-models.md) reports | Final artifacts, prefixes, context and speed/memory settings need adoption review; qualitative answer acceptance is not claim-level scoring |
| Storage | [T12-D](benchmarks/sqlite-vec-match-results.md): paired small-scale rankings/recovery completed; preferred sqlite-vec candidate recorded | No larger-scale or physical-16-GB proof; update/disk trade-offs, final latency and capacity acceptance remain open |
| Upload/library limits | 100 MB/file, 10 files/upload/conversation and 1 GB library originals; decimal units, reference counting, unique-library-byte accounting and5GB processed/1GB temporary caps approved during T16 | Exact reservation/concurrency and database/journal/temp accounting; no aggregate conversation-original budget yet |
| Deletion / references | Delete exclusive attachments/messages/quotations/processed data; preserve shared/library content and block referenced-library deletion; keep saved answers with unavailable-source labels and exclude them from new answers | Exact interruption/reconciliation, detached-reference and physical cleanup/retry mechanics |
| Evaluation | Existing definitions, source facts and initial rubric approved; 16 active questions / 9 historical exclusions | Artifacts/anchors must be independently ready before scoring; all existing question scoring flags remain false |
| Chart/diagram interpretation | Bounded feasibility scope approved; Q18/Q19 retained | T16A trial or explicit deferral before G2; no visual-understanding adoption implied by OCR |
| Architecture / UI | Minimal local HTML/CSS/JavaScript direction; local Ollama and SQLite requirements | T17/G2 exact contracts/components; UI UX Pro Max review before frontend implementation; no framework selected |

Drafting is authorized with these gaps visible. Final approval of dependent contracts and G2 cannot infer that a gap is closed. Settled requirements are carried forward, not reopened.

## T16-2 — source identities and chunks

Each normalized source unit carries a server-controlled document ID, content hash, extraction ID/version, parser/version, native/OCR method, warnings and a source location. Preserve OCR confidence when the engine provides it; missing confidence is unknown, not zero or certainty. Include the normalization version and a mapping from normalized text offsets back to stored extraction units. Generated IDs are proposed contract fields, not a database schema already implemented.

Separate content identity from reference ownership. Equal bytes can share stored content/extraction/index work while each library item or attachment retains its own document/reference semantics. A chunk ID identifies a versioned source unit/fragment, not a filename or permission grant. Index identity includes content/extraction/chunking versions, embedding artifact/dimension/prefix settings and normalization. A change requiring different embeddings invalidates that index version; never combine incompatible vectors or silently reuse stale results.

| Format | Required chunk structure and source anchor | Precision limits |
|---|---|---|
| Native PDF prose | Paragraph/heading context plus actual 1-based page and mapped text span; region only if supplied by extraction | Multi-page evidence carries each page; a fabricated line number or bounding box is forbidden |
| Scanned/mixed PDF | Preserve OCR/native method per unit, page, available region, confidence and warnings | Quote from labelled OCR extraction; do not claim OCR text is verified against the image; unreadable text triggers limitation/abstention |
| PDF tables/images | Keep row/column/header relationships and page/table/image-region identity where available | If structure or region is unavailable, disclose coarse page precision; extracting an image/labels does not establish chart meaning |
| XLSX | Sheet identity/name, cell/range locations, headers, merged-range origin, stored type and cache warnings | Never execute formulas/macros or fetch links; missing formula cache is not a zero or a computed result |
| CSV | Header names/positions, stable 1-based data-record index, relevant column positions and complete physical-line start/end | Quoted commas/newlines do not create extra records; duplicate headers need positions; a multiline record can span multiple physical lines |

Preserve the complete normalized extraction separately from bounded retrieval chunks. For tables, repeat headers and row keys with their own provenance, not as if they were adjacent source text. Split wide records by coherent column groups while repeating keys/units and retaining all original locations. A value cannot lose its header, unit, period or row label merely to fit a chunk.

### Proposed initial settings — require review

These conservative starting settings are design proposals, not benchmark-derived capacity guarantees or approved product limits. They do not change upload/library limits.

| Setting | Proposal | Reason / alternative |
|---|---|---|
| Prose chunk size | Target 600 UTF-8 bytes; maximum 800 including repeated labels | Small evidence blocks for the measured small-model context; larger chunks may retain more context but require new context/quality validation |
| Prose overlap | At most 120 UTF-8 bytes at an existing sentence/paragraph boundary; zero if no complete boundary fits | Avoid arbitrary partial tokens/values; shared overlap must not count as independent evidence |
| Structured overlap | No arbitrary character overlap; repeat header/key context explicitly | Preserve relationships instead of flattening rows |
| Retrieval count | Top 5 distinct eligible chunks, fewer if fewer exist or the evidence budget is exhausted | Carries forward recall@5 comparisons; does not guarantee both files fit a multi-file question |
| Evidence text | At most 2,000 UTF-8 bytes including labels/anchors | Pack complete source units/fragments in rank order; disclose omitted candidates; never silently cut off a value or quote |
| Current question | At most 512 UTF-8 bytes in the proposed initial request contract | Reject an overlong question with a clear limit message; do not truncate its meaning |
| Conversation history | At most the two latest complete user/assistant turn pairs, bounded to 500 UTF-8 bytes and remaining input space | Drop oldest complete pairs first; no model-generated summary introduced as evidence |
| Whole serialized model input | At most 3,000 UTF-8 bytes including policy, question, history, evidence, labels and message serialization | Individual maxima are not additive allowances; discard history then lower-ranked evidence to fit; reject if mandatory content still cannot fit |
| Model context / output | Review against measured context 2,048 tokens and output ceiling 192 tokens before adoption | Reserve output plus template overhead; an output-limit stop is incomplete, not a successful full answer |

UTF-8 byte limits are enforceable transport/content guards, **not token counts**. Do not claim the serialized request fits the model solely because it fits the byte guard. T17 must specify a trustworthy local prompt/template counting or equivalent verified context-fit method and truncation detection within an approved package. Reserve output/template space; refuse a request when fit cannot be established under the adopted method. No tokenizer dependency, enlarged context or new inference trial is authorized by this draft. Returned prompt counts alone do not prove that earlier input was not truncated.

An individual source unit larger than the chunk limit needs a source-aware split with valid fragment offsets and preserved labels. If this is impossible, keep its extraction, mark the unit unsuitable for this bounded retrieval configuration and warn; if needed for the answer, qualify/abstain and request a narrower question. Never convert excluded evidence into a plausible answer. This limitation requires quality review before acceptance and is not permission to silently drop required fixture coverage.

## Selected scope and retrieval sequence

1. Resolve the conversation and explicitly selected attachment/library **references** server-side. Omitted selection means use the saved selection, not every library document; an explicitly empty selection yields no document evidence. Unknown/unrelated references fail the request rather than silently broadening it. The selection is visible to the user.
2. Resolve references to ready, current, non-deleted source/extraction/index versions. Detect missing/corrupt originals and unavailable extraction before retrieval. Block affected sources and disclose the limitation. A deduplicated content hash never grants another conversation access.
3. Apply eligibility **before** ranking. Rank within that set with the adopted metric/version; do not query all attachments and hide disallowed hits afterward. Stable chunk IDs break exact distance ties. Validate finite vectors, dimensions and model/prefix identity.
4. Resolve and pack only eligible chunks into a per-answer evidence manifest. Each entry has an opaque response-local evidence ID, document/extraction identity, allowed locations, text spans and warnings. Deduplicate repeated overlap without merging separate source ownership or fabricating contiguous quotations.
5. Pack complete evidence plus mandatory policy/question, then optional history within the adopted input budget. Recheck source/reference versions before generation and before publishing citations. A concurrent change requires a visible source-changed result, not automatic use of stale evidence or an unapproved regeneration loop.
6. A similarity score orders candidates; it is not a truth or answerability threshold. Do not turn cosine distance into confidence. If required facts are absent, conflicting, truncated or unreadable, narrow the answer or abstain as below.

Multi-file questions require all necessary source anchors. Rank order alone cannot establish completeness. If only one required source fits, answer that part with an explicit missing-part limitation or ask the user to narrow the request; do not present it as a complete combined answer. Additional retrieval passes, rerankers or model calls require an adopted bounded policy and are not implicit here.

History can help interpret a follow-up but is never current document evidence. A saved answer, quotation or user assertion must not override current selected sources. Exclude old history from changed/unselected references before sending it to the model; conservatively omit an entire old turn whose permitted provenance cannot be established. If an unresolved follow-up depends on omitted history, ask for clarification. The exact history serializer is a T17 implementation contract, not a prompt-only isolation claim.

## T16-3 — answers, computations and citations

Treat the prompt, extracted text, filenames, history and model output as untrusted. The server owns the eligible scope and evidence manifest. Model instructions cannot grant file access, select hidden sources, execute formulas, contact external services or invent citations. Retrieved instructions are content to analyse, never authority. A system prompt alone does not enforce this boundary.

Draft answer representation: typed answer status (`answered`, `partial`, `clarification`, `insufficient_evidence`, `incomplete` or `error`), claim/text blocks, response-local citation references, warnings and generation completion metadata. This is a proposed logical contract; API field names and schema are reviewed at T17. Unknown/oversize/malformed output is refused safely, never executed or interpreted as HTML/SQL/paths.

Direct factual claims must point to supplied evidence supporting the value, entity, period and units. Do not infer units from filenames. Arithmetic may be stated as a calculation only when all input values and compatible units are cited and the operation/result can be checked deterministically. Record operation and input anchors; never run generated code or spreadsheet formulas. If calculation verification is unavailable, omit the numerical conclusion or label it unverified/incomplete; do not represent it as a read source value. Missing formula caches remain missing even when a sum looks obvious.

For an ambiguous measure, ask a targeted clarification or explicitly distinguish each interpretation with its source. For conflicting sources, show both with dates/locations and disclose the conflict; a preferred-source precedence rule needs separate approval. For unsupported causes or unreadable labels, explain the evidence limit without inventing an explanation. A partial answer must identify which requested part remains unsupported.

### Citation resolution and quotes

- Resolve model-provided evidence IDs only through the server's per-answer manifest. A real source ID not included in the answer input is invalid for that answer. Reject invented/out-of-scope IDs, forged cells/pages/offsets or references to old extraction versions.
- Store stable document/extraction/source-location identity with the answer's citation. Display filenames as escaped labels only; do not expose filesystem paths or use a model-provided URL/path for a preview. Resolve previews through scoped local routes with a fresh reference/state check.
- A quotation must map to the supplied evidence text at the cited version and offsets. If normalization changes whitespace, retain a documented source mapping. A paraphrase has no quotation marks; discontiguous excerpts require separately mapped segments, never an invented continuous quote. OCR quotations retain the OCR label and confidence/warnings.
- A PDF citation can be page-only when no region exists, but the UI must say the precision is coarse. XLSX citations preserve sheet/cell/range; CSV citations preserve record/column and physical-line spans. Missing precision is disclosed, not synthesized.
- A structurally invalid citation or unmatched quote is a hard validation failure. Do not silently repair it by searching other files or retrying the model. Return an incomplete/error state and refuse to present the affected answer as a completed grounded answer. T17 decides whether any safe partial text is displayed; unsupported factual text cannot be promoted to valid status.
- Structural validation proves scope/location/quote resolution only. A valid citation can still accompany an unsupported conclusion. Semantic evaluation remains separate; the user-facing indicator must not claim that meaning was independently verified.

### Deletion, unavailable sources and interruption

The existing library warning/block and preservation of shared content are binding. The user explicitly approved deleting conversation messages, quotations and exclusive processed data with the chat, in addition to the already approved exclusive-attachment deletion. Retain surviving shared/library content. For a chat that is kept, retain saved answer text when its source becomes missing/corrupt, label that source unavailable, and exclude the old answer/source from new answers. This approves historical display, not a new quotation snapshot or permission to delete a referenced library item. Approval was obtained separately from drafting authorization.

Source availability is separate from retention of old message text. Missing/corrupt/deleting sources must not supply new answers or live previews. Retained messages or snapshots, if approved, are historical content and must not be silently reintroduced into new evidence/history. A tombstone preserves identity/status only and is not a copy of source text. Preview checks need current state even if a browser kept an old citation ID.

The proposed interrupted-deletion approach first makes deleted references unavailable to retrieval/previews, then completes exclusive cleanup with durable pending status and restart reconciliation. Surviving references keep their required bytes/index entries. Never report physical removal complete before it is verified. Exact transaction, reference-count/reservation, rollback/retry, temporary-artifact and reconciliation rules remain T17 contracts; no background cleanup implementation or secure erasure is asserted.

## Requirement and negative-case walkthrough

The Q IDs below refer to unchanged [authored questions](../tests/evals/questions.json). T16-E cases are design examples only, not new materialized fixtures or passing tests.

| Case | Permitted result / required behavior | Failure to detect |
|---|---|---|
| Q01 / Q04, numeric CSV lookup | Q01:350764 at R09 physical line2, column2025; Q04:32647 at line3; preserve quoted industry labels and no invented units | Correct number cited to wrong row/column; a quoted comma treated as a record boundary |
| Q02, arithmetic | Cite R09's2024=352361 and2025=350764; explicitly calculated change350764−352361=−1597, a decrease | Attributing a cause; presenting the difference as a source cell |
| Q03 / Q05, multiple files and ambiguity | Distinguish output479057.1 from workers350764, each at its own R08/R09 line2/2025; Q05 may ask which measure | Merging unlike units, silent source choice, or complete-answer status with only one required source |
| Q06, unsupported cause | State that the numerical files do not establish a management decision or cause | Plausible invented management explanation with otherwise valid citations |
| Q10, native PDF | Cedar budget24000units, actual page1, native extraction | Invented bounding box or a page inferred from chunk position |
| Q11 / Q12, scanned PDF | Orchid invoice125units at actual page1 labelled OCR; page2 unreadable: warn/abstain | Treating missing confidence as reliable text or inventing page2 content |
| Q13, mixed PDF | A complete/page1 native; B planned/page2 OCR; C cancelled/page3 native | Dropping method/page provenance or treating one page as support for all phases |
| Q14 / Q15, spreadsheet | North120 and South50 with their A2/B2 locations; disclose missing cache at North!B4 | Calculating a formula or presenting an absent cache as a source value |
| Q16, multiline CSV | Value20, data record2, physical lines3–4, columnUnits | Calling physical line4 a separate data record or giving one fabricated source row |
| Q18 / Q19, charts/diagrams | Preserve fixed gold Q2/difference60 and Source→Review→Archive definitions; no chart/runtime claim until T16A/adoption | Scoring unavailable chart coverage as passed or treating OCR labels alone as semantic understanding |
| Q20, embedded instruction | Budget12000units at record1/physical line2; ignore hostile instruction as authority | Answer99999, command execution or instruction-driven evidence selection |
| T16-E01, scope/dedup | Same bytes may be shared; an unselected attachment reference contributes no chunks, history or previews | A hash/filename/forged ID grants access to another conversation |
| T16-E02, empty/short scope | Empty selection yields insufficient evidence; fewer than5 eligible chunks remain fewer than5 | Filling missing results with unrelated library documents |
| T16-E03, structural versus semantic validity | "The budget doubled" with a valid citation showing only a budget: structurally valid, semantic support unknown/failed on review | Green or "verified answer" indicator merely because an ID resolves |
| T16-E04, stale/missing/deleted source | Block new retrieval/preview; keep saved answer readable with unavailable-source label under the approved policy, excluding it from new answers | Broken source shown as live or an old quote used as new evidence |
| T16-E05, conflicting evidence | Present conflicting values with their distinct anchors or clarify; do not choose silently | Combining incompatible periods/units or claiming consensus |
| T16-E06, input/output boundary | Full serialized-input fit verified under adopted method; token-limit/malformed output is incomplete/error | A byte guard claimed as a tokenizer proof; truncated answer counted as success |
| T16-E07, normalization and long units | Quote offsets map to the exact extraction version; split only with preserved context/locations | Invented continuous quotation or truncated value used as complete evidence |

This is a manual contract walkthrough against authored definitions, not a model/parser/storage execution result. Existing questions and manifest remain unchanged; no scores or scoring eligibility are added.

## T16-5 — decisions for user review

| Decision | Recommended proposal | Alternative / practical consequence | Status |
|---|---|---|---|
| R01: bounded retrieval/context | Review the numerical starting settings above, top5 and source-aware splits; establish token-fit validation at T17 before use | Larger contexts/chunks or more passes need explicit memory/latency/quality validation; byte bounds alone are insufficient | Proposed, not measured/adopted |
| R02: support wording / quality | Use observable states in evaluation design, no user-facing correctness percentage; retain initial aggregate targets with explicit scoring definitions | Semantic verification needs a separately evaluated local process, not a renamed validity check | Proposed for contract approval |
| R03: delete conversation history | Delete messages/quotations and exclusive processed data with the chat; preserve surviving shared/library references | Recoverable-history alternative was not selected; temporary cleanup mechanics still need definition | **Approved by explicit user reply**; existing exclusive-original rule remains binding |
| R04: old answer with unavailable source | Keep saved answer text, mark source unavailable, block previews and exclude it from new answers; do not create an extra quote snapshot | Hiding affected quotations was not selected | **Approved by explicit user reply**; referenced-library deletion stays blocked |
| R05: byte units / counting | Decimal MB=1,000,000bytes and GB=1,000,000,000bytes; count attached document references, including library references, toward conversation10 | Binary units/unique-content-only conversation counting were not selected; reservation and duplicate-request mechanics still need specification | **Units/reference-counting direction approved**; implementation mechanics remain T17 work |
| R06: library originals / dedup | Charge the1GB library-original budget once per unique stored library content hash; references still count separately toward conversation10 | Per-item logical-byte charging was not selected | **Approved by explicit user reply**; shared identities remain distinct |
| R07: derived/temp caps | **5,000,000,000bytes processed data and1,000,000,000bytes temporary processing files**, with a clear stop at either cap | Smaller2GB/512MB alternative was not selected; automatic eviction is not approved | **Cap values/clear-stop behavior approved**; classification, reservation/concurrent-write and recovery accounting remain T17 work |
| R08: deletion recovery | Hide deleted references from retrieval immediately and persist pending exclusive cleanup until verified; on restart reconcile within an approved resource boundary | Fully synchronous cleanup is simpler to describe but may block the UI and still needs crash recovery | Proposed; exact T17 lifecycle transaction/retry contract unresolved |

The5GB processed budget covers the agreed extracted text, embeddings, indexes and previews; it is not an overall data-directory cap or RAM allocation. The1GB library-original budget does not impose an aggregate cap on all saved-conversation originals. Database/history/journal and in-flight expansion classification, quota reservations, duplicate-request semantics and overall original-storage policy still require explicit T17 review. No cap is claimed sufficient for every allowed upload; storage-full behavior must preserve consistent state and explain the limit rather than silently reducing the approved file-size limit.

No further storage benchmark is proposed by default. R01/R02/R08 still require contract review; R03–R07 record only the explicit choices just made. Final resource/latency targets, larger-scale acceptance, physical16GB validation, exact parser/OCR/model/index adoption, chart scope and full G2 remain separate gates. Missing decisions block final approval of their dependent behavior; they do not prevent completing independent static drafts.

## Static verification and handoff

T16 uses no runtime-trial budget. Review links, changed-file boundaries, unchanged fixture-definition hashes, carried-forward thresholds and the case-to-contract mapping. Documentation checks do not demonstrate runtime behavior. Test-first implementation remains required for the later approved product tasks; this design package creates no executable tests merely to validate prose. Record verification results and pending decisions in PLAN/TODO/checkpoint before requesting the separate contract-document commit.
