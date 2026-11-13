# Stage 1 Atomic Task Checklist

**Status:** T01–T03 and T05 complete; T04 explicitly deferred. T05 closes with approved PyMuPDF comparison deferral. **Prepared:** 2026-11-13 (Asia/Calcutta).

**Authority:** Approved SPEC, AGENTS and PLAN. T04 closes by user-approved optional-tool deferral; T05 permissive trial was authorized after licensing review; T06 is excluded from Stage 1; T07–T50 and proposed T02R/T07A/T16A are unstarted.

## Proposed scope-alignment revision — 2026-11-13

User approved PDF/XLS/XLSX/CSV only for this stage. DOCX/TXT are excluded entirely from Stage 1; later inclusion requires explicit user approval. T05 is committed in d8d12e7. Completed task history and original fixture ground truth are retained. The following changes are proposed for review: T02R active-corpus refresh, T06 exclusion, T07 XLSX/CSV, new T07A XLS, CSV-first T23–T34, T37 XLS and T39 CSV robustness. No new trial or installation is authorized by this revision.

### T02R — Align active evaluation coverage with the four-format scope

**Status:** Proposed; first next task after review. **Prerequisites:** Approved format amendment and reviewed task revision. **Scope:** M, definition-only.
**Objective:** Keep scores and fixture coverage faithful to PDF/XLS/XLSX/CSV without losing historical ground truth.

- [ ] Keep DOCX/TXT fixture/question definitions excluded from Stage 1; exclude them from active scoring and materialization and migrate the injection scenario to an in-scope artifact without changing its expected safety behavior.
- [ ] Specify an XLS fixture with sheet/cell/merged-header/stored-value anchors and invalid/protected/macro/external-link cases; document missing real XLS samples and an approved materialization path before trials. Reuse checked CSV questions for the first vertical slice.

**Verification:** Validate JSON references, active/excluded selection and format coverage; review new gold anchors and scoring denominators. No document generation, dependency installation or model evaluation.
**Evidence:** Pending — revised manifest/questions/evaluation design and consistency checks.
**Likely files:** `tests/evals/manifest.json`, `tests/evals/questions.json`, `docs/evaluation.md`.

## Checklist conventions and completion rules

- User authorized T03 closeout and read-only T04 review, then explicitly declined SkillSpector. T05 review and permissive trial were authorized. Replying “ok, next step please” to the explicit closeout/commit question approves PyMuPDF comparison deferral, the T05 commit and initially T06 review; later user instructions supersede that next step by excluding DOCX/TXT from Stage 1 and revising formats. G1–G4 and D01–D09 still govern later work; no runtime adoption or T06 installation is authorized.
- Record explicit task authorization before starting, then work on one task at a time. All required prerequisites/decisions must be satisfied. Plan approval alone does not authorize installs, trials, component adoption, commits, or every subsequent task.
- Every task includes G3: relevant skill verification, actual evidence, quality/security review as applicable, README/PLAN/TODO updates, readable diff, commit question, and next-task authorization. Existing permission persists for its approved scope.
- Scope S means normally 1–2 substantive files; M means 3–5, plus routine README/PLAN/TODO updates. Likely paths are proposals, not instructions to create empty modules. Re-split before work if a task exceeds one focused session/five substantive files.
- Code tasks use test-first development: meaningful failing test, smallest passing change, refactor, focused pytest plus relevant regression checks and Ruff. Mock Ollama in routine tests; label actual local model/OCR smoke results separately. Validate commands after approved setup, normally `uv run pytest <listed-test-path>`, `uv run ruff check .`, `uv run ruff format --check .`.
- Every trial first verifies exact upstream/version/artifacts, alternatives, license/transitive/native obligations, maintenance/security, permissions/network behavior, Windows/CPU support, RAM/disk and offline assets. G1 permission is required before optional installation/download/execution; G2 adoption is separate. Use only approved local non-sensitive fixtures.
- Evidence is pending for every task. Before completion, attach actual dated commands/results, red/green or experiment records, fixture/artifact/configuration identity, report links, limitations and user decisions. Do not fabricate test passes or benchmark outcomes. Documentation uses consistency/link/diff review.
- Statuses after authorization: Ready, In progress, Blocked (state why), Verified — awaiting review, Complete. Optional evaluations may conclude unavailable/rejected/deferred only with recorded user agreement and an explicit fallback. Essential Stage 1 behavior cannot silently be deferred away.
- Checkpoints after every 2–3 tasks review accumulated evidence and unresolved blockers. Verify `/status` availability; persist task/decision/test state before `/compact` when needed. No automatic commits, stage transitions or parallel agents.

## M0 — Decisions, investigations and design approval

### T01 — Resolve blocking Stage 1 decisions

**Status:** Complete — approved decisions/deferrals recorded and reviewed. **Prerequisites:** G0 and task authorization satisfied by the user's approval and direction to T01. **Scope:** S.
**Objective:** Obtain concrete product/resource/lifecycle choices before dependent trials or implementation.

- [x] Record D01–D09 answers and approval references, or explicit deferrals with the exact downstream blocker; do not infer file limits, OCR languages, visual semantics, retention, UI choice or quality/resource budgets.
- [x] Preserve confirmed library/reference invariants and identify any proposed SPEC amendment for separate approval; distinguish plan approval from provisioning/adoption permission.

**Verification:** Review the decision matrix/options with the user and trace every unresolved item to blocked tasks.
**Evidence:** `docs/decisions.md` and SPEC's T01 clarification record approved choices; the user explicitly confirmed downstream allocation and authorized T02 (“yes please”). Invariants/approval boundaries reviewed; deferred work remains gated. No application tests apply to decision recording; no commit authorized.
**Likely files:** `docs/decisions.md`; SPEC only for an exact later-approved amendment.

### T02 — Define representative fixtures and evaluation rubric

**Status:** Complete — user approved the fixture/rubric design (“good”) and review proceeded to T03. **Prerequisites:** T01 complete; T02 authorized. **Scope:** M, design only.
**Objective:** Establish a compact approved corpus and measurable acceptance examples before tool selection.

- [x] Specify five-format samples, native/scanned/mixed PDFs, tables/images, DOCX structure, multi-sheet/cached-formula workbooks, quoted/encoded CSV/TXT and invalid/protected/resource/injection cases with expected source anchors.
- [x] Define answerable/unanswerable/multi-file/ambiguous/table questions, relevance/grounding/citation/refusal rubrics and approved thresholds; keep user/generated document files out of version control.

**Verification:** Manually trace expected answers/locations to approved samples; review permissions, hashes, safe manifests and missing-sample blockers.
**Evidence:** User approved design/rubric (“good”). `docs/evaluation.md` and the two evaluation JSON files contain nine hashed originals, nine authored definitions, sixteen negative cases and nineteen questions; Q01–Q06 CSV ground truth checked locally. Artifact generation/verification remains T22, PDF/workbook content unverified/excluded until inspected. JSON/hash/anchor checks passed; no parser/model/application test or benchmark ran. No commit authorized.
**Likely files:** `docs/evaluation.md`, `tests/evals/manifest.json`, `tests/evals/questions.json`; no generated binary documents.

### T03 — Review the actual host and dependency/provisioning proposals

**Status:** Complete — host/dependency review and explicitly authorized project baseline verified. Later tool/model artifact approvals remain with their individual G1 tasks. **Prerequisites:** T01–T02 complete; project-local setup authorized. **Scope:** Review plus explicit provisioning exception.
**Objective:** Establish actual environment constraints and exact installation proposals without installing anything implicitly.

