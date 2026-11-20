# R1-L — proposed instrumented launcher validation

## Decision requested

Approve one bounded **synthetic, standard-library launcher investigation**, including prerequisite official-documentation checks, test-first successor aids, fake controls, at most two real owned workers, review and closeout. This proposal is documentation only: nothing has been allocated, implemented, researched online or executed for R1-L. Proposal-document commit, package execution and later results commit are distinct approvals.

R1-A is committed as `bcdb9c4`; its [18 passing fake controls](../benchmarks/public-source-accounting-results.md) are a prerequisite, not proof of a real Windows adapter. [R1-S](../benchmarks/public-source-repair-results.md) reported two cumulative job processes after one direct worker, with zero active members. Process identities and the event sequence were not captured. Do not assert a launcher cause or reinterpret the old receipt as success.

## Objective and alternatives

Determine whether a fresh owned launch can be accounted for accurately from creation through cleanup, and explain any discrepancy using recorded evidence. Preserve the expected **one process per control**. A diagnostic containment allowance for a discovery is not an accepted new baseline.

| Approach | Assessment |
|---|---|
| Raise expected count to two | Reject: conceals the unexplained observation. |
| Repeat the previous helper unchanged | Reject: lacks the evidence that was missing. |
| Instrument only after resume | Insufficient: misses the distinction between initial accounting/assignment and execution. |
| Fresh stage-by-stage probe with raw accounting and identity observations | Recommended, conditional on declaration and observation-method verification before launch. |

A completed investigation may still conclude **unresolved**. Stop rather than repeat the pair or manufacture an explanation when short-lived events cannot be identified.

## Exact proposed boundary

| Item | Limit or requirement |
|---|---|
| Fresh ignored allocation | `data/t17/public-review-launcher-01/`; refuse an existing allocation |
| Shared execution allowance |80 units:56 normal,24 protected stop/report/verification; prepay the full finite block manifest before any preparation |
| Charging units | Each orchestration call, nested tool, shell, executable and discovered descendant counted separately; failures retained, no refunds or counter resets |
| Active time |1,200 seconds across research, preparation, authoring, tests, launch, review and closeout; approval wait excluded before allocation starts |
| Authored/receipt output |2MiB combined; no private documents or model assets |
| Source changes | At most two new tracked Python aids under `tests/evals/spikes/` (probe and tests); preserve all prior aids/ledgers/hashes; no edits to shared historical harnesses |
| Existing executables | Recorded `F:/Python/Python314/python.exe` with `-I -S -B`; existing project-local Ruff; PowerShell/Git inspection only as prepaid tasks; record hashes before use |
| Real controls | At most two direct owned stdlib workers, sequential: clean exit0, then explicit exit7; no automatic retries |
| Diagnostic discovery allowance | At most four cumulative observed worker-job processes across the entire pair, at most two per job; expected count remains one. Any additional count requires a recorded explanation or stop; never silently spend this as another direct launch. |
| Kernel containment | One active worker-job process,512MiB process/job memory; no breakaway permission; terminate/close only owned handles/jobs |
| Headroom | At least4GiB available physical RAM; controller private memory at most512MiB; check before launch and during observation |
| Time per control | At most5seconds from creation admission to normal completion; then at most5seconds additional forced teardown/verification; at most20seconds total for both real control/cleanup phases |
| Public reference research | At most8 external tool calls, including search/open, only official Microsoft Windows and Python documentation; reserve every call. No dependency advisories, user data, artifact/package/model download or installation. Retain short paraphrased findings, not fetched executable content. |
| Excluded execution | No Ollama/model, OCR, parser, sqlite extension or other candidate loading; no public-source HTTP helper; no application code or private input |

**Execution environment proposed for approval:** the host may remain connected for these controlled stdlib probes; the authored controller/workers contain no network calls. Public reference research must finish before the real-worker phase and cannot overlap it. A Windows job is not filesystem or outbound-network confinement; this proposal makes no such claim. This limited connected synthetic boundary does not authorize the old candidate trials, private-document processing or the application's unresolved native trust boundary. If this boundary is not accepted, redesign the handoff before execution rather than assuming prior disconnected-trial approval applies.

Before authoring, assign all80 units to ordered blocks, including prerequisite tools, expected failures, real-worker starts, discovery allowance, review and protected closeout. Verify the block sum and minimum stop reserve. A budget clock must cover preparation and final cleanup; no subprocess or authoring action may occur outside its admitted block. R1-A's single-writer policy can inform the successor but cannot intercept host calls: external orchestration must retain the prepaid manifest as well.

## Observation design — verification required before launch

