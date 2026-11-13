# Session checkpoint - 2026-11-14 (Asia/Calcutta)

## Goal and persistent scope

Stage 1 local document assistant for Windows 11, 16 GB RAM, CPU only. Approved SPEC/PLAN/TODO; formats PDF/XLSX/CSV only. Legacy XLS deferred; DOCX/TXT excluded. One user/browser UI, local Ollama, SQLite; no complete application/UI yet. Early native-PDF/tabular and embedding/chat evaluations exist, with limitations and no runtime adoption. SkillSpector deferred; do not revisit. Read AGENTS/SPEC/README/PLAN/TODO before continuing. No subagents authorized.

## Current T09 state

Windows native isolation investigation ended after AppContainer permission grants were denied. Do not reopen it by default. User accepted a disconnected, synthetic-only OCR trial without filesystem confinement; original exact manual package approved and proposal committed in `76db076`. Runner preparation committed in `c7709cd`.

The user ran manual-01 offline. Offline uv resolution succeeded (53 packages, 16 additions), then our checker falsely rejected installed `pdfminer.six` versus lock `pdfminer-six`; no installation/sync, fixture or OCR occurred. Teardown verified, no active worker, root pyproject/lock restored. Old ledger recorded 104/240 reservations and must remain untouched. Sanitized report: `data/t09-manual-ocr/manual-01/summary.json`; [diagnosis](benchmarks/manual-ocr-first-stop.md). Never read raw OCR/user document content into remote tools.

Name canonicalization fix plus first-stop report committed as **`6120666`**. Exact versions remain required. Source checks case-insensitive runs of `.`, `_`, `-` as the same distribution separator. Its 13 regression/contract tests and Ruff passed; no native rerun.

## Fresh handoff prepared, not approved to execute

User approved preparing a fresh resealed handoff and requested chat compaction. Working source now supports explicit `manual-02` run selection (including worker request routing and PowerShell defaults), while retaining stopped manual-01. Added regression: **14 tests in 0.061 s**, Ruff passed, PowerShell syntax parsed. Standard-library-only preparation rehashed existing artifacts and generated `data/t09-manual-ocr/manual-02/run.ps1`, prepared state, proposed project file and source/config seal. No package installed/imported as OCR, PDF/image generated or native trial executed.

The user subsequently explicitly approved the new [continuation package](proposals/manual-ocr-continuation.md), **160 total starts** including fresh preparation, and its source/handoff commit. This is not a reset of the prior 104. It retains exact cached artifacts, offline/manual/synthetic limits and 60 comparison/20 negative roots. Its ignored meter links the prior meter SHA/count; `execution_approved=true` is authorized for the user's disconnected local start only. Do not give the old run command or reset/reseal its state.

Current closeout: OCR coordinator/test/PowerShell run-selection changes, README/TODO/handoff updates, continuation proposal and this checkpoint are approved for commit. Verify working diff/seal/ledger and create only that reviewed source commit. Then hand off `data/t09-manual-ocr/manual-02/run.ps1`. No automated native retry, installation or OCR is authorized while connected. User execution remains disconnected with local fixture review and teardown verification before reconnecting. If this checkpoint is read after closeout, inspect Git for the resulting commit and the sanitized manual-02 status before taking further action; never assume the user has run it.

## Host, workspace and checks

Tools expose no callable `/compact` or `/status` operation. Do not claim compaction ran. The user can use a host-provided command if available; this checkpoint preserves state independently. No goal mode is active/requested.

Unrelated untracked `agents/`, `skills/`, `references/`, `images/` and reference/onboarding docs predate this task. Preserve them; never stage the whole workspace. `.venv/`, `data/`, samples/models/databases/generated artifacts remain ignored. Git writes require approved host escalation; source edits do not approve commits. Project installs stay inside `.venv`; no global/PATH/pip fallback. Native installation/OCR still awaits the user-run offline phase and explicit continuation approval; no accuracy/offline application claims yet.
