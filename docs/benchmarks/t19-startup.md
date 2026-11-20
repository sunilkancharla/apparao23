# T19 — Local configuration and startup diagnostics

Date: 2026-11-20. Authorization: the user's explicit instruction to proceed with T19 following T18 commit `0658bea`. Existing Python/project-local environment and pinned dependencies reused. No dependency, lock, SPEC, AGENTS or ignore-rule changes; no installation, downloads, private documents, global environment changes, native model/OCR execution or historical evaluation reruns.

## Implemented scope

`app/config.py` validates explicit `DA_*` settings against C01: literal `127.0.0.1`, distinct configurable app/Ollama ports (8000/11435), managed `data/app` default, explicit local asset paths and protected-directory separation. Errors omit configuration values. Existing ancestry is checked for symlinks/Windows reparse attributes before managed-root creation and before asset reads. A temporary write probe is removed when closed; no existing file is overwritten or deleted.

`app/diagnostics.py` checks the pinned Ollama executable and English OCR asset SHA256 values from the accepted dependency inventory. Approved chat/embedding manifest hashes anchor bounded manifest parsing; config/template/license/weight blobs must match their manifest sizes and SHA256 values. Missing, changed and incomplete assets yield component codes. Asset checks run once at startup, not per request. No native library, model or OCR engine is imported/executed. Matching asset bytes do not establish engine interoperability or model quality.

The model endpoint is configured as a literal loopback authority. The diagnostics code attempts an exclusive local bind to check port availability, without connecting to or making HTTP requests to an existing listener. An occupied/restricted port reports `OLLAMA_PORT_IN_USE`; a free port reports `OLLAMA_NOT_STARTED`. T19 never attaches to a service it does not own. Launching/monitoring owned Ollama and actual model API integration remain later implementation work, including T27/T30; old trial allowances are not reused.

`app/main.py` reserves the exact app port and passes that owned socket to Uvicorn. Supported invocation: `.\.venv\Scripts\python.exe -m app.main` from the project root. Invalid config or unavailable app port exits 2 with safe explanatory text. Only `GET /api/health` is exposed; it returns a typed component summary with HTTP503 and `ready: false`. An unwritable managed root remains visible through diagnostics. No UI, uploaded content, chat, database or mutation API is exposed.

Host must match the configured loopback authority exactly. A supplied Origin must match the exact configured origin. Duplicate/mismatched authorities and mutation methods are refused with403; HTTP route errors and unexpected handler exceptions use safe structured errors. Responses have no-store/nosniff/frame-denial/referrer/CSP headers. Proxy-header trust and access logging are disabled by the launcher; docs/OpenAPI assets are disabled. No outbound HTTP client, cloud fallback, service download, telemetry or CDN is introduced. Missing services are not mistaken for readiness.

## Verification

Tests were written before their corresponding behavior. The initial run failed collection because `app` did not exist; after implementation, 21 tests passed with one symlink-permission skip. Additional tests reproduced an unsanitized unexpected-error response and Windows control-character/drive-relative path acceptance; the fixes passed. The first real-server poll timed out in the sandbox; the integration run was repeated with host permission and subsequently passed. Polling now handles both connection refusal and connection timeout within a ten-second deadline. No host firewall/global setting was changed.

Final normal suite (historical `tests/evals/` excluded by T18 configuration):

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp=data/t19-tests-final-02
```

Observed: **36 passed, 1 skipped, 1 warning, 6.16 seconds**. The skipped test needs Windows symlink-creation permission. A separate test injects a Windows reparse attribute at the filesystem metadata boundary and verifies refusal without that privilege. The unchanged warning is Starlette's deprecation of its HTTPX test-client integration; no filter or new dependency was added.

Coverage includes unsafe/unknown settings, missing and tampered assets, synthetic approved-manifest/layer checks, writable/unwritable roots, protected-root overlap, reparse ancestry, safe exception text, Host/Origin denial, blocked mutations, actual loopback health requests, port collisions and captured-log redaction. Routine checks use missing/synthetic fixture assets. A real Python server and a second collision-check launcher run as bounded child processes; the server is terminated and reaped in `finally`. The unknown-listener test verifies that no connection was accepted by that listener. No native runtime or inference process starts.

Ruff `check app tests/test_project_setup.py tests/unit tests/integration` passed. Ruff format passed for all seven relevant Python files. Initial formatting/lint findings (formatting, nested context manager, explicit subprocess check, privacy-boundary exception catch) were resolved. The final broad exception catch is intentional only at the HTTP privacy boundary; exception values/tracebacks are not emitted.

Review mutation: temporarily changed the Host mismatch comparison to equality. The focused missing-prerequisite API test failed with403 versus expected503, proving it exercises the request guard. The original source bytes were restored and verified exactly; the mutation was not retained.

## Review and limitations

Review covered correctness, scope, privacy, request boundaries, filesystem ownership and bounded work. No additional dependencies or unexpected external calls were introduced. No application request payload or query string is logged. Captured stdout/stderr from the actual launcher contained neither the sentinel question nor its configured private data-root path. These are synthetic log checks, not a full operating-system traffic audit or an assertion that same-account hostile processes are isolated.

Managed-path validation is a check/use control, not filesystem confinement or protection against concurrent same-account replacement. Startup hashes are not a permanent integrity guarantee. Restored/changed assets require a restart to refresh diagnostics. OCR package/native loading and model execution remain unverified by this slice. The application deliberately remains unready even if every asset is present because it has no owned model-service integration yet.

The health API is read-only. A browser anti-CSRF handshake must precede later mutation endpoints; blanket mutation refusal protects this slice without introducing an unused token flow. Full browser UX/preview headers, persistence, quota enforcement, generation budgets and strict disconnected-runtime acceptance remain later tasks. No T20 work or stage transition is included. Changes remain unstaged pending the separate commit decision.
