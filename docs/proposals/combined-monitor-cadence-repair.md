# Proposed monitor cadence and timing repair

**Status: approved for the bounded fake-only repair and proposal commit.** Static review prepared 2026-11-14 (Asia/Calcutta), after combined-04 results commit `74fb75a`. The user explicitly approved committing the five proposal documents and implementing the 32-start/ten-active-minute package. No timing-limit relaxation or native trial is approved. This is a Stage 1 evaluation-harness package, not a product performance budget. Later source/results commits retain their separate gate.

## Findings from existing source

In `combined_native.py`, `Supervisor.observe` measures `now - previous` at the beginning of each iteration, runs the entire `sample` method, then waits another 0.1 seconds. The interval therefore contains previous check work, the unconditional wait and scheduling delay. It is not simply the wait duration. `sample` includes disconnection, ledger/deadline/descendant accounting, process/system memory inspection, TCP inspection and live filesystem scans.

The supplied gap is computed before the current reading is collected, while the observation's `at` timestamp is recorded later. Therefore the current field is a loop-start interval, not a direct measurement between completed resource readings. A long current collection or final TCP/storage scan is not represented by that same incoming gap. A later loop may detect its delay; it does not identify which phase took time.

Combined-04's saved 259.0546-ms interval exceeded 250 ms. This proves a boundary violation under the existing metric. It does not show how much time was spent scanning versus waiting for CPU, nor prove that removing idle wait will complete the native matrix. Combined-03's lost failing reading remains unknown. These findings are static code reasoning; no timing study or native measurement was run for this review.

## Alternatives and recommendation

| Alternative | Benefit | Cost or limit |
|---|---|---|
| Repeat unchanged | Preserves implementation exactly | Known stop can recur; timing attribution and metric mismatch remain |
| Raise the hard gap, for example to 1 second | Allows more timing variation | Broadens the unobserved interval of sampled RAM/headroom/controller checks; needs an explicit safety-policy change and supporting evidence |
| Keep 250 ms, account for check work in the 100-ms cadence, and measure actual timestamps | Avoids deliberately adding 100 ms after a busy scan, improves diagnostics and preserves the strict ceiling | Scheduling or a slow scan can still stop the trial; requires fake clock/integration tests and later separately approved native validation |

**Recommend the third option.** Do not approve a larger gap merely because a native run exceeded the present limit by 9 ms. Do not split or skip existing network/storage/accounting checks to make a test pass. No new dependencies, background services, Windows scheduling policy, thread-priority changes or new parallel monitor thread.

## Exact proposed behavior

- Retain a 100-ms desired loop-start interval. Subtract time spent on the current iteration from the remaining wait; use the existing stop event to wait only the positive remainder. If work takes longer than the target, do not add another unconditional wait or queue catch-up iterations.
- Retain the 250-ms hard stop for loop-start intervals. Also measure gaps between completed resource-reading collections, current resource collection duration, and full iteration duration with a monotonic clock. Enforce the same 250-ms maximum for those measured intervals; do not allow a slower scan to hide behind an earlier start timestamp. Exact equality remains accepted. Initial/direct startup sampling has no prior reading gap, but its collection and iteration durations still apply.
- At each boundary where a timing check can execute, fail closed if the elapsed interval exceeds the hard maximum. Keep resource metrics and timing labels distinct; do not describe a start interval as a reading interval. A resource collection consists of sequential system/process/job measurements, not an atomic snapshot; record collection start/end times and duration.
- Record sanitized scalar timing diagnostics for collection, TCP inspection, storage scan, total iteration, and interval/wait as applicable. Report which interval crossed the limit and preserve the failed packet before owned shutdown where storage permits. An exception before a phase finishes must still stop work; never manufacture a successful timing or resource sample.
- Keep the observer's existing fail-closed path, private error-path handling and owned teardown. Receipt-write failures also stop. Validate monotonic/nonnegative timing inputs in fake tests. Timing checks run when the controller regains execution; this is a software observation limit, not a kernel real-time deadline or a promise to interrupt a blocked system call at exactly 250 ms.

All memory/resource caps, physical disconnection, CPU settings, model/OCR configuration, accounting ceilings, deadlines, ownership checks, storage caps and content-privacy rules stay unchanged. Kernel job/worker caps remain independently enforced. No old ledger may be mutated, reset, resealed or rerun. Leave the stopped combined-04 selector/handoff disabled by its existing started-ledger/seal checks; this repair does not create a new runnable native epoch.

## Proposed bounded fake-only work package

Approval would authorize **32 shared process starts/attempts and ten active minutes**, including initialization/inspection shells, negative tests, fake regressions, lint/format and closeout checks. Human/host approval waits are excluded. Establish one fresh local `data/t11/monitor-cadence-repair-01/` allocation or explicit initial reservation before launching package commands. Include the closed combined-04 meter and prior resource diagnostic completion hashes; never reset their counters. Stop at the shared boundary rather than starting another allocation. No native OCR/model inference/imports, API calls, installation, downloads, rendering or real document/answer access. Standard-library Windows bookkeeping for the existing bounded fake-test bootstrap remains permitted.

Source scope: at most the existing `combined_native.py`, `combined_trial.py` and `test_combined_trial.py`, plus affected documentation and safe local fake receipts. No code is included in this proposal. A new native run identity, budget, source/artifact seal and disconnected handoff need a later explicit approval.

| Task | Prerequisite | Acceptance and verification |
|---|---|---|
| T11-M1: Establish fake allocation | Exact package approval | Fresh shared meter/hash links, allowed sources and clock model reviewed; all shell/tool/test starts reserved before launch |
| T11-M2: Reproduce cadence/timestamp problems | M1 | Failing deterministic clock tests show that work plus an unconditional wait inflates cadence, and that loop-start gaps can miss a late completed reading or long current scan |
| T11-M3: Implement minimum repair | M2 | Work-aware event wait, distinct timing fields and unchanged 250-ms stops; fake observer tests prove stop/no retry, durable sanitized receipts and no skipped network/storage/accounting checks |
| T11-M4: Verify and close out | M3 | Full combined fake suite, Ruff and diff/privacy review pass inside the same allocation; report elapsed/counts and update README/TODO/checkpoint; ask separately before source/results commit |

Required clock cases: 20-ms work followed by an 80-ms wait, 150-ms work with zero extra wait, exact 250-ms acceptance, just-over-250-ms refusal, delayed wake-up, long collection, late TCP/storage completion, first/direct sample, backwards/nonfinite timing refusal, receipt-write error, and cancellation during the wait. Preserve existing memory, ownership, privacy, deadline, quota and teardown regressions. No real sleeps or CPU-load benchmark are needed to establish these deterministic contracts.

## Decision requested

**Subsequent approval and completion:** The user approved the exact fake-only package and the five proposal documents' commit (`fd3361b`). The [completed repair evidence](../benchmarks/combined-monitor-cadence-repair.md) records 34 passing fake tests in 2.164 s, Ruff and preserved limits. A separate source/results commit and any native continuation remain unapproved. The original approval request below is historical.

Approve or amend the 32-start/ten-minute fake-only repair, with the 250-ms ceiling preserved and all old native runs closed. The proposed timing fields and stricter completed-reading/scan checks are part of that exact package. Approval would not authorize any larger interval, native run, runtime adoption or stage transition. Git commit remains a separate explicit decision; the five proposal documents can be approved for commit together with the package if desired.
