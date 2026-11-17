# T17-IF-EA — adapter suite caught missing-field normalization bug

## Outcome

The user approved EA1–EA6 and its planning commit, made as `a09d8cc`. Expected RED demonstrated that an explicit dictionary still invokes prohibited default discovery. The corrective adapter/graph source was then authored. Its fixture suite ran **11 tests: nine passed and two errored**. Optional work stopped as required. The original ten controls and real dependency comparison **did not run**.

The [approved EA boundary](../proposals/marker-environment-adapter-review.md) remains authoritative for this stopped run. Ignored source, full diagnostics, captured streams, process receipts and accounting are under `data/t17/marker-environment-adapter-01/`. No correction or rerun has been applied there.

## Evidence and task status

| Task | Result |
| --- | --- |
| EA1 | Nine fixed inputs, 20 installed tool-source hashes and two installed metadata identities matched. Original strict guard and unchanged verified capture aid copied; old dispatch excluded. |
| EA2 | RED failed as expected at denied hostname discovery. Baseline adapter/graph hashes and a pre-implementation receipt establish ordering; behavior tests existed before corrective implementation. |
| EA3 | Partial: nine tests passed, two errors share the missing-field normalization bug. Suite is not GREEN; no assertion was weakened or removed. |
| EA4 | Blocked by EA3; original ten-control attempt not started. |
| EA5 | Blocked; real retained-artifact/lock graph not started. Fixture graphs are not project dependency findings. |
| EA6 | Stop receipt and findings recorded; closeout checks below. |

Passing cases covered observed/hypothetical profile separation, active/inactive/extras markers, factory freshness/restoration including exceptions, avoiding the original discovery factory, retaining strict socket/subprocess denials, unrelated-error propagation, the shared cross-profile graph cap and unknown/multiple-version metadata fixtures.

Errors occurred in `test_missing_fact_and_compound_are_unknown` and `test_graph_statuses_and_extras`. The full 4,053-byte authored test diagnostic is retained in `green.json`. Worker stdout was a bounded error status, not the test diagnostic. Both captured worker results were complete, and both workers/controllers exited. The original strict guard, including hostname denial, remained installed in the tool workers.

## Cause and proposed correction

Installed packaging 26.3 declares `UndefinedEnvironmentName(KeyError)`. Its missing-field lookup raises this public exception with the field as its argument. The adapter used `str(error)`; KeyError-style formatting produces **`'platform_release'` including quotes**, which fails the whitelist's comparison with `platform_release`. The adapter re-raised it. This is a bug in the authored adapter, not evidence of dependency incompatibility or a need to relax the guard.

The proposed correction reads the single public exception argument and validates its type before the existing whitelist:

```python
field = error.args[0] if len(error.args) == 1 else None
if not isinstance(field, str) or field not in {'platform_machine', 'platform_release', 'platform_system', 'platform_version', 'extras', 'dependency_groups'}:
    raise
```

Only the first two lines change; the existing raise and allowed-field set remain unchanged. Do not strip arbitrary quotes, invent values, broaden exception handling or swallow unrelated errors. The failed tests already require the correct field value and conservative unknown behavior; preserve them unchanged.

No orchestration correction, Ruff/web/model run, candidate installation/import, platform-helper subprocess or product feature occurred. Packaging remained the existing review tool. The copied capture aid's earlier eight-case result is historical evidence, not a new suite run. No Job, filesystem confinement, kernel egress or memory benchmark is claimed.

At the stop receipt: 374.500 active/wall seconds, zero host-wait exclusion, 64 work units/32 starts prepaid, two of four check invocations consumed. Unused reservations do not authorize restarting this stopped root. Final elapsed time, leases and retained bytes are in the local summary. Read leases exclude total OS/interpreter I/O.

## Proposed bounded follow-up EAF1–EAF5 — pending approval

This concrete follow-up is included in the seven-file results review so approval can cover its execution directly. It is **a new package**, not a reset/retry of EA's ledger. No follow-up code, root or process has been created. The factory override, partial-profile contract, original strict guard, original ten-control semantics and conditional graph rules in the EA proposal remain unchanged.

Fresh ignored root: **`data/t17/marker-environment-adapter-02/`**. Refuse an existing/reparse root; bootstrap/freeze first. Copy only the source below and the verified tool inventories, preserve earlier roots read-only, and validate every identity. The prior failed tests are reused explicitly as RED evidence; do not spend another invocation reproducing the same failure.