- [x] Read CPU/RAM/disk/OS, Python/uv/Ollama/local-model inventory; review baseline FastAPI/Uvicorn/HTTPX/pytest/Ruff and required transitive/native assets against PLAN's dependency fields.
- [x] Validate proposed PowerShell commands/loopback endpoints and present exact versions/artifacts/downloads/commands/resource budgets for each G1 approval; include model/language assets and optional evaluation environments.

**Verification:** Read-only host checks and primary-source license/security/compatibility review; record which concrete next trials are authorized.
**Evidence:** User replaced the loose-tool proposal with dedicated `.venv` installation of the reviewed baseline. CPython 3.14.6 isolation, uv 0.13.8 publisher checksum, 24 locked distributions, imports/tool versions, project cache, offline lock/sync and ignore rules verified. `pyproject.toml`, `uv.lock` and `docs/provisioning.md` record exact setup. Global packages untouched. Target stays 16 GB/CPU-only; Ollama/models/OCR not installed. Later artifact/adoption/privacy/advisory checks remain gated; no application tests/benchmarks or commits.
**Likely files:** `docs/dependencies.md`, `docs/provisioning.md`, `docs/benchmarks/environment.md`.

**Checkpoint CP01 — T01–T03:** Proposed. Review blockers, safe fixture/rubric design and exact trial proposals; obtain scoped G1 approvals before downloads. Apply G3; no product implementation.

### T04 — Evaluate SkillSpector and manual skill-review process

**Status:** Complete — optional tool deferred by explicit user decision; no trial/adoption. **Prerequisites:** T03 complete; user declined further SkillSpector work. **Scope:** Read-only identification and decision record.
**Objective:** Assess SkillSpector before acceptance of additional third-party skills/instructions.

- [ ] Verify repository/version/license, scripts/permissions/outbound calls, Windows support and footprint; compare an approved benign/suspicious local skill fixture with manual review.
- [ ] Record useful findings, false positives/missed risks and adopt/reject/unavailable/defer decision; review next-needed skill instructions/scripts manually regardless of scan outcome.

**Verification:** Reproduce the bounded trial and manually inspect findings; a clean report is not a security guarantee. Do not preload/execute all skills.
**Evidence:** `docs/benchmarks/skillspector.md` records partial upstream/source review and the user's “then do not bother about it” decision. Scanner/fixture/performance checks were not run; the original trial acceptance checkboxes remain unchecked. This task closes via the explicit user-approved optional-tool deferral rule. Relevant local workflow instructions were manually reviewed; no scanner/scripts/dependencies installed or executed.
**Likely files:** That report and at most two local fixture/evaluation aids; no unreviewed skill scripts executed.

### T05 — Compare native PDF parsers

**Status:** Complete with user-approved PyMuPDF empirical-comparison deferral. **Prerequisites:** T02–T04; permissive trial authorized after licensing review. **Scope:** M.
**Objective:** Measure native PDF text/table/image provenance and error/resource behavior.

- [x] Compare a bounded viable candidate set on text/mixed/blank pages, tables/regions and image references, retaining warnings/parser-version and golden page anchors.
  - pypdf/pdfplumber compared on controlled/native/image/blank/table/column fixtures and three reports; PyMuPDF metadata reviewed only. User approved deferring its empirical comparison at closeout. This is an explicit evaluation exception to the original benchmark sequence, not evidence of a PyMuPDF trial or a runtime selection; SPEC remains unchanged.
- [x] Measure time/RAM/footprint/offline behavior and malformed/protected/resource-boundary handling for the authorized permissive subset; document license/native dependency tradeoffs and unavailable precision, with explicit sampling/security limitations.

**Verification:** Run identical PDF samples, compare expected structure/locations and inspect failures; no adoption inferred from trial installation.
**Evidence:** `docs/benchmarks/pdf-parsers.md`: nine trial packages installed only in project .venv, baseline pins unchanged; 24 final sample runs, 48/48 limited fact checks, five passing tests, memory/timeout/socket-denial controls, offline frozen sync/lock checks and warning/layout/OCR limits. No runtime adoption. Real-report table coverage and full-report resources remain gaps; T08/T09/T17 must address them before adoption. Resource/offline evidence is bounded by the host sandbox, not a final disconnected application gate. User accepted closeout/deferral and authorized its commit on 2026-11-13.
**Likely files:** That report and at most three bounded evaluation files under `tests/evals/spikes/`.

### T06 — Retired: DOCX excluded from Stage 1

**Status:** Removed from Stage 1 scope at the user's explicit request; not completed or awaiting execution. This identifier is retained only to preserve task history. There are no Stage 1 acceptance criteria, files, dependencies, installation or trial actions for this task. Any later-stage DOCX/TXT support requires a new user-approved scope and plan.

**Checkpoint CP02 — T04–T06:** Proposed. Review skill trust and PDF closeout; record DOCX exclusion and four-format revision, especially locations, licenses and local-only paths. Apply G3; approve the next trial separately.

### T07 — Compare XLSX and CSV extraction baselines

**Status:** Proposed. **Prerequisites:** T02–T04, T02R; exact trial approved under G1. **Scope:** M, bounded shared fixture trial.
**Objective:** Establish structured local tabular/text baselines with minimal dependencies.

- [ ] Compare viable XLSX handling including openpyxl as a candidate with standard-library CSV paths; retain sheets/cells/records/columns/headers/physical-line spans, quoted cells and encoding warnings.
- [ ] Evaluate merged headers, formula/cached values without execution, external links, protected/invalid inputs and approved memory boundaries; record fidelity, resource, license and offline tradeoffs.

**Verification:** Compare expected cell/range/record and physical-line anchors and values on the fixed small corpus; disclose missing cached values and unsupported encodings.
**Evidence:** Pending — `docs/benchmarks/tabular-text-parsers.md` and local measurements.
**Likely files:** That report and at most three evaluation files.

### T07A — Compare legacy XLS parsers

**Status:** Proposed. **Prerequisites:** T02R, T03–T04, T07; exact trial provisioned only after G1 approval. **Scope:** M.
**Objective:** Establish a local binary XLS extraction path independently of XLSX.

- [ ] Review a bounded candidate shortlist, including license, maintenance/advisories, Windows/Python compatibility, native/transitive dependencies, footprint and offline behavior; compare against a justified alternative before choosing.
- [ ] Use fixed golden sheets/cells/stored values, merged/header context and date types; measure time/RAM, errors/protected/invalid files and honest missing-cache warnings. Never execute formulas, macros, embedded content or external links; reject mislabeled unsupported workbooks.

**Verification:** Bounded local comparison with fixture hashes, golden value/anchor checks and negative/network/resource controls. No runtime adoption inferred.
**Evidence:** Pending — `docs/benchmarks/xls-parsers.md`, exact trial proposal and measured comparison. Real XLS sample coverage is currently unverified.
**Likely files:** That report and at most three evaluation aids.

### T08 — Evaluate Microsoft MarkItDown against format-specific baselines

**Status:** Proposed. **Prerequisites:** T05, T07, T07A; T06 explicitly excluded; exact MarkItDown configuration/install approved under G1. **Scope:** M.
**Objective:** Determine whether MarkItDown improves the project enough to justify dependencies and provenance tradeoffs.

