# T17-IF-CC — complete subprocess capture before parser review

**Approved; planning committed as `86bdaa9`; execution completed with a diagnosed parser blocker.** [CC findings](../benchmarks/reconciliation-capture-correction.md) record expected RED, eight passing GREEN capture cases and one fully captured parser failure at `socket.gethostname`. Guard unchanged; no retry, graph/research or adoption. The original approved boundary below is retained for audit; it does not authorize another run.

## Purpose and prerequisites

The [RC review](../benchmarks/wheel-evidence-reconciliation.md) stopped because its first parser control failed and a single stream read lost later error output. The failure's cause remains unknown. Fix the capture boundary first; do not retry dependency reconciliation or research through the unverified wrapper.

Use the existing `F:/Python/Python314/python.exe -I -S -B` and standard library only for the capture harness and synthetic children. No dependency/interpreter installation, candidate import, wheel/native/archive reread, web request, model call or product implementation. Existing packaging **26.3** may be used solely for the final parser-control attempt, after its source/metadata boundary is rechecked. It remains a review tool, not a newly selected runtime dependency.

Keep the closed RC root read-only. Verify these inputs under `data/t17/wheel-evidence-reconciliation-01/` before reuse:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `review.py` | 12,875 | `735e83445e8415fac64818a521f2cb184894051152c7ef12f9662e8171f1224e` |
| `tool-verified.json` | 3,354 | `ceac44262e5538db67fac59f1bc63bfcc40c59186ddcf5884ba46e30bbb68531` |
| `synthetic-process.json` | 171 | `3a35bec653e3d9354604962e34e41736428f76395f9a0e753a6257e857c37989` |
| `summary.json` | 1,153 | `e6ef5d4192ee695734f0f3510a4929e04f090466fa61c2c88d9f39ecee2f193e` |

The committed RC report is 6,151 bytes, SHA-256 `20fb2130a3351dc97021c5ec15583f748b90a1dbe92499eb1f38fcfe289592aa`. Check the installed packaging source hashes against the saved inventory and freeze its installed METADATA/RECORD before the first import. Fail on identity/version/boundary mismatch. Do not import the old script to discover its functions: it contains top-level command dispatch.

## Ordered work and acceptance

| ID | Objective / prerequisites | Acceptance and evidence | Status |
| --- | --- | --- | --- |
| CC1 | After approval, bootstrap/freeze; inspect the old failure and tool boundaries as data | Fresh root, shared leases, exact identities, allowed-command list and source/import review recorded before execution. No old script or package executed during inspection. | Pending approval |
| CC2 | Test-first capture correction, after CC1 | Expected RED assertion demonstrates the single-read defect using a deterministic staged stream control; smallest passing implementation drains both byte streams to EOF within aggregate caps/deadlines, preserving exit code and ownership evidence. | Pending CC1 |
| CC3 | Validate corrected capture, after CC2 | GREEN suite covers empty streams; delayed multi-chunk stdout/stderr; full nonzero-exit traceback; exact aggregate byte boundary; split UTF-8 bytes; intentional overflow; timeout; injected reader failure. Expected negatives clearly separated from unexpected harness failures. | Pending CC2 |
| CC4 | One parser-control attempt only after passing CC3 | Copy only reviewed loader/control logic into the fresh root, excluding graph/licence/research dispatch. Revalidate packaging source identities; retain complete admitted stdout/stderr, exact command, exit code and verified child exit. On parser failure, explain only what captured evidence supports; no speculative fix or second attempt. | Pending CC3 |
| CC5 | At completion or stop, close out | Record tests, actual limits, complete/incomplete capture flags, teardown, findings and remaining blockers; verify preservation, scope, local links, whitespace, readable diff, empty index and non-null receipt. Separate results-commit and next-package gates. | Pending completion/stop |

Use the repository's already reviewed incremental, test-first, security, quality-review and documentation workflows. Evaluation code and fixtures remain ignored; no new versioned helper/application source is proposed.

## Capture and execution design

Use a small standard-library controller with concurrently drained **binary** stdout/stderr streams. Read bounded chunks in loops; a short read is not EOF. Keep stream bytes separate, decode after capture, preserve decoding limitations, and stop admitting data at the combined limit. A normal admitted result is complete only after both streams reach EOF and the owned process exits. Never use one `ReadAsync` result as the entire stream or rely on a token-return setting as a byte guard.

