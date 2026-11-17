# T17-IF-SC — stopped during accounting; source review not started

## Outcome

The user approved SC1–SC4 and the five planning documents, committed as `0868f05`. The [approved package](../proposals/hub-source-coordinate-review.md) began in fresh ignored `data/t17/hub-source-coordinate-review-01/`.

**SC1 stopped before optional source/evidence reads or public research.** Initial accounting and approval records were durably created. The next accounting update wrote and flushed `meter.json.pending`, but `System.IO.File.Replace` rejected its backup-path argument with `ArgumentException: The path is not of a legal form.` The package requires stopping optional work on unexpected I/O; no source-review retry followed.

PowerShell's conversion of the null backup argument is a suspected explanation, not an experimentally verified diagnosis. This outcome establishes neither a provenance conflict nor a problem with the previously verified wheel. The earlier [HS findings](hub-only-static-review.md) remain the latest source evidence.

## Task status

| Task | Result |
| --- | --- |
| SC1 | Partial: fresh durable bootstrap succeeded; subsequent accounting replacement failed before output-control demonstration and entry preservation. |
| SC2 | Not started: zero public research calls or targets. |
| SC3 | Partial recommendation only: correct accounting in a separately approved continuation; historical and release coordinates remain unresolved. |
| SC4 | Protected partial-stop findings and checkpoint; closure checks and final allocation recorded locally. No installation/adoption decision can be supported. |

No test suite, Ruff check, worker, candidate import/execution, payload inspection/download, model/API/native trial, build, environment/PATH/lock change or application implementation occurred. No worker/service required teardown. The proposal and pre-commit verification were read as part of the separately authorized planning commit, before execution bootstrap; they were not source research.

## Failure handling and accounting

- Initial meter: eight bootstrap units and 512 reporting bytes reserved.
- Pending update: nine total units, 65,536 local-read bytes and 2,560 reporting bytes reserved. Those reservations remain charged, although the planned source/evidence operations never ran.
- The original meter and flushed pending update are retained unchanged. `stop.json` and immutable protected-closeout ledger records preserve the sequence without repairing, reopening or resetting this attempt.
- The host exception escaped the controlled emitter. This reporting failure is recorded explicitly; retaining its pending allowance does not make the failed invocation retrospectively compliant.
- The output-control demonstration and entry-preservation verification did not run. Fourteen small identities were recorded during protected closure, explicitly as **post-stop evidence**; five immutable HS source/report/dependency identities matched their reviewed delivery hashes.
- Actual closure counters, elapsed time, artifact accounting and verification results belong in local `closeout.json`. No payload rehash or new provenance evidence was obtained.

Protected closure uses newly named, exclusive-create JSON records rather than retrying the failed replacement operation. This preserves evidence; it is not authorization to resume research under a changed accounting approach.

Closure consistency checks passed: 14 post-stop identities unchanged, 360 local links, exact five-file delivery scope, empty staged index, whitespace and ignored runtime-root checks. Readable tracked/new-file diffs were captured and reviewed. These are documentation/evidence checks, not completed SC1 entry verification or application tests.

## Recommendation and remaining gates

Prepare a fresh source-only continuation that avoids the failed replacement path, preferably using an immutable accounting-record sequence with a verified latest-record rule. Review that mechanism before optional reads, preserve this stopped root and keep the existing research/payload boundaries. Do not run a diagnostic or continuation merely because this report recommends one.

The exact wheel-to-publisher/build/source relationship is still unresolved. Neither historical source `178e1a1797858724c79fd9d12d79d0902d730497` nor observed release `3739729b86489e4ae28b5a62e622be320b141493` was substituted or newly validated. Transitive dependency/native/offline review, parity/input-fit validation, runtime adoption and G2 remain open. Stage 1 PDF/XLSX/CSV, OCR/privacy requirements and the 16 GB CPU-only target are unchanged.

Request a separate commit of this report plus PLAN/TODO/README/checkpoint (five files), and approval to prepare the accounting-corrected continuation proposal. This does not request runtime adoption or permission to execute an unreviewed continuation.
