# T03 Provisioning Proposals

**Status:** Dedicated `.venv` baseline installed and verified at the user's request. The historical proposals below are superseded where indicated; parser/OCR/model/service provisioning remains gated.

## Current verified setup

- `F:/document_assistant/.venv` uses CPython 3.14.6, disables global site-packages and user-site inheritance. Other installations/uninstallations are left to the user; global packages were not changed.
- Since uv was absent, existing Python's stdlib `venv --without-pip` bootstrapped the environment. Subsequent dependency resolution/install used uv; no pip/requirements workflow was substituted.
- The proposed ZIP host returned HTTP 403. Official PyPI wheel `uv-0.13.8-py3-none-win_amd64.whl` was retrieved and matched to its publisher SHA-256: `cfbc13020a64cdf2f116d2936824c38edbf41e5c07f1ea291baf02e31ebf3ed0`. Download: 15,624,377 bytes. Paths/size budgets checked before placing uv/uvx/uvw executables in `.venv/Scripts`; receipt under `.venv/.bootstrap/uv-receipt.json`. No installer, PATH/profile changes or `.tools` installation.
- Installed direct pins: FastAPI 0.162.2, Uvicorn 0.54.0, HTTPX 0.28.1; dev pytest 9.2.0 and Ruff 0.17.5. `uv.lock` records 24 installed distributions. No source builds, global upgrades, parsers, OCR tools, Ollama or models.
- `pyproject.toml` persists `.venv/.cache/uv`, disabled automatic Python downloads and copy link mode. Environment including bootstrap/cache: 157,216,478 bytes at verification; not a RAM measurement.
- Verified imports/package locations, global PyMuPDF invisibility, uv/Ruff/pytest versions, lock consistency and frozen offline sync. No telemetry exporter/SDK/cloud CLI in the resolved graph; API-only telemetry dependency remains. No application tests, document/model benchmarks or runtime privacy certification.
- `.gitignore` excludes environments, originals and runtime/generated files. No staging/commit. The user brought baseline preparation forward from T18; other T18/application work is not complete.