- [ ] Compare identical PDF/XLS/XLSX/CSV samples for fidelity, tables, page/sheet/row anchors, scans/images, OCR integration needs, time/RAM and install footprint against T05/T07/T07A.
- [ ] Inspect plugin/LLM/remote-processing paths and verify the trial stays local; document limitations and ask adopt/reject, with OCR integration measurements completed in T09.

**Verification:** Produce side-by-side results and manually trace output to original locations; no cloud text/image conversion paths allowed.
**Evidence:** Pending — `docs/benchmarks/markitdown.md`, exact configuration and user decision.
**Likely files:** That report and at most two comparison aids.

### T09 — Compare local OCR and scanned/mixed-PDF paths

**Status:** Proposed. **Prerequisites:** T05, T08; D02/D03; approved rendering/OCR/language assets under G1. **Scope:** M.
**Objective:** Measure a viable local OCR path without assuming language or chart semantics.

- [ ] Compare a Tesseract-based option with another viable Windows/CPU alternative on approved scans/mixed pages/languages; retain native/OCR distinction, page/region/image references and confidence/warnings where available.
- [ ] Measure accuracy against ground truth, page time, peak RAM, renderer/language footprint and offline behavior; test native-parser/MarkItDown integration where viable and propose bounded processing settings.

**Verification:** Golden page/OCR text checks, low-quality/missing-language/error cases and local-only observation; missing assets must not trigger downloads.
**Evidence:** Pending — `docs/benchmarks/ocr.md`, artifact/licenses and adoption proposal.
**Likely files:** That report and at most three local evaluation files.

**Checkpoint CP03 — T07–T09:** Proposed. Review the four-format comparison and any unsupported XLS path and OCR evidence/languages/visual limits. Record tool decisions; no parser product code before G2. Apply G3.

### T10 — Benchmark local Ollama embedding candidates

**Status:** Proposed. **Prerequisites:** T02–T04; D06; approved exact models/downloads under G1. **Scope:** M.
**Objective:** Measure retrieval usefulness and embedding resource cost on the actual CPU-only machine.

- [ ] Trial `embeddinggemma` as a candidate and a justified approved alternative; record digest/license/dimensions/settings/input limits/truncation and query/document consistency.
- [ ] Use fixed fixture/questions and approved cold/warm repetitions to measure batch throughput, relevance/recall at chosen k, RAM/disk and latency against D06; do not select defaults yet.

**Verification:** Reproduce PLAN's actual-machine protocol using bounded reference search, retain failed runs and model-change reindex implications.
**Evidence:** Pending — `docs/benchmarks/embeddings.md`, raw measurements/settings and recommendation.
**Likely files:** That report and at most three evaluation files.

### T11 — Benchmark local Ollama chat candidates

**Status:** Proposed. **Prerequisites:** T09–T10; approved exact chat models/downloads under G1. **Scope:** M.
**Objective:** Find practical evidence-grounded CPU chat settings within the 16 GB workstation budget.

- [ ] Compare `qwen2.5:3b` as a candidate with another approved model/size on fixed evidence/questions/settings; record digest/quantization/context, load/first-token/full-answer latency, token rate and variation.
- [ ] Score grounding/citation/refusal/ambiguity/multi-file/table/history cases; measure combined system/Ollama/evaluation/OCR memory pressure and model-load/unload contention before recommending context/batch/concurrency limits.

**Verification:** Actual-machine repeated trials against D06 using the approved rubric; report failed/slow/memory-pressure cases instead of cloud fallback.
**Evidence:** Pending — `docs/benchmarks/chat-models.md`, raw results and recommendation.
**Likely files:** That report and at most three evaluation files; reuse measurement aids where possible.

### T12 — Compare local vector storage and consistency strategies

**Status:** Proposed. **Prerequisites:** T10–T11; D01/D04; exact optional index trial approved under G1. **Scope:** M.
**Objective:** Retain SQLite metadata/history while selecting the smallest adequate local vector approach.

- [ ] Compare a simple local vector representation with a justified index-library alternative at approved volume using approved embeddings; measure ranking, query/index time, RAM/disk and offline/Windows behavior.
- [ ] Demonstrate restart, remove, rebuild, deduplication and versioning plus SQLite/file/index consistency after interruption; propose identity/reference/reconciliation boundaries without guessing retention.

**Verification:** Repeat insert/query/restart/remove/rebuild and failure-injection cases; compare integrity and resource/quality outcomes.
**Evidence:** Pending — `docs/benchmarks/storage-index.md` and recommended consistency strategy.
**Likely files:** That report and at most three evaluation files.

**Checkpoint CP04 — T10–T12:** Proposed. Review actual CPU/RAM/quality/latency evidence and feasibility. Return unmet budgets for a user decision; no model/index adoption without G2. Apply G3.

### T13 — Identify and evaluate the intended RTK project

**Status:** Proposed. **Prerequisites:** T01, T03–T04; D08 identity; approved optional trial under G1. **Scope:** S.
**Objective:** Evaluate only the user-intended RTK project against a concrete developer-workflow need.

- [ ] Confirm repository/version/purpose, license, Windows support, permissions/outbound calls and resource cost before installation; do not infer features from the name.
- [ ] Compare one representative workflow with/without the approved tool and record adopt/reject/defer plus fallback; unresolved identity may conclude only with user-approved deferral.

**Verification:** Inspect the exact artifact and reproduce the bounded local trial or document the agreed deferral.
**Evidence:** Pending — `docs/benchmarks/rtk.md`, measured benefit/risks and user decision.
**Likely files:** That report and at most one non-sensitive fixture description.

### T14 — Identify and evaluate the intended ponytail project

**Status:** Proposed. **Prerequisites:** T01, T03–T04; D08 identity; approved optional trial under G1. **Scope:** S.
**Objective:** Review ponytail independently without assumptions from similarly named tools.

- [ ] Verify exact repository/version/purpose, license, Windows/CPU compatibility, scripts/permissions/outbound behavior and footprint before proposing installation.
- [ ] Run one approved representative workflow/fixture and record adopt/reject/defer decision with manual/native fallback; unresolved identity needs explicit user deferral.

**Verification:** Manually inspect trust boundaries and reproduce the bounded comparison or approved deferral.
**Evidence:** Pending — `docs/benchmarks/ponytail.md`, trial/deferral and decision.
**Likely files:** That report and at most one fixture description.

### T15 — Evaluate UI UX Pro Max before frontend adoption

**Status:** Proposed. **Prerequisites:** T02–T04; D05; exact optional tool/trial approved under G1. **Scope:** M, design aid only.
**Objective:** Evaluate whether the aid improves required local browser flows without selecting a framework implicitly.

- [ ] Verify repository/version, skill/scripts/code/assets licenses, Windows needs and file/network behavior; review generated outputs locally on non-sensitive content.
- [ ] Compare a small chat/upload/library/citation-preview sketch with manual design for keyboard/focus/labels/contrast and loading/empty/error/status states; use supplied images only as references and obtain a tool decision.

**Verification:** Walk the sketches against accessibility/flow criteria and review assets/code before reuse; a trial is not product UI implementation.
**Evidence:** Pending — `docs/benchmarks/ui-ux-pro-max.md`, design notes and adopt/reject/defer decision.
**Likely files:** That report, `docs/ui-design.md`, and at most two sketches.

**Checkpoint CP05 — T13–T15:** Proposed. Review exact optional-tool identities/benefits and UI direction. Document approved deferrals/fallbacks; no automatic runtime additions. Apply G3.

