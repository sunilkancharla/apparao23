# Spec: Document Chat — Stage 1: Local Prototype

## Approved workflow amendment — UI aid skipped; early CSV validation (2026-11-20)

The user explicitly chose to skip T15/UI UX Pro Max, including its source review and use. It is no longer a prerequisite for T33. Use the already approved minimal local HTML/CSS/JavaScript approach with manual accessibility/flow review; no alternative framework/tool is selected. This supersedes earlier UI UX Pro Max trial/checkpoint requirements only.

The user approved an initial CSV validation package immediately after T34 and before format expansion, tracked as T34A in PLAN/TODO. Cover selected-Ollama input boundaries and the actual local retrieval → generation → citation/saved-chat pipeline on fixed authored CSV cases. Define exact fixtures, pinned artifacts/settings, execution/resource budgets, controls and stop conditions before its separately approved trial. Byte caps/response counts alone cannot establish exact input fit; report unresolved boundaries honestly. Keep T48's final all-format quality/resource evaluation and existing thresholds unchanged. Benchmarked quality does not independently verify every future answer's meaning, and no runtime semantic verifier is adopted.

## Approved scope amendment - XLS deferred (2026-11-13, latest decision)

The user explicitly directed: "leave the .xls files from our context" and use PDF, XLSX and CSV for Stage 1. This supersedes all earlier requirements to support or evaluate legacy XLS in this stage. XLS is unsupported for Stage 1 uploads/library ingestion and is excluded from parser provisioning, fixture generation, positive-support evaluation and acceptance. Defer T07A and T37; retain prior evidence, definitions and local samples as history without parsing or deleting them. Reintroducing XLS requires explicit approval. No other format, OCR, chart, privacy, resource or approval requirement changes.

## Approved T08 evaluation exception (2026-11-13)

After reviewing MarkItDown v0.1.9 source/dependencies, the user accepted non-adoption and deferral of its empirical comparison, approved committing the review and authorized T09 read-only OCR review. Earlier MarkItDown comparison requirements below are subject to this exception. No measured MarkItDown quality/performance or runtime parser selection is implied. PDF/XLSX/CSV provenance, local OCR and privacy acceptance remain required. Evidence: `docs/benchmarks/markitdown.md`.

## Approved T16 storage and retention clarifications

**Approved T17-A policy and validation-target decisions:** during the static architecture package, the user explicitly chose the following. These settle their earlier open points without approving G2 or execution:

- Count metadata, saved-chat/history and index databases plus retained journals against the5GB processed-data cap; charge upload staging, render scratch and temporary copies against1GB temporary data. No silent eviction.
- Allow10GB (10,000,000,000bytes) aggregate **conversation-only originals**, once per stored content hash. The1GB library-original cap remains separate;100MB/file and10references/conversation/upload are unchanged. Exact class-transition/reservation implementation remains a proposed T17 contract.
- Validation targets: one heavy job at a time; warm complete answers within30seconds;90-second hard answer timeout; at most8GiB total across owned app/workers/Ollama processes; at least4GiB available RAM on the unchanged16GB CPU-only target. These are targets to validate, not achieved results, runtime defaults or trial permission.
- After deletion, retain only minimal content-free records (opaque IDs, deletion/cleanup status and retry-key digests) to prevent old retries recreating items. Count them against5GB and retain them until an explicitly approved maintenance policy removes them. They must not retain document text, messages or quotations; no arbitrary expiry or automatic pruning is approved.

**Approved chart-evaluation sequencing decision:** after T16 review commit `cdbb975`, the user explicitly chose "Defer chart trial until after first CSV flow". Schedule T16A after the first usable CSV upload-to-saved-chat flow (T34). This satisfies the prior chart-trial-or-explicit-deferral gate for T17/G2; the evaluation remains tracked and must precede any chart-interpretation adoption/claim. No chart support is promised in the first CSV flow. PDF/XLSX/CSV, scanned-PDF OCR, local processing and all other adoption/acceptance requirements remain unchanged. Earlier statements requiring chart evaluation before G2 are superseded only by this explicit timing deferral.

The user explicitly selected the following choices during T16 design review. These settle the corresponding earlier open points without adopting the draft retrieval settings, runtime components or G2 architecture:

