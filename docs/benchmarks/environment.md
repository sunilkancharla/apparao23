# T03 Workstation Inventory

**Status:** Read-only inventory completed; no performance benchmark or application smoke test. Recorded 2026-11-13, Asia/Calcutta.

## Subsequent authorized environment setup

The initial inventory below predates provisioning. The user subsequently required a dedicated `.venv` and reviewed baseline installation here. `.venv` now uses Python 3.14.6 with system/user site disabled; uv 0.13.8 resides in `.venv/Scripts`, cache in `.venv/.cache/uv`, and the locked baseline has 24 installed distributions. Imports, versions, lock check and frozen offline sync passed. Global PyMuPDF is not visible inside the environment. Global installations were not changed. Environment/cache/bootstrap disk footprint was 157,216,478 bytes; no RAM benchmark. See `docs/provisioning.md` for receipt and commands. Ollama/models/OCR remain uninstalled by this task.

## Approved target versus observed hardware

The approved target remains **Windows 11, 16 GB RAM, CPU only**. Windows reported different installed hardware; the user explicitly replied “don't change, keep it as before.” Do not change SPEC or rely on the detected GPU/additional RAM to pass acceptance.

| Item | Observed |
|---|---|
| OS | Windows 11 Home Single Language; version 10.0.26300, build 26300 |
| CPU | Intel Core i5-8250U @ 1.60 GHz; 4 cores / 8 logical processors |
| Reported physical RAM | 21,379,649,536 bytes, about 19.9 GiB |
| Available RAM at inspection | 9,262,196 KiB; a changing snapshot, not workload capacity |
| Display adapters | Intel UHD Graphics 620; NVIDIA GeForce MX150; no GPU use approved |
| F: free space | 37,233,471,488 bytes, about 34.7 GiB; snapshot only |

Later experiments must record actual host memory and combined process/system pressure and evaluate the agreed 16 GB target explicitly. Results measured on this larger-memory machine alone do not prove strict 16 GB compatibility. Define the resource/headroom protocol before those trials; do not silently impose a new app memory limit or modify system memory settings.

## Local tools and service checks

- Python 3.14.6, 64-bit AMD64, at `F:/Python/Python314/python.exe`; `py -0p` lists only this interpreter. Standard-library SQLite reports 3.50.4. This satisfies the specified Python 3.11+ floor; parser/native-wheel compatibility remains a trial check.
- Git is on PATH. uv and Ollama were not on PATH. uv was also absent from the checked per-user executable/WinGet locations; Ollama was absent from two checked conventional per-user paths. These checks are not an exhaustive machine-wide installation search.
- No process matching Ollama was visible. Read-only requests to `127.0.0.1:11434/api/version` and `/api/tags` failed, including outside the sandbox: “Unable to connect to the remote server.” No service version or model inventory can be established. This is not proof that no models exist anywhere on disk.
- No project `.venv`, `pyproject.toml` or `uv.lock` exists. Global installed packages are inventory evidence only, not the project environment.

| Globally installed package | Observed version |
|---|---|
| FastAPI | 0.162.2 |
| Uvicorn | 0.54.0 |
| HTTPX | 0.28.1 |
| pytest | 9.2.0 |
| PyMuPDF | 1.28.2 |

uv, Ruff, pypdf, python-docx, openpyxl and MarkItDown were not found in this interpreter's distribution metadata. Do not reuse global packages or launch document parsing merely because a package happens to be installed.

## Method and limits

Used `Get-Command`, bounded conventional-path existence checks, `Get-Process`, standard-library Python version/architecture/SQLite/importlib.metadata inspection and two read-only loopback API requests. Hardware CIM queries were denied by the sandbox; the user approved the read-only queries outside it, and they succeeded. The localhost requests were also retried outside the sandbox to distinguish access restrictions from a service failure.

No inference endpoint, model pull, parser trial, package install, GPU driver change or external content-processing service was invoked. Public upstream documentation was consulted separately, without user document content. Version output and package metadata do not demonstrate that the project runs, that wheels resolve together, or that runtime is offline/private. Those remain later checks.