### T16 — Specify retrieval, citations and evidence-support contracts

**Status:** Proposed. **Prerequisites:** T02/T02R, T05, T07/T07A and T08–T12 (T06 excluded); D04/D06. **Scope:** M, design only.
**Objective:** Define measurable grounding behavior and truthful support signals before coding.

- [ ] Specify source-aware chunks, selected-document retrieval, bounded evidence/history, ambiguity/no-evidence handling, citation IDs/location/quote checks and removed-source behavior with expected cases.
- [ ] Approve observable indicator validity/coverage/abstention/warning signals, semantic-support limitations, and internal evaluation thresholds; never equate citation validity with correctness probability.

**Verification:** Walk supported/unsupported/ambiguous/table/multi-file/injection examples through the contract; manually trace expected claims and source anchors.
**Evidence:** Pending — reviewed contract, examples and rubric approvals.
**Likely files:** `docs/retrieval-design.md`, `docs/evaluation.md`, `tests/evals/questions.json`.

### T17 — Present architecture and component-adoption decision pack

**Additional review prerequisite:** Resolve the approved chart-evaluation scope through the proposed T16A investigation below or an explicit user-approved deferral before architecture adoption.

**Status:** Proposed. **Prerequisites:** T01–T16, with only explicit optional-tool deferrals; all blocking decisions resolved. **Scope:** M, review only.
**Objective:** Obtain G2 approval of exact components and interfaces before application implementation.

- [ ] Present benchmark-backed parser/OCR/model/index/UI alternatives and selections, diagram/inventory, ownership/provenance/data-root/API/status/error boundaries, loopback security, retention and interruption/recovery design.
- [ ] Record explicit G2 approval or changes for exact versions/artifacts, contracts/resource budgets and the next task; synchronize PLAN/TODO without silently changing SPEC.

**Verification:** Trace each selected component to license/offline/benchmark evidence and every requirement to planned acceptance checks; a draft ADR alone does not unblock T18.
**Evidence:** Pending — architecture review, ADR and G2 approval.
**Likely files:** `docs/ADR/0001-stage1-architecture.md`, `docs/contracts.md`, `docs/dependencies.md`, `docs/provisioning.md`.

**Checkpoint CP06 — T16–T17 / G2:** Proposed. Stop for architecture/component adoption and authorization of T18. No product code or automatic installation/commit. Apply G3.

## M1 — Minimal tested foundations

### T18 — Establish the approved reproducible Python project

**Status:** Proposed. **Prerequisites:** T17/G2; explicit task/provisioning authorization. **Scope:** M.
**Objective:** Introduce only the environment and tooling needed for the first implementation slice.

- [ ] Create approved `pyproject.toml`, `uv.lock` and local `.venv` with Python 3.11+ and necessary reviewed packages; validate actual Windows commands and dependency inventory.
- [ ] Add ignore rules before staging for runtime/private data, secrets, environments, generated document fixtures and model assets; verify minimal pytest/Ruff operation without empty speculative modules.

**Verification:** Approved uv sync/run workflow, meaningful test/config smoke, Ruff lint/format and ignored-path inspection; do not stage or commit implicitly.
**Evidence:** Pending — actual setup/check commands, versions, lockfile and license review.
**Likely files:** `pyproject.toml`, `uv.lock`, `.gitignore`, one meaningful test-configuration/smoke file.

### T19 — Implement loopback configuration and startup diagnostics

**Status:** Proposed. **Prerequisites:** T18; approved T17 data/network contracts. **Scope:** M.
**Objective:** Start the local app with explicit prerequisites and useful failure behavior.

- [ ] Configure loopback binding/Ollama endpoints and application-data root; keep assets/logging local and sensitive payloads out of logs.
- [ ] Report missing service/models/OCR assets and unwritable paths clearly without silent downloads, external telemetry or cloud fallback.

**Verification:** Test-first mocked config/startup/API failures; actual local start and missing-prerequisite walkthrough, without unapproved provisioning.
**Evidence:** Pending — startup tests, loopback checks and redacted-log review.
**Likely files:** `app/main.py`, `app/config.py`, `tests/unit/test_config.py`, `tests/integration/test_startup.py`.

**Checkpoint CP07 — T18–T19:** Proposed. Review reproducibility, local startup/privacy/error behavior and validated commands; tests/Ruff and docs reflect reality. Apply G3.

### T20 — Persist minimal ownership and conversation references

**Status:** Proposed. **Prerequisites:** T19; approved D04/T17 schema/lifecycle. **Scope:** M.
**Objective:** Establish only the SQLite identities/reference distinctions needed by upcoming uploads.

- [ ] Persist content/document identity, minimal conversations, exclusive/library ownership and references with integrity/uniqueness constraints; shared content identity must not merge visibility.
- [ ] Version/initialize schema and preserve references after restart with transaction rollback on failure; do not prebuild unrelated future message/lifecycle features.

**Verification:** Test-first identity/reference/uniqueness/rollback/reopen cases against approved ownership policy.
**Evidence:** Pending — storage/schema/restart tests and contract review.
**Likely files:** `app/storage/database.py`, `app/storage/documents.py`, `tests/unit/test_document_storage.py`, one schema file if warranted.

### T21 — Implement normalized provenance contracts

**Status:** Proposed. **Prerequisites:** T20; T17 approved interfaces. **Scope:** M.
**Objective:** Preserve exact/coarse source anchors through a common typed extraction representation.

- [ ] Define document/passage/table/image references with stable IDs/hash/extraction version, filename/format, parser/version, native/OCR method, warnings/confidence and format-specific anchors.
- [ ] Validate required metadata and explicit missing/coarser precision; round-trip structured tables/locations without confusing originals and normalized output or inventing anchors.

**Verification:** Test-first model/serialization/invalid-metadata and table/provenance round-trip fixtures for all planned formats.
**Evidence:** Pending — contract tests and reviewed examples/limitations.
**Likely files:** `app/ingestion/models.py`, `tests/unit/test_provenance_models.py`, `docs/contracts.md`.

### T22 — Build the reproducible local fixture harness

**Status:** Proposed. **Prerequisites:** T21, T02. **Scope:** M.
**Objective:** Turn approved fixture definitions into reusable tests without committing private/generated documents.

- [ ] Load stable evaluation manifests; create necessary synthetic document artifacts only in ignored/temporary paths using approved packages and keep private samples separate with ground truth/hashes.
- [ ] Provide representative valid/invalid/native/scanned/table fixtures and mocked Ollama responses so routine tests need neither internet nor a running model.

**Verification:** Repeat fixture generation/loading and compare expected content/anchors; run harness/mock checks and inspect ignored artifacts.
**Evidence:** Pending — reproducibility, coverage and privacy review.
**Likely files:** `tests/conftest.py`, `tests/fixtures/factories.py`, `tests/unit/test_eval_fixtures.py`, `tests/evals/manifest.json`.

**Checkpoint CP08 — T20–T22:** Proposed. Review ownership/provenance/fixture integrity and relevant tests/Ruff before first upload. Apply G3.

## M2 — First usable upload slice: CSV

### T23 — Upload a validated CSV conversation attachment

**Status:** Proposed. **Prerequisites:** T22; D01 and T17 upload/security policy. **Scope:** M.
**Objective:** Provide a safe API path from one local upload to a stored original/reference.

