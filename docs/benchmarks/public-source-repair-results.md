# R1-S startup/cleanup repair — stopped, no research

The user approved the eleven-file R1 closeout commit and exact no-network R1-S package. Commit `986305d` records the former. Fresh allocation: `data/t17/public-review-repair-01/`. Failed R1 state and original authored aids remain unchanged.

## Checks and changes

Two successor aids (`public_source_repair.py` and `test_public_source_repair.py` under `tests/evals/spikes/`) initialize the missing body reservation on a copy of the real stopped ledger, implement both job-accounting callbacks, and independently attempt close, reaping and receipt persistence. No fetch entry point exists.

Tests reproduced both original defects using the archived initializer and actual `NativeJob.close()` with fake kernel calls. Two successor tests initially failed because its file did not yet exist. After implementation, **13 tests passed in0.026seconds**, including nine earlier URL/count/body/deadline/launcher cases. Ruff passed on both new files after correcting its initial findings. Existing isolated base Python (`-I -S -B`) and project-local Ruff were used; nothing was installed.

An in-memory mutation disabling cleanup caused the regression to fail as expected (one failure,0.001seconds). The first mutation command failed from PowerShell quoting before testing; its charge remains. The successful mutation used standard input, changed no source and launched no workers. This is not complete mutation coverage.

## Real integration stop

The first direct standard-library worker exited **0**, but Windows reported **two cumulative job processes**, exceeding the expected single-process protocol. The observer recorded this before raising. The pair stopped; the forced-failure real worker was **not run**. No automatic retry is authorized. There were zero HTTP attempts, downloads, installations, candidate/parser/OCR/model loads or inference.

| Persisted observation | Value |
|---|---:|
| Cumulative kernel processes |2 |
| Active job processes after direct child exit |0 |
| Direct child reaped / job handle closed |true / true |
| Caught cleanup-accounting error |RuntimeError |
| Elapsed through observation, before final cleanup |0.4137144seconds |
| Minimum sampled available physical memory |10,849,521,664bytes |
| Sampled peak job memory |6,897,664bytes |

The generic `teardown_verified` is false because it requires zero active processes **and exactly one cumulative process**. Separate fields establish zero active job members, a reaped child and closed handle. This is not evidence of a surviving worker, successful pair, verified single-process launcher or model-resource result. No system-wide process inventory or additional-process identity was captured. Executable metadata says “Python”, original filename `python.exe`, size106,208bytes; that does not explain the count.

Individual and terminal receipts persisted despite the real accounting exception. Thus persistence improved, but the expected clean/injected-failure pair remains incomplete. Launcher/accounting diagnosis must precede further research.

## Accounting and next boundary

Fresh shared limits:24starts/four protected stop slots,600seconds,2MiB outputs. One direct worker and two observed job processes are recorded separately without refunds. **The manual counter was incomplete:** authoring-tool calls and some Git/rg subprocesses were omitted. Counting tool starts and children gives at least29events before final closeout, exceeding24; exact reconciliation is incomplete. This is an authored execution-accounting violation, not a compliant bounded success. No further experiments are allowed. Final stop meter/summary preserve the earlier counter and record the violation without resetting/refunding it. Old stopped-meter SHA256 remains `fa99530e3e3ed93cb51737320026632baefe8bd51e43a92484b1a8fba7a77259`.

R1-S is **partial, stopped**. Preserve successor sources/receipts. Recommend a separately approved static launcher/accounting diagnosis, with no further worker or HTTP execution yet. No process allowance was silently increased. Freshness, input fit, native trust and representative target-resource validation remain G2 requirements. Results commit requires separate approval.