| Fixed EA source/input | Bytes | SHA-256 |
| --- | ---: | --- |
| `adapter.py` | 2,028 | `959ef8fb327b9a7a7a164b5211470de99238f68f93f81cbf7e2e5d003de857ef` |
| `graph.py` | 3,708 | `9cabb127c6c21f2dc75baf8fd1fd8957d4746baff0f55faaab315cb72231d3da` |
| `tests.py` | 5,555 | `c364f4658b1bdfac6460467395916fc9559a812c7769d67fe225c4a06109bc5a` |
| `tool.py` | 1,921 | `43d5a30bb50d40782d121674006f1b65e979d1e6a635a138398e332c38f4bd2c` |
| `parser_controls.py` | 10,059 | `7c5a2fc97c6441f8a3abe5b88b3d6490b4bb78c149d2a960255bef85f662716b` |
| `run.py` | 1,381 | `f449c577446a05b6e37024671a6fd4e2f5bd6fdd832a1988d50bd3cc65a6cf32` |
| `guard.py` | 422 | `c58b576024f5efaa341fb324295d8aa98c81ad3b45be735e5db58611fe758490` |
| `capture.py` | 4,482 | `15849ddbd03c992da78baee314b48731c036d7ab5563e1719e61892f64b590d3` |
| `input-identities.json` — nine original pinned identities | 2,065 | `e69356268b49c314e9e32483f5515b7946058e098168ae06521c10e22a5c4884` |

All table paths are relative to the stopped EA root. Verify the nine targets named by `input-identities.json`, plus the 20 source/two metadata identities from its pinned inventories, before use. Use existing isolated `F:/Python/Python314/python.exe` and packaging 26.3; no new tools/dependencies or global paths.

| ID | Objective / prerequisite | Acceptance / evidence |
| --- | --- | --- |
| EAF1 | After approval, bootstrap/freeze and copy the exact failed source/tests | Fixed hashes, prior failure evidence and strict guard verified. No old dispatch or library-source patch. |
| EAF2 | After EAF1, apply only the two-line exception-field correction; run unchanged 11-test suite once | Full suite passes; tests/graph/guard/capture unchanged; missing fields remain unknown, unrelated errors propagate. Failure stops optional work. |
| EAF3 | Only after EAF2 passes, one original ten-control attempt | Complete admitted capture/exit/teardown and passing result; no discovery or broader exception. Failure blocks graph. |
| EAF4 | Only after EAF3 passes, one real local graph comparison | Same two labelled partial profiles and 20 exact-node global union, statuses/unknown closure/lock conflicts preserved; no resolver, pin change or licence/provenance claims. |
| EAF5 | Completion/stop closeout | Actual resources, source diff, tests, preservation/scope/link/whitespace/readable-diff/empty-index/non-null receipt; separate results-commit/adoption gates. |

Shared new-package limits: **48 prepaid units** (correction/GREEN 8, original controls 8, graph 16, protected closure 16); **32 total owned starts**, including all shells/controllers/workers/negative/regression/Git work; **three ordered check invocations** (unchanged GREEN, original controls, conditional real graph); zero Ruff/web/model runs. Parent alone owns immutable leases; include unused/failed reservations and never reset the meter.

Allow **1,800 active seconds**, optional cutoff 1,200 and closure reserve 600; exact allowlisted interpreter commands without a shell, 60-second command deadline plus 15-second teardown. Hold direct handles/PIDs through exit; workers may not spawn descendants. Use **64 MiB** explicit reads including 8 MiB ledger allowance, **16 MiB** retained artifacts, **64 KiB** aggregate reporting including 16 KiB closure reserve, 8 KiB raw host/worker streams per invocation, 3,000 UTF-8 displayed bytes and 2 MiB authored graph JSON. At most 48 immutable ledger records/validations, 4 KiB each. Retain admitted diagnostics before display; complete means both EOFs and verified exit.

Unexpected GREEN failure, unsafe identity, cap/cutoff, host denial, lost/truncated capture or uncertain ownership stops optional work. Complete original-control failure blocks graph. One trustworthy orchestration correction within the same limits; no automatic reruns. At most two measured host-prompt submission-to-entry/decision-observation waits totaling 24 hours, without intervening model work; no exclusion of ordinary work. Report wall/active/host separately.

No hostname exception, subprocess permission, cache prewarming, private helper calls, installed-file edits, archive/native rereads, candidate imports/installs, public research or user data. Keep the review-only public factory override/restoration and labelled partial profiles; passing remains declarative evaluation, not runtime adoption or target-machine performance proof.

Deliver ignored source/receipts/profiles/graph/accounting and `docs/benchmarks/marker-environment-adapter-followup.md`, plus affected updates to this report's follow-up status, dependencies, preflight, PLAN, TODO and README: seven versioned closeout documents maximum. Preserve AGENTS, SPEC, pyproject/lock, existing versioned tests/manifests, historical checkpoints and unrelated changes. The future results commit/adoption remain separate gates.

Request **EAF1–EAF5 execution approval** and the **current seven-file EA results commit** separately. Approving the results commit alone does not authorize the follow-up. Dependency/licence/provenance/offline/parity/G2 decisions remain open.

Current EA closeout checks passed: seven-document scope; nine frozen inputs/nine prior pinned identities preserved; 20 tool-source/two installed metadata hashes and eight follow-up source hashes checked; 21 local links, whitespace, readable diff, empty index and non-null receipt verified. SPEC, lock/configuration, existing versioned tests/manifests, historical checkpoints and unrelated user files remain unchanged. No EAF root or corrective code has been created. Final accounting is retained in the stopped root's summary.