- [ ] Validate CSV extension/content/size/parseability as feasible; use safe server-controlled storage identity, separate display filename and the configured data root under the correct conversation reference.
- [ ] Reject invalid/unsupported/oversized/traversal/unsafe Windows filename cases with useful errors; clean partial/temporary artifacts without exposing paths or sensitive content.

**Verification:** Test-first upload/API/file-boundary tests including mismatches, boundary sizes and interrupted writes; local valid/invalid API smoke and security review.
**Evidence:** Pending — upload tests and original-file/reference trace.
**Likely files:** `app/api/uploads.py`, `app/ingestion/validation.py`, `app/storage/files.py`, `tests/integration/test_uploads.py`, `tests/security/test_upload_paths.py`.

### T24 — Expose batch upload and per-file processing status

**Status:** Proposed. **Prerequisites:** T23; approved processing/concurrency contract. **Scope:** M.
**Objective:** Report each file independently without concealing partial failures.

- [ ] Enforce approved batch/count/resource budgets and persistent per-file queued/processing/ready/failed states, useful errors/warnings and independent successful siblings.
- [ ] Handle retries/interrupted processing consistently under the approved recovery design; never report indexed/ready before the required work is actually complete.

**Verification:** Mixed-success/count-limit/status-transition/retry/restart tests with mocked delays/errors and bounded processing.
**Evidence:** Pending — batch/status/error/recovery results.
**Likely files:** `app/api/uploads.py`, `app/ingestion/processing.py`, `app/storage/documents.py`, `tests/integration/test_processing_status.py`.

### T25 — Extract and preview CSV with record/column provenance

**Status:** Proposed. **Prerequisites:** T24, T21. **Scope:** M.
**Objective:** Complete original upload → structured CSV records → safe source preview.

- [ ] Extract approved CSV dialect/encoding behavior with deterministic record/header/column anchors and physical-line spans (including quoted multiline cells), hash/version/warnings and explicit empty/invalid-content errors; store normalized output separately from originals.
- [ ] Preview bounded escaped text through document IDs and selected references, not arbitrary filesystem paths; disclose any unavailable precision.

**Verification:** Test-first record/column/quoted-multiline/encoding/empty-input/preview escaping/path/scope cases and a local upload-to-source walkthrough.
**Evidence:** Pending — CSV provenance/preview tests and trace to original records/columns and physical lines.
**Likely files:** `app/ingestion/csv.py`, `app/api/sources.py`, `app/storage/extractions.py`, `tests/unit/test_csv_extraction.py`, `tests/integration/test_source_preview.py`.

**Checkpoint CP09 — T23–T25:** Proposed. Demonstrate valid/bad/batch CSV upload, honest status and traceable local preview; review failure cleanup/privacy. Apply G3.

## M3 — First complete grounded-answer path

### T26 — Chunk passages without losing source structure

**Status:** Proposed. **Prerequisites:** T25; T16 chunk/context policy. **Scope:** M.
**Objective:** Produce deterministic bounded chunks with traceable boundaries.

- [ ] Retain document/extraction/chunk identities, hashes, filename/format, exact/coarse locations and warnings under the approved size/overlap/context policy.
- [ ] Preserve table headers/rows and native/OCR markers in contract fixtures; handle empty/oversized passages and cross-boundary evidence explicitly.

**Verification:** Test-first deterministic boundaries/overlap/table/metadata checks and manual trace to expected anchors.
**Evidence:** Pending — chunking tests and golden provenance examples.
**Likely files:** `app/retrieval/chunking.py`, `app/retrieval/models.py`, `tests/unit/test_chunking.py`.

### T27 — Embed through the approved local Ollama model

**Status:** Proposed. **Prerequisites:** T26; approved T10/T17 selection. **Scope:** M.
**Objective:** Add bounded loopback embeddings with explicit model/dimension/error handling.

- [ ] Use only the approved endpoint/model with bounded batches/timeouts and recorded model identity/dimensions; validate missing/invalid/incompatible/truncated responses according to contract.
- [ ] Surface absent service/model, timeout and malformed-response errors without downloads, sensitive logs or remote fallback.

**Verification:** Test-first mocked local HTTP/model/error cases; separately authorized actual-model embedding smoke with non-sensitive text.
**Evidence:** Pending — routine tests and separately labelled local integration result.
**Likely files:** `app/retrieval/embeddings.py`, `app/ollama.py`, `tests/unit/test_embeddings.py`, `tests/integration/test_local_embeddings.py`.

### T28 — Persist an idempotent versioned local index

**Status:** Proposed. **Prerequisites:** T27; T12/T17 consistency/index design. **Scope:** M.
**Objective:** Index content once per approved identity/version and preserve searchable integrity across restart.

- [ ] Persist vectors/chunk metadata/index state; unchanged uploads reuse indexed content while retaining distinct ownership/reference/display metadata.
- [ ] Handle content/parser/model version changes and interrupted indexing through approved retry/rebuild behavior without duplicate chunks, scope leaks or false-ready state.

**Verification:** Test-first duplicate/repeat/version-change/failure/restart cases and inspect reference scope plus stored chunk/vector counts.
**Evidence:** Pending — index idempotency/recovery tests and local smoke.
**Likely files:** `app/retrieval/index.py`, `app/ingestion/processing.py`, `app/storage/index_state.py`, `tests/integration/test_indexing.py`.

**Checkpoint CP10 — T26–T28:** Proposed. Review source-preserving chunks, local embedding errors, version/dedup/restart integrity and relevant checks. Apply G3.

### T29 — Retrieve evidence within the selected document scope

**Status:** Proposed. **Prerequisites:** T28; T16 retrieval contract. **Scope:** M.
**Objective:** Return useful bounded evidence without unrelated/removed attachments or old-context contamination.

- [ ] Resolve selected references, embed queries locally and rank chunks with complete provenance under approved relevance/context budgets; support multiple files and table context.
- [ ] Exclude unselected/unrelated/removed sources and apply no-evidence/ambiguous behavior; same-content attachments in different conversations must remain correctly scoped.

**Verification:** Deterministic mocked ranking/scope/budget tests and a small agreed retrieval evaluation with expected relevant passages.
**Evidence:** Pending — isolation and measured relevance results.
**Likely files:** `app/retrieval/search.py`, `tests/unit/test_retrieval.py`, `tests/integration/test_retrieval_scope.py`.

### T30 — Generate and persist grounded chat exchanges

**Status:** Proposed. **Prerequisites:** T29; T11/T16/T17 approved generation/history contract. **Scope:** M.
**Objective:** Add the local chat API with evidence-bound answers and explicit abstention.

- [ ] Separate system policy, untrusted current evidence and bounded history; answer multi-file questions only when supported and handle insufficient/ambiguous evidence without treating document instructions or old messages as authority.
- [ ] Persist messages/timestamps/document context consistently using the approved local model/timeouts; handle missing model, malformed output and interrupted requests with clear safe errors.

**Verification:** Test-first mocked grounded/abstention/history-injection/API failure/persistence cases; separately labelled actual local-model smoke.
**Evidence:** Pending — chat tests, known-evidence examples and local smoke limitations.
**Likely files:** `app/chat/service.py`, `app/api/chat.py`, `app/storage/messages.py`, `tests/integration/test_chat.py`, `tests/security/test_prompt_boundaries.py`.

### T31 — Validate citations and resolve safe passage previews

