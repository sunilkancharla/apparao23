# Session 2 — Backend Session Summary

Updated: **20 November 2026**. Scope: **T18–T22**, from commit **0658bea** through **57973a6**, including T19's documentation follow-up **a51900c**.

## 1. Session Overview

This session began building the backend foundations selected during the [research session](SESSION_1_Research_Session_SUMMARY.md). The goal was to prepare reliable building blocks before implementing document uploads and chat.

The work verified the existing Python environment, added a local startup/diagnostics server, created SQLite ownership storage, defined source-location models, and built reproducible test documents with a shared test budget.

**T18–T22 are implemented and committed.** These are backend foundations, not the complete document assistant. Uploads, application parsing, retrieval, real model integration, answers, citations and saved chat still require later tasks. The health endpoint deliberately reports that the application is not ready for model use.

## 2. Task-wise Work and Files

Each task explains the purpose, work completed, verification and limits. Expand its file list for individual descriptions.

**Created** means the file was added in that task's commit. **Updated** means an existing file changed. Shared documentation appears under each task that updated it. Generated documents, databases and previews are described separately; they were not committed.

#### T18 — Establish the approved reproducible Python project

**Summary:** Check that the existing project environment can run the basic backend tools consistently.

**Process:** Reused the dedicated project `.venv`, existing dependencies and lockfile. Added setup tests for the isolated Python environment and the FastAPI/Pydantic/HTTPX combination. Adjusted normal test discovery so historical evaluation scripts are not accidentally run as ordinary tests.

**Outcome:** The development foundation works with the existing pinned packages. No replacement environment, new dependency or model download was needed. The test-only endpoint checks valid input and rejects invalid/missing input; it is not a product API.

**Verification:** Offline lock check passed with **53 locked packages**; **4 setup tests passed**; Ruff lint/format passed. The lockfile and ignore rules remained unchanged. One Starlette warning about its HTTPX test-client integration was retained without suppression or dependency changes.

**Commit:** `0658bea` — Establish T18 project foundations and isolated setup checks.

<details>
<summary>Files associated with T18 (6: 1 created, 5 updated)</summary>

**Tests — Python**

- [tests/test_project_setup.py](../../tests/test_project_setup.py) — **Created.** Checks that tests use the isolated project interpreter and that the API framework, validation library and test client work together.

**Project configuration — TOML**

- [pyproject.toml](../../pyproject.toml) — **Updated.** Sets the ordinary test directory and excludes historical evaluation scripts from automatic discovery.

**Documentation — Markdown**

- [docs/provisioning.md](../provisioning.md) — **Updated.** Records the actual setup checks, commands, warning and environment limits.
- [README.md](../../README.md) — **Updated.** Adds verified foundation commands and describes what they test.
- [PLAN.md](../../PLAN.md) — **Updated.** Records the completed foundation increment and implementation order.
- [TODO.md](../../TODO.md) — **Updated.** Records T18 acceptance evidence and status.

</details>

**Generated/local files:** Existing environment/cache files were reused. No new document fixture or product server was created by T18.

#### T19 — Implement loopback configuration and startup diagnostics

**Summary:** Start a small server on this computer and explain which prerequisites are missing, without downloading or starting models automatically.

**Process:** Added validated configuration for the local application address, Ollama port, managed data directory and asset locations. Added checks for approved local asset identities, writable storage and occupied ports. Implemented a read-only health endpoint with safe responses and restrictions on request Host/Origin headers.

**Outcome:** The supported launcher can start at `127.0.0.1:8000`. Visiting `/api/health` returns a component-status report. Another launch on the same port fails clearly instead of changing ports, killing another process or attaching to an unknown service. The app does not connect to or launch Ollama in this task.

**Verification:** The full suite reached **36 passed, 1 skipped, 1 warning**; Ruff passed. Tests included actual Python server startup, occupied-port refusal, missing prerequisites, safe errors and checks that captured output did not contain the synthetic question/private path. A deliberately inverted Host check caused its test to fail, confirming that the guard is exercised.

**Limit:** Health remains **HTTP 503 / `ready: false`** until later owned-model integration. Asset checks are a startup snapshot, so changed prerequisites require a restart. The skipped test needs Windows symlink-creation permission; a separate reparse-attribute test passed.

**Commits:** `e99630a` — Implement T19 loopback startup and safe prerequisite diagnostics; `a51900c` — Record approved T19 closeout and implementation commit.

<details>
<summary>Files associated with T19 (10: 7 created, 3 updated)</summary>

**Application source — Python**

