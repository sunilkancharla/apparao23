# R1-P — console-host evidence and process-accounting options

## Recommendation

**Test detached console creation once before considering an auxiliary-process allowance.** Keep the expected count1, current job/memory limits, ownership checks and zero-active cleanup requirement. Do not ignore `conhost.exe` in accounting or change a failed result into a pass.

The user requested this static/public-reference assessment after R1-I commit `4847f1b`. This review used three web-tool calls and existing source/reports. No worker/helper/test ran, no closed ledger changed and no executable source, dependency, approved requirement or runtime policy was modified. Proposed follow-up execution below requires a new package approval.

## What the evidence supports

The [R1-I receipt review](public-source-owned-identity-results.md) established two owned image basenames, `python.exe` and `conhost.exe`, with same-handle job membership and retained creation identifiers. The expected count failed even though readback still contained active limit1 and512MiB memory limits. These are observations of one synthetic run; publisher authenticity and the reason for the limit behavior were not verified.

Microsoft identifies `conhost.exe` as the console API host. This makes a console-host explanation consistent with the observed basename, but does not authenticate the particular local executable or prove which internal Windows path created it. [Console definitions](https://learn.microsoft.com/en-us/windows/console/definitions).

The documented launch modes differ: `CREATE_NO_WINDOW` suppresses a console window, while `DETACHED_PROCESS` creates a console process without attachment to its parent's console; an application can subsequently request a console. Therefore the latter is a distinct experiment, not a guarantee that this local workload will create no helper. The controlled file-based handshake does not require an interactive console. [Creation of a console](https://learn.microsoft.com/en-us/windows/console/creation-of-a-console), [creation flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags), [Python flag support](https://docs.python.org/3.14/library/subprocess.html#subprocess.DETACHED_PROCESS).

Lifetime accounting includes exited processes and certain failed associations. It must remain a separate observation from currently active membership, and neither counter alone proves why a process appeared. A console-host exception to the active limit was **not established as a documented contract** in the primary references reviewed. Community discussions surfaced in search but are not used as a platform guarantee or adoption evidence. [Accounting fields](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information).

Console detachment is distinct from job breakaway. `CREATE_BREAKAWAY_FROM_JOB` and job breakaway permissions change job association behavior and are excluded. A detached experiment must still retain suspended creation, explicit checked assignment and verified job limits. [Creation flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags), [job membership model](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects).

## Options

| Option | Benefit | Cost and decision |
|---|---|---|
| Keep rejecting count2 without more work | Preserves existing acceptance | Launcher-dependent execution remains blocked; retain as safe default until a decision. |
| One `DETACHED_PROCESS` stdlib experiment | Tests a documented console mode while preserving count1 | Recommended next; no promise of success. Must verify actual exit, observations, limits and cleanup. |
| Allow one verified owned console helper | Could accommodate observed platform behavior | More complicated identity/authenticity, resource, lifetime and unknown-descendant rules; needs explicit policy/limits approval and dedicated tests. Basename alone is insufficient. Not recommended as the first change. |
| Switch to `pythonw.exe` or a different supervisor | Could change console behavior | Adds an executable/launch-path review and different error/output handling; not selected or authorized. |
| Ignore the helper, subtract it from totals, enable breakaway or increase the active cap silently | Makes existing check appear to pass | Reject: loses honest resource/process accounting or changes the approved boundary. |

For any future auxiliary policy, charge **every** owned process and its memory/time to the shared allowance. Distinguish an intended worker from its auxiliaries only for classification; classification cannot erase actual starts or residual members. Require a reviewed system-image identity strategy, not filename allowlisting; preserve explicit rejection of unknown members and bounded teardown until the owned job is empty. No such policy is adopted by this review.

## Proposed R1-DT — one detached stdlib validation

**Pending package approval; no allocation or source preparation yet.** This tests the recommended launch mode without expanding accepted worker counts.

| Boundary | Exact proposal |
|---|---|
| Fresh ignored root | `data/t17/public-review-detached-01/`; refuse reuse |
| Shared allowance |64units:48normal/16protected stop/report/verification, fully prepaid before preparation; failures retained, no refunds |
| Active time / output |900seconds across preparation through closeout;2MiB combined authored/receipt output |
| Authored aids | At most two new Python files under `tests/evals/spikes/` (successor probe and tests); reuse verified declarations/helpers, preserve every previous aid/ledger/seal |
| Research/installations | Zero external calls, downloads, package changes or global changes; the official references above supply the proposed mode |
| Executables | Same sealed existing base Python with `-I -S -B`, project Ruff, prepaid PowerShell/Git inspection; no replacement interpreter |
| Real execution | At most one direct stdlib worker attempt with ready/release files and expected exit0; no console input/output dependency or candidate components |
| Creation flags | Replace `CREATE_NO_WINDOW` with `DETACHED_PROCESS`; retain `CREATE_SUSPENDED` and `CREATE_UNICODE_ENVIRONMENT`: proposed combined value `0x0000040C`. Omit `CREATE_NEW_CONSOLE`, `CREATE_NO_WINDOW` and all breakaway flags. |
| Process acceptance | Expected1cumulative/1active at ready, zero active after cleanup; diagnostic ceiling2allows bounded identity recording on a discrepancy only, never acceptance or another launch |
| Resource limits | Requested/readback active cap1,512MiB process/job and controller-private caps, at least4GiB available physical RAM |
| Timing |5seconds normal control plus5seconds teardown; retain independent owned termination path and its fake checks |
| Discrepancy capture | Preserve the previously approved style of at most250ms target within the normal deadline, at most2owned handles; incomplete evidence fails, no extended allowance |
| Environment | Connected synthetic stdlib-only host, no network code in controller/worker; no filesystem/outbound-network confinement claimed; no private input, parser/OCR/model/Ollama/extension loading |

Detachment changes console attachment, not the approved security/privacy boundary. No shell launch, parent console inheritance assumption, detached-from-job behavior, automatic elevation, services or antivirus changes are permitted. File-based status receipts must remain usable when console streams are unavailable. Future parser/model adapters that need stdout/stderr would require separately verified explicit pipe/file handling; this smoke cannot establish their compatibility.

Suggested fully prepaid blocks: prepare3, test authoring2, red4, successor implementation2, green/lint5, corrections8, trial6, report authoring2, review5, close3, normal contingency8, protected16 =64. Count orchestration, nested tool, shell, executable and discovery units separately. The trial6includes controller/tool/shell overhead4 plus one direct and at most one discovered association. Unused reservations remain charged; no closed allocation funds new work.

### Ordered tasks

Root [TODO](../../TODO.md) tracks state. Every task below is pending approval.

| ID | Objective / prerequisite | Acceptance / evidence |
|---|---|---|
| R1-DT1 | Freeze fresh manifest/clock and prior identities; package approval | Full64-unit accounting before preparation; previous sources/closed states unchanged. |
| R1-DT2 | Test-first successor launch configuration; DT1 | Fake cases require exactly the detached/suspended/Unicode flags, reject console/breakaway combinations, retain readback/ownership/receipt/deadline/count checks; R1-A regressions and Ruff pass. No existing result is reinterpreted. |
| R1-DT3 | One sealed stdlib attempt; DT2 and admission checks | Record actual flags, stage counts, effective limits and same-handle identities; normal exit0only if all checks conform; bounded owned cleanup in all cases. |
| R1-DT4 | Review and close; DT3 or earlier stop | Separate count/limit/identity/resource/exit/cleanup verdicts, output/duration and complete charges; save checkpoint and request separate source/results commit. |

Success requires a single accounted worker throughout the relevant stages, checked assignment/limits, a complete ready/release exchange, exit0, accepted resource/time bounds and verified empty owned job/checked closes. It does not prove why earlier runs created `conhost.exe`, guarantee later workloads or authorize application-native adoption.

Stop on a second member after bounded evidence capture, any higher ceiling, wrong flags/readback/ownership, missing receipt, timeout/headroom/output/budget issue or need for another executable/network/privilege. No retry, fallback mode, auxiliary-policy adoption or reuse of the unspent contingency as a second launch is allowed. Results commit, later candidate integration, public dependency review and G2 remain separate gates.

## Critical-path recommendation

Keep this launcher investigation separate from public dependency/advisory research. Built-in read-only web tools can gather official public evidence without this local HTTP helper; a fresh bounded research package can use that route rather than make advisory freshness depend on a successful Windows subprocess probe. This review does not perform that larger research or reopen the failed R1 allocation. Likewise, a successful stdlib probe alone cannot approve private-document native execution or model-input fit.