- Use decimal MB=1,000,000 bytes and GB=1,000,000,000 bytes. Count attached document references, including library references, toward the approved10-file conversation limit. Identical stored library originals count once against the approved1GB library-original budget; reference identities remain distinct.
- Allow **5GB (5,000,000,000 bytes) processed data** for extracted text, embeddings, indexes and previews, plus **1GB (1,000,000,000 bytes) temporary processing files**. Stop processing clearly at either cap. These are disk budgets, not RAM targets or validated capacity guarantees; the approved100MB/file,10files/upload/conversation and1GB library-original limits remain unchanged.
- Deleting a conversation also deletes its messages, quotations and exclusively owned processed data, while preserving library/shared content and surviving references. The existing exclusive-attachment deletion rule remains binding.
- If a source in a retained chat becomes missing or corrupt, keep the saved answer readable, label its source unavailable and exclude that historical answer/source from new answers. Referenced-library deletion remains blocked. No additional quotation snapshot is authorized.

The user also approved the following T16 review directions after draft commit `486fd1b`:

- Keep R01's small-context settings in `docs/retrieval-design.md` as a **provisional validation baseline**, including top5, maximum800-byte chunks,2,000-byte evidence and3,000-byte serialized input. Model-input fit and representative multi-file checks are required before final adoption. This is not a new trial authorization or a final product-context limit.
- Approve R02's indicator design: "Citations checked; meaning not independently verified", with missing-evidence/OCR/partial-answer warnings and no citation-validity-based correctness percentage. Existing internal quality targets remain unchanged; runtime implementation and semantic accuracy are not claimed.
- Approve R08's recovery design: durably record deletion and block retrieval/previews before removing exclusive data; after interruption, resume bounded cleanup and display cleanup pending until removal is verified, preserving shared/library content. Exact coordination, resource bounds and recovery implementation remain T17/G2 contracts.

Exact reservation/concurrent-write accounting, database/journal/temp classification, interruption/reconciliation, retry and physical cleanup verification remain design requirements for T17. No secure-erasure guarantee follows from logical deletion. Detailed decision evidence is recorded in `docs/decisions.md` and `docs/retrieval-design.md`.

## Objective

Build a single-user, browser-based, local document-chat assistant with conversation attachments, a reusable document library, scanned-PDF OCR, grounded citations, saved chats, and an evidence indicator. The target machine is Windows 11 with 16 GB RAM and no dedicated GPU.

## Tech Stack

- Python 3.11+; FastAPI/Uvicorn and a minimal browser UI initially (a frontend framework is an approval decision).
- `uv` with local virtual environment; Ollama for CPU-capable local generation and embeddings; HTTPX for local API requests.
- SQLite for metadata/chat history; local retrieval index/vector storage to be selected after benchmarks.
- Format-specific parsers and/or MarkItDown, local OCR engine for scanned PDFs, pytest and Ruff.
- Support PDF, XLSX and CSV; both conversation attachments and reusable library. DOCX and TXT are excluded entirely from Stage 1.
- Confirmed limits, OCR language, UI and lifecycle rules are consolidated below. Only the listed unresolved details require decisions.

## Confirmed Stage 1 decisions

Current approved requirements; do not ask for these decisions again. Remaining details are listed under Open Questions.

- **Limits:** 100 MB per file, 10 files per upload/conversation, and 1 GB of library originals. The approved T16 clarification above defines decimal units, reference/library counting and5GB processed/1GB temporary budgets; remaining enforcement/recovery details are reviewed before implementation. Benchmark findings do not silently reduce approved limits.
- **OCR:** English only.
- **Frontend:** Minimal locally served HTML/CSS/JavaScript. Use Design 1 as the primary landing-page reference and Design 2 for chat, citations and the evidence panel. A frontend framework requires separate review/approval.
- **Performance decision timing:** Set final speed/memory targets after initial local benchmarks, before model/architecture adoption. Agree bounded trial budgets first; initial measurements are exploratory. Quality/evaluation thresholds need agreement before applicable acceptance evaluations.
- **Chat deletion:** Delete its exclusive attachments, messages, quotations and exclusively owned processed data; preserve reusable library documents and content still required by other references. The approved T16 clarification above defines unavailable-source historical display; exact cleanup/recovery mechanics remain for T17.
- **Data charts/diagrams:** Approve a bounded local feasibility evaluation before deciding runtime support. Use an agreed English-labelled sample set to assess trends, comparisons, labelled values and data-diagram relationships, with real document/page/chart-region or sheet references where available. Compare structured data/labels/OCR with a local visual approach only after exact trial provisioning is approved. Check against manual ground truth, disclose approximate readings and abstain when unsupported. Measure correctness/grounding, citation support, cold/warm latency and total memory pressure on the target CPU-only 16 GB machine. Exact types, thresholds and trial budget are agreed first. No universal visual-understanding guarantee, cloud processing or automatic model/dependency adoption is authorized. The reviewed detail is in `docs/proposals/chart-interpretation.md`; runtime implementation/acceptance tasks require a separate adoption decision after results.
- **Referenced library deletion:** Warn and block deletion while saved conversations reference the library document. This interim Stage 1 rule is approved. SQLite history and document IDs/references remain Stage 1 requirements; more advanced deletion/citation handling may be considered later. Apply the approved T16 retention/display choices; detached-reference, temporary-artifact and physical cleanup/recovery details must be defined before lifecycle implementation.

