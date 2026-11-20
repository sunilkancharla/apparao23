# T17-IF-PR — one metadata probe using the existing controls

## Status and purpose

**Proposed; PR1–PR3 execution and the four-file planning commit await approval.** WIC results are committed as `0882bc0`. The user approved that commit and preparation of this proposal, not another execution attempt.

Resolve one question: can the reviewed native controller retrieve and validate the fixed HTTPX2 release metadata? The [previous attempt](../benchmarks/wheel-static-inspection-continuation.md) passed 12 reporting-control checks but never launched its probe. This smaller package excludes wheel downloads, artifact inspection and new helper implementation.

## Fixed inputs and output

Reuse these authored files from the closed `data/t17/wheel-static-inspection-02/` root, as read-only inputs:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `control.py` | 5,397 | `6f0ff9bf61b00a234be87b9f276ae111adaf876e59e7be90d4ec8e49586d72b7` |
| `probe.py` | 5,267 | `fc9efd62b5c6eadb9723b0a9cccaf1aa2be0efad29a5d62df53e7262ad7a2770` |

After approval, copy only verified regular-file bytes into fresh ignored **`data/t17/wheel-metadata-probe-01/`**. Refuse an existing root, unsafe ancestor, source mismatch or changed source. Verify once-read bytes before compiling/executing those same bytes; do not reopen a mutable source after hashing. Resolve the copied sources' `__file__` to the new root. Keep every earlier root unchanged. Freeze the previous report and relevant receipts as well as authored instructions, proposals and configuration before optional execution.

Use existing `F:/Python/Python314/python.exe -I -S -B`, stdlib only. A small owned invocation wrapper may bind sources, account, capture, time, supervise and save receipts; no changes to the two reused sources or new versioned code files. A source-code defect stops this package.

The only network target is **`https://pypi.org/pypi/httpx2/2.16.2/json`**. Validate the existing expected metadata entry `httpx2-2.16.2-py3-none-any.whl`, declared size 97,893 and publisher SHA-256 `f05c13aade4c45dbf1c9060647a1058f0acad62398fad96e741269edb33d46f5`, without downloading that wheel. Success establishes this response and its publisher declarations, not payload integrity, dependency readiness or runtime suitability.

## Ordered tasks

| ID | Objective and prerequisite | Acceptance and evidence | Status |
| --- | --- | --- | --- |
| PR1 | After approval, bootstrap accounting, freeze/copy fixed inputs and rerun the existing control suite | Fresh safe root; source identities match; 12 checks and synthetic-child teardown pass; finite output/capture and launch accounting prepared before requesting host network permission. | Pending approval |
| PR2 | After PR1, submit one host permission request and attempt the fixed metadata probe | Persist submission/command-entry clocks; charge every shell even on early guard failure; one owned attempt or truthful pre-start stop; bounded metadata validation and verified teardown. | Pending PR1 |
| PR3 | At success, stop or cutoff, close | Report actual network/ownership/timing/coverage evidence, update task/readiness documents, check preservation/scope/links/whitespace/readable diff, validate non-null summary and request a separate results commit. | Pending completion or stop |

No substantial implementation or source authoring occurs between PR1 and the probe. At most two control-suite invocations total, including any diagnostic rerun, and one actual probe attempt. Tests use the existing synthetic cases; no real negative-control network or new source mutation. No Ruff run is needed for unchanged copied sources and documentation.

## Explicit timing change: host waiting is recorded separately

The old 360-second deadline included preparation and host permission waiting. This proposal explicitly replaces that timing rule for this smaller attempt; it does not silently reset the closed allocation.

- Start accounting and the monotonic active clock at bootstrap, before optional reads. Prepare the entire invocation first. Persist a single permission-submission timestamp/tick and immediately request escalation sequentially inside one tool-orchestration call, with no return to model reasoning or other work between those steps. Prepay all possible launch starts before submission, including a shell whose first guard fails. Reach submission within 360 active seconds; otherwise close without probing.
- The approved native command's **first operation** records entry time/tick and accounts for that shell start, before any guard can fail. Treat only the interval from the persisted submission tick to command entry as the host-review/queue interval. No other work runs during it. Record both UTC timestamps and the interval; do not call it pure human waiting or invent an approval timestamp.
- Exclude that one recorded interval from the active budget. Reject negative/ambiguous clocks, duplicate launch or a host interval over 24 hours. On denial/cancellation, record the decision-observation tick as the interval end, label it distinctly from command entry and close without launching. No hidden timer reset or exclusion of model reasoning, source preparation or unrelated tool time.
- Start the probe within 120 active seconds after approved command entry, while total optional active work remains below 600 seconds. Keep its existing 30-second controller deadline and 15-second teardown allowance. Record actual child startup if observable; absence of a child is not a network failure.
- Total budget: **1,200 active seconds**, stopping optional work at 600 and reserving 600 for closeout. Retain elapsed wall time and the excluded interval alongside active time. If timestamps or ownership are uncertain, stop and report that limitation.

