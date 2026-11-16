# R1-I — additional owned image captured; count discrepancy remains

## Outcome

The user approved the exact R1-I package, connected synthetic boundary, brief capture window and five-document proposal commit. Proposal committed as `7fae685`. Fresh allocation: `data/t17/public-review-identity-01/`.

**The missing additional image was captured as `conhost.exe`.** The direct image was `python.exe`. Each image query used a retained handle whose membership in this exact owned job was checked first; both creation-time identifiers were retained. Full paths, command lines, environment and unknown executable contents were not retained or inspected as file content.

Limit readback passed before creation, after assignment and at ready: flags8968(`0x2308`), active-process limit1, process memory536,870,912bytes and job memory536,870,912bytes. Nevertheless accounting at ready reported2lifetime associations and2active members. The probe deliberately stopped after the approved identity capture. **Evidence collection succeeded; single-worker operational validation did not.** Identifying the basename does not explain the limit behavior, authenticate its publisher or establish the cause of previous trials.

## Prerequisites and implementation evidence

One external tool call reviewed the new official declarations: [OpenProcess](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess), [GetProcessTimes](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocesstimes), [query access rights](https://learn.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights), [FILETIME](https://learn.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-filetime) and [Python timer behavior](https://docs.python.org/3.14/library/threading.html#timer-objects). Queries used `PROCESS_QUERY_LIMITED_INFORMATION`(`0x1000`), no privilege changes, and a two-DWORD creation-time structure without an unaligned integer-pointer cast. Earlier reviewed launcher declarations were reused by identity-preserved imports; no prior source was edited.

Two new authored aids are `tests/evals/spikes/public_source_identity.py` and `test_public_source_identity.py`. The initial red command failed because the implementation did not yet exist. Then28fake tests passed in0.376seconds and Ruff passed. Review before launch added notification retention, complete operational-success checks, and incomplete-identity rejection. **30tests passed in0.210seconds; Ruff passed again.**

The suite includes18R1-A regressions plus limit readback, count2capture-before-reject, larger-ceiling rejection without capture, membership-before-image ordering, truncated/duplicate PID lists, unavailable identity, capture deadline, owned-only watchdog callback and explicit callback failure. Further cases reject unexpected exits, excessive cleanup/control/capture duration, watchdog firing and incomplete creation/image identity. Fake tests do not launch trial workers. No fresh mutation score or exhaustive Windows failure coverage is claimed.

Verified focused commands (the real sealed `run` allocation is closed and must not be repeated):

```powershell
& 'F:\Python\Python314\python.exe' -I -S -B tests/evals/spikes/test_public_source_identity.py
& .\.venv\Scripts\ruff.exe check tests/evals/spikes/public_source_identity.py tests/evals/spikes/test_public_source_identity.py
```

An independent daemon timer could request termination of the owned job/direct suspended child at the five-second deadline. Its callback makes no ledger writes and is quiesced before handle closure. Fake checks exercised the callback and error recording. The timer did not fire during this real attempt, so real forced-deadline behavior was not demonstrated. The250ms capture window remains a target, not a hard real-time guarantee for OS calls.

## Real receipt

Exactly one direct creation attempt was admitted, using the sealed base interpreter and synthetic ready/release code. There were no parser/OCR/model/SQLite-extension calls, private documents, installations, downloads or worker network calls. The one reference-research call finished before worker execution. The second association was durably charged as a discovery, not hidden or used to approve count2.

| Observation | Result |
|---|---|
| Baseline / created before assignment |0lifetime,0active |
| Assigned before resume |1lifetime,1active |
| Ready after resume |2lifetime,2active |
| Limit snapshots | All three returned144bytes and matched requested fields |
| Accounting snapshots | Returned48bytes; independent and typed decoding agreed |
| Owned images | `python.exe`, `conhost.exe` |
| Same-handle membership / creation identity | Confirmed and retained for both |
| Capture duration |0.0014237seconds, about1.42ms |
| Normal phase / cleanup |0.3123457 /0.0478255seconds |
| Total control duration |0.3601682seconds |
| Minimum sampled available physical memory |11,122,483,200bytes |
| Sampled peak job memory |8,990,720bytes |
| Final accounting |2lifetime,0active |

The count mismatch caused controlled job termination before a normal successful worker exit. The direct process was reaped. The additional query handle, direct thread/process, job and completion port all had successful checked CloseHandle returns. The watchdog was quiescent and did not fire. Raw notifications were drained and retained as supporting evidence; their completeness is not asserted.

Separate verdicts: **effective limits pass; identity coverage pass; owned cleanup pass; expected count fails**. The terminal state is stopped without retry. These observations do not validate the app's physical16GB CPU-only target, model resources or containment of private inputs.

## Shared allocation and preservation

The fresh meter persisted its monotonic epoch and full64-unit manifest before optional checks. Limits were48normal/16protected units,900active seconds and2MiB combined authored/receipt output. Blocks: prepare3, research8, test authoring2, red4, implementation2, green/lint5, correction8, trial6, report authoring2, review5, close3, protected16. No setup failure or counter reset occurred.

Actual admitted block upper bounds are retained without refunds: research used one of four external calls(2of8units), correction7of8units, and the trial used all6units for tool/shell/controller, one direct attempt and one discovered association. These are conservative block charges, not a claim of measured native process starts for every host tool. Final protected documentation verification and closeout charges/duration are recorded separately in the final meter/summary. Unused reservations fund no further experiment.

Post-run review verified all14prior source/closed-meter/interpreter identities and all6current seals unchanged. Raw limit/accounting snapshots, owned identities, creation IDs and checked cleanup results remain locally in the ignored allocation. No raw runtime receipts, generated handshake artifacts or private files are proposed for Git.

## Next decision

R1-I closes with successful bounded identity collection and **failed operational count validation**. Do not change the expected count or launch again under this allocation. Next prepare a public-reference/static assessment of the observed `conhost.exe` behavior and suitable process-accounting options. It should compare preserving the current rejection with a separately proposed policy for verified owned auxiliary processes; neither relaxed limits nor automatic adoption is approved here. Fresh public-source dependency review, model-input fit, native trust, G2 and application implementation remain open. Source/results commit requires separate approval.