## Commands and actual setup

Verified environment, lock, test and evaluation commands are maintained in `README.md` and `docs/provisioning.md`. Use the dedicated project `.venv` and its uv; do not install another interpreter, modify PATH or inherit global packages. Model/service/parser provisioning requires an approved exact work package. No application startup command is implemented yet; document it when the first slice exists. Model names `embeddinggemma` and `qwen2.5:3b` remain candidates, not defaults.

## Project Structure

```text
document_chat/
  AGENTS.md                 # persistent Codex project rules (after spec approval)
  SPEC.md                   # approved specification for active stage
  PLAN.md                   # milestones and implementation sequence
  TODO.md                   # small, testable tasks
  README.md                 # updated as each feature lands
  pyproject.toml
  uv.lock
  app/
    main.py                 # FastAPI entry point
    api/                    # HTTP routes and validation
    ingestion/              # PDF, XLSX, CSV, OCR
    retrieval/              # chunks, embeddings, search, citations
    chat/                   # Ollama orchestration and conversation context
    storage/                # documents, library, chat history
    security/               # authorization in Stage 3
    static/                 # local web UI assets, or approved frontend
  tests/
    unit/
    integration/
    evals/
    security/
  docs/
    ADR/
    benchmarks/
  data/                     # local runtime files; excluded from Git
```

This is a **candidate layout**, not a requirement to create unused directories in Stage 1. The existing `agents/`, `skills/`, `references/`, and `docs/` folders may remain; do not confuse installed Codex plugin skills with application source files.


## Functional Requirements and Scope

### 1. Product summary

Build a ChatGPT-like document assistant for office documents. A user can upload one or more supported files, ask questions in a conversational interface, receive answers grounded in the uploaded material, inspect the source passages used, and return to saved conversations.

The application uses a locally running Ollama model. The prototype is intended to run on the user's Windows 11 computer (16 GB RAM, no dedicated GPU), so model size, memory use, indexing time, and response latency must be measured rather than assumed.

### 2. Stage 1 goals

1. Prove document upload → extraction → chunking → indexing → retrieval → answer generation → citation.
2. Support a first, explicitly bounded set of office formats.
3. Persist conversations and enough message context to continue a conversation after restarting the app.
4. Show which file and page/sheet/row/section or text passage supports an answer, where the format permits reliable location metadata.
5. Establish a repeatable evaluation baseline for retrieval and answer grounding.
6. Keep the entire inference and document-processing path local after installation.

### 4. Functional requirements

### FR-01 — Upload and validate files
- Allow upload of one file or multiple files in one operation.
- Stage 1 supported formats: PDF, XLSX and CSV. XLS, DOC/DOCX, TXT, XLSM, XLSB and other unlisted formats are outside this stage.
- Validate extension, detected content type where feasible, file size, and parseability.
- Reject unsupported, corrupt, password-protected, or oversized files with a clear error.
- Prevent path traversal and unsafe filename handling.
- Show per-file processing status and useful failure details.

