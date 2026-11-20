# Stage 1 Decision Register

## 2026-11-20 — T32 commit approved; UI aid skipped; CSV validation scheduled

The user approved all reviewed T32 changes and explicitly requested the commits. T15/UI UX Pro Max is skipped entirely at the user's direction, including source review/use; remove its prerequisite from T33 and retain manual accessibility/flow review with the already approved local HTML/CSS/JavaScript stack. Do not research, install or use the skipped aid unless requested again.

The user accepted initial CSV validation immediately after T34, before format expansion. T34A will define a fresh bounded package for selected-Ollama input boundaries and actual local embedding/retrieval/generation/citation/restart behavior against fixed CSV ground truth. Exact artifacts/fixtures/settings, execution budgets and controls still need the normal package gate before any native trial; no old allocation is reopened. The accepted T17 omissions remain historical limitations, not passes. Use ordinary selected Ollama interfaces; no standalone tokenizer, custom build, private runner bridge or runtime semantic verifier is implicitly selected. T48 remains the final all-format quality/resource baseline. Unknown input fit and per-answer meaning remain labelled until evidence supports a narrower claim.

The user explicitly reserved T33 for a new session: do not start its implementation in this closeout. They also explicitly requested `docs/session_summaries/SESSION_4_AI_Session_SUMMARY.md`, covering T26–T32 in Session 3's format. This authorizes that one summary despite the standing no-checkpoint/default-summary rule; prior session summaries and historical checkpoint files remain unchanged. Record durable progress/decisions in PLAN/TODO and linked reports. No stage transition, dependency installation or new model/OCR/native run is authorized here.

## 2026-11-20 — G2 approved; T17 closed; bounded T18 authorized

After presentation of the updated architecture, the bounded T18 foundations scope and the documentation commit, the user answered "I approve all of them, please proceed." Record G2 acceptance of [ADR0001](ADR/0001-stage1-architecture.md), its existing component pins/C01–C08 contracts and the Ollama-internal tokenizer route. The same approval covers committing the reviewed documentation and performing the [bounded T18 increment](../PLAN.md). T17 is complete as an architecture/decision task.

The accepted omissions remain unverified: outstanding selected-runtime build/notice/security evidence, exact input-fit/output-boundary proof and physical 16 GB CPU-only acceptance. Standalone dependencies are no longer selected. No omitted test becomes a pass, no hardware or privacy requirement changes, and PDF/OCR limitations remain. Normal implementation tests and Stage 1 acceptance still apply. T18 reuses existing local tools with no new dependencies/downloads/model trial; subsequent packages and Stage 2 remain separately gated.

## 2026-11-20 — Ollama internal tokenizer selected

The user explicitly chose: "okay then we go with the internal tokenizer". Use the selected local Ollama runtime's model-native tokenization for generation and embeddings. This supersedes the 2026-11-19 standalone Hugging Face route choice. Remove the separate Tokenizers/Hub/HF-Xet seventeen-node candidate graph from proposed Stage 1 provisioning; existing packages used elsewhere remain untouched. Preserve the cached research assets and historical evidence without another standalone trial.

Use the ordinary Ollama chat/embedding interfaces for the application. This choice does not authorize a custom runtime build, private runner-port discovery or an internal counting bridge, and does not establish a supported public count-only preflight endpoint. Runtime response token metrics describe completed processing; they do not prove exact pre-request fit. Input/output reservation and truncation/boundary behaviour remain unverified under the already accepted T17 investigation omission. Do not invent an endpoint or claim those checks passed.

SPEC's product requirements and 16 GB CPU-only target remain unchanged. This component decision does not by itself approve the complete G2 architecture or T18. Normal implementation tests remain required; no installation, new runtime/model trial, dependency/lock change or cache deletion occurred in recording it.

## 2026-11-19 — stop the three remaining T17 investigations

The user explicitly accepted proceeding without further checking/retesting of (1) remaining dependency build-source/native-notice/security evidence, (2) actual standalone-tokenizer/Ollama parity and input boundaries, and (3) the 16 GB CPU-only target-machine proof, and asked to move to the next step. Treat these as user-accepted unverified limitations for advancing the T17 architecture decision. Do not reopen these investigation packages or repeat their completed checks without a concrete new reason/user request.

This supersedes their earlier mandatory pre-G2 investigation ordering. It does not turn missing evidence into a pass, establish complete licence/security clearance, demonstrate token/context correctness or prove physical-16-GB feasibility. Keep the recorded PDF/OCR limitations. SPEC's product scope, local-processing/privacy rules, target hardware and acceptance requirements remain unchanged; normal tests of newly implemented behaviour remain required. No new physical proxy was approved.