- [app/__init__.py](../../app/__init__.py) — **Created.** Establishes the application package.
- [app/config.py](../../app/config.py) — **Created.** Validates local settings, protects configured paths and probes whether the managed data directory is writable.
- [app/diagnostics.py](../../app/diagnostics.py) — **Created.** Checks approved runtime/model/OCR asset bytes and local port availability without contacting an unknown model service.
- [app/main.py](../../app/main.py) — **Created.** Provides the supported launcher, health endpoint, local request restrictions, security headers and safe HTTP errors.

**Tests — Python**

- [tests/unit/test_config.py](../../tests/unit/test_config.py) — **Created.** Tests defaults, unsafe settings, protected paths, write failures and reparse/symlink checks.
- [tests/integration/test_startup.py](../../tests/integration/test_startup.py) — **Created.** Tests health responses, request restrictions, prerequisite failures, real startup, collisions and log redaction.

**Documentation — Markdown**

- [docs/benchmarks/t19-startup.md](../benchmarks/t19-startup.md) — **Created.** Records implementation, actual checks, findings and remaining limits.
- [README.md](../../README.md) — **Updated.** Documents startup, environment settings, diagnostics and test commands.
- [PLAN.md](../../PLAN.md) — **Updated.** Records the T19 execution point and later work.
- [TODO.md](../../TODO.md) — **Updated.** Records completed checks, evidence and approval.

</details>

**Generated/local files:** Temporary startup-test directories and synthetic prerequisite files stayed outside Git. The configured managed root is probed when the app starts; T19 did not create a working document/chat database or install models.

#### T20 — Persist minimal ownership and conversation references

**Summary:** Store which conversation owns or references each document, while keeping shared content separate from access to it.

**Process:** Added a small, versioned SQLite schema for content identities, conversations, logical documents and references. A library document can be referenced by multiple conversations. An exclusive attachment belongs to one conversation. Equal content hashes can share one metadata identity without merging document/reference identities or conversation visibility.

**Outcome:** Backend methods can create conversations, register library documents, create exclusive attachments and resolve/list references within a conversation. Reattaching the same library document to the same conversation returns its existing reference. Database constraints enforce ownership, unique membership and the ten-reference limit.

**Verification:** Added **21 storage tests**; the full suite reached **57 passed, 1 skipped, 1 warning**; Ruff passed. Tests covered rollback, reopen, uniqueness, conflicting metadata and scope isolation. A child process committed a reference, began another write and exited without cleanup: reopening preserved the committed reference, removed the uncommitted write and returned `integrity_check=ok`.

**Review finding:** A database with the correct version but a removed ownership trigger was initially accepted. Opening now checks the actual schema as well as its identity/version. A deliberate scope-filter mutation was also detected by the isolation test.

**Limit:** This is a trusted backend storage interface, not an upload API. It does not publish original files, implement quota reservations, delete documents, store messages or create vectors. Storage is not yet connected to the launcher/HTTP routes. Process-exit recovery is not proof of power-loss durability.

**Commit:** `99dc36e` — Implement T20 scoped document ownership and SQLite persistence.

<details>
<summary>Files associated with T20 (9: 5 created, 4 updated)</summary>

**Storage source — Python**

- [app/storage/__init__.py](../../app/storage/__init__.py) — **Created.** Establishes the local storage package.
- [app/storage/database.py](../../app/storage/database.py) — **Created.** Initializes/opens schema v1, checks database identity/structure, enables foreign keys, requires DELETE journaling/FULL synchronization and provides explicit write transactions.
- [app/storage/documents.py](../../app/storage/documents.py) — **Created.** Implements conversation/document/reference operations and conversation-scoped lookups.

**Tests — Python**

- [tests/unit/test_document_storage.py](../../tests/unit/test_document_storage.py) — **Created.** Exercises real SQLite ownership, constraints, rollback, schema refusal and restart/process-exit recovery.

**Documentation — Markdown**

- [docs/benchmarks/t20-storage.md](../benchmarks/t20-storage.md) — **Created.** Records schema behavior, test evidence, review findings and limits.
- [docs/ADR/0001-stage1-architecture.md](../ADR/0001-stage1-architecture.md) — **Updated.** Explains how the implemented ownership schema maps to the accepted architecture.
- [README.md](../../README.md) — **Updated.** Describes storage methods and their integration limits.
- [PLAN.md](../../PLAN.md) — **Updated.** Records T20 progress and the next task.
- [TODO.md](../../TODO.md) — **Updated.** Records storage acceptance evidence and approval.

</details>

**Generated/local files:** Synthetic `metadata.sqlite3` databases and temporary SQLite recovery/journal files were created in ignored test roots. No database binary was committed.

#### T21 — Implement normalized provenance contracts

**Summary:** Define a common way to describe extracted content and where it came from, so later citations can point back to the right source.