**Status:** Proposed. **Prerequisites:** T30, T25. **Scope:** M.
**Objective:** Bind surfaced citations to supplied evidence rather than model-invented metadata.

- [ ] Allow only citation IDs in the answer's supplied evidence; derive real filenames/locations from stored provenance and reject fabricated IDs/quotes/pages/sheets/rows.
- [ ] Expose bounded escaped previews through scoped IDs and approved missing/removed-source behavior; disclose coarse location precision without arbitrary local-file access.

**Verification:** Test-first allowlist/location/quote/preview-scope/XSS cases and manually trace a CSV answer to original records/columns.
**Evidence:** Pending — citation/preview tests and source trace examples; no claim of full semantic verification.
**Likely files:** `app/chat/citations.py`, `app/api/sources.py`, `app/chat/service.py`, `tests/unit/test_citations.py`, `tests/security/test_source_preview.py`.

**Checkpoint CP11 — T29–T31:** Proposed. Demonstrate selected evidence → answer/abstention → real citation; review unsupported/injection/error cases and persisted context. Apply G3.

### T32 — Expose transparent evidence-support signals

**Status:** Proposed. **Prerequisites:** T31; T16 approved semantics. **Scope:** M.
**Objective:** Explain observed citation/support coverage without implying calibrated accuracy.

- [ ] Return the approved interpretable validity/coverage/abstention/warning states and explanations, distinguishing identifier validation from actual semantic support.
- [ ] Handle absent/invalid/partial citations, mixed support and extraction limits consistently; no numerical correctness probability or unsupported semantic assurance.

**Verification:** Test-first indicator cases from T16 and manual comparison of wording with actual available evidence/limits.
**Evidence:** Pending — indicator tests and reviewed examples/text.
**Likely files:** `app/chat/evidence.py`, `app/chat/service.py`, `tests/unit/test_evidence_indicator.py`.

### T33 — Deliver the local browser CSV chat flow

**Status:** Proposed. **Prerequisites:** T32; T15 conclusion and T17 approved UI approach. **Scope:** M.
**Objective:** Let the user upload, ask, read support signals and inspect sources through a minimal browser interface.

- [ ] Connect existing upload/status/chat/source operations with selected-document context, per-file processing, loading/empty/success/warning/error states and safely rendered untrusted text; serve all assets locally.
- [ ] Implement keyboard/focus/label/contrast behavior, evidence explanations and citation previews from the approved design without adding an unapproved framework or build system.

**Verification:** Local browser CSV end-to-end and keyboard/error walkthrough, output-escaping/API regression and asset/network inspection; automation tools only if separately reviewed/approved.
**Evidence:** Pending — browser checklist and relevant automated checks.
**Likely files:** `app/static/index.html`, `app/static/app.js`, `app/static/styles.css`, `app/main.py`, `tests/integration/test_ui_routes.py`; adjust only for an approved frontend alternative.

### T34 — List, reopen and rename saved conversations

**Status:** Proposed. **Prerequisites:** T33. **Scope:** M.
**Objective:** Restore transcript and correct document context after application restart.

- [ ] List/reopen/rename via API/UI with saved messages/timestamps/selected references, correct chat isolation and honest missing-reference states.
- [ ] Restart the actual app/storage and continue a chat with the correct evidence/history; conversation deletion remains a separate lifecycle slice in T45.

**Verification:** Persistence/list/rename/reopen/isolation tests plus real restart and grounded follow-up question walkthrough.
**Evidence:** Pending — saved-chat tests and actual restored-context observation.
**Likely files:** `app/storage/conversations.py`, `app/api/conversations.py`, `app/static/app.js`, `tests/integration/test_saved_conversations.py`.

**Checkpoint CP12 — T32–T34:** Proposed. Demo full CSV upload → answer/citation/indicator → restart/reopen, including accessibility and error paths. Apply G3 before format expansion.

## M4 — Add each remaining format through the working path

### T35 — Support native-text PDFs with table/image references

**Status:** Proposed. **Prerequisites:** T34; approved T05/T08/T17 parser selection. **Scope:** M.
**Objective:** Extend upload-to-answer support to native PDFs with honest page/region citations.

- [ ] Extract native pages, practical table row/column structure, table regions/image references and warnings/parser version; detect pages requiring the later OCR path and preserve originals separately.
- [ ] Integrate validation/status/index/answer/preview with real page anchors; reject protected/corrupt files and disclose structure/visual limitations rather than claiming full image semantics.

**Verification:** Golden page/table/image provenance tests, protected/error/security cases and local upload → text/table question → source preview smoke.
**Evidence:** Pending — PDF tests and end-to-end source trace.
**Likely files:** `app/ingestion/pdf.py`, `app/ingestion/processing.py`, `app/api/sources.py`, `tests/unit/test_pdf_extraction.py`, `tests/integration/test_pdf_flow.py`.

### T36 — Process scanned and mixed PDFs through local OCR

**Status:** Proposed. **Prerequisites:** T35; approved T09/T17 OCR/language assets and D03 scope. **Scope:** M.
**Objective:** Add scanned-page processing with traceable native/OCR distinctions and resource limits.

- [ ] Detect/render/OCR pages according to approved policy; preserve original page/region/image references, confidence/warnings and native/OCR flags without unnecessarily duplicating native text.
- [ ] Expose bounded processing/progress, low-quality errors and missing language assets; no runtime downloads or unapproved chart semantics, and table/image references remain traceable.

**Verification:** Native/scanned/mixed/language/low-quality/absent-asset tests, page-citation checks and actual scanned-PDF answer smoke with resource observations.
**Evidence:** Pending — OCR integration/provenance tests, warning examples and measured local smoke.
**Likely files:** `app/ingestion/ocr.py`, `app/ingestion/pdf.py`, `app/ingestion/processing.py`, `tests/unit/test_ocr.py`, `tests/integration/test_scanned_pdf_flow.py`.

### T37 — Support legacy XLS sheet and cell citations

**Status:** Proposed replacement of the unstarted DOCX slot, awaiting task-revision review. **Prerequisites:** T36; approved T07A/T08/T17 XLS selection. **Scope:** M.
**Objective:** Extend the working pipeline to binary XLS with real sheet/cell anchors.

- [ ] Preserve sheets/cells/ranges, table/header relationships, stored values/date types and parser/version warnings under approved budgets; never calculate formulas or execute macros/embedded content or fetch links.
- [ ] Complete upload/index/answer/preview; reject corrupt/protected/mismatched inputs and expose unsupported features or missing cached values clearly.

**Verification:** Golden workbook/table/value/anchor and negative/security/resource tests, plus a local cited-answer walkthrough.
**Evidence:** Pending — XLS tests and source-location smoke; XLSX success is not XLS evidence.
**Likely files:** `app/ingestion/xls.py`, `app/ingestion/processing.py`, `tests/unit/test_xls_extraction.py`, `tests/integration/test_xls_flow.py`.

**Checkpoint CP13 — T35–T37:** Proposed. Review native/scanned/mixed PDF and XLS demos, especially table/image/OCR and sheet/cell anchors, limits and security. Run relevant regressions; apply G3.

### T38 — Support XLSX sheet and cell provenance

**Status:** Proposed. **Prerequisites:** T37; approved T07/T08/T17 spreadsheet policy. **Scope:** M.
**Objective:** Answer workbook questions using unambiguous sheet/row/column evidence.