### FR-02 — Extract and normalize content
- Extract text while preserving useful structure and metadata.
- Preserve PDF page numbers, XLSX sheet names and cell/range/row/column context, and CSV record/column context with physical-line spans where available.
- Do not flatten tables into ambiguous text without recording their structure.
- Store original files separately from normalized extraction output.
- Record parser name/version and extraction warnings for troubleshooting.
- Evaluate Microsoft MarkItDown as one candidate, not as an assumed universal parser. Compare it with format-specific parsers using the supplied sample files.

### FR-03 — Chunk, embed, and index
- Split extracted content into retrieval-sized chunks without losing source metadata.
- Store chunk ID, document ID, filename, format, location metadata, extraction version, and content hash.
- Use a locally runnable embedding model and local vector store.
- Make indexing idempotent: re-uploading an unchanged file should not create duplicate indexed content.
- Provide a way to remove a document and its indexed chunks.

### FR-04 — Conversational question answering
- Provide a chat interface with a local Ollama chat model.
- Retrieve relevant chunks and pass them to the model as evidence.
- Instruct the model to answer only when supported by retrieved evidence; otherwise state that the available documents do not contain enough information.
- Keep conversation context across turns without allowing unrelated old context to override current evidence.
- Clearly distinguish evidence-backed statements from uncertainty.

### FR-05 — Source citations
- Each answer should expose the source file and the most precise location available.
- A citation should open or preview the relevant source passage when feasible.
- Do not fabricate page numbers, sheet names, row numbers, or quotations.
- If exact location metadata cannot be produced for a format, disclose the coarser location.

### FR-06 — Chat persistence
- Save conversations, messages, timestamps, and associated document collection references locally.
- List, reopen, rename, and delete conversations.
- On reopening, restore the conversation transcript and document context.
- Support both conversation-specific attachments and a reusable library with distinct ownership and saved document references.

### FR-07 — Basic quality evaluation
- Create a small, version-controlled evaluation set from sample documents.
- Include answerable, unanswerable, multi-document, table lookup, and ambiguous questions.
- Track retrieval relevance, citation correctness/coverage, answer groundedness, refusal on unsupported questions, latency, and memory use.
- Do not display a single numerical “accuracy score” to end users until its meaning and calibration are defined. Initially show internal evaluation metrics and, if useful, a clearly labelled evidence/coverage indicator.

### 5. Non-functional requirements

- Local-only runtime after setup; no telemetry or external API calls by the application.
- Practical operation on 16 GB RAM without a dedicated GPU.
- Clear loading, progress, empty, success, and error states.
- Data should survive normal application restarts.
- Logging must not expose full document contents or sensitive chat text by default.
- Maintainable modular code and automated tests for parsing, retrieval, citations, persistence, and API behavior.

### 8. Security and privacy baseline

- Treat document text as untrusted input and potential prompt injection.
- Keep system instructions separate from retrieved document content.
- Never execute embedded code, macros, scripts, or commands.
- Restrict file size and supported formats; use safe temporary-file handling.
- Keep all app data under a configured application-data directory.
- Provide deletion behavior for original files, extracted text, embeddings, and related metadata.
- Do not expose one user's data to another; Stage 1 assumes a single local user.

## Code Style

- Use Python type annotations, PEP 8, Ruff, small single-purpose modules, and descriptive names. Write docstrings for public functions, classes, data models, and APIs; comment non-obvious logic rather than restating it.
- Use `uv` for dependency management and a project-local `.venv`. Maintain a reproducible lockfile. Reassess each dependency for license, Windows compatibility, maintenance, memory cost, and offline behavior before adding it.
- Treat uploaded document content as untrusted data, not instructions. Never execute macros, embedded scripts, or document-provided commands.
- Maintain atomic `PLAN.md` and `TODO.md` tasks. Update `README.md` after each completed task or coherent feature with its actual functionality and libraries.
- At each coherent task/work-package closeout, show checks and the Git diff and **ask for approval before committing**. Approved package steps do not need repeated task-start questions. Record material design choices in `docs/ADR/`.
- Use Codex Agent Skills progressively: invoke only the skill appropriate to the current task; do not install or load every skill at once. `AGENTS.md` should be established after spec approval to capture persistent project rules.


## Testing Strategy

- Unit and API tests: file validation, parsing, OCR/page provenance, table/cell metadata, chunking, indexing/deletion, retrieval, citations, evidence indicator and saved chats.
- Mock Ollama for routine tests; add local manual smoke tests for text PDF, scanned PDF, XLSX, CSV, unsupported questions, multi-file questions, and restart persistence.
- Benchmark memory, CPU latency, extraction fidelity, source-location correctness and local-only traffic.