Use existing OS APIs through Python's standard library only; do not install a tracing service, driver, package or global configuration. Proposed calls include process creation in a suspended state, job assignment/accounting, process/job membership and image identity, thread resume and checked handle teardown. Verify all names, constants, signatures, structure packing, return conventions and supported behavior against official documentation first. No API behavior in this design is represented as already validated.

Collect the following ordered, monotonic observations in bounded receipts:

1. **Fresh job baseline:** raw accounting bytes, decoded fields and returned length, zero-worker expectation, limit-setup return values and an opaque per-job identity.
2. **Created but not assigned/resumed:** retain direct child PID and primary thread/process handles; record membership in the newly owned job before explicit assignment. Do not infer ownership from a filename or parent PID alone.
3. **After exactly one assignment, before resume:** checked assignment result, immediate raw accounting snapshot, membership result and direct process image identity. A discrepancy here must not be described as proof that the Python workload spawned anything.
4. **After resume:** child writes a tiny synthetic ready message with its own PID and waits on a bounded parent-controlled release. Record PID agreement and owned membership/identity snapshots before allowing exit. No arbitrary commands, user content or environment dump in that handshake.
5. **Event/identity coverage:** review job notifications/completion-port support as the proposed event method, plus bounded owned-PID snapshots. Select it only after declaration and failure-path tests. Record missing/lost events, access failures and PID-reuse uncertainty explicitly. Polling alone cannot establish the identity of every short-lived process; neither notification completeness nor complete coverage is assumed.
6. **Exit and cleanup:** save actual exit, final raw accounting, active-member observations, termination result when used, wait/reap result and every handle-close return. Persist accounting errors independently of cleanup. Receipt failure must prevent success.

Retain stage labels, return/error codes and hashes needed to diagnose the count. Keep output to owned identities and sanitized executable basenames/hashes; do not inventory unrelated processes or collect command lines, credentials or document paths. A snapshot sufficient to find the retained direct child's primary thread must discard unrelated entries immediately.

**Declaration admission gate:** record field offsets, structure sizes and raw-buffer decoding checks using an independent expected layout from the reviewed official declarations. Check both an independent decoder and the probe's typed structure. If authoritative declarations or a usable event method cannot be verified within the research budget, stop before any real worker. Do not treat agreement between two copies of the same unverified structure as validation.

## Ordered task checklist

Root [TODO](../../TODO.md) is the task-state authority. These tasks describe the package's acceptance, prerequisites and evidence; none is authorized merely by appearing here.

| ID | Objective and prerequisite | Acceptance / evidence |
|---|---|---|
| R1-L1 | Freeze allocation and preserve identities; needs exact package approval | Full prepaid80-unit manifest, clock/output boundaries and hashes for base interpreter, prior aids and closed ledgers; no old state changed. |
| R1-L2 | Verify declarations and observation method; needs L1 | At most8 official reference calls; exact reviewed layouts/signatures and observation limitations documented; stop before launch if unverifiable. |
| R1-L3 | Test-first successor preparation; needs L2 | Failing then passing fake cases for before/after assignment observations, membership ambiguity, wrong layouts, duplicate starts, missing events, accounting/cleanup failures, deadlines and second-control false success; reuse R1-A regressions and run Ruff. |
| R1-L4 | Single admitted diagnostic pair; needs L3 and resource checks | At most two direct starts, shared discovery charges, stage/identity/raw-accounting receipts; second control only if first meets its stated success criteria. No implicit retries. |
| R1-L5 | Independent review and closeout; needs L4 or an earlier stop | Distinct count/identity/cleanup/control verdicts, hashes, complete shared charges, factual outcome and saved checkpoint; separate results-commit request. |

## Acceptance and stop conditions

The pair passes only if both expected controls have correct exits and exact error categories; verified declarations decode consistent snapshots; every observed cumulative process is accounted for and identified to the stated observation coverage; count conformity and cleanup checks independently pass; receipt, resource and shared-budget checks pass. An injected callback error must be distinguishable from an ordinary error. Candidate process-count adoption is outside this package.

If the count differs from one, preserve the evidence and stop unless the reviewed declarations conclusively show a decoding defect that can be corrected **before launch**. Do not repair a completed real probe and rerun it under the same allocation. In particular, first-control ambiguity means the second control is not started.

Stop immediately for unknown ownership, missing mandatory observations, counter ambiguity, unverified declarations, insufficient reserve/headroom, timeout, missing receipt, unexpected process count, or any demand for extra launches/installations/network during worker execution. On stop, terminate/reap the owned job, check cleanup, save an honest unresolved receipt, close the allocation and preserve evidence. If cleanup cannot be verified, report that uncertainty; do not claim readiness for another trial.

Success here permits a later public-review proposal, not its execution. Advisory freshness, model-input fit, target16GB feasibility and G2/application adoption remain separate open requirements.
