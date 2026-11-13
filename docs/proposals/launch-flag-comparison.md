# T09 - Proposed launch-flag comparison

**Date:** 2026-11-14 (Asia/Calcutta). **Status:** User explicitly approved this exact comparison and its three-document proposal commit ("yes please"). Approval is not execution evidence. [Latest observed mismatch](../benchmarks/job-accounting-investigation.md).

## Review finding

The existing basic and extended cases change two factors together: `EXTENDED_STARTUPINFO_PRESENT` and `CREATE_NO_WINDOW`. Source review confirms the extended case adds both flags and uses STARTUPINFOEX with an initialized empty attribute list. The result therefore does not identify which factor, or their combination, is associated with the additional cumulative process count.

Microsoft documents `CREATE_NO_WINDOW` as running a console application without a console window, and the extended flag as selecting STARTUPINFOEX. Those meanings do not identify the additional process in this project. [Primary flag reference](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags). Do not infer that either flag is faulty or silently remove one from a future security boundary.

## Exact conditional schedule

Use the same original `F:/Python/Python314/python.exe`, authored marker probe, minimal allowlisted environment, working directory and `-I -S -B` arguments. Keep suspended creation plus Unicode environment (`0x00000404`) in all cases. No child-policy, AppContainer, staged interpreter or new environment variants.

| Order | Extended startup | No-window | Complete flags | Startup structure |
|---|---|---|---|---|
| 1 | Off | Off | `0x00000404` | STARTUPINFOW |
| 2 | On | Off | `0x00080404` | STARTUPINFOEXW, initialized empty attribute list |
| 3 | Off | On | `0x08000404` | STARTUPINFOW |
| 4 | On | On | `0x08080404` | STARTUPINFOEXW, initialized empty attribute list |

At most **four roots**, each once, in that order. A later case runs only if all preceding safety controls pass. On a mismatch preserve snapshots and stop, even if that leaves the factorial comparison incomplete. No retry, reordered fallback or inference about unrun combinations. An exit failure without a marker is recorded but is not a passing readiness case; stop rather than extend the schedule to seek a pass.

## Authorized work if approved

1. Create a fresh ignored `data/t09-launch-flags/<unique-id>/` ledger, receipts and synthetic probe/output directories. Capture hashes of previous meters/source/config; verify the selected original runtime bytes against the preserved 810-entry manifest. Reject drift/reparse paths. Do not modify any old run or runtime copy.
2. Add an explicit opt-in flag-matrix entry point to the existing diagnostic helper and focused tests. Tests first cover the four exact flag/structure pairs, preserved safety conditions, environment isolation and stop-before-next-case behavior. Do not alter the old schedules or enable this comparison implicitly. Record instrumented source identity.
3. Retain one-process worker Jobs, kill-on-close/no-breakaway, controller plus one current child limit, memory floor/caps and verified suspended assignment. Reuse the approved owned-Job count/PID snapshots before creation, after creation, after assignment, immediately after wait, at 20/100/250 ms and at cleanup. Persist PID, exit/marker state, creation flags and initial snapshots before raising. Query only owned Jobs, not unrelated process details. Keep native-width buffer limits and stop on unreadable/incomplete membership.
4. Preserve the initial worker total=1/active=0 and controller/PID invariants. Later snapshots do not convert a mismatch into acceptance. Charge any observed extra cumulative start, retain its unidentified status if its PID was never observed, and stop further launches. Do not expand active limits, add breakaway, elevate workers or bypass host policy to obtain results.
5. Terminate/wait/close owned workers/handles, verify final active membership and report observations plus unrun cases. A flag-associated difference is not a complete causal explanation or approval to change runtime launch/security policy. No AppContainer profiles, ACL/firewall/Windows changes, packages/downloads, network controls, user documents, OCR or model work.

## Shared limits

**40 conservative process-start/attempt slots total:** 12 helper/test, 4 trial roots, 8 wrapper/tool/controller allowances, 8 verification/cleanup/closeout and 8 reserve. Charge all test/tool/shell/interpreter roots, failed attempts and observed extra processes in one new ledger. Reserve before launch and protect eight closeout slots. No counter resets, old suite runs, reserve-funded trial retries or automatic follow-up allocation.

**15 minutes preparation, 5 minutes execution; 10 seconds per worker; 512 MiB private commit per controller/worker; >=4 GiB available RAM; one worker at a time; 16 MiB new disk; 1 MiB aggregate output; zero downloads/external requests/Ollama calls.** Hash verification reads only existing selected runtime/config/source/receipt bytes. Stop on safety failure, insufficient resources, accounting/cleanup failure, timeout or budget exhaustion.

## Adoption and handoff

One approval covers the exact helper/tests, conditional schedule, bounded snapshots, cleanup and reporting above. It does not approve a production flag change, relaxed accounting rule, isolation retry, OCR Part B, further diagnostics or Git commit. Even four passing marker cases would not establish native OCR/AppContainer compatibility. Review evidence and remaining uncertainty before another package.

Preparation verification: source/primary-documentation review, local-link and whitespace/diff checks. No implementation or native comparison has run under this proposal.