## Boundaries

- **Always:** local processing, untrusted-document isolation, source-grounded answers, explicit abstention, citations, evidence support signals, user-approved commits.
- **Ask first:** changes to confirmed limits/languages/scope, unresolved chart/runtime or retention choices, parser/model/runtime adoption, unapproved dependency/work packages and LAN access. Do not reopen settled requirements or repeat approval for covered steps.
- **Never:** hosted inference/embeddings, executing document instructions/macros, fabricated citations, multi-user auth or MCP actions in Stage 1.

## Success Criteria

- One local user can upload supported files into chats and the reusable library, ask grounded questions, and reopen saved conversations.
- Agreed text and scanned PDF samples yield traceable page references; tables/images retain references even if semantic image understanding is limited.
- Source citations and an interpretable evidence indicator appear; internal evaluation metrics are recorded.
- All tests and demo pass; user explicitly approves Stage 2.

## Open Questions

- Exact growth/reservation/concurrency and journal/class-transition implementation under the approved accounting split and1GB library/10GB conversation-only originals/5GB processed/1GB temporary caps; no silent eviction or cap changes.
- Detached-reference, temporary-file and physical cleanup/reconciliation/retry mechanics, preserving the approved chat-history deletion, unavailable-source display and shared/library rules.
- Chart/diagram sample types, trial budgets/thresholds and runtime adoption after the approved feasibility evaluation, now explicitly deferred until after the first usable CSV flow/T34; no chart-support claim before separate adoption.
- Exact parser/OCR/model/index artifacts, performance/context/concurrency budgets and final architecture after evaluation. English-only OCR and minimal HTML/CSS/JavaScript are already approved.

## Agent Skills and Tool Evaluation Checkpoints

**Rule:** Each checkpoint is a `PLAN.md`/`TODO.md` task. Ask the user before installing an optional tool, benchmark it on representative samples, record the outcome in `docs/benchmarks/` or an ADR, and retain it only if it improves the project. Never silently add a tool to production.

| When to try it | Candidate tool / skill | What to test or decide |
|---|---|---|
| Before writing implementation tasks | `@spec-driven-development`, then `@planning-and-task-breakdown` | Review this stage's SPEC, resolve blocking questions, then create atomic PLAN/TODO tasks. |
| Before accepting third-party Agent Skills or external tool instructions | **SkillSpector** | Explicitly deferred by the user. Continue manual instruction/script/permission/outbound-call review; do not install, run or revisit SkillSpector unless requested. |
| During document ingestion/parser spike | **Microsoft MarkItDown** | Compare against format-specific libraries on PDF, XLSX, CSV, scanned PDFs and tables. Record unsupported formats rather than assuming coverage. Measure extraction fidelity, provenance, OCR compatibility, installation size and offline operation. |
| When deciding on UI implementation | **Manual design review; UI UX Pro Max skipped** | The user excluded review/use of this optional aid. Review accessibility, upload flows, citation previews and chat UX manually using the approved frontend stack. |
| When implementing and testing tasks | `@incremental-implementation`, `@test-driven-development`, `@code-review-and-quality` | Apply one relevant skill at a time; run tests and review changes before requesting commit approval. |
| When Codex context grows or a task boundary is reached | Codex `/status`, `/compact` | Check usage/status and compact only after saving important decisions, active tasks, and test results in repository files. |
| At dependency or tool-review milestones | **RTK**, **ponytail** | User-mentioned experimental tools: verify their exact repositories, purpose, license, platform support and security model before proposing a trial. Do not infer features from the names. |


### Stage 1 tool trials

1. **Before parser implementation:** compare MarkItDown with the evaluated PDF alternatives, XLSX candidates, standard-library CSV and local OCR on a representative fixture set. Compare page/sheet/cell/row provenance, tables, scanned pages and images; select the smallest adequate combination. The user accepted deferral of PyMuPDF's empirical comparison at T05 closeout; its metadata review is not a benchmark.
2. **Before trusting additional Agent Skills:** manually inspect instructions, scripts, file access and outbound requests. SkillSpector is explicitly deferred at user direction; no scanner trial is required.
3. **During first web UI implementation:** use manual layout/accessibility review. UI UX Pro Max review/use is skipped by the explicit 2026-11-20 workflow amendment.
4. **During Codex setup:** try `/status` to inspect the session and `/compact` only at sensible task boundaries. Review RTK and ponytail only after identifying their exact projects and proposed benefits.


