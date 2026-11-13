# Document Assistant

**Latest scope decision (2026-11-13):** Stage 1 supports PDF, XLSX and CSV only. Legacy XLS is deferred; DOCX/TXT remain excluded. T07A/T37 and XLS-specific evaluation definitions are inactive, with historical evidence and local samples preserved. T08 is closed with approved non-adoption/trial deferral. T09 artifact preparation is complete after its approved continuation; no OCR packages were installed or OCR runs performed. Part B remains gated.

Stage 1 is a planned single-user document-chat prototype targeting Windows 11, 16 GB RAM and CPU-only operation. SPEC, AGENTS, PLAN, TODO and T02's design/rubric are approved. T01–T03 and T05 are complete; T04 SkillSpector was explicitly deferred. T05 closes with approved PyMuPDF empirical-comparison deferral; runtime adoption remains pending.

## Current state

The [OCR execution-boundary comparison](docs/proposals/ocr-trial.md#native-execution-boundary-recommendation---pending-decision) recommends AppContainer feasibility review before a separately approved preflight. Sandbox and a manually disconnected synthetic-only trial are alternatives with different limits. No boundary is selected or tested; no OCR installation/execution is authorized by this documentation.

The [AppContainer preflight](docs/benchmarks/appcontainer-preflight.md), subsequently approved and proposed in `e6ecd5a`, stopped at the first unrestricted staged-Python startup (`0xC0000142`). Eight policy tests and Ruff passed; the existing runtime was copied/hashed under `.venv`, without changing global Python. No profile, permissions change, network control or OCR occurred. Isolation compatibility remains unverified; further execution requires a separately approved diagnostic package.

The dedicated project environment is `F:/document_assistant/.venv`, using Python 3.14.6 and local uv 0.13.8. Installed baseline: FastAPI 0.162.2, Uvicorn 0.54.0, HTTPX 0.28.1, pytest 9.2.0 and Ruff 0.17.5, with exact transitive versions in `uv.lock`. Global/user packages are not inherited. No application or selected runtime parser/OCR/index/model exists yet. The optional pdf-eval group installs pypdf 7.0.1, pdfplumber 0.11.10 and seven pinned dependencies locally for evaluation only; all baseline versions are unchanged. The approved tabular-eval group adds openpyxl 3.1.5, et-xmlfile 2.0.0 and defusedxml 0.7.1 for T07 evaluation only.

## Project documents

- [SPEC.md](SPEC.md): user-approved Stage 1 requirements and acceptance criteria.
- [AGENTS.md](AGENTS.md): persistent development and approval rules.
- [PLAN.md](PLAN.md): proposed architecture, open decisions, evaluation milestones and acceptance mapping.
- [TODO.md](TODO.md): the original 50 task IDs, with DOCX excluded from Stage 1 and completed scope-alignment task T02R, deferred XLS task T07A plus investigation T16A, with prerequisites, acceptance criteria and evidence requirements.
- [Decision register](docs/decisions.md): confirmed choices, approved downstream review points and sample inspection evidence.
- [Evaluation design](docs/evaluation.md): fixture coverage, inspection limits, scoring definitions and proposed quality gates.
- [Environment inventory](docs/benchmarks/environment.md), [dependency review](docs/dependencies.md) and [provisioning proposals](docs/provisioning.md): T03 findings and approval boundaries.
- [Fixture manifest](tests/evals/manifest.json) and [question definitions](tests/evals/questions.json): nine hashed supplied files, eleven authored definitions (seven in scope), twenty negative cases (sixteen in scope) and twenty-five questions (sixteen in scope). T02R added binary XLS definitions and a CSV injection replacement; no new document was generated.

T01–T03 are complete and T04 is deferred. No further installation, experiment, model pull, adoption or commit is authorized merely by plan/design approval.

## Planned functionality

T10 evaluation is committed in `55d68f6`. The approved [T11A chat benchmark](docs/benchmarks/chat-models.md) now has completed results for all 96 planned request slots, across 97 retained attempts including the original timeout. Both pinned Apache-licensed Qwen2.5 1.5B/Qwen3 1.7B Q4_K_M models are in the project store; no new Python/global installation. The continuation completed only the remaining 13 Qwen3 requests, using 30/32 starts and 19/40 calls with no downloads. Final 27 tests and Ruff passed; owned processes stopped and port cleanup independently verified. Completed-response medians were 10.57 s and 14.21 s respectively, with separate-session/cache caveats and the original timeout kept outside those duration summaries. Raw answers and an escaped local review of 35 distinct output/failure groups are under `data/t11a/continuation-01/combined-review.html`; the user qualitatively accepted the local outputs on 2026-11-13; structured answer/citation scores remain unfilled. T11A evaluation code/documentation is committed in `0872c22`. No runtime model or full Stage 1 capability is adopted. Qwen2.5 3B's research-license decision remains separate. Further inference is not needed for this frozen schedule; commits and subsequent tasks require their own approval.

The approved scope calls for local Ollama generation/embeddings, a browser UI, PDF/XLSX/CSV ingestion, scanned-PDF OCR, conversation attachments, a reusable library, saved chats, citations, and an evidence-support indicator. These are requirements, not implemented capabilities.

## Setup and verification

The user authorized dedicated environment setup before later application tasks. Global installations/uninstallations are left to the user. uv executables, dependency environment and cache are contained in `.venv`; no PATH/profile changes. No application start command exists yet; the PDF evaluation tests are runnable below.

From the project root, verified commands are:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\uv.exe --version
.\.venv\Scripts\uv.exe lock --check --offline
.\.venv\Scripts\uv.exe sync --frozen --group pdf-eval --group tabular-eval --offline --no-build
.\.venv\Scripts\ruff.exe --version
.\.venv\Scripts\python.exe -m pytest --version
```

Historical T05 verification commands (five tests then passed; later T07 checks are recorded below):

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp=data/pytest-pdf-t05-07 --tb=short
.\.venv\Scripts\ruff.exe check tests/evals/spikes
.\.venv\Scripts\ruff.exe format --check tests/evals/spikes
```

For a rerun, choose a fresh unused path below `data/` for `--basetemp`; pytest can remove an existing base directory. The socket-denial test requires the restricted environment used for T05. See the [PDF report](docs/benchmarks/pdf-parsers.md) for benchmark reproduction, measurements and limitations.

Optional shell activation: `.\.venv\Scripts\Activate.ps1` (not invoked during verification). Explicit paths work without activation. `pyproject.toml` keeps uv cache inside `.venv`, disables automatic Python downloads and uses copy link mode. Offline sync was checked with this environment/cache already present; fresh provisioning needs approved network downloads. `.gitignore` excludes `.venv`, originals, runtime data and generated document artifacts. See [setup details](docs/provisioning.md) for the hash-verified uv bootstrap and exact checks. Five PDF evaluation tests passed; no application tests or model benchmarks exist yet.

## Current evaluation and next step

The approved continuation/license findings are committed in `6491666`. [OCR artifact preparation completed](docs/benchmarks/ocr.md): all 16 wheels and three English assets verified, with 14 cached wheels reused unchanged. Ten synthetic preparation tests passed. The continuation transferred 14,856,592 bytes across 12 requests, including redirects/license-source responses; the original stop and meter remain preserved. Native/bundled notice obligations are recorded, including the exact FlatBuffers companion notice. No installation, OCR import, rendering or inference occurred. Next: agree the native execution boundary and approve Part B before installation/measurement. T09's OCR comparison is still incomplete.

**Earlier evaluation records (historical where superseded by the completed continuation above):**

Stop report committed in `7c50144`. The authorized [FlatBuffers license investigation](docs/benchmarks/ocr.md) found upstream Apache-2.0 text and exact byte matches for all ten cached runtime Python files. Recommend preserving that pinned license alongside the unchanged wheel through an explicitly approved exception. A [new artifact-only continuation](docs/proposals/ocr-trial.md#proposed-part-a-continuation-after-flatbuffers-investigation) would reuse the 14 cached wheels and fetch only the remaining 14,780,070 artifact bytes under fresh limits. The user approved this exact exception, artifact-only continuation and findings commit; installation and OCR execution remain unapproved.

The approved OCR proposal is committed in `bf3b82e`. [Part A stopped](docs/benchmarks/ocr.md) when the pinned FlatBuffers wheel had no located license/notice material. Fourteen wheels matched exact hashes/sizes; notice collection completed for thirteen. Transfer was 125,721,610 bytes across 14 requests; all 16 conservative process slots are consumed. Five synthetic preparation tests passed after retained failures. Separately listed English assets remain unfetched; cached wheels contain bundled native/default-model bytes but were not installed or imported. Next proposed work is source/license investigation and a new bounded continuation using verified cache. T09 remains incomplete, and Part B/native OCR execution remains unapproved.

The OCR shortlist is committed in `1337560`. The [T09 proposal](docs/proposals/ocr-trial.md) pins 16 new wheels and three English assets (133.99 MiB planned payload), including tesserocr's bundled Tesseract 5.5.4 and RapidOCR CPU. Full OCR comparison remains conditional on reviewed artifacts and an agreed native execution boundary. The installed environment and lock remain unchanged; actual partial downloads are recorded above.

T08 review/approved deferral is committed in `1621862`. The initial [T09 OCR source review](docs/benchmarks/ocr.md) compared Tesseract and RapidOCR/ONNX Runtime CPU for English PDF OCR. Its standalone-installer gap led to the later tesserocr wheel proposal; the actual Part A stop above now governs continuation. RapidOCR still requires explicit English local models to avoid default selection/download paths. No runtime engine or assets are adopted/installed. OCR remains required; T09 is not complete.

T08's [MarkItDown source/dependency review](docs/benchmarks/markitdown.md) is complete. Recommendation: keep format-specific parser candidates for architecture review and avoid adopting MarkItDown as the ingestion backbone, because its Markdown result lacks the structured source mappings our citations need. Its XLSX path adds pandas; exact classifier/native/transitive costs remain unmeasured. No packages installed or samples converted. The user approved non-adoption, deferring the empirical comparison, committing this review and starting the T09 read-only OCR review. No runtime parser is selected.

T07A's [XLS review](docs/benchmarks/xls-parsers.md) is committed in `e3c598d`; the user approved its exact bounded trial. Preflight stopped because direct Winsock controls did not establish enforced native network denial. Four control tests and Ruff passed; no packages downloaded/installed, parsers imported, fixtures generated or samples parsed. The three supplied XLS samples retain checked hashes/compound-file headers. The user subsequently deferred XLS outside Stage 1; this stopped trial is retained as history and will not continue. No XLS capability or runtime reader is adopted.

T07's approved XLSX/CSV trial is finished; the user approved committing its reviewed results and process updates. Remaining acceptance coverage is still open. The [report](docs/benchmarks/tabular-text-parsers.md) records 40 successful original-file workers, 15,656 sampled workbook cell values agreeing between readers per repetition, CSV value/line checks, nine passing full-suite tests plus a later focused duplicate-member test and mutation detection. These are bounded extraction results, not model/application scores. Genuine encrypted/VBA controls and full-workbook scalability remain gaps.

The T07 counter recorded 79 workers; the full suite also ran 13 T05 regression workers outside it, totaling 92. The combined 80-worker cap was not enforced across the test session. No further workers after identifying the gap. Future combined trials need one shared budget including regressions. The persistent trial budget prevents silently rerunning parser tests; arrange a fresh approved run and unused output/basetemp before reproduction. Ruff and offline frozen sync/lock passed. No application is implemented.

The three approved process improvements are implemented: SPEC consolidates settled decisions; AGENTS permits exact bounded packages without repeated step approvals; PLAN/TODO prioritize T10 embedding and T11A fixed-evidence chat feasibility, with combined OCR/model checks before adoption. CSV remains the first end-to-end slice. XLSX/PDF expansion and full Stage 1 acceptance remain required. Optional RTK/ponytail cannot delay the first slice; UI UX Pro Max stays before frontend implementation.

T07/process updates are committed in `e8ec471`. The approved T10 package installed hash-verified Ollama 0.40.16 at `.venv/tools/ollama/0.40.16/ollama.exe` and both models under `data/ollama/models`; no global/PATH/service or Python dependency changes. The [completed bounded embedding comparison](docs/benchmarks/embeddings.md) records four CPU passes per model: both achieved recall@5 1.00 on 12 closely related CSV variants; lexical recall@5 was 0.9583. Gemma passes took 5.23–7.43 seconds, Nomic 5.56–6.26 seconds. Nomic had smaller weights/lower observed run-wide native memory and is recommended for later adoption review; no runtime model is selected. Original failure/accounting uncertainty is preserved. The approved continuation used 24/24 starts and 82/100 calls, with zero downloads; final 11 tests passed. Ruff passed before the hash-reference correction. The owned server stopped and port release was verified. Do not rerun helpers/tests against either consumed phase: another run needs an explicit new allocation. Combined chat/OCR, wider quality and disconnected-runtime acceptance remain unverified. T11A chat review is next and separately gated; T07A XLS is deferred outside Stage 1. DOCX/TXT remain excluded entirely.