Spawn only exact allowlisted interpreter commands, without a shell, remote requests or inherited global site-packages. Synthetic children are authored, content-free fixtures; the parser child admits only the reviewed local packaging package plus the standard library. Preserve the existing network/subprocess/native-loading audit restriction for that parser attempt. Do not invoke its platform-probing helpers or import other project-local packages.

Hold each direct child handle and PID from creation through exit. Every child has a deadline and bounded teardown; expected timeout/reader-error controls must terminate and wait for it. Do not launch grandchildren. This narrow review does not add a Job, filesystem confinement, kernel egress enforcement or memory monitor, and makes none of those guarantees. Failure to establish capture or owned-process exit stops optional work.

For normal children, admit at most **8 KiB combined stdout/stderr**. The deliberately oversized synthetic control may produce at most **16 KiB**; the harness retains at most the admitted 8 KiB plus a one-byte overflow sentinel, records truncation explicitly, terminates/waits, and does not claim complete output. This expected negative is authorized fixture behavior, not permission for real parser overflow. A real parser overflow stops the package.

The host-facing command prints only a bounded final status; it does not relay live child streams. Retain admitted diagnostics before display. Host output has an 8 KiB raw cap and a **3,000-byte UTF-8 display cap**, checked before emission; planned oversized displays are withheld. Actual lost capture, truncation of an admitted normal result, unknown ownership or unexpected suite failure stops optional work. Do not silently rerun or reset accounting.

## Shared limits and stop boundary

Fresh ignored root: **`data/t17/reconciliation-capture-correction-01/`**; refuse an existing root or reparse ancestor. Bootstrap before optional reads. Parent alone writes a shared ledger; prepay non-refundable leases for all controllers, children, shell/inspection, RED/GREEN, negative, parser and Git-check processes, including failed or unused reservations.

| Resource | Ceiling |
| --- | --- |
| Work | 48 prepaid units: bootstrap/source 8; capture/controls 16; parser evidence 8; protected closure 16. |
| Active time | 1,800 seconds; optional cutoff 1,200, closure reserve 600. No separate early research/start deadline. |
| Processes | 32 prepaid owned starts for the whole package. Allocate before launch; include controllers and all synthetic/regression children, not only the parser. |
| Checks | Three ordered invocations total: expected RED, GREEN suite, one parser-control attempt. Zero Ruff runs. No unbudgeted rerun. |
| Timeouts | At most 60 seconds per real controller/parser command and 15 seconds teardown; synthetic timeout fixture uses a shorter explicit limit. |
| Reads / retained files | 32 MiB streamed-read leases, including 4 MiB ledger allowance; 8 MiB retained artifacts. No binary/archive rereads or external-response acquisition. |
| Reporting / ledger | 48 KiB aggregate reporting with 12 KiB closure reserve; 32 immutable records/validations, at most 4 KiB each. Stream limits above remain separate from authored JSON artifact sizes. |

If a host permission prompt is necessary, record submission and first native entry/decision observation without intervening model work. Allow at most two measured host-wait intervals, cumulatively 24 hours; report wall/active/host time separately. Exclude no ordinary preparation or execution time. Permission denial stops optional work.

One trustworthy orchestration correction is allowed within these same leases. The expected RED and explicitly handled negative fixtures are not unexpected failures. Lost accounting/capture, an unexpected GREEN failure, cap/cutoff, unsafe identity/input or uncertain teardown stops optional work. A fully captured parser failure ends CC4 with a diagnostic result; it does not authorize fixing parser semantics, changing dependencies or proceeding to graph/research.

## Deliverables and approval

After approval, produce ignored harness/fixtures/process receipts/accounting and `docs/benchmarks/reconciliation-capture-correction.md`. Update this proposal, PLAN, TODO, README and the input-fit preflight record as needed: **six versioned closeout documents maximum**. Keep historical checkpoints, unrelated user files, SPEC, dependencies, lockfile, evaluation manifests and existing versioned test source unchanged.

If capture and parser controls pass, dependency/licence/provenance reconciliation still needs its own next approved package. If the parser fails, propose the smallest evidence-based correction instead. Neither outcome adopts a dependency, selects an architecture, closes G2 or advances Stage 1.

Request approval for **CC1–CC5**, including the synthetic negative fixtures and one conditional packaging 26.3 control attempt, and separately for the **four-file planning commit**: this proposal, PLAN.md, TODO.md and README.md. Preparation alone does not authorize execution or that commit.