## Agent Skills Execution Workflow

1. **Specification review:** use `@spec-driven-development` to review this document and resolve blocking open questions. Do not start implementation before explicit approval.
2. **Task planning:** use `@planning-and-task-breakdown` to produce atomic `PLAN.md` and `TODO.md`, including dependency/tool spikes and acceptance tests.
3. **Implementation:** use `@incremental-implementation` and `@test-driven-development` for one small task at a time. Use `@frontend-ui-engineering` or `@api-and-interface-design` when relevant.
4. **Review and security:** use `@code-review-and-quality` at task boundaries; add `@security-and-hardening` for file ingestion, trust boundaries and Stage 3 authorization.
5. **Documentation and approval:** update README and ADRs, present diff/test evidence, ask before Git commit, and wait for explicit approval before entering the next stage.

## Carried-Forward Decisions and Stage Gate

This section incorporates the user's clarifications and supersedes conflicting provisional assumptions elsewhere in this draft.

### Approved format-scope amendment — 2026-11-13

The user further clarified that DOCX and TXT are excluded entirely from Stage 1 development. Do not plan or implement their parsers, install their dependencies, generate their fixtures, benchmark their extraction or include their positive-support cases in Stage 1 acceptance. Later-stage inclusion is optional and requires a new explicit user decision. Unsupported-format rejection checks may still use these extensions.

**Historical format decision (superseded for XLS by the latest amendment at the top).** The user instructed: “we will stick with - pdf, xls, xlsx, csv for this stage”. This explicitly replaces the earlier five-format scope. Support PDF (native/scanned/mixed), legacy binary XLS, XLSX and CSV across uploads, library, retrieval, citations and acceptance. DOCX and TXT are excluded entirely from Stage 1. Their existing fixture/question definitions remain historical design material and must not enter active Stage 1 scores.

Evaluate XLS separately from XLSX. Preserve sheet/cell/range provenance and available stored values; never execute workbook formulas, VBA/macros, embedded code or external relationships. Disclose missing cached values and unsupported features. Existing rejection rules for encrypted/password-protected, corrupt and unsupported files remain applicable. This approves the format scope, not a parser choice or installation. Limits, English OCR, local inference, chart evaluation and other approved requirements remain in force.

### Confirmed product and deployment decisions
- **Stage 1 is single-user:** one person uses the application locally during the prototype. Do not build multi-user authentication or authorization in Stage 1.
- **Initial interface:** a local web application accessed through a browser.
- **Later interface direction:** desktop packaging may be considered in a later stage; it is not a Stage 1 requirement.
- **Document organization:** support both (a) files attached to an individual conversation and (b) a reusable document library that can be referenced by multiple conversations.
- **PDF scope:** PDFs may contain selectable text, scanned/image-only pages, tables, and embedded images. Stage 1 must detect scanned pages and provide an OCR path for them. Preserve table structure and image/page references where possible. Complex visual interpretation of charts, diagrams, or photographs must be explicitly evaluated; do not claim full visual understanding merely because images were extracted.
- **Quality presentation:** retain internal evaluation metrics and provide users with a transparent evidence indicator. The indicator must describe evidence support/citation coverage, not pretend to be a calibrated probability of factual correctness.
- **Stage 1 deployment:** local workstation prototype. The application must use local inference and local storage. The strict no-internet-at-runtime acceptance requirement is finalized in Stage 3.
- **Future deployment:** the product is expected to support both individual workstations and a local company server. Multi-user support is introduced in Stage 3, not Stage 1.
- **Integrations/actions:** MCP and external business actions are deferred; they are not part of the initial stages unless a later approved requirement makes them necessary.