The next step is the final G2 architecture decision in [ADR0001](ADR/0001-stage1-architecture.md), followed by T18 once architecture/component adoption and that implementation task are approved. The present instruction accepts the named verification omissions; it does not silently select different components or mark G2 approved. No additional research proposal, new benchmark report, installation or application code is needed for this documentation handoff.

## 2026-11-19 — dependency/input-fit work and commit authorized

The user explicitly requested finishing T17 items 1 and 2, reporting the outcome and performing the reviewed commit without another explicit approval. [Package](proposals/t17-standalone-validation-closeout.md), [findings](benchmarks/t17-standalone-validation-closeout.md). No additional routine project-approval request is needed for this scope or commit. Host permission controls remain separate.

The exact retained seventeen-node graph, cached wheel/registry identities and publisher subjects passed the fresh static checks. Publication records contain no build-input predicate; the existing build-source/native-notice conditions remain unresolved. Therefore installation and native parity are not claimed complete. No waiver, dependency/version substitution, G2 acceptance, target-hardware change or T18 start was inferred. The selected standalone direction is unchanged.

## 2026-11-19 — standalone tokenizer direction selected

**Superseded by the user's [2026-11-20 internal-tokenizer decision](#2026-11-20--ollama-internal-tokenizer-selected).** The following records the earlier direction; it is not an active provisioning requirement.

The user explicitly chose to proceed with standalone tokenization for local model-input accounting. Treat this route choice as settled; do not reopen an Ollama-only counting design or repeat completed artifact/vocabulary research without a specific new finding.

Use the existing Hugging Face Tokenizers candidate and pinned local model-specific assets as the validation baseline (currently Tokenizers 0.23.3 with the full recorded seventeen-distribution graph). Ollama remains responsible for generation and embeddings. The packaged native runner remains an evaluation reference, not an additional selected production service.

This selects the direction, not a claim that the standalone engine is already installed, that downloaded assets establish exact runtime parity, or that unresolved dependency/licence conditions have passed. Next dependent work is the focused reviewed provisioning and existing FP/NP comparison, reusing the verified weights, vocabulary mapping and tests. The 16 GB performance gate is separate from tokenizer correctness and is not a reason to repeat the route decision. Scope, provisional context/output settings and final G2 approval remain unchanged.

## 2026-11-19 — consolidated T17 authority and evidence disposition

The user explicitly requested finishing the four remaining T17 blocks, including scoped commits, in one go without intermediate project approvals. [Package](proposals/t17-consolidated-closeout.md), [report](benchmarks/t17-consolidated-closeout.md). This authorizes that package's independent safe work; it does not approve G2, T18, a requirement change, hardware proxy or blanket security/licence exception. RPT results were committed as 34ca104.

Retain the exact existing proposed core components. The packaged native runner was an evaluation reference, not a silently selected production counter. Standalone Tokenizers and all seventeen candidates remain on hold for unresolved provisioning/trust and full pipeline parity. Nomic vocabulary representation differences were reconciled, but its GGUF/reference 2,048 context differs from the earlier unverified 8,192 declaration. Keep provisional product settings and unknown-overhead/equality gates unchanged.

The completed report explicitly retains B01 (standalone/selected-Ollama parity), B02 (physical16GB or explicitly approved proxy) and B03 (selected-runtime notice/advisory/provisioning closure). New positive counts/synthetic format checks do not turn those gaps into passes. No user document, global install, checkpoint, application feature or stage transition was involved.

## T17-A commit and R1 approval — attempt closed, no research/adoption finding

The user answered "yes, i do approve all" to the exact11-file commit and R1public-source package. Committed architecture/policies as `dbd9137`. R1was attempted under a fresh allocation and stopped before HTTP on authored initializer/cleanup-adapter defects, not network or upstream evidence. [Stop report](benchmarks/public-source-review-stop.md) records the preserved state and unperformed research. No retry, field/counter reset, new repair package or G2 approval is inferred; R1-Srequires a separate explicit decision. Prior storage/retention/resource/format/chart decisions remain unchanged.

## T17-A policy decisions — explicitly approved during static design

The user approved T17-A1–A6 with "I approve and proceed further" after readiness commit `e9d107e`. Four policy/target questions were separately answered with their recommended options:

- Metadata/history/index databases and retained journals count as processed data under5GB; upload staging/render scratch/temp copies count against1GB temporary; no silent eviction.
- Conversation-only originals have a10GB aggregate cap, charged once per stored content hash, separate from1GB library originals and preserving100MB/file/10references limits.
- Validation targets: one heavy job at a time, warm complete answers≤30s,90s hard answer timeout, aggregate owned app/workers/Ollama≤8GiB and available RAM≥4GiB;16GB CPU-only target unchanged. These are not achieved results or permission for a new trial.
- Minimal deleted-target records may retain opaque IDs, deletion/cleanup status and retry-key digests, never document/chat text or quotations; charge against5GB and retain until an explicitly approved maintenance policy removes them. No arbitrary TTL/automatic pruning.

Recorded in SPEC and [C03–C07](contracts.md). The [proposed architecture ADR](ADR/0001-stage1-architecture.md) is still Proposed. Package authorization and these decisions do not approve its remaining mechanism/default/component choices, native trust boundary, installation, current-security claims, new research/validation or G2. Advisory/native-notice freshness, verified model-input fit, target-resource feasibility and representative parser/OCR/scale limitations remain visible adoption gates.

## Chart feasibility timing — deferred until after the first CSV flow

After T16 review commit `cdbb975`, the user explicitly answered "Defer chart trial until after first CSV flow (recommended)" to the chart-trial-or-deferral gate. Move T16A after T34, preserving the approved feasibility scope, fixture ground truth and separate adoption decision. This is an explicit narrow waiver of pre-G2 trial timing, not a chart-support claim, deletion of evaluation coverage or waiver of PDF/XLSX/CSV, scanned-PDF OCR, local-processing or other adoption/acceptance requirements. Do not ask for this unchanged deferral again. See [readiness assessment](proposals/t17-architecture-readiness.md) and [chart scope](proposals/chart-interpretation.md).

T16's nine review-update documents are committed as `cdbb975`. T17 readiness preparation is authorized; the concrete T17-A static package is proposed for review. G2 and product implementation remain unapproved, with A01–A08 adoption/accounting/context/resource/validation gaps recorded.

## T16 review directions approved — static package complete

Drafts committed as `486fd1b` under the user's explicit nine-file Git approval; the same request authorized the remaining static review. The user then explicitly selected all three recommendations:

- **R01:** keep the draft's small-context settings as a provisional validation baseline, requiring model-input fit and representative multi-file checks before final adoption. No new trial or final product defaults are approved.
- **R02:** approve "Citations checked; meaning not independently verified", missing-evidence/OCR/partial warnings and no correctness percentage derived from citation validity; preserve existing internal targets.
- **R08:** approve durable deletion records and retrieval/preview blocking before exclusive cleanup, with bounded restart recovery and pending status until verified; preserve shared/library data.

