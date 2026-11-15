# Stage 1 Decision Register

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
