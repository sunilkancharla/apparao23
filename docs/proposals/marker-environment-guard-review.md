# T17-IF-MG — narrow marker-environment guard correction

**Proposed; MG1–MG5 execution and the four-file planning commit await approval.** CC results were committed as `d36bd49`. The user approved that commit and preparation of this review. Source comparison below was read-only preparation; no new trial root, import, policy change or parser retry occurred.

## Source comparison and recommendation

[CC findings](../benchmarks/reconciliation-capture-correction.md) establish complete error capture and the failed hostname lookup. Reading the existing local source clarifies the two options:

| Option | Observed behavior / consequence |
| --- | --- |
| Supply an explicit environment to `Marker.evaluate` | In packaging 26.3, `markers.py:532–544` calls `default_environment()` before merging the supplied dictionary. `_cached_default_environment()` calls `platform.machine()`, release/system/version and Python-version helpers. A dictionary alone therefore does not bypass this blocked lookup. Avoiding it would require a separately reviewed override/private-API strategy. |
| Allow only the exact `socket.gethostname` audit event | Preserves the public marker API and changes one guard decision. In this Python's `platform.py:1004–1016`, missing `os.uname` leads to `_node()` and then Windows version/machine helpers; `_node()` calls `socket.gethostname`. Recommend this exception only in the review child, keeping all other socket, subprocess, native-loading and import restrictions. |

The Windows path also contains local WMI/version helpers and a possible `ver` subprocess fallback. Source inspection does not prove which later branch will execute. Do not prewarm platform caches, monkeypatch marker internals, suppress another denial or automatically broaden the guard. A later blocked operation is a new diagnostic result, not permission to allow it.

The proposed hostname exception does not authorize socket creation, DNS resolution, connections or external traffic. Do not log, persist or display the returned hostname or raw `uname` object. No product security policy, target hardware, dependency version or architecture selection changes.

## Fixed source and evidence

The relevant local source files were read as text during preparation, without importing them:

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| `.venv/Lib/site-packages/packaging/markers.py` | 20,554 | `6cbe860d35d98d2b599e7f0ec73feab124e015711b30be9045e678c92940d9cc` |
| `F:/Python/Python314/Lib/platform.py` | 50,643 | `4277b504e5e668c498fa6ffb96805ffb1ee86610eda7ad266c822f441ac6cd78` |

Retain these immutable inputs from the closed `data/t17/reconciliation-capture-correction-01/` root:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `capture.py` | 4,482 | `15849ddbd03c992da78baee314b48731c036d7ab5563e1719e61892f64b590d3` |
| `parser_controls.py` | 3,072 | `41261c05e5f876c72a24b1a0818650e58a562209e46359b8fc3858b526fcbc53` |
| `tool-verified.json` | 3,354 | `ceac44262e5538db67fac59f1bc63bfcc40c59186ddcf5884ba46e30bbb68531` |
| `tool-metadata-freeze.json` | 419 | `f74181e8de5730bbacfa87eeffb6e444c9976a3f2bdacf6e1929a103ce3d9333` |
| `summary.json` | 2,932 | `15ff675827a28eeeda908086cf5006b85a1bbe2246cc6f26be3a2ea04ea8432e` |

The committed CC report is 6,884 bytes, SHA-256 `2bb79aa8c19a1507a55cfe7ccd0c18aaee8bf6dc842d84e9c689bf6961ac083a`. Revalidate the 20 packaging source hashes and the installed METADATA/RECORD against their saved identities before use. Existing packaging **26.3**, with its previously recorded Apache-2.0 OR BSD-2-Clause declaration, remains a review-only tool. Use existing `F:/Python/Python314/python.exe -I -S -B`; no installation or global site-packages.

## Ordered tasks and acceptance

| ID | Objective / prerequisite | Acceptance / evidence | Status |
| --- | --- | --- | --- |
| MG1 | After approval, bootstrap/freeze and inspect exact generated source/commands | Fresh root and shared leases; fixed inputs/tool identity; only reviewed guard/loader/control functions and the unchanged copied capture aid. Old dispatch, graph/research and global import-path expansion excluded. | Pending approval |
| MG2 | Write a meaningful failing guard test before the correction | With the unchanged old policy, an assertion requiring the exact hostname event to be allowed fails as expected. Record RED before authoring the corrected predicate. | Pending MG1 |
| MG3 | Make the smallest approved policy change, then GREEN checks | Only `socket.gethostname` is exempted. Test the actual predicate used by the parser against this exact event and denied socket creation/connect/resolution/near-match events, subprocess/native-load and non-stdlib imports. No real networking used for negative controls. | Pending MG2 |
| MG4 | One parser-control attempt after GREEN | Corrected guard installed before default-environment evaluation; unchanged capture aid retains admitted bytes/EOF/exit/teardown. Record whether the original ten marker/report controls pass. A full captured failure ends the attempt; no second try or additional exception. | Pending MG3 |
| MG5 | Completion/stop closeout | Actual source/policy diff, tests, budgets, ownership and blockers; preservation/scope/links/whitespace/readable-diff/empty-index/non-null receipt. No adoption or resumed reconciliation. | Pending completion/stop |

