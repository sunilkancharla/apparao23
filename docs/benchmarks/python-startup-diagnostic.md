# T09 - Startup diagnostic: basic launches work; accounting stop

**Date:** 2026-11-13. **Authorization:** User approved the [eight-case diagnostic](../proposals/python-startup-diagnostic.md) and three-document proposal commit, recorded in `1658cdc`. **Outcome:** Two cases completed; a third reached the accounting stop. Five cases were not attempted. No retries or isolation/OCR execution.

## Subsequent approved receipt repair

The user approved committing these results and making the discussed changes. Results/helpers were committed in `c52151a`. The diagnostic now writes observed case PID, exit status, duration, launch settings and Job counts before checking the **unchanged** total=1/active=0 guard. It labels the early receipt `not_yet_validated`; marker parsing/classification occurs only after that guard passes. This preserves failure evidence without accepting the mismatched case or suppressing its exception.

Two new synthetic tests first failed for the missing receipt function. After implementation/style fixes, **10 policy tests passed in 0.004 s**, and full Ruff passed on the helper/test pair. Tests confirm a mismatched count leaves a receipt and still raises, and a valid count preserves the normal result. Ignored unit-only receipts are `data/t09-startup-diagnostic/receipt-repair-01/`, using separate conservative test/check reservations (16 including closeout), without changing either old trial meter. These are synthetic unit checks, not a new native diagnostic allocation. No trial worker, network control, profile, permission change, repair of the runtime or OCR executed. Historical missing B-case details remain unavailable; this patch does not reconstruct them. Further native accounting investigation still needs a reviewed package.

## Observations

| Case | Observed outcome | Limit |
|---|---|---|
| A-original | Exit 0, valid Python 3.14.6 startup marker and original executable/prefix; 0.261 s; worker Job total=1, active=0 | Minimal standard-library marker only. |
| A-staged | Exit 0, valid Python 3.14.6 marker and staged executable/prefix; 0.441 s; worker Job total=1, active=0 | Establishes this staged copy can start under row A, not that the old worker/OCR will initialize. |
| B-original | Authored startup marker exists with original Python 3.14.6 identity; controller stopped at `Unexpected descendant or active worker` | The helper checked Job accounting before saving this case's exit/accounting receipt. Exact failing Job values, exit status and duration were not preserved. This case is not a completed/pass result. |
| B-staged, C-original, C-staged, D-original, D-staged | Not attempted | Mandatory accounting stop; no later comparisons or environment/restriction conclusions. |

Row A used ordinary STARTUPINFOW, suspended + Unicode-environment flags (`0x00000404`), a minimal explicit environment and a verified one-process worker Job before resume. Row B added extended startup/no-window settings with an initialized attribute list, without the child restriction. The protocol and identities are defined in the proposal; the old AppContainer preflight was not called.

Final controller Job accounting reported **total=5, active=1, terminated=0** after three charged worker attempts; controller plus those three direct workers would account for four starts. This is an accounting discrepancy. The missing per-case values/process identity prevent attributing it to a specific descendant, transient accounting state or launch mechanism. Do not name an extra executable or claim a particular host defect. The controller's only remaining active Job process was itself; owned worker handles were terminated/waited/closed through the helper's cleanup path, with no reported cleanup exception. The original marker from B was inspected read-only after the stop, without executing another child.

**Interpretation:** The original failure is not explained by a staged Python that cannot start under any configuration: A-staged worked. Runtime-copy corruption is also unsupported by the identity checks below. The full eight-case contrast was not completed, so neither the specific failing DLL nor the effect of child restriction, environment augmentation or host sandbox is established. A zero exit/marker and policy tests do not prove isolation or native OCR compatibility.

## Preparation, budgets and evidence

- Expected initial RED: missing diagnostic module. Eight focused safety-policy tests then passed in **0.002 s**; full Ruff check passed for both new files. Tests cover fixed case order, environment isolation, Windows quoting, marker/identity classification, byte drift, charging before creation, path escape and owned-handle cleanup policy. These do not reproduce the native accounting discrepancy. No old benchmark suite ran.
- Rehashed all **810 entries / 38,852,581 staged bytes** and compared selected original bytes to the same manifest. Manifest SHA-256 `7281100de25d46d810be2223a79ff3471ee8718808ac280bf97c4b50e81463e2`; config SHA-256 `64fa09f21067c74d119d98f328e5f78eaa0198878a20b5257dd523256a01c327`. No drift found; no copy, repair or new runtime file. Exact helper/source identities are retained locally.
- Original preflight meter remained unchanged: SHA-256 `c84a9f818a52154e780b797753ccd823383bac6faa536d3208f1187c3bfb1d1c`, independently rechecked after the stop. This diagnostic has its own ledger; unused old budgets were not reused.
- **26/48 conservative process-slot reservations including final documentation checks**, covering wrappers, tests/Ruff, controller, three trial attempts and closeout. Reservations are not a complete kernel-observed process census: the unexpected accounting is precisely why the schedule stopped. Do not silently classify the discrepancy as harmless or certify exact descendant accounting. Preparation began 13:22:40 UTC, controller began 13:25:16 UTC and trial attempts occurred around 13:25:43 UTC, within approved time caps; no timeouts were recorded for the two completed cases.
- No downloads, external requests, Ollama calls, package installs, global installation changes, permission/profile/firewall/Windows changes, user-document parsing or OCR. New files are authored helper/tests, documentation and ignored small synthetic outputs/receipts. No repaired launcher or isolation adoption is claimed.

Ignored evidence is under `data/t09-startup-diagnostic/diagnostic-01/`: ledger/events, red/green/Ruff receipts, `identities.json`, two completed `case-A-*.json` receipts, three startup marker files, `result.json` and `execution.txt`. The failing-case receipt gap is retained as a limitation, not filled from inference. No case was re-executed to obtain missing details.

## Next decision

T09 and OCR Part B remain gated. Before proposing another native run, review the launcher/accounting path and capture per-case PID, exit code and Job totals **before** raising a safety-stop exception. Test that failure-evidence path first. That code review/repair must not weaken the accounting condition or treat the incomplete B case as accepted. If a further run is justified, propose a small new bounded accounting investigation, preserving both stopped runs and their meters. No such repair/re-execution is authorized by these results. Commit the result/helper package only after explicit user approval.
