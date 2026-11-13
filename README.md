# Document Assistant

Stage 1 is a planned single-user document-chat prototype targeting Windows 11, 16 GB RAM and CPU-only operation. SPEC, AGENTS, PLAN, TODO and T02's design/rubric are approved. T01–T03 are complete; T04 SkillSpector was explicitly deferred. T05 is next; adoption/implementation remain gated.

## Current state

The dedicated project environment is `F:/document_assistant/.venv`, using Python 3.14.6 and local uv 0.13.8. Installed baseline: FastAPI 0.162.2, Uvicorn 0.54.0, HTTPX 0.28.1, pytest 9.2.0 and Ruff 0.17.5, with exact transitive versions in `uv.lock`. Global/user packages are not inherited. No application, selected parser/OCR/index/model or benchmark result exists yet.

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

The user authorized dedicated environment setup before later application tasks. Global installations/uninstallations are left to the user. uv executables, dependency environment and cache are contained in `.venv`; no PATH/profile changes. No application start or test-suite command exists yet.

From the project root, verified commands are:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\uv.exe --version
.\.venv\Scripts\uv.exe lock --check --offline
.\.venv\Scripts\uv.exe sync --frozen --offline --no-build
.\.venv\Scripts\ruff.exe --version
.\.venv\Scripts\python.exe -m pytest --version
```

Optional shell activation: `.\.venv\Scripts\Activate.ps1` (not invoked during verification). Explicit paths work without activation. `pyproject.toml` keeps uv cache inside `.venv`, disables automatic Python downloads and uses copy link mode. Offline sync was checked with this environment/cache already present; fresh provisioning needs approved network downloads. `.gitignore` excludes `.venv`, originals, runtime data and generated document artifacts. See [setup details](docs/provisioning.md) for the hash-verified uv bootstrap and exact checks. No app tests or model benchmarks have run.

## Next step

T03 host/baseline review is complete. T04 SkillSpector concludes with explicit user-approved deferral; no scanner trial or installation occurred. Manual skill/script review remains the fallback. The next planned task is T05, native PDF parser comparison, with candidate provisioning still subject to review.

T01 approvals include the limits, English-only OCR, core deletion rules, minimal HTML/CSS/JavaScript, speed/memory targets after initial benchmarks and the [bounded chart evaluation scope](docs/proposals/chart-interpretation.md). These are recorded in SPEC's approved T01 clarification. The user approved downstream review points for remaining retention, sample/quality and exact tooling/provisioning details. No trial or runtime support has been implemented.

Dedicated baseline setup is complete; later parser/OCR/model/service installation and architecture adoption remain separately gated. The target stays 16 GB/CPU-only. Six evaluation questions have checked CSV ground truth; thirteen authored artifact definitions await T22. No application or document/model benchmark is implemented by environment setup.
