# T09 - Launch flag comparison results

**Report date:** 2026-11-14 (Asia/Calcutta). **Authorization:** Exact conditional flag comparison and proposal commit approved by the user; proposal committed in `2475ef8`. [Approved package](../proposals/launch-flag-comparison.md). **Outcome:** Two cases passed the marker/accounting checks; the third reached the required stop. The fourth was not attempted.

## Observations

All attempted cases used original Python 3.14.6, the same minimal authored marker probe/environment, suspended creation and verified one-process worker Job. Only the two declared startup factors varied.

| Case | Extended startup | CREATE_NO_WINDOW | Flags | Result |
|---|---|---|---|---|
| F1 | Off | Off | `0x00000404` | Exit 0, valid marker; worker total=1/active=0; passed. |
| F2 | On, empty attribute list | Off | `0x00080404` | Exit 0, valid marker; worker total=1/active=0; passed. |
| F3 | Off | On | `0x08000404` | Exit 0, valid marker; worker cumulative total=2; accounting stop. |
| F4 | On, empty attribute list | On | `0x08080404` | Not attempted after F3's mandatory stop. |

F3's early case receipt recorded worker total=2/active=1. Its immediately subsequent post-wait snapshot recorded total=2/active=0, empty worker PID list. The 20/100/250 ms snapshots and cleanup retained total=2/active=0 with no worker PID. Final controller state was total=5/active=1, only its own PID active: controller plus three direct trial attempts and one additional cumulative start. That extra start was charged. Its identity was not captured; do not name it or assert a known host component caused it.

**Interpretation:** In this single fixed comparison, enabling CREATE_NO_WINDOW without extended startup reproduced the additional cumulative count, while extended startup without CREATE_NO_WINDOW did not. This narrows the launch-setting association and supports reviewing a future isolation candidate that omits CREATE_NO_WINDOW. It does not establish a universal Windows defect, identify the extra process or authorize a runtime/security change. No child-process restriction, AppContainer capabilities or staged-interpreter variant was tested here; those remain separate compatibility questions. The original `0xC0000142` is not proven resolved.

The guard still rejected F3 even though its marker/exit were successful and its later active count reached zero. No polling-to-pass, count whitelist, active-limit expansion, retry, reordered case or fourth launch occurred. One observation per combination is not a replicated benchmark or complete factorial result. Recorded durations include instrumentation and are not product performance targets.

## Verification and limits

- Three new policy tests first failed for missing flag-matrix/settings functions. Final focused run: **17 tests passed in 0.011 s**. Full Ruff passed for helper/tests. The added tests cover exact factor/order settings, original-only overrides without child-policy additions and unchanged previous row meanings; earlier stop, environment and snapshot tests remain intact. No consumed old benchmark suite ran.
- Reverified the 810 selected original runtime entries against the preserved manifest, baseline config, unchanged preflight source and prior meter hashes. The intentionally instrumented diagnostic source was separately hashed. No runtime copy, recopy, package install or global change. Exact hashes and timing evidence remain in ignored receipts.
- Explicit opt-in `compare_flags=True` selects the new run and fixed schedule; ordinary previous calls retain their schedules/settings. Cases use unique F1-F4 output names. Worker Job and controller/PID invariants were not weakened. Startup failure or a safety mismatch stops this schedule.
- **26/40 conservative process-slot reservations including final documentation closeout**: initialization, red/green tests, tools/controller/wrappers, three trial attempts, one observed additional start and checks. This is not a complete identity census. Native execution remained inside its preparation/execution deadlines; no timeouts were recorded for attempted cases. No new allocation or old meter reset.
- Final snapshots showed no active worker, and owned worker termination/wait/handle cleanup reported no error. The intentional controller exception denotes the safety stop, not an unexpected Python controller crash. Original prior meters remained unchanged through the run.
- No downloads, external requests, Ollama/model calls, OCR, PDF rendering, user-document reads, AppContainer profiles, permission/firewall/Windows feature changes or production launch-policy adoption.

Ignored evidence: `data/t09-launch-flags/flags-01/` contains the ledger/events, baseline/verified identities, red/green/Ruff receipts, three case receipts/markers, owned-Job snapshots, `result.json` and `execution.txt`. Prior reports/stops are retained; this result does not retroactively mark them passed.

## Next review

Recommend reviewing a revised isolation preflight using extended startup **without CREATE_NO_WINDOW**, retaining the actual AppContainer/child-policy and accounting requirements. It needs a new bounded package and its own validation; no profile, revised preflight, additional flag case, OCR installation or execution is authorized by these results. Report the remaining staged-runtime, token, network/filesystem and native-library compatibility gaps before approval. Commit this result/instrumentation only after user approval.