Use the already reviewed incremental, test-first, security, quality-review and documentation workflows. Keep authored evaluation source/fixtures ignored; no new versioned application/helper code. The earlier CC authoring-order deviation remains historical; MG2 explicitly requires RED execution before corrected-policy implementation.

## Execution boundary

Fresh ignored root **`data/t17/marker-environment-guard-01/`**; refuse an existing root/reparse ancestor. Bootstrap before optional reads. Keep older roots read-only. Copy the verified capture aid to the fresh root, verify its bytes, and retain its existing byte-stream/ownership semantics. Its eight-case historical result is reused, not reported as a new run. If changing that aid becomes necessary, stop and request a revised package.

Generate only the reviewed marker loader, guard and controls in the fresh root. The policy checks must exercise the same predicate installed in the parser, not a duplicate approximation. Negative audit-event cases call the policy directly; they do not open sockets, resolve names, spawn an extra command or load a native library. Any claim concerns the policy decisions exercised, not kernel network isolation.

Use exact allowlisted interpreter commands without a shell for child execution. Do not execute old top-level dispatch, import candidates, reopen wheels/native payloads, read user documents, call models, fetch public sources or run graph/licence reconciliation. Do not modify installed source, global configuration/PATH, dependencies, the lock or product files.

Install the guard before the first real environment lookup. Permit only the exact hostname audit event in this child; keep all other prior audit/import denials. No cache prewarming, private API replacement or alternate network permission. Actual hostname values are not evidence artifacts.

The sole parser child has a 60-second maximum plus 15-second teardown; retain its direct handle/PID through exit. No fixture child may spawn descendants. Capture at most 8 KiB combined stdout/stderr; complete means both stream EOFs and verified process exit. Overflow, capture loss or uncertain ownership stops optional work. The host emits only bounded status, not live parser output. No Job, filesystem confinement, kernel egress or memory benchmark is added or claimed.

## Shared budgets and stops

Parent alone owns a shared ledger and prepays non-refundable leases for the entire suite, controllers, child, shells, source inspection, negative/regression work and Git checks. Include failed/unused process reservations; never reset an exhausted allocation.

| Resource | Ceiling |
| --- | --- |
| Work | 48 prepaid units: bootstrap/source 8, guard/controls 16, parser evidence 8, protected closure 16. |
| Time | 1,800 active seconds; optional cutoff 1,200 and closure reserve 600. |
| Processes/checks | 32 owned starts total; three ordered check invocations: RED, GREEN policy suite, one parser attempt. Zero Ruff runs. No extra capture-suite rerun. |
| Reads/disk | 32 MiB explicit streamed-read leases including 4 MiB ledger allowance; 8 MiB retained evidence. Does not claim total OS/interpreter I/O measurement. |
| Reports/ledger | 48 KiB aggregate reporting with 12 KiB closure reserve; 8 KiB raw host streams/invocation, 3,000 UTF-8 displayed bytes; at most 32 immutable records/validations and 4 KiB/record. |

Admitted diagnostics are saved before display; a planned oversized display is withheld. Actual truncation/lost capture, unexpected GREEN failure, unsafe identity/input, host denial, cap/cutoff or uncertain teardown stops optional work. Expected RED/handled policy denials are intentional controls. A complete parser failure is a diagnostic outcome, not permission to fix another behavior. Allow one trustworthy orchestration correction within the same limits; no automatic reruns.

If host permission is needed, measure at most two submission-to-native-entry/decision-observation waits totaling 24 hours, with no intervening model work. Exclude no ordinary work; report wall/active/host totals separately. No permission prompt is implied for routine covered edits/tests.

## Deliverables and approval

After approval: ignored controls/source/capture/accounting receipts, `docs/benchmarks/marker-environment-guard-review.md`, and affected updates to this proposal, PLAN, TODO, README and input-fit preflight record (**six versioned closeout documents maximum**). Preserve AGENTS, SPEC, dependency/lock/configuration records, existing versioned tests/manifests, historical checkpoints and unrelated user files.

Passing marker controls only supports proposing a fresh dependency/licence/provenance reconciliation package. It does not install/adopt packages, close G2 or advance stages. Another denial requires another evidence-based review; do not broadly disable the audit policy.

Request approval for **MG1–MG5**, explicitly including this review-child-only hostname event exception, test-first policy controls and the conditional single parser attempt. Separately approve the **four-file planning commit**: this proposal, PLAN.md, TODO.md and README.md. Preparation alone does not authorize execution or that commit.
