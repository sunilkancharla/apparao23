# Stage 1 Atomic Task Checklist

## Latest approved scope amendment - XLS deferred

User direction on 2026-11-13 limits Stage 1 to PDF/XLSX/CSV. T07A and T37 are excluded/deferred, not completed; their historical evidence and unchecked criteria remain below. S-XLS/Q21-Q25 and XLS-specific negative controls are excluded from active evaluation. T08 is closed with user-approved non-adoption and empirical-trial deferral; T09 read-only review is authorized. T16/T17 bypass T07A; T38 follows T36. No further XLS trial, isolation setup, installation or implementation is authorized. Verification: JSON scope/reference/count checks and historical ground-truth comparison passed; Git whitespace checks passed. Documentation/selection metadata only, no execution or dependency changes. Earlier scope/approval entries below are historical where superseded.

**Status:** T01–T03/T02R/T05 complete; T04 deferred; T07 bounded results reviewed and approved for commit; coverage follow-up remains open, with the budget-accounting gap recorded. Three approved process improvements implemented. T05 closes with approved PyMuPDF comparison deferral. **Prepared:** 2026-11-13 (Asia/Calcutta).

**Authority:** Approved SPEC, AGENTS and PLAN. Format amendment committed in e1ee6ff; T02R in 28ec7ad. The user explicitly approved the exact T07 package and three process improvements. Provisioning/local trial ran; the user approved recording the reviewed results/gaps and committing the package; remaining acceptance coverage is not waived. T04 closes by user-approved optional-tool deferral; T05 permissive trial was authorized after licensing review; T06 is excluded from Stage 1; T08–T50 and proposed T07A/T16A are unstarted.

## Proposed scope-alignment revision — 2026-11-13

User approved PDF/XLSX/CSV only for this stage. DOCX/TXT are excluded entirely from Stage 1; later inclusion requires explicit user approval. T05 is committed in d8d12e7. Completed task history and original fixture ground truth are retained. Historical task revision (superseded for XLS by the latest amendment): T02R active-corpus refresh, T06 exclusion, T07 XLSX/CSV, new T07A XLS, CSV-first T23–T34, T37 XLS and T39 CSV robustness. No new trial or installation is authorized by this revision.

### T02R — Align active evaluation coverage with the historical four-format scope

**Status:** Complete — definitions verified; user approved the reviewed result and commit (“yes please”). **Prerequisites:** Approved format amendment; the user explicitly authorized this task after the scope commit. **Scope:** M, definition-only.
**Objective:** Keep scores and fixture coverage faithful to PDF/XLSX/CSV without losing historical ground truth.

- [x] Keep DOCX/TXT fixture/question definitions excluded from Stage 1; exclude them from active scoring and materialization and migrate the injection scenario to an in-scope artifact without changing its expected safety behavior.
- [x] Specify an XLS fixture with sheet/cell/merged-header/stored-value anchors and invalid/protected/macro/external-link cases; document missing real XLS samples and a gated materialization procedure for review before trials. Reuse checked CSV questions for the first vertical slice. Exact XLS tooling/artifact and trial approval remain T07A; no generation is claimed or authorized here.

**Verification:** Validate JSON references, active/excluded selection and format coverage; review new gold anchors and scoring denominators. No document generation, dependency installation or model evaluation.
**Evidence:** `docs/evaluation.md` T02R section and dated verification record: 11 authored definitions (8 in scope), 20 negative cases, 25 questions (21 in scope, 4 excluded), S-XLS/Q21–Q25 and S-CSV-INJECTION/Q20. Explicit scope/readiness flags, IDs/references, original gold preservation, nine source hashes/sizes, in-memory CSV and XLS anchor/date definitions and local links checked successfully; `git diff --check` passed. No artifacts/packages/parser/model/application tests or scores. Concrete XLS generation/independent cache verification and representative XLS coverage remain T07A/T17 gates. User approved T02R closeout and this commit on 2026-11-13. T07 review remains the next proposed task; no trial installation or execution authorized.
**Likely files:** `tests/evals/manifest.json`, `tests/evals/questions.json`, `docs/evaluation.md`.

## Checklist conventions and completion rules

- User authorized T03 closeout and read-only T04 review, then explicitly declined SkillSpector. T05 review and permissive trial were authorized. Replying “ok, next step please” to the explicit closeout/commit question approves PyMuPDF comparison deferral, the T05 commit and initially T06 review; later user instructions supersede that next step by excluding DOCX/TXT from Stage 1 and revising formats. G1–G4 and D01–D09 still govern later work; no runtime adoption or T06 installation is authorized.
- Record one explicit approval for a bounded package containing ordered task IDs, exact artifacts/versions, provisioning/fixture/execution permissions, resource limits, checks and stop conditions. Proceed sequentially within that approved scope without repeating permission questions. Ask for scope/budget/artifact expansion or another unapproved package; commits, G2 adoption and stage transitions retain explicit gates.
- Each coherent package closeout includes G3: actual checks/evidence, relevant review, TODO and affected documentation updates, readable diff and commit question. Keep README current for coherent results and PLAN for sequence/scope changes; existing authorization persists for covered steps.
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

**Checkpoint CP02 — T04–T06:** Proposed. Review skill trust and PDF closeout; record XLS/DOCX/TXT exclusion and three-format scope, especially locations, licenses and local-only paths. Apply G3; approve the next trial separately.

### T07 — Compare XLSX and CSV extraction baselines

**Status:** Bounded results reviewed and commit approved; follow-up acceptance coverage remains open. Genuine encrypted/VBA coverage and combined worker-cap accounting gaps are retained. **Prerequisites:** T02–T04/T02R and exact T07 package approval satisfied. **Scope:** M, bounded shared fixture trial.
**Objective:** Establish structured local XLSX/CSV baselines with minimal dependencies; no TXT work.

- [x] Compare viable XLSX handling including openpyxl as a candidate with standard-library CSV paths; retain sheets/cells/records/columns/headers/physical-line spans, quoted cells and encoding warnings.
- [ ] Evaluate merged headers, formula/cached values without execution, external links, protected/invalid inputs and approved memory boundaries; record fidelity, resource, license and offline tradeoffs.

**Verification:** Compare expected cell/range/record and physical-line anchors and values on the fixed small corpus; disclose missing cached values and unsupported encodings.
**Evidence:** `docs/benchmarks/tabular-text-parsers.md`: three exact packages installed in `.venv`, earlier pins unchanged; 40 original-sample workers, reader agreement on 15,656 cells/repetition, CSV gold/provenance checks, nine-test full-suite pass plus a later focused guard pass and mutation detection. Offline sync/lock, Ruff and diff checks passed. Genuine encrypted/VBA/full-scale coverage remains unverified. T07 counter=79, plus 13 T05 regression workers outside it (92 overall); the combined 80-worker cap was not enforced, and further workers stopped. No runtime adoption; second criterion remains open for gap review/follow-up before adoption. Approved process consolidation/package approvals/early feasibility order implemented. User approved committing these reviewed results and process changes (“yes please”); no runtime adoption or retroactive budget expansion is inferred.
**Likely files:** That report and at most three evaluation files.

### T07A — Compare legacy XLS parsers