- [ ] Preserve sheet/cell/range anchors, headers/merged-context relationships and table structure under approved limits; use explicit cached-formula/blank/protected/invalid-file behavior without calculations or external fetches.
- [ ] Complete upload/index/table-question/citation-preview flow with honest extraction/value warnings and bounded memory.

**Verification:** Multi-sheet/merged-header/formula/blank/protected/resource-boundary tests and local table lookup citing the expected cell range.
**Evidence:** Pending — spreadsheet provenance/security tests and local smoke.
**Likely files:** `app/ingestion/xlsx.py`, `app/ingestion/processing.py`, `tests/unit/test_xlsx_extraction.py`, `tests/integration/test_xlsx_flow.py`.

### T39 — Harden CSV provenance and mixed-workflow behavior

**Status:** Proposed. **Prerequisites:** T38; approved T07/T08/T17 CSV/encoding policy. **Scope:** M.
**Objective:** Extend the existing T23–T34 CSV path with remaining evaluated dialect, encoding and resource edge cases; avoid rebuilding that parser.

- [ ] Preserve original row/column/header meaning for approved dialects/encodings, quoted/multiline cells and warnings; never execute formula-like cell text.
- [ ] Complete upload/index/table-question/preview flow with correct anchors and clear malformed/unsupported/resource errors.

**Verification:** Golden header/row/column/quoted/multiline/encoding/error tests and local cited table lookup.
**Evidence:** Pending — CSV tests and trace to original rows/columns.
**Likely files:** `app/ingestion/csv.py`, `app/ingestion/processing.py`, `tests/unit/test_csv_extraction.py`, `tests/integration/test_csv_flow.py`.

### T40 — Verify the integrated mixed-format workflow

**Status:** Proposed. **Prerequisites:** T39 and all four format slices. **Scope:** M, bounded integration verification.
**Objective:** Demonstrate cross-format answers and partial-failure handling without metadata loss.

- [ ] Run a mixed batch with valid/corrupt/protected/unsupported/oversized samples and verify per-file statuses, originals/outputs, warnings, deduplication and retry behavior.
- [ ] Ask approved multi-file/table/ambiguous/unsupported questions, restart/reopen, and trace every citation to expected page/sheet/cell/record/column and physical-line span; no unrelated-file retrieval or invented precision.

**Verification:** Parameterized integration/smoke matrix plus relevant regression suite; larger findings become separately proposed tasks rather than hidden extra scope.
**Evidence:** Pending — `docs/benchmarks/format-integration.md`, reproducible matrix and remaining limits.
**Likely files:** `tests/integration/test_mixed_format_flow.py`, `tests/evals/questions.json`, that report; at most two small targeted source fixes if necessary.

**Checkpoint CP14 — T38–T40:** Proposed. Review all formats/multi-file citations/status/errors/restart against acceptance; apply G3 before the reusable-library slice.

## M5 — Library sharing and explicit lifecycle

### T41 — Upload and list reusable library documents

**Status:** Proposed. **Prerequisites:** T40, T20; approved D04 ownership. **Scope:** M.
**Objective:** Reuse the validated four-format ingestion path for a persistent local library.

- [ ] Upload/list library documents with per-file status/warnings/metadata and approved original/output/index identity reuse; do not duplicate unchanged indexed content.
- [ ] Distinguish reusable documents from exclusive chat attachments in API/UI; library upload or deduplication must not silently change unrelated attachment ownership.

**Verification:** Library API/UI/restart/dedup/reference-identity tests and a local mixed-format library walkthrough.
**Evidence:** Pending — library tests and observed processing/list behavior.
**Likely files:** `app/api/library.py`, `app/storage/documents.py`, `app/static/app.js`, `tests/integration/test_library.py`.

### T42 — Select shared library references in conversations

**Status:** Proposed. **Prerequisites:** T41, T34. **Scope:** M.
**Objective:** Share stored evidence across chats while preserving explicit selection and isolation.

- [ ] Attach/select/detach library references alongside exclusive files; multiple chats share stored bytes/chunks without broadening their selected retrieval scope.
- [ ] Persist/restore selections after reopen; detaching a reference does not delete the library document and historical citations follow approved policy.

**Verification:** Two-conversation reference/storage-identity/isolation tests and local restart/detach/citation walkthrough.
**Evidence:** Pending — shared-byte/scope tests and restored-context observations.
**Likely files:** `app/api/conversations.py`, `app/storage/conversations.py`, `app/retrieval/search.py`, `app/static/app.js`, `tests/integration/test_library_references.py`.

**Checkpoint CP15 — T41–T42:** Proposed. Demonstrate both document organizations, shared bytes, isolated selected retrieval and saved references. Apply G3 before removal behavior.

### T43 — Preview document-deletion impact and warn about dependents

**Status:** Proposed. **Prerequisites:** T42; approved D04/T17 deletion policy. **Scope:** M.
**Objective:** Make the actual retention/citation consequences clear before destructive removal.

- [ ] Show dependent conversations and approved effects on originals, extraction, vectors, metadata, messages/quotations and historical previews/citations; enforce any agreed block-while-referenced policy.
- [ ] Implement the approved destructive-action interaction and changed-reference/stale-impact handling without silently dropping shared evidence.

**Verification:** Impact-query/API/UI cases for zero/one/multiple/changed dependents; manually review warning accuracy against D04.
**Evidence:** Pending — dependency/impact tests and reviewed user-facing wording.
**Likely files:** `app/storage/lifecycle.py`, `app/api/library.py`, `app/static/app.js`, `tests/integration/test_deletion_impact.py`.

### T44 — Remove document artifacts and searchable evidence consistently

**Status:** Proposed. **Prerequisites:** T43; approved consistency/recovery design. **Scope:** M.
**Objective:** Apply approved removal across local files, SQLite, index and affected references.

- [ ] Remove/retain each artifact exactly as agreed, update affected reference/citation state and exclude removed evidence from retrieval; preserve content still required by surviving references.
- [ ] Make retry/restart/partial-failure recovery consistent across files/metadata/vectors and derived previews/cache as applicable, with honest processing/error state.

**Verification:** Test-first deletion/reference-count/stale-chunk and failure-injection/retry/restart checks; security review and local remove/retry/query smoke.
**Evidence:** Pending — cleanup/integrity tests and removed-citation observations.
**Likely files:** `app/storage/lifecycle.py`, `app/retrieval/index.py`, `app/api/library.py`, `tests/integration/test_document_deletion.py`, `tests/security/test_deleted_content.py`.

### T45 — Delete saved conversations using the approved retention policy

**Status:** Proposed. **Prerequisites:** T44, T34. **Scope:** M.
**Objective:** Complete saved-chat management without losing reusable library or another chat's evidence.

- [ ] Delete through API/UI and apply approved message/exclusive-attachment retention and cleanup while preserving reusable library documents and surviving references.
- [ ] Handle shared bytes, historical citations, retries and restart consistently; removed chats no longer list/reopen and retained artifacts are described truthfully.

**Verification:** List/reopen/delete tests with exclusive/shared/library attachments, failure/restart and no-cross-chat-loss checks; local walkthrough.
**Evidence:** Pending — retention/isolation tests and actual user-visible behavior.
**Likely files:** `app/api/conversations.py`, `app/storage/lifecycle.py`, `app/static/app.js`, `tests/integration/test_conversation_deletion.py`.

**Checkpoint CP16 — T43–T45:** Proposed. Review deletion warnings, approved artifact/citation retention, cleanup and restart integrity. Apply G3; do not replace policy with implementation convenience.