**Process:** Added typed, serializable models for document/extraction identities, passages, tables, image references, parser versions, native/OCR methods, warnings and text mappings. Added PDF page/region, XLSX sheet/cell-range and CSV record/physical-line/column locations.

**Outcome:** The models preserve supplied IDs, hashes, versions and locations through JSON round trips. Missing or coarse information requires explicit limitations instead of invented coordinates. Table cells retain row/column roles, their own locations, stored values and inert formula text. OCR confidence keeps its engine-labelled scale or remains unknown; it is not treated as a probability of correctness.

**Verification:** Added **50 provenance cases**; the full suite reached **107 passed, 1 skipped, 1 warning**; Ruff passed. Tests covered all three formats, Unicode offsets, mixed native/OCR content, duplicate CSV headers, multiline records, merged origins, PDF image regions and invalid metadata/ranges. A missing-formula-cache test found that a warning was not required; that validation was added. A deliberately broken PDF page requirement was detected.

**Limit:** A valid model proves structural consistency, not that a parser located the source correctly or that a quotation/answer is supported. These models do not read documents, run OCR, execute formulas, allocate ownership or implement citations.

**Commit:** `daf10c5` — Implement T21 typed extraction and provenance contracts.

<details>
<summary>Files associated with T21 (8: 4 created, 4 updated)</summary>

**Ingestion contracts — Python**

- [app/ingestion/__init__.py](../../app/ingestion/__init__.py) — **Created.** Establishes the extraction-contract package; it does not execute parsers.
- [app/ingestion/models.py](../../app/ingestion/models.py) — **Created.** Defines immutable Pydantic models for normalized content, provenance, locations, tables, mappings and OCR confidence.

**Tests — Python**

- [tests/unit/test_provenance_models.py](../../tests/unit/test_provenance_models.py) — **Created.** Checks serialization, metadata requirements, source-location rules and relationships using synthetic values.

**Documentation — Markdown**

- [docs/benchmarks/t21-provenance.md](../benchmarks/t21-provenance.md) — **Created.** Records model behavior, negative cases, verification and limits.
- [docs/contracts.md](../contracts.md) — **Updated.** Documents implemented fields, offset conventions, precision rules and trust boundaries.
- [README.md](../../README.md) — **Updated.** Explains the provenance models in the implemented backend.
- [PLAN.md](../../PLAN.md) — **Updated.** Records T21 progress and implementation order.
- [TODO.md](../../TODO.md) — **Updated.** Records provenance acceptance evidence and approval.

</details>

**Generated/local files:** Provenance examples were synthetic Python/JSON values used in tests. T21 did not generate source PDFs/workbooks or create an extraction database.

#### T22 — Build the reproducible local fixture harness

**Summary:** Generate repeatable test documents and fake model responses, and limit the resources used by the supported routine test processes.

**Process:** Added factories that load approved authored definitions, generate deterministic CSV/XLSX/PDF fixtures and record hashes/expected facts. Added in-memory Ollama responses and a shared session meter for admitted child-process starts, generated artifacts and captured output. Existing startup/storage regression children use that same meter.

**Outcome:** Tests can exercise native/scanned/mixed PDFs, tables, workbook formulas with missing cached values, merged cells, quoted/multiline CSVs and hostile instruction text without opening private originals or running a model. Output is restricted to ignored project roots and existing files are not overwritten. Historical excluded formats and separate chart trials are not materialized.

**Empty-page decision:** The approved blank image-only second scan page is an **empty-page control**. It tests absence of evidence; it does not replace a test with visible but illegible text. Actual illegible-text/OCR behavior remains unverified. Scoring flags remain unchanged.

**Verification:** Added **16 harness tests**; the final suite reached **123 passed, 1 skipped, 1 warning**; Ruff passed. Repeated fixture generation produced identical bytes, hashes and ground truth. All **seven PDF pages** were rendered and visually checked. The final meter recorded **6/64 starts** and **262,980/2,000,000 retained artifact/output bytes**, within the 120-second child/admission boundary.

**Review finding:** PDF rendering indirectly requested a Windows version-query process. The initial meter refused it. Only the exact read-only `ver` probe was then admitted and charged; arbitrary shell commands were not enabled. A deliberately weakened start-limit check was detected by its test.

**Limit:** The meter covers this routine suite's supported children, not arbitrary native/model process trees or malicious descendants, and cannot stop a hung pure-Python controller test. Mock model responses are not model-quality evidence. Fixture reading/rendering is not an application ingestion pipeline or an OCR accuracy benchmark.

**Commit:** `57973a6` — Implement T22 reproducible fixtures and shared test execution budget.

<details>
<summary>Files associated with T22 (10: 7 created, 3 updated)</summary>