## Network, capture and ownership boundary

Request host permission before the first native request. One DNS resolution/connect/HTTPS attempt, no retry/fallback/redirect. The unchanged probe validates all returned IPv4/IPv6 addresses as public, connects to one admitted address and verifies the certificate using the origin SNI/Host. No ambient proxy, authentication, cookies, insecure TLS, firewall/PATH change or private content. Its fixed identity/framing/JSON/duplicate-key checks remain fail-closed. Unsupported response framing is a reported limitation, not permission to modify the source or choose another transport.

Capture both streams concurrently using the reviewed control. Preserve exit codes and strict decoding. Combined raw stdout/stderr must stay within 8 KiB per invocation; the complete displayed summary targets at most 4 KiB. Do not echo metadata bodies or concatenate full source documents. Capture does not waive the limit. Overflow, truncation, unknown accounting or incomplete capture stops optional work and retains an honest lower bound if the exact total is unavailable.

Retain direct controller/child process handles, PID and available birth/exit evidence; no descendant-producing probe code, server, service, GUI or listening port. The existing controller waits for its synthetic/probe child and kills on its timeout. An outer owned wrapper must retain timeout/wait evidence for the controller too. Lost ownership or uncertain teardown stops work; never report verified teardown from an absent result alone.

This public-metadata-only attempt does not add Windows Job or process-memory-monitor implementation. The previous 512 MiB monitoring target remains **unvalidated**, and no enforcement claim is made here. Record any available memory samples and their coverage; missing samples stay explicit. This is a narrower supervision boundary than the postponed binary-acquisition package, with no filesystem/kernel-egress confinement claim. Approval of this proposal accepts that boundary only for this metadata probe; payload acquisition still requires its own reviewed supervision and approval.

## Shared ceilings

| Resource | Proposed limit |
| --- | --- |
| Work | 32 prepaid units: bootstrap/controls 8, probe 8, findings/checks 8, protected closure 8; normal allocation 24. Parent alone writes the shared meter and prepays child leases; no refunds/resets. |
| Time | 1,200 active seconds, optional stop at 600, closure reserve 600; one separately measured host-review/queue interval as above. |
| Processes/checks | 24 owned starts including every shell, controller, synthetic/probe child, failed guard and read-only Git. At most two synthetic-control suites; no new implementation suite or Ruff invocation. Separately approved commits remain separate. |
| Network | One metadata transaction; headers at most 64 KiB, body at most 1 MiB, aggregate HTTP status/header/body at most 2 MiB. DNS/TLS/kernel overhead is outside that byte counter. No wheel request. |
| Reads/disk | 64 MiB streamed reads including 8 MiB ledger allocation, source/hash/receipt/metadata and closure reads; each control suite prepaid within that total. At most 8 MiB retained artifacts including captures, copies, fixtures and authored outputs. No archive/model/user-document reads. |
| Reporting/records | 8 KiB combined streams/invocation, 4 KiB normal display target, 64 KiB aggregate with 16 KiB protected closure reserve. At most 32 immutable ledger records and 32 ledger validations, 4 KiB/record. Count captures/copies against read/disk caps too. |

Allow at most one trustworthy wrapper/accounting correction within these same limits, only before a probe has started. Do not change reused source bytes. Any failed started probe, cap/deadline/host denial, unsafe input, identity mismatch, lost accounting/capture or uncertain ownership ends optional work. No automatic second request or replacement allocation.

## Deliverables and approval

After execution approval: ignored fixed source copies/control and probe receipts plus `docs/benchmarks/wheel-metadata-probe-retry.md`, affected dependency/preflight and PLAN/TODO/README updates. On early stop, keep honest partial findings. No session-checkpoint files, installation, wheel acquisition, candidate import, new versioned helper, model/Ollama call, application coding, G2 adoption or stage transition.

Request approval for **PR1–PR3**, including the explicit host-wait timing change, unchanged-source controls, one native metadata request and the narrower supervision/resource boundary. Separately approve the **four-file planning commit**: this proposal, PLAN.md, TODO.md and README.md. Routine steps inside this package need no repeated project approval; host permission and later results commits retain their own gates.

Preparation used the verified local planning/documentation/security workflows. No new execution root, control copy, fixture, test or network request has been created or started. Existing closed roots and historical checkpoint files remain untouched.
