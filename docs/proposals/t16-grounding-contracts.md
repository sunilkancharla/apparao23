# T16 — evidence, citations and support-indicator design package

## Status and purpose

**Static package completed after review:** drafts committed `486fd1b`. The user explicitly retained R01 as a provisional validation baseline and approved R02 indicator/R08 recovery design, completing review alongside prior R03–R07 choices. The [review outcome](../retrieval-design.md#static-review-outcome-after-draft-commit486fd1b) records clarifications of packing metrics, error precedence and durable cleanup/publication ordering. T16-1–6 are complete as static design/review only. T17/G2, token-fit and multi-file validation, chart gate, final resource/adoption and detailed accounting/recovery mechanics remain open. Review-update commit requires separate approval. Earlier pending-review wording below is historical.

**Authorized for static drafting:** after proposal commit `cc08343`, the user said "please proceed". T16-1–4 drafts are now prepared in [retrieval design](../retrieval-design.md) and [evaluation design](../evaluation.md#t16-draft--support-indicators-and-grounding-review). T16-5 review and final T16-6 closeout await the user's policy/contract decisions; checkpoint and review material are ready. No settings, retention policy, runtime component or G2 adoption is approved merely by authorization to draft. Earlier proposed/requested-approval wording below describes the original package review.

**Policy replies recorded:** the user separately approved chat-message/quotation/exclusive-processed-data deletion, keeping unavailable-source historical answers with a label/exclusion from new answers, decimal units/reference/unique-library-byte accounting and5GB processed/1GB temporary caps with a clear stop. These are synchronized into SPEC, decision register and retrieval choices R03–R07. Only those explicit requirements were added to SPEC; no unapproved contract settings were promoted. T16-5 review remains open for R01/R02/R08 and T17 mechanics. Nine draft/status files, including the necessary SPEC clarification, await a new commit decision; proposal commit `cc08343` does not cover them. No new execution scope was added.

Proposed for review, documentation only. The user approved proceeding with the suggested sequence and recording sqlite-vec as the preferred candidate. This document makes the next package concrete; it does not claim final storage adoption, new benchmark permission, G2 approval or approval of unresolved retention policies.

Storage results are committed as `18be917`. The preferred candidate is SQLite metadata/history with the exact reviewed sqlite-vec0.1.9 Windows artifact for vector search, retaining its pinned companion notices and provenance limitations. The plain SQLite/Python approach remains the measured comparator, not an automatic runtime fallback. See [results](../benchmarks/sqlite-vec-match-results.md) and [decision register](../decisions.md).

T16 will specify how retrieved evidence becomes a supported answer. It will define source locations, selected-reference scope, context limits, abstention, citation checks and honest support indicators before application implementation. Windows11,16GB,CPU-only and PDF/XLSX/CSV remain unchanged; XLS is deferred and DOCX/TXT excluded.

## Prerequisites and remaining gates

Use the approved SPEC, T02/T02R definitions/rubric, existing parser/OCR/model/storage reports and the explicit evaluation deferrals. Preserve missing coverage rather than marking the full upstream tasks complete. Full T12 acceptance, physical16GB validation, representative scale, final performance targets and D01/D04 details remain open.

The existing T16 checklist has upstream acceptance and D04/D06 prerequisites. This package proposes **drafting contracts with an explicit gap register while those final decisions remain open**; it does not waive those prerequisites for final contract approval or G2. Any dependent behavior remains labelled proposed or blocked. T16A chart feasibility or its explicit deferral still precedes T17 adoption. No chart-understanding guarantee follows from OCR.

## Fixed outputs and execution boundary

Primary outputs: new `docs/retrieval-design.md`, a focused T16 section in existing `docs/evaluation.md`, and, only if necessary, additive safe authored definitions in `tests/evals/questions.json`. Preserve existing IDs, facts, source anchors, excluded cases and scoring flags; use new IDs for any new cases. Never rewrite expected facts to fit observed model behavior. Do not open supplied originals or raw native trial outputs in connected tools; work from safe authored definitions and sanitized reports.

Supporting updates: root PLAN/TODO, decision register, README and session checkpoint. No application/evaluation executable code, fixture materialization, database schema/migration, native loading, parser/model/OCR run, model/server/API call, dependency change, installation, download or outbound research is included. No new native allocation or trial epoch is created; all existing runs stay closed. This is a static design package with zero runtime-trial budget. Validation is limited to document review, local links/diffs and, if definitions change, standard-library JSON/reference/scope checks using the existing project environment. No third-party skill scripts execute. Stop for a revised package if measured behavior or new tooling is necessary.

Use the verified local planning/documentation skills for drafting, security-and-hardening for trust-boundary review and code-review-and-quality for closeout. Root PLAN/TODO override skill path defaults. SkillSpector remains deferred; MarkItDown's approved outcome remains unchanged. UI UX Pro Max retains its separate pre-frontend review; RTK/ponytail do not block this package.

## Ordered atomic tasks

Each task is documentation/definition work, with at most three primary files. Supporting status updates do not authorize unrelated changes.

| ID / status | Objective and prerequisite | Acceptance criteria | Verification / evidence |
|---|---|---|---|
| T16-1 / proposed | Map evidence and open decisions; exact package approval | Distinguish completed evaluations, approved deferrals and unresolved adoption/quality/lifecycle requirements; trace each blocker to its dependent contract | Source-to-contract gap table in retrieval design; no upstream task silently closed |
| T16-2 / proposed | Specify chunking, retrieval and context; T16-1 | Preserve native/OCR provenance and table relationships; scope to selected references before ranking; distinguish deduplication from ownership; propose bounded chunk/overlap/top-k/evidence/history settings with truncation and insufficient-evidence behavior | Walk CSV multiline records, XLSX sheet/ranges, native/scanned PDF references, empty/short scopes and cross-conversation exclusion; settings remain proposals pending review |
| T16-3 / proposed | Specify answer/citation contracts; T16-2 | Stable source/extraction/location identities, safe quote validation and coarse-location disclosures; distinguish direct facts from calculations; clarify ambiguity, conflicting evidence, unsupported requests and missing-source behavior | Trace answerable, unanswerable, ambiguous, table, multi-file and injection cases to permitted claims and anchors; document retention-dependent alternatives without choosing them |
| T16-4 / proposed | Specify support signals and evaluation; T16-3 | Separate structural citation validity from semantic support; define observable evidence/coverage/abstention/warning states; retain hard boundary failures and independently scored grounding; propose threshold refinements before acceptance runs | Indicator truth table and per-claim scoring examples in evaluation design; preserve active/excluded sets and N/A denominators; no accuracy probability or fabricated scores |
| T16-5 / proposed | Review contracts and decisions; T16-2–4 | Present concrete D01/D04 choices and quality/context proposals with consequences; identify unresolved final speed/memory budgets, chart and G2 requirements | Requirement/negative-case walkthrough, local links/diff and any necessary definition checks; record approved choices only after user reply |
| T16-6 / proposed | Close out and checkpoint; T16-5 | Clearly label drafted versus approved contracts, record remaining blockers and next T17 prerequisites; show readable changes and request separate commit approval | PLAN/TODO/README/checkpoint and review summary; no product implementation, runtime adoption or stage transition |

Approval of this exact package covers its routine drafting, static checks, review and status updates without repeated task-start requests. User policy/threshold decisions, runtime adoption, Git commits, new execution packages and stage transitions retain their separate gates. If a policy answer is unavailable, finish the independent drafts and mark final approval blocked by that specific decision.

## Storage and lifecycle choices to prepare for decision

These are recommendations for the design review, **not adopted behavior**. The approved100MB/file,10files/upload/conversation and1GB library-original limits do not change.

| Topic | Recommended direction | Alternative and consequence | Still needs a decision |
|---|---|---|---|
| Derived data / temporary storage | Separate explicit disk budgets for normalized text, embeddings/indexes/previews and temporary work; reserve before writes and give a clear storage-full response | Automatic cache eviction can recover space but needs rules distinguishing regenerable cache from retained evidence | Exact byte units, caps, reservation/recovery rules and counting for shared/deduplicated content; no arbitrary cap is selected from the small trial |
| Conversation deletion | Delete its messages and exclusive originals/derived data; retain library/shared content and surviving references | Retaining deleted chat history or quotations needs an explicit retention purpose and expiry policy | Messages, quotations, historical citations, temporary artifacts, backups if any, and cleanup/restart behavior; no secure-erasure guarantee |
| Removed or unavailable source | Preserve the approved warning/block while a library item is referenced; for genuinely missing/corrupt evidence, mark it unavailable and exclude it from new answers | Keeping a quote snapshot may aid historical review but retains document content after source removal | Whether old messages/quotes remain readable, become redacted or retain a snapshot; never invent a working preview or silently reuse stale evidence |
| Index maintenance | Preserve stable IDs, version identity and reference scope; report interrupted cleanup/reindex explicitly | Rebuilding everything is simpler but increases CPU/time and must not expose partial/old data | Transaction/reconciliation and retry semantics at T17; no background maintenance task is implemented here |

D01/D04 can be reviewed alongside the drafted contracts. T16-1–4 may describe both alternatives; final approval of dependent contracts must wait for the relevant choice. This avoids asking for a retention decision without first showing its effect on saved chats and citations.

## Evaluation rules carried forward

Preserve the approved initial T02 gates:100% of enabled deterministic source/value/structure checks; every enabled unsupported/injection control; no invented locations/quotes or hidden-source leaks. The initial aggregate targets remain recall@5>=0.90, fully correct answers>=0.90, groundedness>=0.95 and supported citation correctness/coverage>=0.95, subject to the already required T16 review before acceptance runs. Report per-category counts, partial/unsupported/contradicted claims and over-abstention; an aggregate never overrides a hard failure. Missing artifacts fail readiness, excluded formats stay excluded and empty denominators are N/A. Existing scoring flags do not become eligible merely because a design is written.

No new speed, memory, context or quality threshold is adopted by this proposal. A valid citation ID means a reference resolves; it does not establish that the cited source supports the claim. An evidence indicator describes observed support and limitations, never a calibrated probability of correctness.

## Requested approval

Approve T16-1–6 as the exact static design package, including drafting against explicitly recorded upstream gaps while preserving final acceptance/G2 gates. Separately approve committing the six proposal/status documents now prepared: this proposal, PLAN, TODO, README, decision register and session checkpoint. Later contract/definition commits require their own approval. No further storage benchmark or runtime adoption is requested.