**Status:** Excluded/deferred from Stage 1 by the latest explicit user scope decision; not completed. Historical record follows: Exact trial and review-document commit approved; review committed in e3c598d. Preflight stopped because native network denial could not be established. Four control tests and Ruff passed; no download/install, parser import, generated fixture or workbook parsing. T07A remains incomplete. **Prerequisites:** T02R, T03–T04, T07; approved package's stop conditions remain binding. **Scope:** M.
**Objective:** Establish a local binary XLS extraction path independently of XLSX.

- [ ] Review a bounded candidate shortlist, including license, maintenance/advisories, Windows/Python compatibility, native/transitive dependencies, footprint and offline behavior; compare against a justified alternative before choosing.
- [ ] Use fixed golden sheets/cells/stored values, merged/header context and date types; measure time/RAM, errors/protected/invalid files and honest missing-cache warnings. Never execute formulas, macros, embedded content or external links; reject mislabeled unsupported workbooks.

**Verification:** Bounded local comparison with fixture hashes, golden value/anchor checks and negative/network/resource controls. No runtime adoption inferred.
**Evidence:** [XLS review/preflight report](docs/benchmarks/xls-parsers.md): pinned readers/writer, notices, native dependencies, risks and alternatives reviewed. User approved the 100-slot/10-MiB bounded package and document commit. Native Winsock control returned TCP4/TCP6 10035 and UDP4 accepted (0); these do not establish enforced network denial, so the documented stop rule applied before documents/dependencies. Four red-to-green control tests passed; Ruff passed. Final ledger reserves 12 slots (six explicit roots plus conservative launcher allocations), zero downloads/calls; kernel descendant/job enforcement remains unverified. All planned parser comparisons are unrun, Q21–Q25 unscored, no runtime adoption. Stronger native isolation design or a separately approved reduced trial is the next decision; no automatic retry/fallback.
**Likely files:** That report and at most three evaluation aids.

### T08 — Evaluate Microsoft MarkItDown against format-specific baselines

**Status:** Closed with user-approved non-adoption and empirical-trial deferral on 2026-11-13 ("okay, proceed"). **Prerequisites:** T05, T07; T06/T07A excluded; any exact trial configuration/install requires G1 approval. **Scope:** M.
**Objective:** Determine whether MarkItDown improves the project enough to justify dependencies and provenance tradeoffs.

- [ ] Compare identical PDF/XLSX/CSV samples for fidelity, tables, page/sheet/row anchors, scans/images, OCR integration needs, time/RAM and install footprint against T05/T07.
- [ ] Inspect plugin/LLM/remote-processing paths and verify the trial stays local; document limitations and ask adopt/reject, with OCR integration measurements completed in T09.

**Verification:** Produce side-by-side results and manually trace output to original locations; no cloud text/image conversion paths allowed.
**Evidence:** [MarkItDown review](docs/benchmarks/markitdown.md): v0.1.9 tagged source and registry wheel identity reviewed, MIT license, direct/extras dependencies, Windows/Python range, permissions/remote paths and provenance limitations documented. Markdown does not provide the structured citation mapping required by this project; pandas/classifier dependencies add cost. No installation/import, fixture generation, sample conversion, performance measurement or empirical comparison. Exact transitive graph/native assets and trial boundary remain unverified. Documentation/link/whitespace checks passed; no application/parser tests ran. The user approved non-adoption, empirical-trial deferral, this documentation commit and proceeding to the T09 read-only review. T08 closes under that exception, without empirical scores or runtime adoption.
**Likely files:** That report and at most two comparison aids.

### T09 — Compare local OCR and scanned/mixed-PDF paths

**Status:** Shortlist `1337560`, proposal `bf3b82e`, original stop `7c50144`, approved license exception/continuation `6491666`. Part A artifact preparation completed through the separately approved continuation; original failed run retained. Part B remains unapproved pending its native execution boundary. No engine installed or benchmarked; T09 is incomplete. **Prerequisites:** T05, T08 (approved trial deferral); D02/D03; exact G1 gates remain binding. **Scope:** M.
**Objective:** Measure a viable local OCR path without assuming language or chart semantics.