**Test support and fixture programs — Python**

- [tests/__init__.py](../../tests/__init__.py) — **Created.** Makes local test-support imports unambiguous.
- [tests/conftest.py](../../tests/conftest.py) — **Created.** Supplies the shared session budget, wraps supported child launches and defaults generated tests to a fresh ignored project directory.
- [tests/fixtures/__init__.py](../../tests/fixtures/__init__.py) — **Created.** Establishes the authored fixture-support package.
- [tests/fixtures/budget.py](../../tests/fixtures/budget.py) — **Created.** Implements sticky admission/output limits, bounded pipe capture and owned-child deadline/cleanup behavior.
- [tests/fixtures/factories.py](../../tests/fixtures/factories.py) — **Created.** Loads authored definitions, builds deterministic files/ground truth and provides network-free Ollama mocks.

**Tests — Python**

- [tests/unit/test_eval_fixtures.py](../../tests/unit/test_eval_fixtures.py) — **Created.** Checks reproducibility, document structure, safe output paths, mock responses, budget refusal and PDF renders.

**Documentation — Markdown**

- [docs/benchmarks/t22-fixtures.md](../benchmarks/t22-fixtures.md) — **Created.** Records fixture contents, budget accounting, visual checks, the empty-page decision and remaining gaps.
- [README.md](../../README.md) — **Updated.** Documents fixture generation, current commands and budget limitations.
- [PLAN.md](../../PLAN.md) — **Updated.** Records T22 completion evidence and the next task.
- [TODO.md](../../TODO.md) — **Updated.** Records fixture/budget acceptance evidence and approval.

</details>

**Generated/local files — excluded from Git:**

- `S-CSV.csv` and `S-CSV-INJECTION.csv` — Authored CSV test documents.
- `S-XLSX.xlsx` — Workbook with multiple sheets, a formula lacking a cached value and a merged range.
- `S-PDF-NATIVE.pdf`, `S-PDF-SCAN.pdf` and `S-PDF-MIXED.pdf` — Native-text, image-only and mixed-page PDF fixtures.
- `truncated.pdf`, `mismatch.xlsx` and `invalid.csv` — Deliberately invalid inputs for later validation checks.
- `ground-truth.json` — Expected facts, artifact hashes, sizes and control limitations.
- Seven page PNGs and a local contact-sheet PNG — Visual-review outputs; not proof of OCR/answer quality.
- Temporary regression databases and a local setup-marker debug log — Local test/setup artifacts, also excluded.

The existing [tests/evals/manifest.json](../../tests/evals/manifest.json) and [tests/evals/questions.json](../../tests/evals/questions.json) were reused, not changed or created in T22. Private originals, generated documents, model assets and runtime data were not added to Git.

## 3. Verification Progress

| Task | New ordinary test cases | Full-suite result at closeout | Commit |
|---|---:|---|---|
| T18 | 4 | 4 passed; one warning | `0658bea` |
| T19 | 33 | 36 passed, 1 skipped, 1 warning | `e99630a` + `a51900c` documentation |
| T20 | 21 | 57 passed, 1 skipped, 1 warning | `99dc36e` |
| T21 | 50 | 107 passed, 1 skipped, 1 warning | `daf10c5` |
| T22 | 16 | 123 passed, 1 skipped, 1 warning | `57973a6` |

T19's 33 added cases comprise 32 passes and the one skipped symlink test. The skipped test needs a Windows privilege unavailable in this session; reparse-attribute rejection was tested separately. The retained warning concerns Starlette's HTTPX test-client integration. Neither is a claim that model or document quality has been validated. Ruff lint and format checks passed for each task.

These results are recorded historical checks, not new runs performed to write this summary. Temporary mutations deliberately broke selected guards to confirm their tests failed; all original source bytes were restored before closeout.

## 4. Current Status and Next Step

**Implemented:** isolated setup checks, a local diagnostics server, scoped SQLite ownership storage, typed provenance contracts and a reproducible fixture/mock/budget harness. Across these tasks, Git records **24 new authored files** and updates to **7 existing files**: **31 distinct files**, with shared documentation listed under each task that changed it.

**Still to integrate:** validated uploads, quota/idempotency handling, application parsing, OCR, embedding/indexing, retrieval, local answer generation, citations, saved chat and the browser UI. No new dependency was added during T18–T22, and this session did not rerun historical model/OCR evaluation packages or prove final Stage 1 acceptance.

The next implementation task is **T23 — Upload a validated CSV conversation attachment**, under its applicable authorization and the T20–T22 review gate. T23 has not started at this summary's boundary. This summary changes no product behavior, stage, approval or existing historical summary.