The [static review](retrieval-design.md#static-review-outcome-after-draft-commit486fd1b) clarified pre-packing versus supplied-evidence metrics, error/no-evidence precedence and crash-safe cleanup/publication ordering. These are design corrections, not executed tests, new numeric quality thresholds or component adoption. R03–R07 policy choices below remain unchanged. T16-1–6 static work is complete; T17 detailed contracts, chart feasibility/explicit deferral, final performance/scale/physical16GB acceptance and G2 remain open. Review-update commit approval is separate from the already consumed draft commit approval.

## T16 storage/retention choices approved — contract review remains

The user explicitly selected the recommended options in two sets of T16 questions:

- Delete the chat's messages, quotations and exclusive processed data with the chat, preserving library/shared content and surviving references.
- For missing/corrupt sources in a chat that is kept, retain the saved answer, label its source unavailable and exclude it from new answers. Referenced-library deletion remains blocked; no extra source snapshot is approved.
- Use decimal MB/GB; count attached document references, including library references, toward the10-file conversation limit; identical library originals count once toward the1GB library-original budget while reference identities remain distinct.
- Allow **5GB processed data (5,000,000,000bytes)** and **1GB temporary processing files (1,000,000,000bytes)**. Stop processing clearly when either cap is reached. These are disk caps, not RAM limits or measured capacity guarantees. Existing100MB/file,10files/upload/conversation and1GB library-original limits remain unchanged.

These explicit requirements are synchronized into [SPEC](../SPEC.md#approved-t16-storage-and-retention-clarifications) and retrieval choices R03–R07. R01 chunk/context settings, R02 indicator/quality interpretation and R08 interruption/reconciliation remain draft contracts for review. Database/history/journal/temp classification, exact reservation/concurrency/duplicate-request mechanics and aggregate saved-conversation-original storage policy remain T17 requirements; no unspecified cap or eviction policy is inferred.

## T16 static design authorized — drafts prepared

The user said "please proceed" after proposal commit `cc08343`, authorizing the bounded [T16 static design package](proposals/t16-grounding-contracts.md), including explicit upstream gap tracking. Draft [retrieval/citation](retrieval-design.md) and [support/evaluation](evaluation.md#t16-draft--support-indicators-and-grounding-review) contracts are ready for review. Package authorization alone approves drafting; the explicit policy decisions above were obtained separately. No executable code, new fixtures, scoring eligibility, installation, native/model/parser execution, runtime adoption, G2 or trial permission is introduced.

Review the remaining proposed choices R01/R02/R08 in retrieval design. R03–R07 now reflect the explicit policy replies above, with remaining implementation mechanics identified. Context-fit validation and final performance/quality/component adoption still require review. Existing original-file deletion, shared/library preservation and referenced-library blocking remain approved and unchanged.

## Storage preferred candidate — approved direction, adoption pending

After reviewing the committed T12-D results (`18be917`), the user replied "yes proceed please" to the recommendation to record SQLite plus the exact reviewed sqlite-vec0.1.9 Windows artifact as the preferred candidate, resolve storage/retention details and prepare T16 before G2. Record that preference only. It does not approve installing/loading the artifact in an application, native query optimization, new benchmarks, reduced upload/library limits or final runtime adoption.

The [comparison](benchmarks/sqlite-vec-match-results.md) supports lower measured search latency with matching synthetic reference results, at the cost of larger files and several higher update costs. Preserve pinned companion notices, the exact-artifact restrictions and the binary/source-provenance limitations. The baseline remains a comparator, not a silently selected fallback. Final storage/adoption, scale/performance and D01/D04 details remain for review. The [T16 package](proposals/t16-grounding-contracts.md) is proposed for static contract drafting; no unresolved lifecycle policy is selected by this preference.

## sqlite-vec exact-wheel companion notices — accepted

Following static-review commit `3092aeb`, the user explicitly said "i do accept" to using the pinned upstream license texts as companion notices for the exact reviewed Windows wheel. This narrow exception applies only to `sqlite_vec-0.1.9-py3-none-win_amd64.whl`, SHA-256 `4a28dc12fa4b53d7b1dced22da2488fade444e96b5d16fd2d698cd670675cf32`, with unchanged bytes and the MIT/Apache texts from upstream commit `e9f598abfa0c06b328d8fe5da9c3760cce74be10` identified in the [artifact report](benchmarks/sqlite-vec-artifact-review.md). Preserve both pinned texts alongside the artifact/any later explicitly approved local evaluation and keep the missing-bundled-notices finding visible. No repackaging, blanket exception for other artifacts, binary/source-build equivalence, unrestricted redistribution or legal clearance is inferred. This records the notice decision only: installation, wrapper import, DLL/SQLite loading, a new empirical package and G2 adoption remain separately gated.

## MarkItDown non-adoption and trial deferral - 2026-11-13

The user replied "okay, proceed" to the concrete proposal to defer the empirical MarkItDown trial, commit the source/dependency review and start T09 local OCR review. Accept non-adoption of MarkItDown for Stage 1 and close T08 with that evaluation exception. This selects no runtime parser, waives no OCR/provenance/privacy requirement, and authorizes no OCR installation or benchmark. See [review](benchmarks/markitdown.md).

## Latest approved format decision - XLS deferred (2026-11-13)

User explicitly requested PDF, XLSX and CSV only for Stage 1, deferring legacy XLS. This supersedes earlier XLS inclusion: exclude T07A/T37 and XLS-specific fixtures/questions/negative controls from active work and acceptance. Preserve earlier evidence, original expected answers and local samples. XLS must be rejected as unsupported by the future Stage 1 upload contract; later support requires explicit approval. T08 no longer depends on T07A. This scope decision does not resolve or waive native-network isolation for other future trials, change dependencies, authorize installations, or delete files. Reintroducing XLS or selecting isolation remains separately gated.

## Approved process improvements and T07 package — 2026-11-13

The user explicitly approved T07 and all three improvements: consolidate settled SPEC requirements, bounded work-package approvals, earlier model feasibility/CSV-first delivery. Preserve Git/G2/scope/stage gates; do not ask repeatedly for covered package steps. T10/T11A move earlier; combined OCR/model checks remain before adoption. Optional RTK/ponytail cannot block the first slice, UI UX Pro Max remains before frontend implementation. Moving tasks authorizes no future model/service downloads.

Actual T07 results, coverage gaps and combined worker-budget accounting failure are in `docs/benchmarks/tabular-text-parsers.md`. Installed three pins inside `.venv`, no runtime adoption/application ingestion. The user approved committing the reviewed results and process changes (“yes please”). This does not waive remaining acceptance coverage, retroactively expand the worker budget or adopt runtime components.

## Format-scope decision — 2026-11-13

User explicitly instructed “we will stick with - pdf, xls, xlsx, csv for this stage”. Approved Stage 1 formats are PDF/XLS/XLSX/CSV; DOCX/TXT are excluded entirely from Stage 1; later inclusion requires explicit user approval. The user clarified that DOCX/TXT must be excluded entirely from Stage 1 development, evaluation provisioning, fixture materialization and positive-support acceptance. They may be included in later stages only if the user explicitly requests it. This supersedes earlier five-format statements and the initial instruction to skip DOCX temporarily. SPEC and persistent rules are synchronized. Propose T02R corpus refresh, separate T07A XLS evaluation, CSV-first implementation and repurposed unstarted T37/T39 tasks; sequence changes await review. Do not add parser dependencies or claim XLS support yet. No formulas/macros/external relationships may execute. Limits, OCR, privacy and other approved behavior remain in force.

T05 was committed as d8d12e7 under the prior explicit closeout/commit approval. The user subsequently approved committing the separate format-scope updates (“yes please”). This authorizes the reviewed documentation/evaluation-definition commit, not further task execution, provisioning or runtime adoption.

## Approval and current task

The user approved AGENTS.md, PLAN.md and TODO.md and explicitly agreed to T01's downstream decision allocation (“yes please”). T01 is complete; the user approved T02's fixture/rubric design (“good”) and T03 read-only review proceeded. T03 inventory/dependency/provisioning reports are prepared; installations, downloads, adoption, commits and later tasks remain gated. SPEC's T01 clarification records approved product choices.

## Confirmed design direction

- Design 1 (`images/Design1_Offline Document Assistant Dashboard.png`) is the primary landing-page reference.
- Design 2 (`images/Design2_Document Assistant Dashboard Interface.png`) informs the chat interface, citations and evidence panel.
- The user approved minimal locally served HTML/CSS/JavaScript for Stage 1, without a frontend framework. The references do not add requirements from image details or authorize UI implementation now.

## Supplied samples: metadata inspection

The user supplied files under `sample_files/` for project evaluation. Local directory metadata shows 3 PDFs, 4 XLSX workbooks and 2 CSVs. No legacy XLS files, DOCX files or TXT files were found there. The largest PDF is 54,671,155 bytes (about 55 MB). No document content was parsed, evaluated, uploaded or modified during this check; native/scanned characteristics and extraction quality are not yet verified.

Use these as initial local sample candidates, not the complete acceptance corpus. Subsequent authorized T02 inspection recorded hashes, workbook sheet metadata and selected CSV answers/locations in the fixture manifest; authored definitions supply design coverage for missing formats and controls. PDF/workbook contents and generated artifacts remain unverified. Supplied originals must not enter Git; no files have been staged. Parser/model trials remain separately gated.

## Decision status

IDs match PLAN. Nothing listed as open is an approved default.

| ID | Status | Decision needed / evidence so far |
|---|---|---|
| D01 | Approved | User answered “1 ok” to 100 MB per file, 10 files per upload/conversation, and 1 GB of library originals. Derived-data/storage budgets, exact enforcement/counting rules and measured viability remain for review; do not silently reduce these approved limits after benchmarks. |
| D02 | Approved | User selected English-only OCR. No additional OCR language assets are required by the current decision. |
| D03 | Evaluation scope approved | User answered “1 ok” to the bounded evaluation-first chart scope in `docs/proposals/chart-interpretation.md`. Runtime support is decided after measured local results. T16A proposes the separate investigation; no trial installation or execution is authorized yet. |
| D04 | Core deletion rules approved; retention details open | Delete a chat's exclusive attachments and preserve library/shared content. User approved the interim Stage 1 rule (“ok, next”): warn and block library deletion while saved conversations reference it. More advanced deletion/citation handling can be considered later. Remaining historical-message/citation, derived-artifact and temporary-file retention details must be settled before lifecycle implementation; detaching references does not implicitly approve destruction of historical citation evidence. |
| D05 | Approved | User answered “1 ok” to minimal HTML/CSS/JavaScript, with Design 1 for the landing page and Design 2 for chat/citations/evidence. A framework requires a separately reviewed change. |
| D06 | Timing and initial T02 rubric approved | Final speed/memory targets follow initial local benchmarks, before T17 adoption. Bounded trial budgets first. User approved T02 initial quality rubric/gates; T16 refinements require review before acceptance. Hardware inventory differs, but user explicitly said “don't change, keep it as before”: retain 16 GB/CPU-only target. |
| D07 | T02 design approved | Supplied samples are inventoried/hashed; CSV ground truth locally checked; authored definitions cover missing formats/controls. PDF/workbook contents and generated artifacts remain unverified. T02 approval is design acceptance, not permission to publish/commit original documents or proof of parser quality. |
| D08 | Deferral approved | Exact RTK/ponytail identities and trial decisions move to T13/T14. No reliance or install until exact projects are identified and approved. |
| D09 | Deferral approved | Exact provisioning/assets/commands/trial budgets move to T03 and individual G1 proposals. No blanket installation permission. |

## T01 completion criteria

T01 acceptance is satisfied: D01/D02, D03 evaluation scope, D04 core deletion rules, D05 frontend and D06 decision timing are approved, and the user explicitly approved the downstream allocation below. Library/reference invariants are preserved, approved SPEC clarifications recorded and no dependencies adopted. T01 completion does not complete deferred contracts/trials.

## Approved allocation of remaining details

**2026-11-14 - Synthetic OCR evaluation boundary:** After consolidated isolation result commit `ed4cb3a`, the user accepted a user-operated disconnected trial without filesystem confinement ("yes continue please") and authorized preparing its [bounded package](proposals/manual-disconnected-ocr-trial.md). Acceptance is limited to authored synthetic inputs on the local Windows account; it does not waive Stage 1 application privacy/security, authorize user documents, adopt OCR engines, approve provisioning/execution of the still-proposed package or reopen Windows isolation diagnostics. Exact package and Git approval gates remain.

T03 host/baseline review is complete, with future model/OCR/tool artifacts still requiring individual G1 approval. T04 SkillSpector was explicitly deferred by the user (“then do not bother about it”); no scanner installation/trial. Use manual skill/script review. See `docs/benchmarks/skillspector.md`; do not revisit the optional scanner unless requested.

Subsequent user direction overrides the earlier uv-only loose-tool proposal: use a dedicated project `.venv` and install the reviewed baseline here; the user will manage installations/uninstallations elsewhere. This explicitly brings environment preparation forward from T18. Verified setup is recorded in `docs/provisioning.md`; no global changes, application implementation, parser/OCR/model installation or commit was authorized/performed.

- D01 enforcement/counting and derived-storage budgets: T17 contracts before T20/T23 implementation.
- D04 historical-message/citation, detached-reference, derived-artifact and temporary-file retention: T17 contracts before ownership/lifecycle implementation; preserve approved deletion rules.
- D06 quality rubric and D07 full sample/expected-evidence definitions: T02, with detailed grounding thresholds in T16 before acceptance evaluation. Keep originals local and out of Git.
- D08 RTK/ponytail identities: T13/T14; no installation/reliance/adoption until exact projects are identified and approved. If still ambiguous then, obtain an explicit skip/defer decision.
- D09 exact assets, commands and trial budgets: T03 and individual G1 proposals; no blanket provisioning approval.

The user confirmed the allocation, authorized T02 and approved its design/rubric. T03 reports are in `docs/benchmarks/environment.md`, `docs/dependencies.md` and `docs/provisioning.md`. The first concrete download proposal is P01, uv 0.13.8 only; no provisioning permission has been inferred. Original target explicitly retained after hardware clarification. No parser/model was installed or benchmarked, and no files staged/committed.

Following the licensing explanation/recommendation, the user said "ok sir, carry on". T05 provisioned only the nine-package permissive subset in the project .venv and compared pypdf/pdfplumber. No paid license or PyMuPDF installation occurred. Results and limitations are in `docs/benchmarks/pdf-parsers.md`. Replying “ok, next step please” to the explicit deferral/commit question, the user approved T05 closeout, deferral of PyMuPDF's unrun empirical comparison and its source commit on 2026-11-13. This is an explicit evaluation exception to the original sequence; no runtime parser adoption is approved. Later commits/trials retain their gates.
