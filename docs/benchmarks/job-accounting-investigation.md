# T09 - Job accounting investigation results

**Report date:** 2026-11-14 (Asia/Calcutta). **Execution:** 2026-11-13, about 13:38:49-13:38:52 UTC. **Authorization:** Exact two-case package and proposal commit approved by the user; proposal committed in `db50257`. [Approved package](../proposals/job-accounting-investigation.md). This report completes closeout after an interruption; no trial was restarted.

## Result

The basic A-original launch completed with exit 0, a valid Python 3.14.6 marker and one worker Job process. The extended/no-window B-original launch also exited 0 and wrote its marker, but its worker Job recorded **two total processes**, violating the unchanged total=1/active=0 acceptance rule. The package stopped. Neither case used AppContainer or OCR.

| B-original observation | Controller total / active | Worker total / active | Active worker PIDs |
|---|---|---|---|
| Before creation | 2 / 1 | 0 / 0 | None |
| After suspended creation | 3 / 2 | 0 / 0 | None; worker not yet assigned to its own Job |
| After assignment, before resume | 3 / 2 | 1 / 1 | Owned worker PID |
| Immediately after wait | 4 / 1 | 2 / 0 | None |
| 20 ms, 100 ms and 250 ms observations | 4 / 1 at each | 2 / 0 at each | None |
| Cleanup | 4 / 1 | 2 / 0 | None |

Controller active membership after exit/cleanup contained only the controller PID. The additional cumulative process count appeared after resume and before the first post-wait snapshot. The snapshots did not capture the additional process's live PID or identity. Do not name it, assume malicious behavior or attribute it to a particular Windows/host component. The count did not disappear during the bounded observations, so merely waiting for this total to return to one was not supported by this run. Active-process limits and cumulative process counts describe different measurements; this result does not demonstrate an exceeded simultaneous active-process limit.

B's receipt now preserves PID, exit code `0x00000000`, launch flags `0x08080404`, original executable/prefix, valid startup marker, Job total=2/active=0 and `not_yet_validated` classification. It remains a stopped case, not an accepted launch. A used flags `0x00000404`; it passed the initial Job/PID guard and completed. Durations include instrumentation and are not OCR/application latency measurements. No causal comparison of individual extended/no-window flags was performed.

**Conclusion:** This investigation captured the previously missing accounting evidence. It does not identify the extra process, explain the original `0xC0000142`, establish isolated runtime compatibility or justify weakening the guard. Both conditional launches were attempted once; A completed and B reached the required safety stop. No later snapshot converted that stop into a pass.

## Verification and scope

- Four new policy tests first failed for missing PID-decoding/snapshot functions. Final focused run: **14 tests passed in 0.005 s**; full Ruff checks passed, including after the explicit investigation entry point was added. Tests cover 32/64-bit PID decoding, short/incomplete/oversized buffers, snapshots retained before failure and failure preventing the next case, alongside the existing ten safety tests. These are synthetic tests, not proof of complete process observability.
- Rehashed the **810 selected original runtime files / 38,852,581 bytes** against the preserved manifest. Verified baseline config, preflight source and both prior meter hashes; recorded the intentionally instrumented diagnostic source separately. No staged copy or additional runtime assets were created. The previous investigation/diagnostic meters remained unchanged through execution.
- Snapshot queries were confined to the owned controller/worker Jobs. No unrelated process command lines, system-wide process scan or tracing session. Probe code used the original direct Python executable, minimal allowlisted environment, `-I -S -B`, suspended creation, verified Job assignment and no inherited handles. Existing host boundaries remained in force.
- Final controller Job: total=4, active=1, terminated=0; only its own PID active. The observed additional count was explicitly charged as one extra kernel-accounted start. Worker termination/wait/handle cleanup completed without a reported cleanup exception. The controller itself exited with the intentional safety-stop exception. `terminated=0` is the Job accounting field, not a claim that exited workers remain running.
- Shared ledger: **28/32 conservative reservations including interruption recovery and final documentation closeout**. This includes tests, tool/host/redirector allowances, two trial roots, one observed additional start and checks. Reservations are not a complete per-process identity census. Trial execution was within the original preparation/execution caps. Later closeout is documentation-only; it does not reopen the expired execution window or authorize unused slots for another run.
- No downloads, external requests, Ollama calls, package/global installation changes, profile/ACL/firewall/Windows feature changes, network controls, user-document reads, PDF rendering or OCR. No old benchmark suite or stopped schedule was rerun. No fresh runtime or isolation claim.

Ignored receipts: `data/t09-job-accounting/accounting-01/` contains baseline/verified identities, events and meter, red/green/Ruff logs, two case receipts, controller baselines, snapshots for both cases, `result.json` and `execution.txt`. Native-attempt events are appended to JSONL; host/test reservations are retained in the meter's event list and were not all duplicated into JSONL. Do not claim the JSONL alone is a complete append-only launch ledger. Source changes are the opt-in observer/investigation path and four policy tests; the earlier eight-case schedule remains unchanged.

## Remaining decision

T09 is incomplete, and OCR Part B remains gated. Review the extended-startup/no-window launch configuration before defining any further experiment. A follow-up would need its own exact flag comparisons, observable accounting and stop rules; do not silently whitelist the extra count, resume old cases, bypass host policy or install OCR to work around it. Commit this report, documentation and reviewed instrumentation only after user approval. Further native execution or isolation adoption requires a separately approved package.
