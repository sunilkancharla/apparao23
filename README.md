# Document Assistant

Stage 1 is a planned single-user document-chat prototype targeting Windows 11, 16 GB RAM and CPU-only operation. SPEC, AGENTS, PLAN, TODO and T02's design/rubric are approved. T01–T03 and T05 are complete; T04 SkillSpector was explicitly deferred. T05 closes with approved PyMuPDF empirical-comparison deferral; runtime adoption remains pending.

## Current state

The dedicated project environment is `F:/document_assistant/.venv`, using Python 3.14.6 and local uv 0.13.8. Installed baseline: FastAPI 0.162.2, Uvicorn 0.54.0, HTTPX 0.28.1, pytest 9.2.0 and Ruff 0.17.5, with exact transitive versions in `uv.lock`. Global/user packages are not inherited. No application or selected runtime parser/OCR/index/model exists yet. The optional pdf-eval group installs pypdf 7.0.1, pdfplumber 0.11.10 and seven pinned dependencies locally for evaluation only; all baseline versions are unchanged. The approved tabular-eval group adds openpyxl 3.1.5, et-xmlfile 2.0.0 and defusedxml 0.7.1 for T07 evaluation only.

## Project documents

- [SPEC.md](SPEC.md): user-approved Stage 1 requirements and acceptance criteria.
- [AGENTS.md](AGENTS.md): persistent development and approval rules.
- [PLAN.md](PLAN.md): proposed architecture, open decisions, evaluation milestones and acceptance mapping.
- [TODO.md](TODO.md): the original 50 task IDs, with DOCX excluded from Stage 1 and completed scope-alignment task T02R, proposed XLS task T07A plus investigation T16A, with prerequisites, acceptance criteria and evidence requirements.
- [Decision register](docs/decisions.md): confirmed choices, approved downstream review points and sample inspection evidence.
- [Evaluation design](docs/evaluation.md): fixture coverage, inspection limits, scoring definitions and proposed quality gates.
- [Environment inventory](docs/benchmarks/environment.md), [dependency review](docs/dependencies.md) and [provisioning proposals](docs/provisioning.md): T03 findings and approval boundaries.
- [Fixture manifest](tests/evals/manifest.json) and [question definitions](tests/evals/questions.json): nine hashed supplied files, eleven authored definitions (eight in scope), twenty negative cases and twenty-five questions (twenty-one in scope). T02R added binary XLS definitions and a CSV injection replacement; no new document was generated.

T01–T03 are complete and T04 is deferred. No further installation, experiment, model pull, adoption or commit is authorized merely by plan/design approval.

## Planned functionality

The approved scope calls for local Ollama generation/embeddings, a browser UI, PDF/XLS/XLSX/CSV ingestion, scanned-PDF OCR, conversation attachments, a reusable library, saved chats, citations, and an evidence-support indicator. These are requirements, not implemented capabilities.

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

T07's approved XLSX/CSV trial is finished; the user approved committing its reviewed results and process updates. Remaining acceptance coverage is still open. The [report](docs/benchmarks/tabular-text-parsers.md) records 40 successful original-file workers, 15,656 sampled workbook cell values agreeing between readers per repetition, CSV value/line checks, nine passing full-suite tests plus a later focused duplicate-member test and mutation detection. These are bounded extraction results, not model/application scores. Genuine encrypted/VBA controls and full-workbook scalability remain gaps.

The T07 counter recorded 79 workers; the full suite also ran 13 T05 regression workers outside it, totaling 92. The combined 80-worker cap was not enforced across the test session. No further workers after identifying the gap. Future combined trials need one shared budget including regressions. The persistent trial budget prevents silently rerunning parser tests; arrange a fresh approved run and unused output/basetemp before reproduction. Ruff and offline frozen sync/lock passed. No application is implemented.

The three approved process improvements are implemented: SPEC consolidates settled decisions; AGENTS permits exact bounded packages without repeated step approvals; PLAN/TODO prioritize T10 embedding and T11A fixed-evidence chat feasibility, with combined OCR/model checks before adoption. CSV remains the first end-to-end slice. XLS/XLSX/PDF expansion and full Stage 1 acceptance remain required. Optional RTK/ponytail cannot delay the first slice; UI UX Pro Max stays before frontend implementation.

T07/process updates are committed in `e8ec471`. The approved T10 package installed hash-verified Ollama 0.40.16 at `.venv/tools/ollama/0.40.16/ollama.exe` and both models under `data/ollama/models`; no global/PATH/service or Python dependency changes. The [completed bounded embedding comparison](docs/benchmarks/embeddings.md) records four CPU passes per model: both achieved recall@5 1.00 on 12 closely related CSV variants; lexical recall@5 was 0.9583. Gemma passes took 5.23–7.43 seconds, Nomic 5.56–6.26 seconds. Nomic had smaller weights/lower observed run-wide native memory and is recommended for later adoption review; no runtime model is selected. Original failure/accounting uncertainty is preserved. The approved continuation used 24/24 starts and 82/100 calls, with zero downloads; final 11 tests passed. Ruff passed before the hash-reference correction. The owned server stopped and port release was verified. Do not rerun helpers/tests against either consumed phase: another run needs an explicit new allocation. Combined chat/OCR, wider quality and disconnected-runtime acceptance remain unverified. T11A chat review is next and separately gated; T07A XLS remains required. DOCX/TXT remain excluded entirely.
