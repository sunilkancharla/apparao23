# T09 - Proposed bounded Python startup diagnostic

**Status:** User explicitly approved this diagnostic package and its three-document proposal commit ("continue please"). Approval is not execution evidence; results will be recorded separately. This is a new diagnostic package, not a restart of the stopped AppContainer preflight. [Prior failure and evidence](../benchmarks/appcontainer-preflight.md). Stage 1 remains PDF/XLSX/CSV, Windows 11, 16 GB and CPU only.

## Question and scope

Determine whether the observed startup failure follows the staged runtime, launch configuration or both. The existing evidence establishes only an unrestricted positive worker's exit `0xC0000142`; it identifies neither a failed DLL nor a cause. Even a successful contrast may only narrow the cause. Do not promise this small experiment will identify a particular DLL or repair startup.

Compare two existing **direct** executables, without modifying either:

- Original: `F:/Python/Python314/python.exe`, the base identified by project `.venv/pyvenv.cfg`.
- Staged: `F:/document_assistant/.venv/tools/appcontainer-preflight/preflight-01/runtime/python.exe`.

Controllers/tests use the project `.venv`; launching its existing base as a diagnostic reference adds no global installation or permission change. Before launching, read the safe previous manifest, verify all 810 staged file sizes/hashes and compare the same selected original file bytes. Reject drift, reparse paths or a changed Python configuration; no repair, recopy, extra DLL or runtime selection expansion. Record manifest/config hashes and relevant authored launcher revision. Do not change the previous run or its meter.

## Fixed eight-case matrix

Each row runs once for each executable, **eight roots total**. Use the same authored standard-library-only probe, isolated/no-site/no-bytecode flags `-I -S -B`, explicit command quoting, fixed working directory and run-local outputs. The probe records version/prefix/executable identity and a fixed startup marker through a bounded file; no OCR, downloaded code, package site initialization or document access.

| Row | Process settings | Environment | Purpose |
|---|---|---|---|
| A | Ordinary `STARTUPINFOW`, suspended launch; no extended attributes or no-window flag | Prior minimal allowlist: SystemRoot, WINDIR, run-local TEMP/TMP | Compare direct original/staged startup without extended startup settings. |
| B | `STARTUPINFOEXW`, suspended + Unicode environment + no-window flags, initialized empty attribute list | Same as A | Compare the extended/no-window launch configuration as a group against A. This is not a one-flag causal isolation. |
| C | Same as B plus the prior child-process restriction attribute | Same as A | Check whether the restriction changes the observed result relative to B. This is diagnostic configuration variation for authored probes, not permission to relax an OCR worker's security. |
| D | Same process settings as A | Minimal allowlist plus PATH restricted to the selected interpreter directory and Windows System32, and COMSPEC set to System32/cmd.exe | Explore dependence on this small explicit environment augmentation; never inherit/log the full host environment or secrets. |

All rows use Unicode environment blocks and explicit absolute application names. A/D differ from B/C in the documented extended/no-window settings only; D additionally compares its environment with A. No probe calls COMSPEC or launches children. Every child is created suspended, assigned to a verified one-process/memory-limited Job and resumed only after membership/accounting verification. A separately limited controller Job must permit exactly the controller and its one current direct child. Preserve host-imposed boundaries; no breakaway or security-policy change.

The old worker imported more standard-library modules than this minimal marker probe. A pass here proves only this probe started, not that the old worker or any OCR engine will initialize. If all rows pass, report that discrepancy without rerunning the old worker. Native ctypes structure/signature/flag review and focused tests must precede process creation.

## Allowed steps and evidence

1. Create a new ignored run directory `data/t09-startup-diagnostic/<unique-id>/` with append-only events, shared meter, input/output and controller-only receipts. No profile is created. Verify safe paths, source identity, >=4 GiB available RAM and kernel Job accounting before trial children.
2. Use the already read incremental/TDD/security workflows. Add a small dedicated diagnostic helper/test pair under `tests/evals/spikes/`; do not call the old `execute()` or alter the old preflight. Write failing tests for the exact eight-case allowlist, environment isolation, argument encoding, pre-launch charging, drift/escape rejection, result classification and cleanup. Fake policy cases do not launch Python children; count all test hosts/interpreters/tool descendants.
3. Run the eight cases in row order, original then staged, one at a time. Charge creation attempts before native calls; read actual Job total/active process counts and record PID, exact flags/environment keys (only the explicit non-secret values), duration, exit status, timeout, marker presence and bounded standard-library identity results. Do not equate zero exit with success without the expected marker and identity.
4. Expected startup failures such as `0xC0000142` are **diagnostic observations**, so continue once through the remaining predeclared cases if resource/accounting/cleanup controls are intact. No retries or adaptive extra launches. Stop immediately on unsafe paths, unexpected descendants, token/security changes, failed Job assignment, creation API permission/host restriction, output-limit failure, missing accounting, timeout or budget exhaustion. Preserve failures and unrun cases. This rule belongs to this new package and does not waive the old preflight's mandatory stop.
5. Terminate/wait/close owned processes and handles, verify no worker remains, and publish a sanitized comparison/report with limitations. No full environment dumps, crash dumps, external network, runtime document reads, loader tool installs, registry/event-log changes, package installs, ACL/profile/firewall changes, Windows features or tracing sessions. No unapproved escalation to a less restricted execution context to make a case pass.

## Combined allocation

**48 conservative process-start/attempt slots total:** 12 helper/test, 8 trial roots, 8 host/redirector/tool descendant allowances, 8 verification/closeout and 12 reserve. Every test, lint, controller, shell, worker, failed creation and necessary teardown/check is charged to one shared ledger; obtain kernel counts for controlled descendants, reserve wrapper overhead before launch, and record unused conservative reservations without resetting them. Reserves cover necessary approved steps, never another trial schedule or a failed case retry. Do not invoke old metered benchmark suites.

**15 minutes preparation plus 10 minutes execution** from the first diagnostic controller; **10 seconds per child**, **512 MiB private commit per controller/child**, **>=4 GiB available system RAM**, **one worker at a time**, **32 MiB new disk**, **1 MiB aggregate output**, **zero downloads/external requests/Ollama calls**. Hash verification is read-only and may read the existing roughly 39-MB copy and selected original bytes; it creates no new runtime copy. Stop rather than silently raise caps. Protect at least eight cleanup/closeout slots before trial launches.

## Decisions after results

- If only staged startup fails, report a staging-dependent difference; no automatic DLL addition or interpreter reinstall.
- If B/C differ from A or each other, report a launch-setting association; do not silently remove restrictions from future OCR workers.
- If D differs from A, report an environment-dependent difference; do not inherit arbitrary host variables as a fix.
- If both executables fail or all probes pass, report the remaining uncertainty. No automatic debugger, host-policy bypass or new comparison.

Any repair, further diagnostics, revised isolation preflight, OCR Part B, runtime adoption or commit needs its applicable separate approval. This package ends with evidence review even if startup succeeds; success is not an AppContainer isolation result.

## Documentation verification

Proposal derived from the committed launcher/source, existing runtime configuration and preserved failure receipts. Local-link/whitespace/diff checks apply; no diagnostic code was written or executed while preparing it. Review this exact package for approval before implementation or launches. Proposal/result commits remain separate from execution approval.
