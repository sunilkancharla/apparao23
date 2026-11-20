# Combined resource diagnostics repair — 2026-11-14

The user approved a fake-only repair bounded by 24 starts and ten minutes. No OCR/model inference, API calls, installation or download was performed. The stopped combined-03 meter was hash-linked in the new local allocation and was never reset or resealed.

## Change and evidence

The resource checker now reports separate identifiers for available physical memory, controller private memory, owned private memory, kernel peak job commit, and sampling gap. A failure carries only these scalar readings, their limits, and all observed violations. Extra input fields are excluded. The supervisor writes the packet atomically to local `resource-failure.json` before propagating the exception to the existing fail-closed observer. The final summary receives the same packet after supervisor cleanup. Successful memory observations retain their existing meaning; the failed packet is separate.

Limits are unchanged: at least 4 GiB physical headroom, at most 512 MiB controller private memory, at most 8 GiB owned/job commit, and at most 0.25 seconds between samples. Equality remains accepted. CPU/model settings, process ownership, network checks, execution budgets, storage guards and cleanup logic are unchanged. A receipt-write error also propagates to the observer and stops work; the in-memory packet remains available for summary handling. A disk failure cannot guarantee a durable receipt.

Four new tests cover each guard and exact edges, privacy of the retained packet, real temporary-file persistence before the observer's failure callback, and receipt-write failure. The initial run had seven expected errors across three new test methods because the diagnostic interfaces did not exist; the existing 24 contracts passed. The fourth test subsequently checked the actual observer path using a fake resource sample.

Final commands:

```powershell
& 'F:/Python/Python314/python.exe' -I -S -B data/t11/resource-diagnostic-01/test_bootstrap.py
& '.venv/Scripts/ruff.exe' check --no-cache tests/evals/spikes/combined_trial.py tests/evals/spikes/combined_native.py tests/evals/spikes/test_combined_trial.py
& '.venv/Scripts/ruff.exe' format --check tests/evals/spikes/combined_trial.py tests/evals/spikes/combined_native.py tests/evals/spikes/test_combined_trial.py
```

Results: **28 tests passed in 1.435 seconds**, lint passed, all three files formatted. Earlier lint findings were corrected without suppressions. The bootstrap uses only trusted standard-library Windows process limits, with fake trial boundaries; it does not load an OCR or inference backend. Source diff review confirmed that guard thresholds and ownership/cleanup controls are preserved. Documentation was checked directly; no extra shell was started after the allocation was consumed.

Conservative accounting includes all 24 PowerShell, Python, Ruff, rg and Git inspection starts in this turn, including pre-initialization inspection. All slots were reserved up front; the allocation is closed, with no further starts permitted. The final execution check was 70.634 seconds after ledger initialization; inspection and closeout also fit within ten minutes. Local budget and completion receipts are under `data/t11/resource-diagnostic-01/` and remain excluded from Git.

## Limits and next gate

This repair cannot recover the missing combined-03 failure reading. Its original stop remains unexplained beyond the generic resource boundary. No combined feasibility, model/OCR adoption or production application claim follows from fake tests. These changes require scoped commit approval. A new native allocation, run identity and seal require separate approval; every previous stopped handoff remains invalid.