Validated commands from the project root:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\uv.exe --version
.\.venv\Scripts\uv.exe lock --check --offline
.\.venv\Scripts\uv.exe sync --frozen --offline --no-build
.\.venv\Scripts\ruff.exe --version
.\.venv\Scripts\python.exe -m pytest --version
```

Optional activation: `.\.venv\Scripts\Activate.ps1` (created but not invoked during verification). Explicit executable paths work without activation/policy changes. Offline sync passed using the current environment/cache; a fresh machine needs approved provisioning. No fully disconnected application claim.

## Historical P01 — loose-tool proposal, superseded and not executed

Concrete first proposal: retrieve the official **uv 0.13.8 x64 Windows ZIP**, verify the published SHA-256, inspect/extract into the project-owned `.tools/uv/0.13.8/` directory, and verify its version. No installer script, global PATH/profile edit, Python/package/model download, self-update, virtual environment, runtime dependency or application scaffold is included.

- [Official release](https://github.com/astral-sh/uv/releases/tag/0.13.8).
- Artifact: `https://releases.astral.sh/github/uv/releases/download/0.13.8/uv-x86_64-pc-windows-msvc.zip`.
- [Published checksum](https://releases.astral.sh/github/uv/releases/download/0.13.8/uv-x86_64-pc-windows-msvc.zip.sha256): `529e78a9cec6cd7e3e014f7ecd8bda0c113969d4ed0f2efeedb85c30943325b8`.
- License: MIT OR Apache-2.0. Alternative: reviewed standalone installer or WinGet package; direct archive is proposed to avoid installer/profile effects. The checksum verifies the retrieved artifact against the publisher's value, not an independent security guarantee.
- Proposed bootstrap budget: at most 64 MiB compressed and 256 MiB extracted; inspect actual size/layout and reject unsafe archive paths before extraction. These are approval-request bounds, not measured artifact sizes. Record the actual footprint afterward. No benchmark workload is part of this bootstrap.
- Destinations: temporary ZIP under the task-specific temporary directory; binary under `F:/document_assistant/.tools/uv/0.13.8/`. Add an ignore rule for `.tools/` before any staging; do not commit binaries or originals. No recursive delete/overwrite of existing directories.

Reviewable command sequence after scoped approval (archive/layout/budget checks must precede extraction/execution):

```powershell
$uvArchivePath = Join-Path ([IO.Path]::GetTempPath()) 'document-assistant-uv-0.13.8.zip'
Invoke-WebRequest -Uri 'https://releases.astral.sh/github/uv/releases/download/0.13.8/uv-x86_64-pc-windows-msvc.zip' -OutFile $uvArchivePath
$uvArchiveHash = (Get-FileHash -LiteralPath $uvArchivePath -Algorithm SHA256).Hash.ToLower()
if ($uvArchiveHash -ne '529e78a9cec6cd7e3e014f7ecd8bda0c113969d4ed0f2efeedb85c30943325b8') { throw 'uv checksum mismatch' }
# Inspect actual archive size, entry paths/layout and expanded-size budget here.
Expand-Archive -LiteralPath $uvArchivePath -DestinationPath 'F:/document_assistant/.tools/uv/0.13.8'
# Locate the verified uv.exe under that root; confirm layout before execution.
```

The [official installation guide](https://docs.astral.sh/uv/getting-started/installation/) supports prebuilt artifacts. No pip/requirements alternative is being substituted. Actual executable layout, version output and commands are not yet locally validated because the tool is not installed.

## Historical P02 — baseline proposal, now provisioned as above

Proposed initial interpreter: existing `F:/Python/Python314/python.exe` (3.14.6), satisfying SPEC's 3.11+ floor; compare an approved older managed Python only if native/parser compatibility requires it. Never inherit global packages. A missing interpreter must produce an error rather than silently download one; uv's [Python guide](https://docs.astral.sh/uv/guides/install-python/) documents that automatic downloads are enabled unless disabled.

Candidate baseline pins: FastAPI 0.162.2, Uvicorn 0.54.0 (minimal), HTTPX 0.28.1, pytest 9.2.0 and Ruff 0.17.5. These are review candidates, not approved together or installed. Transitive resolution/native wheels/license/security/privacy checks in `docs/dependencies.md` must be completed before an exact resolved installation is approved. No standard/all extras, exporters, browser framework or global upgrades.

Candidate commands after approval and after the real task requires an environment:

```powershell
$env:UV_PYTHON_DOWNLOADS = 'never'
# Use the exact verified uv.exe path; not an unverified PATH command.
# uv venv --python 'F:/Python/Python314/python.exe' .venv
# Project pyproject/lock creation is T18, after G2; do not run uv add/sync now.
# uv sync --frozen --offline is an eventual reproduction check after assets are cached.
```

The commented commands are future workflow descriptions, not validated commands or requests to scaffold the application. No project environment or dependency graph was created in T03. Future isolated investigation environments need their own reviewed exact dependency set and budget under G1.

## P03 — Ollama, models and OCR, separate proposals

Do not bundle these with uv bootstrap. First choose exact Ollama release/artifact/license, install/model locations, update policy and bounded download/disk budget. Review cloud disablement/loopback binding and CPU-only configuration, and verify them on actual local runs. No cloud accounts/API keys are required by Stage 1. Observe process/traffic behavior rather than assuming a desktop install cannot update externally.

Then separately review model digests/licenses/quantizations/sizes and English OCR/rendering assets. Model names in SPEC are candidates only. Existing SPEC pull commands are not approved provisioning. No version/size/license or machine suitability is claimed for unreviewed model/OCR artifacts.

## Current review boundary

The target remains 16 GB/CPU-only. Dedicated `.venv` and the reviewed baseline were requested and installed; the historical loose `.tools` proposal was not used. P03 and later optional-tool/model trials retain their approval gates. Installing the baseline does not complete runtime architecture adoption. No source commit or next task starts automatically.

T05 follow-up: the user authorized continuing with permissive alternatives after licensing review. Nine exact pdf-eval packages were installed using uv sync --frozen --group pdf-eval --no-build. Offline frozen sync and lock check passed after provisioning. No baseline pins/global installs changed; PyMuPDF was excluded. Tests/measurements and remaining review gates are in [the PDF report](benchmarks/pdf-parsers.md).

## T07 — Approved tabular-eval group, installed

The user approved the three-pin/local-fixture/trial package. Added openpyxl==3.1.5, et-xmlfile==2.0.0 and defusedxml==0.7.1 with project uv; lock review verified exactly three additions, approved wheel hashes and unchanged earlier pins. Installed using `.venv/Scripts/uv.exe sync --frozen --group pdf-eval --group tabular-eval --no-build`; both groups retained. Offline frozen sync and lock check passed after caching. No source builds/global/PATH/interpreter changes.

The [actual report](benchmarks/tabular-text-parsers.md) records installed notices/footprint, fixtures/measurements, encrypted/VBA gaps and combined worker-budget accounting failure. No further parsing workers after discovery. Future combined trials need a fresh shared cap including regressions; do not silently reset existing budgets. Evaluation only, no runtime adoption. Model/OCR/XLS assets still need exact future package approval; approved process rules remove redundant requests within an already approved package.

## T10 — Approved isolated provisioning and completed continuation

The user explicitly approved the documented continuation without `/goal`. No additional downloads/packages: installed executable and both weight hashes rechecked, frozen corpus/original result preserved. The separate continuation completed Nomic and lexical comparisons with 24/24 starts, 82/100 calls and zero downloads; final 11 helper tests passed. Native observed starts (12) and explicit reservations are persisted separately, including the charged failed hash-reference preflight. The original run's unknown stop cause/count remains a historical limitation. Owned server stopped/port released; neither ledger may be reset or reused to authorize another run. No runtime adoption or disconnected/combined acceptance is implied. See [results, resource accounting and reproduction limits](benchmarks/embeddings.md). The partial-trial record below is historical.

The user approved the exact package after location/license clarification. Provisioning completed: Ollama 0.40.16 at `.venv/tools/ollama/0.40.16/ollama.exe`, both pinned models at `data/ollama/models`, runtime home under `data/ollama/runtime-home`. Archive and layers hash-verified; native extraction 2,267,275,279 bytes; charged transfer 2,515,473,387 bytes including conservative interrupted-write accounting. Native notices were inventoried. No global/service/PATH/user-store modifications or Python dependency additions. The owned server is stopped and port release verified. Gemma completed its schedule, Nomic failed on its first batch; final actual process accounting/stop diagnostics are incomplete. See the [current results and proposed continuation allocation](benchmarks/embeddings.md). Do not restart the original phase or reset its deadline/counters. The following paragraphs preserve the original approved proposal.

The [complete approval package](benchmarks/embeddings.md) pins Ollama v0.40.16 `ollama-windows-amd64.zip` (1,618,244,995 bytes and release SHA-256), EmbeddingGemma 300m BF16 and Nomic Embed Text v1.5 F16 (896,157,760 combined weight bytes, exact manifests/layers). Proposed native executable location is `.venv/tools/ollama/0.40.16/`, archive/cache under `.venv/.cache/ollama`, models under `data/ollama/models`, all runtime home/config/log/temp state under project data. No global/service/PATH changes or modification of existing user model records. No Python packages added. Native extraction/notices must be inspected before execution; model/manifest drift stops provisioning.

One approval would cover the named downloads, license review, isolated setup, necessary test-first helpers, fixed-evidence benchmark and owned-process teardown: 3 GiB network, 12 GiB disk, 90-minute provisioning; separate 30-minute benchmark, 40 shared process starts including regressions/engine children, 200 loopback calls, 6 GiB engine-tree plus 1 GiB controller and 4 GiB minimum available-memory guard. CPU-only/cloud-disabled/loopback operation must be observed. Gemma terms require the user's review/agreement; Nomic uses Apache 2.0. No binaries/weights, engine startup, inference or runtime adoption occurred during read-only review. Chat models/T11A remain a separate exact package, not part of this proposal.
