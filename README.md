# Document Assistant

Stage 1 is a planned single-user document-chat prototype targeting Windows 11, 16 GB RAM and CPU-only operation. SPEC, AGENTS, PLAN, TODO and T02's design/rubric are approved. T01–T03 and T05 are complete; T04 SkillSpector was explicitly deferred. T05 closes with approved PyMuPDF empirical-comparison deferral; runtime adoption remains pending.

## Current state

The dedicated project environment is `F:/document_assistant/.venv`, using Python 3.14.6 and local uv 0.13.8. Installed baseline: FastAPI 0.162.2, Uvicorn 0.54.0, HTTPX 0.28.1, pytest 9.2.0 and Ruff 0.17.5, with exact transitive versions in `uv.lock`. Global/user packages are not inherited. No application or selected runtime parser/OCR/index/model exists yet. The optional pdf-eval group installs pypdf 7.0.1, pdfplumber 0.11.10 and seven pinned dependencies locally for evaluation only; all baseline versions are unchanged.

## Project documents

- [SPEC.md](SPEC.md): user-approved Stage 1 requirements and acceptance criteria.
- [AGENTS.md](AGENTS.md): persistent development and approval rules.
- [PLAN.md](PLAN.md): proposed architecture, open decisions, evaluation milestones and acceptance mapping.
- [TODO.md](TODO.md): 50 approved planned tasks plus proposed investigation T16A, with prerequisites, acceptance criteria and evidence requirements.
- [Decision register](docs/decisions.md): confirmed choices, approved downstream review points and sample inspection evidence.
- [Evaluation design](docs/evaluation.md): fixture coverage, inspection limits, scoring definitions and proposed quality gates.
- [Environment inventory](docs/benchmarks/environment.md), [dependency review](docs/dependencies.md) and [provisioning proposals](docs/provisioning.md): T03 findings and approval boundaries.
- [Fixture manifest](tests/evals/manifest.json) and [question definitions](tests/evals/questions.json): nine hashed supplied files, nine authored fixture definitions, sixteen negative cases and nineteen questions.

T01–T03 are complete and T04 is deferred. No further installation, experiment, model pull, adoption or commit is authorized merely by plan/design approval.

## Planned functionality

The approved scope calls for local Ollama generation/embeddings, a browser UI, PDF/DOCX/XLSX/CSV/TXT ingestion, scanned-PDF OCR, conversation attachments, a reusable library, saved chats, citations, and an evidence-support indicator. These are requirements, not implemented capabilities.

## Setup and verification

The user authorized dedicated environment setup before later application tasks. Global installations/uninstallations are left to the user. uv executables, dependency environment and cache are contained in `.venv`; no PATH/profile changes. No application start command exists yet; the PDF evaluation tests are runnable below.

From the project root, verified commands are:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\uv.exe --version
.\.venv\Scripts\uv.exe lock --check --offline
.\.venv\Scripts\uv.exe sync --frozen --group pdf-eval --offline --no-build
.\.venv\Scripts\ruff.exe --version
.\.venv\Scripts\python.exe -m pytest --version
```

The available evaluation suite passed with five tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp=data/pytest-pdf-t05-07 --tb=short
.\.venv\Scripts\ruff.exe check tests/evals/spikes
.\.venv\Scripts\ruff.exe format --check tests/evals/spikes
```

For a rerun, choose a fresh unused path below `data/` for `--basetemp`; pytest can remove an existing base directory. The socket-denial test requires the restricted environment used for T05. See the [PDF report](docs/benchmarks/pdf-parsers.md) for benchmark reproduction, measurements and limitations.

Optional shell activation: `.\.venv\Scripts\Activate.ps1` (not invoked during verification). Explicit paths work without activation. `pyproject.toml` keeps uv cache inside `.venv`, disables automatic Python downloads and uses copy link mode. Offline sync was checked with this environment/cache already present; fresh provisioning needs approved network downloads. `.gitignore` excludes `.venv`, originals, runtime data and generated document artifacts. See [setup details](docs/provisioning.md) for the hash-verified uv bootstrap and exact checks. Five PDF evaluation tests passed; no application tests or model benchmarks exist yet.

## Next step

T03 host/baseline review is complete. T04 SkillSpector concludes with explicit user-approved deferral; no scanner trial or installation occurred. Manual skill/script review remains the fallback. T05 is complete. The [PDF evaluation report](docs/benchmarks/pdf-parsers.md) records the authorized pypdf/pdfplumber trial: 24 bounded real-sample runs, five passing evaluation tests, native/table/image controls and known layout/OCR gaps. User accepted deferral of the unrun PyMuPDF empirical comparison and authorized the T05 commit. No runtime parser was selected.

T01 approvals include the limits, English-only OCR, core deletion rules, minimal HTML/CSS/JavaScript, speed/memory targets after initial benchmarks and the [bounded chart evaluation scope](docs/proposals/chart-interpretation.md). These are recorded in SPEC's approved T01 clarification. The user approved downstream review points for remaining retention, sample/quality and exact tooling/provisioning details. No trial or runtime support has been implemented.

Dedicated baseline setup is complete; later parser/OCR/model/service installation and architecture adoption remain separately gated. The target stays 16 GB/CPU-only. Six evaluation questions have checked CSV ground truth; thirteen authored artifact definitions await T22. Environment setup did not implement an application; the later T05 PDF experiment is separately documented.
