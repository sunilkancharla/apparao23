# R1-L — instrumented probe stopped after resume

## Outcome

The user approved the exact R1-L package, connected synthetic execution boundary and five-document proposal commit. Proposal committed as `c023f37`. The fresh allocation is `data/t17/public-review-launcher-01/`. **The first real control stopped on an unexpected count; the second was not started.** There is no successful pair, launcher adoption or permission to retry the closed run.

The investigation narrowed the discrepancy to **after resume**: raw accounting showed0before assignment,1after assignment, then2at the ready handshake. This does not identify the second executable or establish the cause of earlier runs. The probe observed2active processes despite requesting a one-active-process limit. That containment expectation was not demonstrated; setup success is not equivalent to verified effective limits. Stop/cleanup evidence remains separate from that failure.

## Official reference review

Five external tool calls reviewed only official Microsoft/Python material as evidence; unrelated search results were not relied on. No document contents, prompts or private inputs were sent. This refreshed Windows API understanding, not dependency advisories, native notices or model-input fit.

- The accounting fields include lifetime associations and currently active processes; failed limit-related associations can affect the counters. That explains why a lifetime count alone cannot prove two successful workers. It is **not** a diagnosis of this run. [Microsoft accounting declaration](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information).
- Notifications can be missed, and PID reuse limits identity claims without a retained handle. The probe associated a completion port while the job was empty, retained its direct process handle and recorded raw notifications; it does not claim complete event coverage. [Completion-port association](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port), [dequeue signature](https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-getqueuedcompletionstatus), [port creation](https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-createiocompletionport).
- Reviewed declarations covered [job query](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject), [job limits](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information), [extended limits](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information), [setting limits](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-setinformationjobobject) and [creating a job](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-createjobobjectw).
- Process declarations/signatures were checked against [creation](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw), [startup information](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-startupinfow), [returned process handles](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-process_information), [creation flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags), [assignment](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject), [membership](https://learn.microsoft.com/en-us/windows/win32/api/jobapi/nf-jobapi-isprocessinjob), [resume](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-resumethread), [image name](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-queryfullprocessimagenamew) and [owned PID list](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_process_id_list).
- Cleanup references covered [wait](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject), [exit code](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getexitcodeprocess), [job termination](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject), [direct termination](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess) and [checked handle closure](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle).
- Memory checks retained the existing stdlib-only helper after reviewing [physical memory](https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-globalmemorystatusex), [memory status layout](https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/ns-sysinfoapi-memorystatusex), [process-memory query](https://learn.microsoft.com/en-us/windows/win32/api/psapi/nf-psapi-getprocessmemoryinfo), [extended memory counters](https://learn.microsoft.com/en-us/windows/win32/api/psapi/ns-psapi-process_memory_counters_ex), [Windows data types](https://learn.microsoft.com/en-us/windows/win32/winprog/windows-data-types) and [Python ctypes](https://docs.python.org/3.14/library/ctypes.html).

From the reviewed field definitions and x64 type alignment, the independent expected sizes were Accounting48, Basic64, Extended144, Startup104, Process24 and Port16bytes. Accounting total/active offsets were36/40. Fake controls compared typed structures with a separate `<4q4I` decoder; the real API returned48bytes. This is source-derived layout verification plus runtime decoder agreement, not an independent SDK compilation or validation on other architectures.

## Test-first preparation

Two new aids, `public_source_launcher.py` and `test_public_source_launcher.py`, preserve all previous sources. The initial red command failed because the probe module did not exist. Then26fake tests passed in0.254seconds and Ruff passed. Two additional cases exercised wrong-layout admission and the **actual new controller** with fake Windows process-creation failure; **28tests passed in0.217seconds**, with Ruff passing again.

The suite includes all18R1-A regressions, stage ordering, duplicate assignment, mismatched raw length, unexpected counts recorded before rejection, membership ambiguity, missing notifications, deadline/memory checks and PID/identity requirements. Fake process-creation failure verified independent job/port cleanup and terminal receipt persistence without a real launch. No new mutation run was claimed; R1-A's prior targeted mutation evidence is unchanged. This does not exhaustively test Windows failure behavior.

## Real observations

The exact sealed base Python ran one controlled worker through direct suspended creation, assignment and resume. Source/interpreter seals and prior identity hashes were checked before admission. The worker wrote a synthetic ready PID and waited for release; it was stopped before normal release or an exit0 result could be accepted.

| Stage | Lifetime count | Active count | Direct child in owned job |
|---|---:|---:|---|
| Fresh baseline |0 |0 |not applicable |
| Created, before assignment |0 |0 |false |
| Assigned, before resume |1 |1 |true |
| Ready, after resume |2 |2 |true |
| Final cleanup |2 |0 |direct child reaped |

The direct process image was `python.exe`; its saved hash matched the sealed interpreter. The ready PID matched the retained direct process PID. Notifications recorded two different nonzero identifier values and a final zero-valued packet; raw numeric message/key/value records remain in the local receipt. No second executable handle/image was captured, and numeric message meanings were not independently mapped in this probe. Do not claim the second process was another Python worker, console host, security helper or attacker.

The count validator stopped at the ready stage, before the later owned-PID-list snapshot. Consequently the design did **not** capture the additional image before teardown. Although limit-setting returned success, effective configured flags/active limit were not persisted from a readback. These are concrete observation gaps for a successor investigation, not grounds to rerun this one.

Verified owned cleanup: job termination returned success, process wait returned0(signaled), direct child reaped, final accounting active0, and thread/process/job/port CloseHandle calls all returned success. Normal success exit was not recorded; the injected-failure worker was not run. Total first-control time including cleanup was0.4083420seconds; cleanup0.0490631seconds. Minimum sampled available physical memory was10,927,702,016bytes; sampled job peak8,749,056bytes. These stdlib-probe measurements do not validate app/model limits or the physical16GB target.

## Allocation and preservation

All80units were prepaid, with24protected. An initial PowerShell manifest-sum check failed on hashtable handling before a meter/source/worker existed. Its directory was retained and initialization corrected in place, with both command blocks charged: preparation6units, correction5plus buffer2; the total stayed80. Because the first QPC was not persisted, setup was conservatively prepaid120seconds and the remaining monotonic epoch limited to1,080seconds; no exact first-command duration or refund is claimed.

The manifest reserves preparation6, research12, test-authoring2, red4, probe-authoring2, green/lint5, correction5, trial8, closeout-authoring2, review5, close3, buffer2 and protected24. Actual research used5calls/10units; correction plus buffer admitted7units. Trial admission used orchestration/tool/shell/controller4 plus one direct start and one discovered association,6of8reserved. Unused reservations remain charged and cannot fund retries. Final closeout separately records any protected verification units, duration and output size.

The10preserved source/closed-meter/interpreter identities were unchanged at post-trial review. Source seals, raw stages, individual receipt and `pair.json` remain under the ignored allocation. No old counter, failed aid, trial or asset was reset/edited. No parser/OCR/model/SQLite extension, private document, cloud inference or new installation was used; no network research overlapped the workers.

## Next boundary

R1-L closes **stopped, unresolved**. Expected process count remains one. Before any new worker, propose a successor that records effective limit readback and captures owned PID/image evidence **before count rejection triggers teardown**, with durable discovery charges and a fresh finite allocation. Do not reopen this run or spend its unstarted second slot as a retry. Public-source research, G2 and application/native adoption remain gated. Source/results commit needs separate approval.
