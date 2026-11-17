# T17-IF-RC — reconciliation stopped during parser controls

## Outcome

The user approved RC1–RC5 and the four-file planning commit, made as `f3dad02`. This review stopped before dependency reconciliation or public research. The first synthetic parser check exited unsuccessfully, and the host wrapper retained only the first line of its error. The failure's cause is **unknown**. No dependency, licence, provenance, runtime or architecture approval follows.

Evidence is in the ignored, now stopped `data/t17/wheel-evidence-reconciliation-01/` root. Earlier roots remain read-only. The [approved package](../proposals/wheel-evidence-reconciliation.md) required stopping optional work on incomplete capture; the run was not retried.

## What was verified

- The existing project-local packaging 26.3 tool was inspected without installing anything. Thirty hashed installed RECORD entries matched their recorded sizes and SHA-256 values. Twenty Python source files were inventoried and frozen.
- Source review found platform helper functions containing subprocess, native-library and file probes. The review's syntax-tree scan found none of its flagged calls executing directly at module level. This limited scan is not a complete security audit or a publisher-authenticity check.
- The ignored parser admits packaging through its exact local package path rather than adding all site-packages to the import path. It contains an audit guard against network, subprocess and native-library loading operations. The failed control attempt does not establish that every guard or parser behavior works.
- The inspection process exited successfully. The synthetic process also exited, with code 1; its retained diagnostic is only `Traceback (most recent call last):`. Neither process remains running. The reserved graph process was never started.

## Task status

| Task | Result |
| --- | --- |
| RC1 | Partial: bootstrap, freeze and static tool review completed; synthetic controls failed with incomplete diagnostics. No passing marker/report-control result. |
| RC2 | Not run. Actual/minimum marker matrices, dependency closure and lock conflicts remain unresolved. |
| RC3 | Not run. Existing declarations, selected notices and native/vendor gaps remain historical evidence only. |
| RC4 | Not run. Zero public-source calls or targets. Existing source-mapping timing deferral remains unchanged. |
| RC5 | Stop receipt and findings recorded; closeout checks are recorded below. No candidate installed/imported, binary/archive reopened, model called or application feature implemented. |

## Capture defect and reporting limits

The host wrapper issued one `ReadAsync` operation on each redirected stream, then treated its result as the entire stream. A read may return before end-of-file. Consequently, a short first read can discard later traceback lines even when the child exits normally. The retained process exit evidence is usable; the diagnostic is incomplete. It would be speculation to attribute the synthetic failure to packaging or any candidate.

Three planned oversized displays were withheld before emission. Their source review data remained in local JSON artifacts; no complete-display claim is made for those attempts. They did not exceed the display limit. The subsequent incomplete subprocess capture was a separate stopping condition.

The ignored wrapper must not be reused as a verified execution harness. The review script is also an unaccepted evaluation artifact, not application code. It was not added to Git or used to change project dependencies.

## Resources and preservation

At the stop receipt: **249.186 active/wall seconds**, no excluded host wait, 64 work units and 32 process starts prepaid; 15 starts charged by that point, including unused reservations. One synthetic invocation was attempted; zero passed suites are claimed. Zero Ruff runs, web requests, installations or candidate executions occurred. Final closeout totals and checks are in the local `summary.json`; the stop-time numbers are not represented as final totals.

The parent ledger retains conservative read/report/process leases, including unused allocations. Source/configuration/evaluation inputs are checked against the bootstrap freeze. Only the seven authored closeout documents are intended changes; unrelated user files and historical checkpoint files are preserved. Runtime evidence, scripts and local package files are excluded from the proposed commit.

## Readiness and next decision

| Area | Readiness / remaining evidence |
| --- | --- |
| Dependency/lock compatibility | Unknown; graph was not executed. No version changes proposed or accepted. |
| Licensing/native notices | Not reconciled; Tokenizers notice selection and HF-Xet bundled/vendor evidence remain open. No legal or ABI clearance. |
| Source/provenance | Not investigated here; Hub source mapping and FSSpec provenance remain open. |
| Offline behavior and tokenizer parity | Not tested here; no runtime adoption or G2 approval. |
| Review harness | Blocked by incomplete stream capture and the unexplained control failure. |

The smallest next package should correct and test the **host capture boundary first**, using delayed, multi-chunk stdout/stderr, a nonzero exit, output-limit and timeout cases. It should retain complete admitted diagnostics, drain both streams to EOF, enforce byte/time caps, and verify owned-process exit. Only a fresh, explicitly approved package should then attempt the parser control again; dependency reconciliation and research should wait for a passing capture harness. The unused control allowance does not override this run's stop condition.

Closeout verification passed: seven-document scope; eight frozen source/configuration/evaluation inputs, three fixed earlier evidence hashes and twenty tool-source identities preserved; touched local links, whitespace, readable diff, empty index and non-null stop summary checked. A documentation whitespace failure (two extra EOF blank lines) was corrected before the final check. Final bounded receipt remains local. Results commit and any follow-up execution require separate approval.
