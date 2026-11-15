# R1-D — static launcher and accounting review

## Scope and outcome

The user requested the next recommended static review after commits `986305d` and `832bb06`. This review read existing source and sanitized receipts only. It did not execute the helpers, tests, workers or candidate components, access the network, install anything, or reopen either closed allocation. Documentation and Git inspection are separate from those closed experiments.

**The second cumulative process remains unexplained.** The saved R1-S receipt establishes direct exit0, cumulative count2, active count0, child reaped and a cleared job-handle field. It contains no process identities or process-creation events. Static review cannot decide whether the count reflects another process, repeated accounting/assignment behavior, or an interpretation problem. These are investigation possibilities, not findings about Windows behavior. Increasing the expected count to2 would conceal an unresolved assumption.

## Required corrections before another execution package

These defects are present in the committed experimental helpers; this review changes no executable source.

| Finding | Source and reachable consequence | Required behavior |
|---|---|---|
| Completion can ignore a failed second control | `public_source_repair.py:158–175`: the second result is appended before checking exit/error expectations. A second result with `teardown_verified=True` but an incorrect exit or unexpected cleanup error breaks the loop with two results. The final `complete` expression checks only length and teardown, so it can report completion incorrectly. This did not happen in the saved first-control stop. | Persist an explicit pass/fail verdict for each control; require both expected names, exits, error categories and cleanup results before completion. |
| Admission does not enforce terminal allocation status | `charge_worker()` checks time/counts, and `integration()` checks prior workers/receipt; neither checks an allowlisted active allocation status. Current stopped R1-S is blocked by its existing worker count/receipt, but a fresh ledger closed before its first worker would not be blocked by these conditions alone. | Reject closed/stopped/exhausted status before every reservation. Never reset a closed ledger to satisfy admission. |
| Shared start accounting is not enforced across the workflow | `charge_worker()` charges direct worker starts only; shell-side increments do not cover every authoring tool or child command. The preserved closeout already discloses an overrun. `Reserved.observe_native()` stores its observation in memory rather than durably charging discoveries to the shared ledger. | Define chargeable units once, pre-reserve every planned tool/command/child block, retain failed reservations, and durably record unexpected descendants before stopping. Verify with fake cases before any real worker. |
| Cleanup and control validity share one verdict | `control()` requires `kernel_total == 1` inside `teardown_verified`. A count discrepancy therefore also makes the cleanup verdict false. Conversely, `job_handle_closed` reads a cleared Python attribute; the reused helper does not check `CloseHandle`'s return. | Report process-count conformity, direct-child reaping, observed active members, handle-close call/result and residual uncertainty separately. Overall acceptance still requires every relevant check. |

Manual negative traces establish the completion/admission gaps directly from their branches; they are **not executed regression tests**. The earlier13 passing tests, lint result and mutation check belong to R1-S and were not rerun here. The shared helper's accounting structure and suspended-assignment path were inspected, but no Windows ABI correctness or launcher diagnosis was independently validated.

## Recommended next package — R1-A, accounting and verdict controls only

**Proposed, not authorized by this static review.** Repair the counting/admission/verdict machinery before spending another real-worker or HTTP allowance. This adds a small prerequisite rather than weakening the previous checks.

- **Fresh allocation:** `data/t17/public-review-accounting-01/`; do not edit/reset old ledgers, sources or receipts. At most two new authored successor aids under `tests/evals/spikes/`, preserving old identities.
- **Limits:**48 shared start units, of which12 are protected for stop/report/verification;900 active seconds including preparation, authoring, tests, lint and closeout;2MiB combined authored/receipt output. No downloads, installations, HTTP, candidate/native/model/parser/OCR execution, or real child-worker trials. Existing base Python and project Ruff may run the fake tests/lint; their tool, shell and executable starts count.
- **Counting definition:** charge each orchestration tool call (`functions.exec`/`wait`), each nested command or authoring tool, each shell and each launched executable/descendant once in its own category. Reserve a complete block's conservative upper bound **before** invoking it, including quoting failures and expected negative controls. No refunds or unrecorded commands. Protect the remaining stop reserve; insufficient allowance means stop without another ordinary action. Git commits remain separate approved closeout actions, not part of this experiment.
- **Order:** first write the full finite command/authoring allocation and initializer schema; add failing fake cases for terminal-status admission, exhaustion, tool/child/discovery charges and second-control false success; implement only those controls; verify separate cleanup/count verdicts and receipt persistence under accounting errors; run focused tests and Ruff; review hashes, accounting and results; close the allocation.
- **Acceptance:** every planned/failed action is represented in the same durable ledger; terminal states reject admission; discovery cannot silently escape charging; success requires both complete control verdicts; fake error paths preserve accurate receipts. Passing these tests does not resolve the unexplained real process count or authorize a public request.
- **Stop conditions:** ambiguous accounting, insufficient stop reserve, a failed required check not repairable within the remaining allocation, output/time exhaustion, or any unexpected outbound/real-worker demand. No implicit retry or new allocation.

After R1-A, propose a distinct, instrumented standard-library launcher trial only if needed, with an approved identity/event observation method, validated Windows declarations and explicit descendant allowance. Keep the existing512MiB/4GiB headroom and timing protections unless separately changed. Identity capture can miss short-lived processes; an incomplete capture must remain unresolved. No such trial, allowance increase or runtime adoption is approved here.

## Validation and handoff

Source review and saved receipts support the findings above. Document-link and whitespace checks apply to this documentation change; no executable behavior or fresh security/notice evidence is claimed. G2 remains open for freshness, trustworthy input fit, native trust and representative target-resource/format validation. Request a separate commit decision for this report and the linked status documents, and a separate R1-A package decision before implementation.