## M6 — Integrated verification and acceptance

### T46 — Review adversarial boundaries and interruption recovery

**Status:** Proposed. **Prerequisites:** T45. **Scope:** M, bounded review.
**Objective:** Verify the integrated local trust/lifecycle model before final quality evaluation.

- [ ] Exercise traversal/Windows filenames, parser/decompression/OCR resource abuse, macros/external links/document injection, model/preview escaping, loopback Host/origin handling and sensitive log leakage without adding multi-user auth.
- [ ] Repeat interrupted ingestion/index/delete/restart scenarios and inspect orphan/temp/searchable artifacts; fix only small in-scope findings and propose separate tasks for larger issues.

**Verification:** Relevant security/recovery regression checks and manual trust-boundary review using the verified security/review skills.
**Evidence:** Pending — `docs/security-review.md`, findings/reproduction/fix evidence and accepted residual limits.
**Likely files:** `tests/security/test_local_boundaries.py`, `tests/integration/test_recovery.py`, that report; at most two targeted source fixes within scope.

### T47 — Verify offline core operation and runtime traffic

**Status:** Proposed. **Prerequisites:** T46; approved assets already provisioned. **Scope:** M.
**Objective:** Demonstrate local core operation without external services/assets or silent downloads.

- [ ] Cold-start with local assets and external network unavailable/blocked, then exercise four formats/OCR, library/chat, citations, restart and deletion using local Ollama; separately verify useful missing-asset failures.
- [ ] Observe browser/app/OCR/Ollama network/log behavior with approved tooling, distinguish loopback from external traffic and record no remote fallback/telemetry/assets/download requirements plus observation limits.

**Verification:** Repeat documented offline smoke without sending sample content remotely or changing machine-wide settings without permission; any new monitoring tool needs its own reviewed trial approval.
**Evidence:** Pending — `docs/benchmarks/offline-runtime.md`, method/settings/observations and limits; later strict deployment gate is not claimed complete.
**Likely files:** That report and `tests/integration/test_no_remote_fallback.py`.

**Checkpoint CP17 — T46–T47:** Proposed. Review security/privacy/recovery findings and measured local/offline behavior; resolve blockers before final evaluation. Apply G3.

### T48 — Run the reproducible quality and resource baseline

**Status:** Proposed. **Prerequisites:** T47; T02/T16 approved rubric/thresholds and all required slices. **Scope:** M.
**Objective:** Produce actual Stage 1 grounding/retrieval/performance results on the user's workstation.

- [ ] Run fixed answerable/unanswerable/multi-file/ambiguous/table/native/scanned cases with exact fixture/model/index/config identities; score relevance, citation correctness/coverage, grounding and abstention under the approved rubric.
- [ ] Measure extraction/indexing/cold/warm answers and combined peak/system memory/disk pressure at approved scale; compare D06 budgets and report raw variation/failed cases/limitations internally, not as user-facing accuracy.

**Verification:** Reproduce from saved manifests/settings in a second run, execute relevant full tests/Ruff and compare results without weakening thresholds/tests.
**Evidence:** Pending — `docs/benchmarks/stage1-baseline.md`, sanitized machine-readable metrics and exact commands.
**Likely files:** `tests/evals/run_baseline.py`, `tests/evals/questions.json`, that report and one sanitized results file; larger quality fixes require separate approved tasks.

### T49 — Verify Windows setup, dependency inventory and user documentation

**Status:** Proposed. **Prerequisites:** T48. **Scope:** M, reproducibility review.
**Objective:** Ensure setup and usage documentation accurately describe the delivered local prototype.

- [ ] Validate locked uv/Windows setup, approved model/OCR/native assets, run/test commands, dependency/model/license inventory and offline provisioning instructions without unapproved downloads.
- [ ] Cross-check README/diagram/ADRs/user guide with real upload/library/chat/citation/indicator/deletion/error behavior, resource limits and visual/OCR/parser limitations; inspect intended Git contents for private/generated artifacts.

**Verification:** Follow instructions in an authorized isolated project environment or explicitly record inability to reproduce; check versions/commands/lockfile/inventory and local links.
**Evidence:** Pending — setup walkthrough, inventory/documentation review and environment limits.
**Likely files:** `README.md`, `docs/provisioning.md`, `docs/dependencies.md`, `docs/user-guide.md`, `docs/ADR/0001-stage1-architecture.md`.

### T50 — Present Stage 1 acceptance demo and obtain sign-off

**Status:** Proposed. **Prerequisites:** T49; mandatory criteria verified, blockers resolved or limitations explicitly accepted. **Scope:** S.
**Objective:** Demonstrate approved Stage 1 acceptance and stop at the stage boundary.

- [ ] Present a traceable acceptance matrix and demo all formats/native/scanned PDFs/table-image references, both document organizations, supported/unsupported/multi-file questions, citations/indicator, restart/reopen/rename and safe deletion.
- [ ] Record user sign-off or requested fixes; ask separately about commits and any Stage 2 transition. Passing tests or an accepted demo does not authorize later-stage features automatically.

**Verification:** User-observed demo and evidence/report traceability; confirm no claim exceeds actual tests/measurements.
**Evidence:** Pending — `docs/stage1-acceptance.md`, sign-off/fix list and any separate transition decision.
**Likely files:** That report plus routine PLAN/TODO/README status updates.

**Checkpoint CP18 — T48–T50 / G4:** Proposed. Review metrics, verified setup and demo. Stage 1 remains incomplete until acceptance evidence/sign-off is recorded; no Stage 2 task is authorized here. Apply G3 and persist final state before compaction.

## Proposed chart-investigation task amendment

### T16A — Proposed local data-chart/diagram feasibility investigation

**Status:** Proposed addition following approval of the evaluation scope; not authorized to run. **Prerequisites:** T02–T03, T09, T11; agreed ground truth/thresholds/budget and exact G1 provisioning. **Scope:** M.
**Objective:** Evaluate the approved chart scope before T17 component adoption without promising runtime visual support.

- [ ] Compare structured source data/labels/OCR with an approved local visual candidate on agreed English-labelled trends/comparisons/values/relationships; verify real chart/page/sheet citations, approximate-value disclosure and abstention against manual ground truth.
- [ ] Measure correctness/grounding/citation support, cold/warm latency and total memory pressure on the target machine; present supported types/failures and an adopt/narrow/defer decision before proposing implementation tasks.

**Verification:** Reproduce approved local trials with fixed fixture/model/config identities; inspect unsupported/ambiguous cases and local-only behavior. No trial runs during T01.
**Evidence:** Pending — report, raw non-sensitive measurements and user adoption decision.
**Likely files:** `docs/benchmarks/chart-interpretation.md`, fixture/question definitions and at most two bounded evaluation aids. This is an investigation proposal, not authorization for dependencies or code execution.

## Current handoff

The plan/T02 design are approved; **T01–T03 and T05 complete; T04 deferred at user request**. Baseline setup was verified and committed in bb68c40. T05 results and limitations are in `docs/benchmarks/pdf-parsers.md`; user accepted PyMuPDF empirical-comparison deferral and authorized the T05 commit (d8d12e7). The subsequent explicit format amendment excludes T06; the proposed T02R/T07/T07A sequence and CSV-first/XLS task changes await review. No application implementation/runtime parser adoption occurred. Further provisioning/adoption remains gated.
