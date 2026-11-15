# T17-R1 — research helper startup stop

## Outcome

The user approved committing the11architecture documents and the exact R1public-source package. The architecture/policy pack was committed as `dbd9137`. R1 then used a fresh ignored allocation at `data/t17/public-review-01/`; no previous native allocation was reopened.

**The research did not run: zero HTTP attempts, zero response bytes, zero public sources fetched.** No current advisory/license/notice refresh or model-input-fit discovery can be claimed. No dependency upgrade, installation, candidate-native/model/parser/OCR load or inference occurred. The command is withdrawn; do not run `public_source_review.py fetch` or reset its ledger.

## Failures and missed integration checks

The initial meter did not include `pending_bytes`, although the request-admission code required it. The worker raised `KeyError: pending_bytes` before opening the lazy HTTP stream or charging a request. The controller then called the reused Windows job helper's `close()`, whose accounting callback required `Reserved.observe_native`; the adapter provided only `reserve_processes`. That `AttributeError` prevented the normal terminal receipt from being written.

These are authored harness defects, not network blocking or unavailable upstream evidence. Eight fake-HTTP tests passed before readiness; a pre-fetch Windows redirector correction added a ninth launch-argument test, with9tests passing in0.003seconds. The initial expected red run failed because the helper did not yet exist. None of those tests passed the actual PowerShell-initialized ledger through worker startup or exercised the full reused close callback protocol. The missing integration coverage is explicit; do not advertise the passing fake suite as a successful research run. Ruff was not run or claimed passed.

## Cleanup evidence and accounting

The public-only worker log records the terminal exception. Source review confirms `NativeJob.close()` calls `TerminateJobObject` and closes its job handle in `finally`, including when the callback raises. The controller returned exit1. This supports owned teardown through the executed cleanup path; no independent process-table inventory was performed and no standalone successful teardown receipt existed at failure. The follow-up sanitized stop receipt identifies this distinction rather than inventing observed active-process counts or memory peaks.

The original running meter was copied to `meter-startup-stop.json`, SHA256 `fa99530e3e3ed93cb51737320026632baefe8bd51e43a92484b1a8fba7a77259`. A separate closeout updated the current meter to `closed_startup_failure_no_retry` and created `summary.json`. Original source seals/readiness history are preserved. Before any HTTP admission, the redirector correction retained the earlier readiness seal and all prepaid charges; no network epoch or attempt count was reset.

All24starts were conservatively reserved before preparation, with four stop slots protected. Closeout accounts for20normal and2stop tool/process starts; two stop slots remain unused. Preparation was fully prepaid600seconds (observed at final readiness322.9891804seconds), report work60seconds and the interrupted fetch allowance240seconds conservatively retained:900/900chargedseconds. No exact final controller duration was persisted; none is reconstructed from file timestamps. HTTP/body counters are0, no pending body reservation was opened. This closed allocation funds no retry or further experiment.

## Next review boundary

Recommend the [separate fake/startup/cleanup integration repair](../provisioning.md#proposed-r1-s--startup-and-cleanup-integration-repair) before another public request. Preserve both failed authored aids and their hashes; use fresh successor identities and a new bounded allocation only after approval. Require tests constructed from the real initial ledger schema and the complete job-close adapter protocol, plus counted standard-library worker success/failure cleanup checks. No new candidate-native research or model trial is requested. Current advisory/notice freshness, model-input fit, native trust and representative resource/target-machine requirements remain G2 blockers. Results/source commit approval is separate.
