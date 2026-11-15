# R1-A — fake-only accounting and verdict controls

## Outcome

The user approved the five-document static-review commit and exact R1-A package. Static review is committed as `3f7591a`. The fresh allocation `data/t17/public-review-accounting-01/` contains the prepaid block manifest, preservation hashes and closeout receipt. Earlier R1/R1-S allocations and all four authored source files remain unchanged.

**18 fake-control tests and Ruff passed.** No real trial worker, HTTP request, installation, download, candidate/native/model/parser/OCR execution or inference occurred. Python ran only authored fake tests and verification; project-local Ruff ran lint. This closes the fake-only task, not the unexplained Windows process count or G2.

## Authored controls

Two new aids under `tests/evals/spikes/` are `public_source_accounting.py` and `test_public_source_accounting.py`. The former is a typed, standard-library, single-writer policy prototype with no launcher or fetch entry point. It does not replace a host permission boundary or automatically intercept external tool calls.

- Reservations itemize orchestration, nested tools, shells and executables; a failed command retains its reservation and cannot reuse its label.
- Closed/unknown allocations reject admission. Exhaustion/deadline stop normal work while preserving a separate cleanup allowance; final closed state rejects cleanup admission too.
- Cumulative process discoveries are durably recorded and charged before stopping, including an overrun. Repeated observations do not double-charge; unknown/decreasing/invalid observations are refused.
- Cleanup observations distinguish close return, child reaping, remaining active members and accounting errors. Exceptions do not skip the other cleanup observations or the receipt attempt. Persistence failure propagates without success.
- A pair succeeds only when both ordered controls have the expected name, exit and exact error category, plus independent cleanup and count acceptance. An ordinary accounting error cannot stand in for the named injected failure.

These are fake-observation checks. A future real adapter must provide verified OS return values, observed identities and durable accounting integration; none is established by a cleared Python handle or passing unit tests. Concurrent ledger writers are unsupported.

## Test-first and review evidence

The initial focused command failed as expected because the new implementation module did not yet exist. After implementation,14tests passed in0.514seconds and Ruff passed. Four additional receipt/observation/closed-cleanup cases brought the suite to **18passed in0.221seconds**, with Ruff passing again after the test changes.

An in-memory mutation weakened the pair-completion predicate to check only cleanup for the second control. The second-control regression failed as expected (one failure,0.004seconds). The mutation was restored in memory and never written to source. It proves detection of this specific old false-success behavior, not comprehensive mutation coverage. No original failed helper or trial was rerun.

Verified commands:

```powershell
& 'F:\Python\Python314\python.exe' -I -S -B tests/evals/spikes/test_public_source_accounting.py
& .\.venv\Scripts\ruff.exe check tests/evals/spikes/public_source_accounting.py tests/evals/spikes/test_public_source_accounting.py
```

Tests use temporary, synthetic receipts and fake clocks/callbacks. They require no model, OCR assets, private documents or network. The old stopped-ledger fixture is not required by this successor suite.

## Shared execution accounting

All **48units were prepaid before authoring/execution**, including12protected stop units. The immutable allocation amounts are: preparation3, test authoring2, red4, implementation authoring2, green/lint5, correction10, closeout authoring2, final review5, close3, protected stop12. Failed/red commands are retained, with no refunds. Each orchestration call, nested command/authoring tool, shell and executable has its own charge category.

The correction block admitted8of its10reserved units: authoring2 and the test/lint/mutation command block6. Final review and closeout are prepaid too. The final receipt records observed duration, output size, block states and preservation/source hashes. Unused units remain charged reservations; they are not permission for another experiment. Host tool accounting still requires this external manifest and disciplined orchestration; the prototype alone cannot enforce calls outside its control.

## Next boundary

R1-A completes the approved fake-only prerequisite. The additional Windows process remains unidentified; do not increase the expected count or claim a successful real startup pair. Next prepare an instrumented standard-library launcher validation with an approved identity/event observation method, validated Windows declarations, explicit descendant accounting and its own finite allocation. Any real trial, public review, architecture adoption or results Git commit requires its separate approval. No security/advisory freshness or model-input-fit evidence was obtained here.
