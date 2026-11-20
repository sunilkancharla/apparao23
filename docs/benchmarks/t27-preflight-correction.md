# T27-R1 — Asset-preflight correction and S2 preparation

Date: 2026-11-20 (Asia/Calcutta). The user approved the exact [R1 repair/S2 package](../proposals/t27-preflight-correction.md) and the prior six-document S1 results-review commit. That review is committed as `8fabbfa`. R1-A/B/C were implemented and verified as recorded below; the operator subsequently completed R1-D and [S2 passed](t27-runtime-smoke-02.md). T27 implementation/bounded native integration verification is complete, with repair/results commit pending; CP10 stays open through the unstarted T28. Final resource/quality/runtime acceptance is not implied.

## Changes and alternatives

`app/diagnostics.py` now locates selected-model manifests under `manifests-v2/ollama.com/library`, the locally confirmed layout for selected Ollama 0.40.16. It retains pinned manifest identities, blob hashes/sizes and ancestry validation. Searching arbitrary directories, accepting a legacy fallback, moving the model store or downloading another model were unnecessary and would obscure the provisioning contract. Both selected-model relative identities are covered using small synthetic manifests/blob bytes; no real model is loaded by these tests.

`app/runtime.py` preserves the first safe failed-component code rather than replacing every asset error with `OLLAMA_ASSET_UNAVAILABLE`. No private path, document text or upstream error body is exposed. The startup integration fixture now represents the selected v2 layout without weakening its original assertions.

The existing smoke helper has a fixed S1/S2 package table. The default S1 allocation is explicitly closed and refuses execution even if its original root were absent. S2 has a distinct root, source seal, ledger identity and worker claim; cross-package claims fail. A parent records `native_teardown: not_started` only for normal worker completion corroborated by a bounded matching preflight-failure result, exactly two prepaid Python starts, zero calls and an empty native map. Unknown errors, malformed codes, forced worker termination and any native admission remain `unverified`. Local terminal output names the result files after supervisor completion.

At repair closeout, the [S2 handoff](../proposals/t27-runtime-smoke-02.md) and [25-file seal](../proposals/t27-runtime-smoke-02-seal.json) were prepared before creating any S2 root or native allocation. The operator subsequently ran that package once; its [separate native results](t27-runtime-smoke-02.md) are preserved and closed. All five [S1 receipt hashes](t27-runtime-first-stop.md#preserved-receipts) were rechecked unchanged; the original S1 seal is unchanged. It intentionally describes historical sources, not the repaired application.

## Verification

Repair tests use dummy executable/blob bytes, mocked process/DLL/transport seams and routine synthetic loopback fixtures. No real Ollama process, native inference, weight load or external request was started by those tests; actual S2 execution was separate and operator-local.

| Check | Actual result |
|---|---|
| Initial focused red tests: model assets plus smoke-budget tests | 18 failed, 13 passed, 0.88 s; failures exposed the layout/error/package/reporting gaps |
| Asset-only green, then assets/budget/owner green | 12 passed, 0.51 s; then 41 passed, 2.76 s |
| Malformed failure-code control before correction | 1 failed, 4 passed, 0.61 s; list-valued code raised `TypeError`; corrected with an explicit string guard |
| Final focused assets/budget/owner | 45 passed, 2.76 s |
| Declared-size negative control | Inverting the blob-size comparison caused the matching-hashes/wrong-declared-size test to fail; 1 failed, 1.06 s; original source restored exactly |
| Final full suite after restoration | **387 passed, 1 skipped, 1 warning, 38.24 s** |
| Ruff check and format check | Passed; 47 Python files already formatted |

The 22 added cases consist of 13 asset checks and nine smoke/package/reporting checks. They cover both selected-model identities, real-verifier preflight, changed manifest, absent/changed/incorrect-size blobs, matching hashes with incorrect declared size, no legacy fallback, unsafe ancestry, safe errors, closed-S1 refusal, cross-package worker refusal, source drift, package forwarding and conservative teardown classification. Existing owner/cancellation/deadline/output controls still pass.

Commands used the project interpreter, disabled third-party pytest plugin autoload and cache writes, and stayed in the approved routine allocation:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest tests/unit/test_model_assets.py tests/unit/test_runtime_smoke_budget.py tests/unit/test_runtime_owner.py -q -rP -p no:cacheprovider
.\.venv\Scripts\python.exe -m pytest -q -rP -p no:cacheprovider
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

These commands document completed verification, not an instruction to repeat or reset the allocation. The existing skip is Windows symlink permission; the existing warning is Starlette/HTTPX deprecation. The mutation-restored diagnostic Git blob is `d1804e01b09f746fa9992e8ee590e4060f489b43`; the new S2 seal records the actual file-byte SHA256 values separately.

## Combined allocation and review

`data/t27-repair-01/repair-budget.json` records the explicitly precharged 40 starts (red 4, green 4, regression 24, checks 8) within the 64-start approved ceiling. Actual red starts: 3; green: 3; regression including owned children: 13. Source-seal creation/check was check start 6; the final combined consistency/diff/receipt review reserves check starts 7–8 for its controller and Git diff child. No phase is reset or refunded; the check allocation is consumed. The final suite's own shared meter recorded **13/64 starts and 337,196/2,000,000 retained bytes**. Across all seven test invocations, reported retained charges total **557,570 bytes**, and reported test duration totals **46.82 seconds**. Seven retained test logs add **64,884 bytes**; the local combined ledger also includes its own bytes, the source seal and readable review diff under the 2,000,000-byte ceiling. These routine figures are separate from native S2, which had not started at repair closeout and was subsequently executed once by the operator.

Manual correctness/security review checked package/root propagation, sticky worker claims, no arbitrary CLI path, asset-pin preservation, fixed diagnostic output, source drift refusal and conservative failure reporting. The full regression and caught size mutation support the correction; they do not prove real Windows job creation, model execution, native cleanup, CPU residency, target-machine memory or offline acceptance. No dependencies, downloads, installs, schema, retention, model selection or readiness policy changed. No historical checkpoint/summary or unrelated user file was edited.

Original repair-closeout diff, including new authored files: `data/reviews/t27-preflight-correction.diff`. The subsequent S2 run passed and its receipts were reviewed; updated combined repair/results diff: `data/reviews/t27-s2-closeout.diff`. Source/results commit remains a separate user decision. T28 indexing is next and unstarted; no further S1/S2 execution is authorized.