### Stage 1 additions and clarifications
1. The active Stage 1 file list is PDF, XLSX and CSV. DOC/DOCX, TXT, PPTX, email and other unlisted formats are excluded from Stage 1; later support requires explicit user approval. Legacy XLS is excluded from Stage 1; later inclusion requires explicit approval.
2. Add OCR as a candidate dependency for scanned PDF pages. Before installation, compare local OCR options for Windows support, language coverage, accuracy, license, installation size, and offline operation.
3. The extraction pipeline must distinguish native PDF text from OCR-derived text and retain page-level provenance and extraction confidence/warnings where available.
4. For PDF tables, preserve row/column relationships where practical; retain a link to the original page/table region. For embedded images, preserve the source page and image reference. Stage 1 may index OCR text extracted from images, but advanced image/chart reasoning is not guaranteed.
5. The reusable library and conversation-specific attachments must have distinct ownership/reference semantics. A conversation may reference library documents without duplicating their stored bytes. Deletion behavior must be explicit: deleting a conversation must not silently delete a library document; deleting a library document must warn about dependent conversations and define what happens to their citations.
6. Show an evidence indicator with understandable signals such as whether citations exist, whether cited passages support the response, and whether the answer required abstention. Keep detailed benchmark scores in an internal evaluation report.
7. Store document identifiers and references with each conversation so reopening a chat restores the correct document context.

### Updated Stage 1 acceptance criteria
- A single local user can use the browser-based application.
- Both conversation-specific attachments and a reusable document library work as specified.
- Text PDFs and scanned PDFs in the agreed sample set are processed; OCR-derived passages retain page references.
- PDF tables and embedded images are preserved or represented with traceable source references; limitations in visual interpretation are disclosed.
- The user sees citations and a transparent evidence indicator; internal evaluation metrics are also recorded.
- No multi-user authentication, RBAC, OAuth, MCP actions, or desktop packaging is required for Stage 1.

### Original stage deliverables and acceptance details

### 9. Stage 1 deliverables

- Working local prototype.
- `PLAN.md` with phase-level and atomic tasks.
- `TODO.md` with status, dependencies, and acceptance evidence.
- `README.md` updated throughout implementation.
- `SPEC.md` (this file), updated only after review/approval of changes.
- Architecture diagram and relevant ADRs.
- Automated tests and a small evaluation dataset/report.
- Dependency inventory with versions and licenses.
- Instructions for downloading model weights and dependencies before offline use.

### 10. Stage 1 acceptance criteria

Stage 1 is complete only when:
1. A user can upload the agreed sample set of supported files.
2. The app extracts and indexes them without corrupting source-location metadata.
3. The user can ask questions requiring one or more uploaded files.
4. Answers cite real source locations; unsupported questions are explicitly declined or qualified.
5. Conversations persist and can be reopened after restarting the app.
6. The agreed evaluation set runs reproducibly and results are recorded.
7. The app's runtime network traffic is verified to be unnecessary for the core workflow after setup.
8. Tests pass and README/setup instructions match the implementation.
9. The user reviews the demo and approves moving to Stage 2.

### 12. Exit gate

Do not begin implementation until the user approves this Stage 1 specification, the initial format list, the local UI/deployment mode, and the proposed architecture after dependency review.

**Conflict rule:** Confirmed decisions in the carried-forward revision and the concise top-level stage scope override older provisional or conditional language reproduced for traceability above. Any still-unresolved choice must be approved before it becomes an implementation commitment.

## Approved delivery-process refinement — 2026-11-13

The user approved consolidating settled requirements, bounded work-package approvals, and earlier hardware/model feasibility with a CSV-first vertical slice. A package states exact task scope, dependencies/versions/artifacts, downloads, local fixture generation, execution limits, checks and stop conditions. One approval covers those necessary steps; do not repeatedly request permission within that approved scope. Obtain a new decision only for scope/budget/artifact changes or another unapproved package. Git commits, G2 architecture/runtime adoption and stage transitions retain explicit approval. Do not silently download models or dependencies at startup.

Prioritize T10 embedding feasibility and a new T11A fixed-evidence chat feasibility task after T07, before the remaining format/tool evaluations. Complete combined OCR/model pressure checks after T09 before final adoption. Optional developer tools cannot delay the CSV upload → retrieval → local answer → citation → saved-conversation path; evaluate them before use. UI UX Pro Max is skipped under the explicit 2026-11-20 amendment; manual frontend review remains required. T34A adds initial CSV runtime/input-boundary validation after T34 and before format expansion. See PLAN/TODO for the revised dependency order. No model installation or next-task execution is implied by this process refinement.