- [x] Investigate FlatBuffers' upstream license after user authorization: stop report committed in `7c50144`; Apache-2.0 LICENSE pinned to source commit/digest and all 10 cached runtime Python files matched upstream bytes. Old Part A meter unchanged. [Narrow companion-notice exception and fresh continuation](docs/proposals/ocr-trial.md#proposed-part-a-continuation-after-flatbuffers-investigation) subsequently explicitly approved by the user with the findings commit. No installation or Part B approval.
- [x] Review Tesseract and RapidOCR CPU paths, English assets, source-level provenance, Windows compatibility evidence, dependencies/licenses, outbound initialization and provisioning gaps; record uncertainty rather than infer runtime readiness.
- [x] Prepare [bounded proposal](docs/proposals/ocr-trial.md) and [artifact inventory](docs/proposals/ocr-trial-artifacts.json): 16 proposed new wheels plus three English assets, 140,501,680 declared bytes; no declared active-version conflicts in metadata-only closure. Include tesserocr 2.13.0's bundled patched engine, explicit missing English-data SHA-256, notice review, separate preparation/execution budgets and native-boundary stop gate. No downloads of those artifacts, installs or OCR runs; preparation is not execution approval.
- [x] Complete Part A artifact preparation/notice inventory under the approved continuation. **Evidence:** [outcome](docs/benchmarks/ocr.md): all 16 wheels/three English assets verified; 14 original cached wheels unchanged, approved exact FlatBuffers companion notice preserved; 80 notice records/64 native entries inventoried. Ten preparation tests passed (0.022 s); old meter unchanged. Continuation: 14,856,592 bytes/12 requests and 26/32 conservative process slots including final checks, no retries; versioned model LICENSE 404 retained alongside separate upstream license/routing evidence. No install/OCR execution. Full distribution/license/security clearance, native execution boundary and Part B approval remain separate requirements. Original 16-slot failed run is historical evidence, not reset or relabelled as success.
- [ ] Compare a Tesseract-based option with another viable Windows/CPU alternative on approved scans/mixed pages/languages; retain native/OCR distinction, page/region/image references and confidence/warnings where available.
- [x] Document [native execution boundary alternatives and recommendation](docs/proposals/ocr-trial.md#native-execution-boundary-recommendation---pending-decision): AppContainer feasibility first; Sandbox and manually disconnected synthetic-only trial compared separately. Public Microsoft documentation reviewed; no local boundary configuration/probe or new execution allocation. Direction, exact preflight package and Part B approval remain unresolved.
- [ ] Agree the boundary direction, prepare its exact preflight/access map and obtain approval before configuration or controls; stop before OCR imports/rendering if boundary controls fail. Do not reuse exhausted trial meters or silently accept reduced filesystem protection.
- [x] Complete authorized [read-only AppContainer feasibility review and preflight proposal](docs/proposals/ocr-appcontainer-preflight.md): base Python resides outside `.venv`; propose a bounded project-local runtime copy without changing that installation. Record profile storage outside the repository, access map, synthetic native controls, 96-slot shared proposed budget and stop/cleanup rules. No profile, ACL change, helper implementation, control execution or OCR. Exact preflight and its side effects remain unapproved.
- [x] Execute the subsequently approved AppContainer preflight to its mandatory stop; proposal committed in `e6ecd5a`. [Actual evidence](docs/benchmarks/appcontainer-preflight.md): 8 policy tests and Ruff passed; 810 runtime files/38,852,581 bytes staged/hashed locally. The first unrestricted startup exited `0xC0000142`; no profile, ACL change, network controls or OCR. Native worker Job total=1/active=0; controller total=2/active=1. Preserve the stop and shared ledger; this is not isolation acceptance. Additional diagnostic execution and result/code commits need approval.
- [x] Prepare requested [bounded startup diagnostic proposal](docs/proposals/python-startup-diagnostic.md) after result commit `9bdfef0`: eight fixed original/staged startup contrasts, no profile or package changes, shared 48-slot budget and explicit diagnostic-failure versus safety-stop rules. Documentation only; execution, repairs and commit remain unapproved.
- [ ] Obtain approval and run only the new diagnostic package; retain old preflight stop, classify startup differences without claiming a particular DLL/root cause or isolation acceptance, and review evidence before any repair or preflight retry.
- [x] Execute subsequently approved startup diagnostic to its safety stop; proposal committed in `1658cdc`. [Evidence](docs/benchmarks/python-startup-diagnostic.md): 8 policy tests/Ruff passed; 810 runtime hashes/original counterparts verified. A-original and A-staged started with valid markers; B-original reached a Job accounting mismatch after writing its marker, with incomplete per-case receipt; five cases unattempted. Preserve final controller total=5/active=1, both stopped ledgers and the receipt gap. No isolated/OCR readiness result; another run or repair needs review/approval.
- [x] Apply user-approved receipt repair after result commit `c52151a`: persist observed PID/exit/Job data before the unchanged accounting guard; retain `not_yet_validated` classification until checks pass. Two new red-to-green tests; 10 final policy tests (0.004 s) and Ruff passed. [Repair evidence](docs/benchmarks/python-startup-diagnostic.md#subsequent-approved-receipt-repair). No native trial rerun or retrospective reconstruction; another accounting investigation remains gated.
- [x] Prepare requested [two-case accounting investigation](docs/proposals/job-accounting-investigation.md) after repair commit `ab1a04d`: bounded Job-count/active-PID snapshots, unchanged initial safety guard, 32-slot combined proposal. Documentation only; no instrumentation or native run yet.
- [ ] Review/approve that exact investigation before implementation/execution; preserve mismatches and stopped ledgers, report any timing observations without silently accepting them, and decide separately on any enforcement change or isolation retry.
- [x] Execute subsequently approved two-case accounting package to its safety stop; proposal committed in `db50257`. [Evidence](docs/benchmarks/job-accounting-investigation.md): 14 policy tests (0.005 s)/Ruff passed; A-original completed; B-original exited 0 with marker but worker total=2/active=0 persisted through 250 ms. Final controller total=4/active=1, only itself active; extra cumulative start charged, identity unavailable. No relaxed guard, retry, profile, permissions change or OCR. Closeout resumed after interruption; further execution and result commit retain their gates.
- [x] Review launch flags and prepare [four-combination proposal](docs/proposals/launch-flag-comparison.md) after result commit `a1f511c`: separate extended startup from no-window, four conditional roots, 40-slot combined budget and unchanged accounting stop. Documentation only; execution, runtime changes and commit remain gated.
- [x] Execute subsequently approved flag comparison to its mandatory stop; proposal committed in `2475ef8`. [Evidence](docs/benchmarks/launch-flag-comparison.md): 17 policy tests (0.011 s)/Ruff passed; F1 basic and F2 extended-only passed; F3 no-window-only exited 0 with marker but worker total=2, active count fell to zero; F4 unattempted. Initial mismatch remains rejected; final controller total=5/active=1, only itself active. No identified extra process, resolved DLL cause, relaxed guard, runtime adoption, profile or OCR. Further isolation execution and result commit remain gated.
- [x] Complete user-authorized [consolidated isolation package without CREATE_NO_WINDOW](docs/proposals/consolidated-isolation-validation.md) to its mandatory stop. [Evidence](docs/benchmarks/consolidated-isolation-validation.md): 11 policy tests (0.011 s)/Ruff passed, verified staged startup and all four native positive loopback paths. Fresh profile created, first ACL grant denied; profile deleted, utility removal denial retained, read-only audit found no run SID on 11 planned targets/ancestors. No restricted worker/OCR, installation or automatic retry. Shared closeout 32/96 reservations. End this diagnostic chain; choose an explicit alternative before further execution. Result/code commit remains gated.
- [x] Record user acceptance of a manual disconnected synthetic-only OCR trial without filesystem confinement, after result commit `ed4cb3a`; prepare [one bounded provisioning/handoff/evaluation package](docs/proposals/manual-disconnected-ocr-trial.md). Exact cached inventory, offline uv/project `.venv`, shared 240-start ceiling, synthetic fixtures, local user handoff and cleanup defined. Documentation only; package implementation/provisioning/execution and commit remain unapproved. No reopening Windows isolation diagnostics or application-safety waiver.
- [x] Prepare subsequently approved manual runner under package commit `76db076`: [evidence](docs/benchmarks/manual-ocr-preparation.md), [local handoff](docs/proposals/manual-ocr-handoff.md), exact cached identities, fake-backend contracts, lazy native adapters/fixture code, shared meter, hash-sealed PowerShell launch and sanitized summaries. 12 final contract tests (0.070 s)/Ruff passed, PowerShell syntax parsed; no install/render/OCR. Native/cache compatibility and quality remain unproven until the user's disconnected run. Preserve all receipts; source/handoff commit remains gated.
- [ ] User performs the already-approved offline handoff, confirms fixture readiness and verified teardown, then reports sanitized completion/stop status after reconnection. No automatic retry, cache fetch or reset; no raw OCR/image content in remote tool output. Review actual metrics before T09 closeout/adoption.
- [x] Diagnose first user-operated stop and repair the distribution-name comparison: [evidence](docs/benchmarks/manual-ocr-first-stop.md). Offline lock succeeded; `pdfminer.six`/`pdfminer-six` alias caused a false baseline mismatch. No sync/install/fixtures/OCR; teardown verified, root config/lock restored. New failing regression then 13 contract tests (0.080 s)/Ruff passed; exact versions remain enforced. Preserve stopped ledger/seal; source changed, so do not rerun/reseal the old handoff. Fresh continuation and repair/result commit retain their gates.
- [x] Commit approved name repair in `6120666`; prepare [manual-02 continuation](docs/proposals/manual-ocr-continuation.md) without changing manual-01. Explicit run selection, source seal and locked execution gate prepared; 14 contract tests (0.061 s)/Ruff passed, PowerShell parsed. Proposed new 160-start allocation is separate from old 104 used; native execution/source commit remain unapproved. [Restart checkpoint](docs/session-checkpoint.md) saved for compaction/handoff.
- [x] Record subsequent explicit approval of manual-02's 160-start continuation and source/handoff commit; enable only its reviewed execution gate and verify seal/prior meter. No install/OCR invoked; hand off the manual-02 command for disconnected user execution. Old manual-01 remains stopped and unchanged.
- [ ] Measure accuracy against ground truth, page time, peak RAM, renderer/language footprint and offline behavior; test native-parser/MarkItDown integration where viable and propose bounded processing settings.

**Verification:** Golden page/OCR text checks, low-quality/missing-language/error cases and local-only observation; missing assets must not trigger downloads.
**Evidence:** [OCR source review](docs/benchmarks/ocr.md): Tesseract 5.5.4 source versus linked Windows 5.5.3 distributor gap, RapidOCR 3.10.0/ONNX Runtime CPU candidate artifacts, English-only model selection, startup-download risks and proposed page/region comparison contract. No artifacts downloaded, dependencies changed, OCR/rendering executed or measurements fabricated. Documentation/local-link/whitespace checks passed. Exact patched binary/model/dependency identities, native execution boundary, representative scan controls, settings/budgets and acceptance thresholds remain unresolved before a bounded trial. T09 is not complete; no OCR/runtime adoption.
**Likely files:** That report and at most three local evaluation files.

**Checkpoint CP03 — T07–T09:** Proposed. Review the three-format comparison and OCR evidence/languages/visual limits. Record tool decisions; no parser product code before G2. Apply G3.

### T10 — Benchmark local Ollama embedding candidates

**Status:** Bounded comparison complete; results reviewed and source commit explicitly approved. Original run limitations retained; no runtime adoption or full offline/target-scale acceptance. **Prerequisites:** T02–T04/T02R and D06 satisfied; original G1 and documented continuation approved. **Scope:** M.
**Objective:** Measure retrieval usefulness and embedding resource cost on the actual CPU-only machine.

- [x] Trial `embeddinggemma` and approved Nomic alternative; record digest/license, validated dimensions, explicit query/document prefixes, context and over-limit rejection.
- [x] Complete frozen corpus/query repetitions, batch-one subset, lexical comparison and resource observations. First passes have uncontrolled OS caches; broader/combined/scale/offline acceptance remains future work. No runtime default selected.

**Verification:** Reproduce PLAN's actual-machine protocol using bounded reference search, retain failed runs and model-change reindex implications.
**Evidence:** [Embedding comparison](docs/benchmarks/embeddings.md): both pinned models completed four CPU passes, recall@5 1.00 on 12 related CSV variants; lexical recall@5 0.9583. Nomic is recommended for later adoption review given smaller weights/lower observed memory, not universally faster. Original failure/counter uncertainty retained. Separate approved continuation used 24/24 starts, 82/100 calls, no downloads; final 11 tests passed (1.14 s), Ruff passed before hash-reference correction. Owned server stopped/port released; corpus and original result preserved. Wider quality/combined pressure/storage and disconnected verification remain later gates; source commit approved separately, no runtime selection.
**Likely files:** That report and at most three evaluation files.

### T11A — Check chat feasibility early using fixed evidence

**Status:** Benchmark execution complete across approved original/continuation epochs; all 96 planned slots have completed results, original timeout retained. Final 27 tests/Ruff pass; user qualitatively accepted the local outputs on 2026-11-13. Structured semantic scores and model adoption remain pending. **Prerequisites:** T02R, T03/T10 complete; original and continuation G1 packages approved. **Scope:** M.
**Objective:** Detect CPU-only generation quality/latency/RAM limitations before completing other parser/tool investigations.

- [ ] Review exact small-model candidates/artifacts/licenses and run bounded fixed-evidence English questions with real CSV/PDF anchors; record context/settings/digest and abstention/citation behavior.
- [ ] Measure first-load and repeated response latency, throughput and total system/Ollama memory on the 16 GB CPU-only target; report infeasibility/tradeoffs without selecting a default or claiming combined OCR feasibility.

**Verification:** Fixed gold evidence/questions, retained failures and reproducible actual-machine measurements. Reuse approved artifacts/settings at T11; avoid duplicate runs absent changed conditions.
**Evidence:** [T11A report](docs/benchmarks/chat-models.md): both pinned Apache-licensed models provisioned locally; all 96 planned request slots completed across 97 retained attempts, including the original timeout. Qwen2.5 completed-response median 10.566 s; Qwen3 14.211 s across sessions. The approved continuation ran only its 13 missing/interrupted Qwen3 cases, used 30/32 starts and 19/40 calls, downloaded nothing, and retained original hashes/ledgers. Final 27 tests and Ruff passed; owned process exit and later host/OS listener-table cleanup verified. Timeout diagnostics and bounded teardown fixes have executed/final-tested source snapshots. Local combined review has 35 output/failure groups; semantic correctness/citation support and strict 16-GB/combined/offline acceptance remain unscored/unverified. User explicitly approved the reviewed source/documentation commit on 2026-11-13 (“yes sir, i am good with that”). No runtime adoption, new dependencies or application code. Later Qwen2.5 3B licensing/candidate decision remains open.
**Likely files:** That report and at most three local evaluation aids.

**User review follow-up:** User review, 2026-11-13: in response to the local factual/citation review request, the user replied “I am good with it”. Record qualitative acceptance of the reviewed outputs; no per-answer grades, claim counts or citation-support measurements were supplied. Numeric semantic metrics remain unscored; this does not select a runtime model or waive PDF, strict-16-GB, combined OCR/model or offline acceptance. T11A source/evaluation documentation is committed in 0872c22. That follow-up originally proposed T07A; the latest scope decision instead makes T08 the next review; installation/trial and adoption retain their exact package gates.

**Checkpoint CP-FEAS — T10/T11A:** Review CPU-only embedding/chat feasibility before more parser/tool investment. Models remain candidates until combined checks and G2 approval.

### T11 — Benchmark local Ollama chat candidates

**Status:** Proposed. **Prerequisites:** T09–T10 and T11A; approved exact chat models/downloads under G1. Reuse early fixed-evidence results; focus remaining work on combined OCR/model pressure and any unresolved quality cases. **Scope:** M.
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

**Scheduling:** After T34 or before proposed tool use; does not block core G2 or the first CSV slice.

**Status:** Proposed. **Prerequisites:** T01, T03–T04; D08 identity; approved optional trial under G1. **Scope:** S.
**Objective:** Evaluate only the user-intended RTK project against a concrete developer-workflow need.

- [ ] Confirm repository/version/purpose, license, Windows support, permissions/outbound calls and resource cost before installation; do not infer features from the name.
- [ ] Compare one representative workflow with/without the approved tool and record adopt/reject/defer plus fallback; unresolved identity may conclude only with user-approved deferral.

**Verification:** Inspect the exact artifact and reproduce the bounded local trial or document the agreed deferral.
**Evidence:** Pending — `docs/benchmarks/rtk.md`, measured benefit/risks and user decision.
**Likely files:** That report and at most one non-sensitive fixture description.

### T14 — Identify and evaluate the intended ponytail project

**Scheduling:** After T34 or before proposed tool use; does not block core G2 or the first CSV slice.

**Status:** Proposed. **Prerequisites:** T01, T03–T04; D08 identity; approved optional trial under G1. **Scope:** S.
**Objective:** Review ponytail independently without assumptions from similarly named tools.

- [ ] Verify exact repository/version/purpose, license, Windows/CPU compatibility, scripts/permissions/outbound behavior and footprint before proposing installation.
- [ ] Run one approved representative workflow/fixture and record adopt/reject/defer decision with manual/native fallback; unresolved identity needs explicit user deferral.

**Verification:** Manually inspect trust boundaries and reproduce the bounded comparison or approved deferral.
**Evidence:** Pending — `docs/benchmarks/ponytail.md`, trial/deferral and decision.
**Likely files:** That report and at most one fixture description.

### T15 — Evaluate UI UX Pro Max before frontend adoption

**Scheduling:** After core G2 and before T33; evaluate the aid/manual alternative without implicitly changing the approved frontend stack.

**Status:** Proposed. **Prerequisites:** T02–T04; D05; exact optional tool/trial approved under G1. **Scope:** M, design aid only.
**Objective:** Evaluate whether the aid improves required local browser flows without selecting a framework implicitly.

- [ ] Verify repository/version, skill/scripts/code/assets licenses, Windows needs and file/network behavior; review generated outputs locally on non-sensitive content.
- [ ] Compare a small chat/upload/library/citation-preview sketch with manual design for keyboard/focus/labels/contrast and loading/empty/error/status states; use supplied images only as references and obtain a tool decision.

**Verification:** Walk the sketches against accessibility/flow criteria and review assets/code before reuse; a trial is not product UI implementation.
**Evidence:** Pending — `docs/benchmarks/ui-ux-pro-max.md`, design notes and adopt/reject/defer decision.
**Likely files:** That report, `docs/ui-design.md`, and at most two sketches.

**Checkpoint CP05 — T13–T15:** Proposed. Review exact optional-tool identities/benefits and UI direction. Document approved deferrals/fallbacks; no automatic runtime additions. Apply G3.

### T16 — Specify retrieval, citations and evidence-support contracts

**Status:** Proposed. **Prerequisites:** T02/T02R, T05, T07 and T08–T12 (T06 excluded); D04/D06. **Scope:** M, design only.
**Objective:** Define measurable grounding behavior and truthful support signals before coding.

- [ ] Specify source-aware chunks, selected-document retrieval, bounded evidence/history, ambiguity/no-evidence handling, citation IDs/location/quote checks and removed-source behavior with expected cases.
- [ ] Approve observable indicator validity/coverage/abstention/warning signals, semantic-support limitations, and internal evaluation thresholds; never equate citation validity with correctness probability.

**Verification:** Walk supported/unsupported/ambiguous/table/multi-file/injection examples through the contract; manually trace expected claims and source anchors.
**Evidence:** Pending — reviewed contract, examples and rubric approvals.
**Likely files:** `docs/retrieval-design.md`, `docs/evaluation.md`, `tests/evals/questions.json`.

### T17 — Present architecture and component-adoption decision pack

**Additional review prerequisite:** Resolve the approved chart-evaluation scope through the proposed T16A investigation below or an explicit user-approved deferral before architecture adoption.

**Status:** Proposed. **Prerequisites:** T01/T02/T02R/T03/T05/T07/T08/T09/T10/T11A/T11/T12/T16, T04 approved deferral, and chart-scope prerequisite above; all core blocking decisions resolved. T06 excluded; T13/T14 are scheduled after the first slice or before use; T15 remains required before T33, not core G2. **Scope:** M, review only.
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
- [ ] Enforce one run budget across parser/model/negative/regression child processes and retained output, with deterministic exhaustion tests; do not repeat T07's counter gap. Before any earlier combined rerun, supply the equivalent shared meter/allocation in its approved package.

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

**Status:** Excluded/deferred from Stage 1 by the latest explicit user scope decision; not completed. Historical record follows: Proposed replacement of the unstarted DOCX slot, awaiting task-revision review. **Prerequisites:** T36; approved T07A/T08/T17 XLS selection. **Scope:** M.
**Objective:** Extend the working pipeline to binary XLS with real sheet/cell anchors.

- [ ] Preserve sheets/cells/ranges, table/header relationships, stored values/date types and parser/version warnings under approved budgets; never calculate formulas or execute macros/embedded content or fetch links.
- [ ] Complete upload/index/answer/preview; reject corrupt/protected/mismatched inputs and expose unsupported features or missing cached values clearly.

**Verification:** Golden workbook/table/value/anchor and negative/security/resource tests, plus a local cited-answer walkthrough.
**Evidence:** Pending — XLS tests and source-location smoke; XLSX success is not XLS evidence.
**Likely files:** `app/ingestion/xls.py`, `app/ingestion/processing.py`, `tests/unit/test_xls_extraction.py`, `tests/integration/test_xls_flow.py`.

**Checkpoint CP13 — T35–T36 (T37 deferred):** Proposed. Review native/scanned/mixed PDF demos, especially table/image/OCR and sheet/cell anchors, limits and security. Run relevant regressions; apply G3.

### T38 — Support XLSX sheet and cell provenance

**Status:** Proposed. **Prerequisites:** T36; approved T07/T08/T17 spreadsheet policy. **Scope:** M.
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

## Approved delivery priority

After T07 closeout: T10 → T11A (early CPU feasibility) → T08 → T09 → T11 (combined pressure) → T12 → T16 → T17/G2 → CSV-first T18–T34, with T15 before T33. T13/T14 follow the first slice or precede proposed use. These are scheduling changes approved with the three improvements; provisioning/execution of those future packages remains gated. New T11A is an early risk check, not runtime adoption or replacement of T11's combined measurements.

## Current handoff

T01–T03/T02R/T05 complete; T04 deferred; T06 excluded. T02R is committed in 28ec7ad. The approved T07 package and three process improvements are committed in e8ec471; remaining coverage still needs follow-up before adoption. Coverage and budget limitations remain explicit rather than marking all T07 criteria complete. T10 provisioning and the approved continuation comparison are complete, with original trial limitations retained in the embedding report. T10 results are committed in 55d68f6; the approved T11A continuation completed all 96 planned slots across epochs, with the original timeout retained. Source/documentation commit explicitly approved; semantic review and model decisions remain open; no further inference is needed for this frozen schedule. No further experimental starts remain in the T10 allocation. XLS is now deferred outside Stage 1. No application ingestion or runtime adoption occurred.

### T09 manual-03 handoff — approved continuation, 2026-11-14

- [x] Record [manual-02 reconnection stop](docs/benchmarks/manual-ocr-second-stop.md): approved offline install/fixtures succeeded; 29/60 comparison results, zero controls; user confirmed Wi-Fi reconnection; teardown verified. Preserve 77/160 ledger and installed evaluation config/lock. No completed quality gate or adoption.
- [x] Prepare explicitly approved [manual-03 package](docs/proposals/manual-ocr-third-run.md). Prerequisites: retained prior run/seal, exact cached inventory and unchanged installed/project versions. Acceptance: fresh ledger/seal, same 60/20 schedule and limits, no connected native execution, clear post-READY offline instructions. Evidence: new contracts initially failed; 15 passed in 0.071 s after test-fixture portability corrections; Ruff passed after import-order correction; PowerShell parsed; artifact/config hashes reverified. Fresh allocation 160, conservative preparation/closeout reservation 36; prior ledgers untouched. README/checkpoint and [handoff](docs/proposals/manual-ocr-handoff.md) updated. Source commit remains unapproved.
- [ ] User executes manual-03 disconnected, reviews synthetic fixtures, remains offline after READY, verifies teardown, then reports sanitized status. No automated native retry; adoption and subsequent work retain gates.

### T09 manual-03 stop and enum repair — 2026-11-14

- [x] Inspect [sanitized stop evidence](docs/benchmarks/manual-ocr-third-stop.md): 30 Tesserocr comparisons, first RapidOCR worker failed enum configuration, zero controls, teardown verified/no active children, ledger 79/160 preserved.
- [x] Correct configuration builder to accept actual library enums offline and fake enums in tests. Strengthened regression failed before repair; 15 passed in 0.118 s; Ruff passed after import-order correction. No connected native import, installation, OCR rerun or adoption. Prior prepared handoffs marked stopped; source commit remains gated.
- [ ] Obtain approval of a fresh bounded native continuation before preparing/resealing another offline run; never reset manual-03. RapidOCR initialization/inference and all controls remain unvalidated.

### T09 manual-04 — approved fresh continuation and scoped commit

- [x] Record explicit user approval of reviewed runner/docs/evaluation config commit and fresh same-test 160-start continuation after enum repair.
- [x] Prepare [manual-04 package](docs/proposals/manual-ocr-fourth-run.md): exact existing pins/assets/guards, new run ID/ledger/seal, prior manual-03 hash/count retained. Prerequisites verified statically; selection regression first failed, then 15 stdlib/fake tests passed in 0.052 s; Ruff/PowerShell syntax passed. Preparation/closeout conservatively reserved 40/160; no connected native OCR/import/render/install/download. Acceptance evidence: ignored seal/ledger, saved tests and current instructions; source commit approved, verify actual Git result.
- [ ] User runs only manual-04 disconnected, reviews fixtures, stays offline after READY until verified teardown, then reports sanitized status. Actual RapidOCR initialization/inference, controls and quality remain pending. No automatic retry or adoption.

### T09 manual-04 results closeout — 2026-11-14

- [x] Verify completed user-run summary: 60 unique comparisons and all 20 controls checked, verified teardown/no active owned children. Offline package check reused 52 installed packages; no native rerun during review.
- [x] Record [results and limitations](docs/benchmarks/manual-ocr-results.md), update README/checkpoint and mark handoff completed. Both engines passed 24/24 readable repetitions with zero observed error; rotated M08 failed for both. Tesserocr mean worker 1.02 s/max sampled private memory 193.82 MiB; RapidOCR 5.21 s/543.92 MiB. Completed native ledger 132/160, plus 4 sanitized closeout slots=136/160. Prior partial epochs remain separate. Documentation diff checks required; results commit pending approval.
- [ ] Decide remaining rotation/representative quality acceptance and prepare a separately reviewed T11 combined OCR/model resource package before further native execution/adoption. No engine adopted, no completed application/offline acceptance claimed.

- [x] User approved the manual-04 results commit and preparation of the next proposal. Rechecked rotated M08: all six measurements retain high text error/numeric mismatch; record user's positive visual assessment separately, with discrepancy open for local output review. No raw OCR output exposed, gold modified or native rerun. Shared result/Git closeout now 144/160; preserve 16 cleanup slots. Next proposal preparation does not authorize execution/adoption.

### T11 combined feasibility proposal — not execution approval

- [x] Prepare [bounded combined OCR/model proposal](docs/proposals/combined-ocr-model-trial.md), after approved OCR results commit 94f3e46. Documentation only: existing Nomic plus two chat candidates, two evaluated OCR engines, 36 chat/44 embedding attempts, 24 overlap OCR roots and four sentinels; proposed 160 starts/128 API attempts, 75-minute execution, conservative 8-GiB owned-workload cap, physical disconnection. Scope does not close T09/entire T11, select runtime engines, change gold or resolve rotated discrepancy. No installation or native run; proposal remains unapproved/uncommitted.
- [ ] User approves/amends exact candidate/schedule/resource/manual-boundary package before any helper implementation, preparation or execution. Separate proposal/source Git gate and runtime-adoption gate remain.

### T11-P1/P2 — approved combined-01 preparation

- [x] Record explicit approval of bounded implementation/offline testing and scoped reviewed commit. Implement only three authored evaluation files; no product code, dependencies, downloads or model adoption.
- [x] Test-first shared process/category/API meter, overshoot persistence, memory/deadline/ownership/residency, actual header/worker overlap, endpoint refusals and failed-request cleanup evidence. Initial 10 core contracts failed/passed; native interval regression fixed; selected-question reconciliation regression added. Final 14 passed in 1.197 s; Ruff lint/format passed. See [preparation report](docs/benchmarks/combined-ocr-model-preparation.md).
- [x] Reconcile historical question-file scope edit without changing any selected wording/gold; freeze old/current file hashes and exact prior case identities. Static preparation verified 142 sealed files and reused local immutable assets/fixtures. Full 48-slot preparation reservation; zero combined native/API attempts; prior ledgers unchanged. PowerShell syntax/hash/diff closeout required before final handoff. Source/docs commit approved; verify actual Git result.
- [ ] T11-P3–P5: user runs [combined-01](docs/proposals/combined-ocr-model-handoff.md) disconnected; remain offline until verified teardown. No new READY prompt or automatic retry. All combined native/resource/residency/quality outcomes remain unproven.
- [ ] T11-P6: after user reports teardown/reconnection, inspect sanitized summary only; retain raw local semantic review and partial/failure evidence. No engine/model adoption or full T09/T11 closure implied.

### USER PAUSE — 2026-11-14

Work paused at user's request to preserve daily token allowance. [Exact restart checkpoint](docs/session-checkpoint.md) records source/evidence/budgets and next steps. Current combined handoff is NOT READY: ownership regression added/guard implemented, but final Ruff stops at B023 test closures;15-test green validation and final reseal/quality review/commit remain pending. Earlier14-test/142-file preparation evidence is historical; the current seal is stale. No combined native/model/OCR execution, install or download occurred. Do not run any combined command until resumed work validates and reseals it. Preserve the56/160 ledger reservation, zeroAPI/native roots and original counters; user pause time is logged separately.

### T11 resumed final validation — 2026-11-14

- [x] User resumed from checkpoint; preserve original budgets/prior ledger links and exclude recorded user-pause time from active preparation. Ownership guard implemented and regression validated for owned versus recycled unrelated PIDs; test closures bound explicitly. Final15 stdlib/fake contracts passed0.713s; Ruff lint/format passed. No OCR/model import/inference, installation, rendering or download.
- [x] Preserve initial connected seal as seal.pre-review.json and regenerate only the never-started source/asset seal. Native roots/API calls remain0 and offline_started unset; preparation48 plus report16 conservatively reserved64/160. Final hash/link/PowerShell/diff review and approved scoped commit complete the handoff; actual native behavior still awaits disconnected user run. Historical pause/not-ready entries above describe the earlier source epoch, not approval to run an old seal.

- [x] Final resumed handoff review passed: all142 sealed files and prior-ledger hashes verified, PowerShell/relative links/diff checks passed; active preparation1453.6s excluding user pause. Combined API/native counts0, offline epoch not started. Proceed with previously approved scoped commit, then provide only the combined-01 disconnected command. No runtime/adoption claim.

### T11 combined-01 stop and approved combined-02 continuation

- [x] Preserve [combined-01 stop](docs/benchmarks/combined-ocr-model-first-stop.md): KeyError at first deadline sentinel, five metadata calls, zero completed controls/comparisons, teardown verified, old ledger75/160 unchanged.
- [x] User approved shared-deadline repair/tests and a fresh same-limit160-start run. Regression executes the actual reused OCR polling loop with fake Win32 calls: exact KeyError reproduced, normal cutoff and expiry agreement verified after fix. One timestamp supplies numeric/ISO cutoffs, with no guard extension. Explicit combined-02 CLI selection and shared module identity prevent old-command redirection; known missing-key diagnostics withhold untrusted keys.
- [x] Final18 stdlib/fake tests passed1.099s; Ruff passed. Rehashed143 source/asset/prior-ledger files without new dependencies/downloads, rendering or native OCR/model calls. Fresh [continuation](docs/proposals/combined-ocr-model-continuation.md)/[handoff](docs/proposals/combined-ocr-model-handoff.md) prepared; conservative32 preparation+8closeout=40/160,zeroAPI/native roots/offline start. Final seal/format/PowerShell/link/diff checks required before handoff. Repair/results documentation commit remains unapproved.
- [ ] User executes only combined-02 disconnected and reports sanitized result after verified teardown; never rerun/reset combined-01. Actual combined behavior, semantic quality and adoption remain unproven.

- [x] Final combined-02 readiness verified: all143 sealed identities, unchanged stopped ledger, PowerShell syntax/format/link/diff checks passed; no new native/API attempt. Current handoff is ready for the already approved disconnected user run. No Git commit created; ask separately before committing reviewed source/notes.

### Approved fake-only storage diagnostic completed — 2026-11-14

- [x] Reproduce both atomic-state replacement and temporary deletion after scan enumeration through actual Supervisor.storage/unchanged strict helper. Historical combined-02 missing path remains unconfirmed; [diagnostic report](docs/benchmarks/combined-storage-diagnostic.md) separates evidence from hypothesis.
- [x] Add sanitized filesystem/source diagnostics and local-only exact-path receipt, keeping quota/permission/reparse/missing-entry refusals unchanged. New regressions initially failed;21 stdlib/fake tests passed1.511s,Ruff passed. Diagnostic20/24 conservative starts inclcloseout,within10min,four cleanup slots;zero OCR/model/API/download/install,stopped native ledger hash unchanged. No live-scan repair or new offline run adopted/approved. Commit remains gated.
- [ ] Review proposed live-run counting policy/fake-worker repair before any fresh native package. Do not rerun combined-02 or share private error receipts.

### Approved live storage repair and reviewed commit — 2026-11-14

- [x] Implement separate live-run counter: handle already-removed descendants, preserve strict original helper, unchanged caps, required-root/type/identity, permission and reparse/link refusals. Actual historical missing path remains unknown. See [repair evidence](docs/benchmarks/combined-storage-repair.md).
- [x] New fake contracts failed before implementation;24 tests passed1.262s,Ruff passed after import separator correction. Both atomic rename/deletion scenarios still fail under strict helper and succeed under live counter. No native OCR/model/API/download/install; stopped native ledger hash unchanged. Repair allocation conservatively22/24 inclscoped Git closeout,10minute limit,two cleanup slots. User explicitly approved reviewed fixes/diagnostic/source/docs commit; verify actual Git result.
- [ ] Propose a fresh native continuation for separate approval; do not run/reset/reseal combined-01/02. Fake success does not close native feasibility, quality or adoption gates.

### Approved combined-03 preparation — 2026-11-14

- [x] User approved fresh combined-03 with same exact experiment/limits and new160-start allocation after repair commit e55a2b7. Preserve combined01/02 and fake diagnostic/repair epochs; new ledger hash-links all seven prior records, no counter reset or native-started reseal.
- [x] Select only combined-03 in CLI/controller/worker. Tests first failed,then24 stdlib/fake contracts passed1.539s; Ruff lint/format passed. Cached-only static preparation/verification creates fresh seal without inference/OCR/model import/render/install/download. Conservative32preparation+8report=40/160; native/API counters0,offline epoch unset. Final identity/PowerShell/link/diff checks precede handoff. New source commit remains unapproved.
- [ ] User runs current [combined-03 handoff](docs/proposals/combined-ocr-model-handoff.md) disconnected; typeOFFLINE,no READY prompt,remain offline through verified teardown. No automatic retry or engine/model adoption.

- [x] Final combined-03 readiness:146 sealed identities/all seven prior records verified unchanged; PowerShell/link/format/diff checks passed,within active-preparation limit. No native/API attempt. Validated current handoff ready; source/docs commit still unapproved.

### Combined-03 executed stop — 2026-11-14

- [x] Preparation source committed as d9a2792 under explicit user approval; executed source/handoff hashes matched seal. Later results remain uncommitted.
- [x] Record [resource-boundary stop](docs/benchmarks/combined-ocr-model-third-stop.md): allfour controls checked,three corpus embedding attempts,zero scored answers;teardown verified. Preserve56/160,eightAPI,fiveroots,nineextras. Resource guard stopped server; ReadError is downstream. Saved66 good observations do not include offending sample, so exact memory/headroom/gap trigger unknown.
- [x] User approved the fake-only 24-start/10-minute resource diagnostic repair. Completed four new regression tests and all 28 fake contracts (1.435 s); Ruff lint/format passed. Exact guard names, scalar measurements and unchanged limits are saved before shutdown, with summary propagation after cleanup. See [repair evidence](docs/benchmarks/combined-resource-diagnostic.md). No model/OCR/API/download activity; no new native allocation. Do not run old handoffs.
- [x] User approved the scoped repair/results commit; created `28844cb` with nine reviewed source/documentation files. Runtime data and unrelated files excluded. A fresh native trial remains separately gated.

### Approved combined-04 package

Package: [exact scope, limits, dependencies and acceptance](docs/proposals/combined-ocr-model-fourth-run.md). The user approved bounded preparation/offline execution and committing the five proposal documents, committed as `473d24a`. Native execution remains the disconnected user-run step, and later source/results commits retain their separate gate. [Preparation evidence](docs/benchmarks/combined-ocr-model-fourth-preparation.md) records tests, sealing and reservations.

- [x] **T11-C4-1 — Establish allocation.** Prerequisite: exact package approval, received. Fresh shared allocation links ten prior records; old epochs preserved. Initial inspection/initialization and approved proposal commit included. Status: complete; final immutability check precedes handoff.
- [x] **T11-C4-2 — Select fresh run.** Prerequisite: C4-1. Two selector regressions first failed; all 28 contracts then passed in 2.150 s and Ruff lint passed. Only combined-04 selectable; old/no-ID CLI and worker calls refused. Resource/privacy/cleanup controls unchanged. Status: complete.
- [x] **T11-C4-3 — Seal handoff.** Prerequisite: C4-2. Static preparation sealed and reverified 149 identities and ten unchanged prior records; PowerShell syntax and formatting passed. Final elapsed preparation check 250.468 s, reservations 36/160 (28 preparation + eight report), zero API/native starts, offline epoch unset. Final documentation links/diff check accompanies handoff. No connected native inference/download. Status: static readiness verified.
- [ ] **T11-C4-4 — Execute offline.** User attested OFFLINE and ran preparation commit `7ca4ee3`. Four controls passed; stopped during the second corpus embedding attempt on sampling_gap=259.0546ms >250ms. Zero scored chats. Matrix acceptance unmet; this allocation is closed, not queued for retry. See [stop evidence](docs/benchmarks/combined-ocr-model-fourth-stop.md).
- [x] **T11-C4-5 — Verify teardown.** Durable failing resource receipt and final summary agree. Zero owned children, process reaped, port released, teardown true. Preserve60/160,sevenAPI,fiveroots,nineextras/14observed; no rerun/reset/reseal. Status: verified.
- [x] **T11-C4-6 — Review results.** Sanitized status/counters/resource packet reviewed; stop report, README, handoff and checkpoint updated. No scored answers exist for semantic review. No adoption or full combined-feasibility claim. Results committed under explicit approval as `74fb75a`.

### Approved monitor cadence repair

[Static review, exact behavior, budget and acceptance](docs/proposals/combined-monitor-cadence-repair.md). User approved this32-start/ten-active-minute fake-only package and committing its five proposal documents. Keep hard250ms; change desired100ms scheduling to account for work and add accurate reading/scan timing checks. Tasks below may proceed in order; original pending labels are superseded by this approval. No native trial authorized.

- [x] **T11-M1 — Establish allocation.** User approved exact package; proposal documents committed as `fd3361b`. Fresh32-start/ten-active-minute fake-only allocation links old combined04 and resource-closeout hashes, reserves all commands up front. No downloads/API/model/OCR activity.
- [x] **T11-M2 — Reproduce timing problems.** Deterministic fake-clock/observer regressions failed first: three assertions/seven errors among33 tests against old implementation. No native workload or real-sleep benchmark.
- [x] **T11-M3 — Repair scheduling and measurements.** Work-aware wait and separate start/reading/collection/TCP/storage/iteration checks, all hard250ms. Scalar failed receipts and available collection timestamps retained; memory/ownership/disconnection/storage checks preserved. [Evidence](docs/benchmarks/combined-monitor-cadence-repair.md).
- [x] **T11-M4 — Verify and document.** All34 combined fake contracts passed2.164s; Ruff lint/format passed, source/privacy review completed. Package closed24/32starts,335.938s; prior hashes/link/diff checks passed. Eight source/report files committed under explicit approval as `0b345d5`. No native feasibility claim or new runner.

### Approved combined-05 package

[Exact scope, settings, limits and acceptance](docs/proposals/combined-ocr-model-fifth-run.md). User approved bounded preparation/disconnected execution and committing the five proposal documents. Tasks below proceed in order; their original pending-approval labels are historical. Later preparation source/results commits remain gated.

- [x] **T11-C5-1 — Establish fresh allocation.** User approved package; proposal documents committed79a2dea. Fresh160-start allocation links12 prior records and snapshots initial hashes/counters. Initial16 and additional12preparation/eightreport reservations share one ledger. Old epochs preserved. [Evidence](docs/benchmarks/combined-ocr-model-fifth-preparation.md).
- [x] **T11-C5-2 — Select fresh run.** Two expected routing regressions first failed; all34 fake contracts then passed1.774s, Ruff lint/format passed. Only05accepted; old/no-ID/traversal refused. Committed timing/resource/native adapter unchanged.
- [x] **T11-C5-3 — Verify sealed handoff.** Independent full rehash verified151identities and12unchanged prior records; PowerShell syntax passed. Readiness199.696elapsed seconds,36/160reservations,zeroAPI/native starts,offline epoch unset. Final links/diff check accompanies handoff. No connected native inference/download. Status: static readiness verified.
- [ ] **T11-C5-4 — Execute disconnected.** User ran offline; four controls passed, three embedding attempts, zero scored chats. Stopped on PermissionError/Windows5 at atomic JSON replacement, not a reported timing guard. Matrix acceptance unmet; allocation closed, never retry. Preparation committed `888f184`. [Stop evidence](docs/benchmarks/combined-ocr-model-fifth-stop.md).
- [x] **T11-C5-5 — Verify teardown.** Teardowntrue,zeroownedchildren,processreaped,portreleased. Preserve last persisted52/160,eightAPI,fiveroots,nineextras/14observed; failed state write means counters alone do not prove all attempted transitions persisted. Do not mutate/reset/reseal old records.
- [x] **T11-C5-6 — Review results.** Sanitized summary/meter and authored state-writer source reviewed; no answers for semantic review. Results committed under explicit approval as `dbe607a`. Exact lock/access cause unresolved; no native feasibility/adoption claim.

### Approved state-file investigation

[Exact synthetic scenarios, limits and acceptance](docs/proposals/combined-state-write-investigation.md). User approved package32starts/ten-active-minutes and committing five proposal documents, including one owned-fixture Windows sharing-handle test. Original pending labels below are superseded by approval; tasks proceed in order. No models/OCR/permissions change or writer-policy repair; later source/results commits remain gated.

- [x] **T11-SW1 — Inventory and allocate.** Exact package approved; five proposal documents committed4a2261e. Fresh32-start/600s allocation reserves all launches and links closed combined05/cadence hashes. Safe-role inventory recorded.
- [x] **T11-SW2 — Exercise synthetic file cases.** Own Windows no-delete-share and ordinary Python reader both reproduced Windows5/errno13; release restored replacement. Same-destination fixed-temp race produced FileNotFoundError; distinct destinations succeeded. Every handle/thread closed. [Evidence](docs/benchmarks/combined-state-write-investigation.md); historical locking handle unresolved.
- [x] **T11-SW3 — Verify accounting consequences.** Failed reserve/API persistence prevented simulated work; leftover temporary state refused restart; no-op still writes while changed/overshoot behavior remains covered. Only safe write/replace operation and known-role diagnostics added; writer policy unchanged.
- [x] **T11-SW4 — Review and document.** All40 tests passed3.464s; Ruff lint/format and source/privacy review passed. Closed29/32starts,466.578s; old hashes/link/diff checks passed. Seven investigation source/report files committed under explicit approval as `612378a`. No repair or native trial authorized.

### Approved state coordination repair

[Exact behavior, scope, budget and acceptance](docs/proposals/combined-state-coordination-repair.md). User approved40starts/15active minutes including both combined/OCR fake suites and a narrow legacy reader hook, plus committing five proposal documents. Original pending labels below are historical; tasks proceed in order. Later source/results commits and native continuation remain gated.

- [x] **T11-SR1 — Allocate and freeze scope.** Exact package approved; proposal documents committed2a65871. Fresh40-start/900s allocation links closed combined05/investigation hashes and reserves all commands. Five-source-file scope/default hook reviewed; legacy lint baseline0.
- [x] **T11-SR2 — Prove failures first.** Real-file/event/actual polling-hook tests failed first:59tests,3failures/4errors. Coordinators released and threads joined; no native model/OCR workload.
- [x] **T11-SR3 — Implement minimal coordination.** Core writer shares existingRLock; combinedOCR polling usesLedger.read via default-preserving legacy hook. No-op observations skip replacement; changed/high-water/overshoot/failure rules preserved. External-reader denial still fails. [Evidence](docs/benchmarks/combined-state-coordination-repair.md).
- [x] **T11-SR4 — Verify and document.** Both suites passed60tests2.534s; allfive files Ruff-clean, combined formatting passed, narrow legacy edits retain clean lint. Source/privacy review completed; final old-hash/link/diff/budget closeout accompanies report. No native continuation/adoption claim. Ten repair/report files await separate commit approval.
