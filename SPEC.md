# Spec: Document Chat — Stage 1: Local Prototype

## Objective

Build a single-user, browser-based, local document-chat assistant with conversation attachments, a reusable document library, scanned-PDF OCR, grounded citations, saved chats, and an evidence indicator. The target machine is Windows 11 with 16 GB RAM and no dedicated GPU.

## Tech Stack

- Python 3.11+; FastAPI/Uvicorn and a minimal browser UI initially (a frontend framework is an approval decision).
- `uv` with local virtual environment; Ollama for CPU-capable local generation and embeddings; HTTPX for local API requests.
- SQLite for metadata/chat history; local retrieval index/vector storage to be selected after benchmarks.
- Format-specific parsers and/or MarkItDown, local OCR engine for scanned PDFs, pytest and Ruff.
- Support PDF, DOCX, XLSX, CSV and TXT; both conversation attachments and reusable library.
- File size/count limits, OCR languages, deletion behavior and advanced image interpretation remain open decisions.

## Commands

Use these as **proposed** Windows PowerShell commands; validate versions, paths, and prerequisites during the dependency-review task before adopting them. Commands describe development setup, not permission to start implementation.

```powershell
uv python install 3.11
uv venv --python 3.11
.\.venv\Scripts\Activate.ps1
uv add fastapi uvicorn httpx
uv add --dev pytest ruff
ollama pull qwen2.5:3b
ollama pull embeddinggemma
uv run pytest
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

- `ollama serve` is needed only if the local Ollama service is not already running.
- Model names are **candidates**, not approved defaults; benchmark on Windows 11, 16 GB RAM, CPU-only. `embeddinggemma` and `qwen2.5:3b` come from the attached example, not a hardware benchmark.
- Add document parsers, OCR engines, vector storage, frontend tools, and security packages only after a reviewed comparison; commands above are not a complete install recipe.
- Provisioning may require internet; production runtime must never silently download models or invoke cloud APIs. Stage 3 includes an explicit disconnected-runtime verification.


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
    ingestion/              # PDF, Word, spreadsheet, CSV, TXT, OCR
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
- Initial candidate formats: PDF, DOCX, XLSX, CSV, and TXT.
- Validate extension, detected content type where feasible, file size, and parseability.
- Reject unsupported, corrupt, password-protected, or oversized files with a clear error.
- Prevent path traversal and unsafe filename handling.
- Show per-file processing status and useful failure details.

### FR-02 — Extract and normalize content
- Extract text while preserving useful structure and metadata.
- Preserve PDF page numbers; spreadsheet sheet names and row/column context; CSV row/column context; DOCX headings/paragraphs/tables where possible; TXT line or section context.
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
- Define whether uploaded files remain attached to a conversation or belong to a reusable local library; this is a clarification item.

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
- After each task/feature show tests and the Git diff, and **ask for approval before committing**. Record material design choices in `docs/ADR/`.
- Use Codex Agent Skills progressively: invoke only the skill appropriate to the current task; do not install or load every skill at once. `AGENTS.md` should be established after spec approval to capture persistent project rules.


## Testing Strategy

- Unit and API tests: file validation, parsing, OCR/page provenance, table/cell metadata, chunking, indexing/deletion, retrieval, citations, evidence indicator and saved chats.
- Mock Ollama for routine tests; add local manual smoke tests for text PDF, scanned PDF, DOCX, XLSX, CSV, TXT, unsupported questions, multi-file questions, and restart persistence.
- Benchmark memory, CPU latency, extraction fidelity, source-location correctness and local-only traffic.

## Boundaries

- **Always:** local processing, untrusted-document isolation, source-grounded answers, explicit abstention, citations, evidence support signals, user-approved commits.
- **Ask first:** file size limits, OCR language, visual chart reasoning, parser/embedding model selection, major dependencies, deletion semantics, LAN access.
- **Never:** hosted inference/embeddings, executing document instructions/macros, fabricated citations, multi-user auth or MCP actions in Stage 1.

## Success Criteria

- One local user can upload supported files into chats and the reusable library, ask grounded questions, and reopen saved conversations.
- Agreed text and scanned PDF samples yield traceable page references; tables/images retain references even if semantic image understanding is limited.
- Source citations and an interpretable evidence indicator appear; internal evaluation metrics are recorded.
- All tests and demo pass; user explicitly approves Stage 2.

## Open Questions

- Maximum file size/count/library volume; OCR languages; whether chart/diagram semantics are needed; deletion and retention semantics; final frontend choice.

## Agent Skills and Tool Evaluation Checkpoints

**Rule:** Each checkpoint is a `PLAN.md`/`TODO.md` task. Ask the user before installing an optional tool, benchmark it on representative samples, record the outcome in `docs/benchmarks/` or an ADR, and retain it only if it improves the project. Never silently add a tool to production.

| When to try it | Candidate tool / skill | What to test or decide |
|---|---|---|
| Before writing implementation tasks | `@spec-driven-development`, then `@planning-and-task-breakdown` | Review this stage's SPEC, resolve blocking questions, then create atomic PLAN/TODO tasks. |
| Before accepting third-party Agent Skills or external tool instructions | **SkillSpector** | Evaluate as a skill-security inspection option: review skill contents, scripts, permissions, trust boundaries, and any external calls. Do not treat its report as a security guarantee; verify availability and usage before adoption. |
| During document ingestion/parser spike | **Microsoft MarkItDown** | Compare against format-specific libraries on PDF, DOCX, XLSX, CSV, TXT, scanned PDFs and tables. Measure extraction fidelity, provenance, OCR compatibility, installation size and offline operation. |
| When deciding on UI implementation | **UI UX Pro Max** | Try as a design/workflow aid for accessibility, upload flows, citation previews and chat UX. Review generated assets/code and check licensing; not a required runtime dependency. |
| When implementing and testing tasks | `@incremental-implementation`, `@test-driven-development`, `@code-review-and-quality` | Apply one relevant skill at a time; run tests and review changes before requesting commit approval. |
| When Codex context grows or a task boundary is reached | Codex `/status`, `/compact` | Check usage/status and compact only after saving important decisions, active tasks, and test results in repository files. |
| At dependency or tool-review milestones | **RTK**, **ponytail** | User-mentioned experimental tools: verify their exact repositories, purpose, license, platform support and security model before proposing a trial. Do not infer features from the names. |


### Stage 1 tool trials

1. **Before parser implementation:** benchmark MarkItDown versus PyMuPDF, python-docx, openpyxl/CSV parsers and local OCR on a representative fixture set. Compare page/sheet/row provenance, tables, scanned pages and images; select the smallest adequate combination.
2. **Before trusting downloaded Agent Skills:** try SkillSpector as an additional review, then manually inspect any shell scripts, file access and outbound requests.
3. **During first web UI implementation:** trial UI UX Pro Max for layouts and accessibility; review output before use.
4. **During Codex setup:** try `/status` to inspect the session and `/compact` only at sensible task boundaries. Review RTK and ponytail only after identifying their exact projects and proposed benefits.


## Agent Skills Execution Workflow

1. **Specification review:** use `@spec-driven-development` to review this document and resolve blocking open questions. Do not start implementation before explicit approval.
2. **Task planning:** use `@planning-and-task-breakdown` to produce atomic `PLAN.md` and `TODO.md`, including dependency/tool spikes and acceptance tests.
3. **Implementation:** use `@incremental-implementation` and `@test-driven-development` for one small task at a time. Use `@frontend-ui-engineering` or `@api-and-interface-design` when relevant.
4. **Review and security:** use `@code-review-and-quality` at task boundaries; add `@security-and-hardening` for file ingestion, trust boundaries and Stage 3 authorization.
5. **Documentation and approval:** update README and ADRs, present diff/test evidence, ask before Git commit, and wait for explicit approval before entering the next stage.

## Carried-Forward Decisions and Stage Gate

This section incorporates the user's clarifications and supersedes conflicting provisional assumptions elsewhere in this draft.

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
1. The initial file list is PDF, DOCX, XLSX, CSV, and TXT. Confirm whether legacy DOC/XLS, PPTX, email formats, and other office formats are required before adding parsers.
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

### Remaining Stage 1 decisions
- Confirm maximum file size, number of files per conversation, and total library size.
- Confirm required OCR languages (English only, or additional languages).
- Confirm whether embedded charts/diagrams need semantic interpretation in Stage 1 or whether traceable extraction/OCR is sufficient.
- Confirm the deletion and retention behavior for documents referenced by saved conversations.

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

## Approved T01 clarifications

These explicit user decisions supersede the corresponding open questions above; other requirements and approval gates remain in force.

- **Limits:** 100 MB per file, 10 files per upload/conversation, and 1 GB of library originals. Derived-data/storage budgets and exact enforcement/counting details are reviewed before implementation. Benchmark findings do not silently reduce these approved limits.
- **OCR:** English only.
- **Frontend:** Minimal locally served HTML/CSS/JavaScript. Use Design 1 as the primary landing-page reference and Design 2 for chat, citations and the evidence panel. A frontend framework requires separate review/approval.
- **Performance decision timing:** Set final speed/memory targets after initial local benchmarks, before model/architecture adoption. Agree bounded trial budgets first; initial measurements are exploratory. Quality/evaluation thresholds need agreement before applicable acceptance evaluations.
- **Chat deletion:** Delete the conversation's exclusive attachments; preserve reusable library documents and content still required by other references. Historical citation/message and derived-artifact retention details remain to be settled.
- **Data charts/diagrams:** Approve a bounded local feasibility evaluation before deciding runtime support. Use an agreed English-labelled sample set to assess trends, comparisons, labelled values and data-diagram relationships, with real document/page/chart-region or sheet references where available. Compare structured data/labels/OCR with a local visual approach only after exact trial provisioning is approved. Check against manual ground truth, disclose approximate readings and abstain when unsupported. Measure correctness/grounding, citation support, cold/warm latency and total memory pressure on the target CPU-only 16 GB machine. Exact types, thresholds and trial budget are agreed first. No universal visual-understanding guarantee, cloud processing or automatic model/dependency adoption is authorized. The reviewed detail is in `docs/proposals/chart-interpretation.md`; runtime implementation/acceptance tasks require a separate adoption decision after results.
- **Referenced library deletion:** Warn and block deletion while saved conversations reference the library document. This interim Stage 1 rule is approved. SQLite history and document IDs/references remain Stage 1 requirements; more advanced deletion/citation handling may be considered later. Historical citation/message, detached-reference and derived-artifact retention details must be agreed before lifecycle implementation.
