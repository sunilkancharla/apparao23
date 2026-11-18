# T17-IF-RPT — bounded closeout-reporting correction

## Approval and purpose

The user approved **preparation** of this correction. Its execution and Git commit are not yet approved. HEAD is 68e012c. Five SMC result documents remain uncommitted; this proposal is the sixth document for the proposed combined planning/results commit. Their recorded limitations remain explicit.

Use the reviewed planning/documentation workflows. After execution approval, also reuse the unchanged reviewed incremental implementation, test-first, security and quality workflows. No skill script, sub-agent, installation or application implementation is needed.

The [SMC findings](../benchmarks/tokenizer-source-metadata-continuation.md) explain the failure: the controller calls ReportGate.admit(status) without its supported closure keyword. An otherwise successful Git-status child therefore hit report_reserve during protected closeout. Collected source/manifest evidence is reusable; no research must be repeated to fix this reporting path.

## Exact correction

Keep the historical ReportGate class, gateway/controller templates, SMC root and all historical ledgers unchanged. Author an ignored owned copy of the controller plus a small parent reporting wrapper, not a versioned application/helper framework.

- The parent explicitly admits optional versus closure work. Before a controller launch it reserves a **512-byte status lease**, including the final newline, from the matching report ceiling. Record the used-before value and the charged lease; never refund unused bytes. Do not infer closure permission from low remaining space.
- The controller reads the explicit Boolean closure field from its owned admission receipt; malformed/missing phase or inconsistent lease fails closed. Its shared serializer calls ReportGate.admit with that phase. The local gate starts from the recorded used-before-lease snapshot; the real parent already retains the full lease charge. This is a checked reservation, not a reset of the global report counter.
- Premeasure the actual serialized status plus newline against both the 512-byte lease and the applicable total ceiling before stdout. Ordinary work cannot consume protected reporting space. The production controller must call this same tested serializer; a stand-alone unused sizing test is insufficient.
- Preserve complete stdout/stderr capture, retained child handle/birth/exit/EOF/reaping, fixed/base64 argument transport and actual versus reserved counters. Keep controller and child failures distinct. Do not remove the existing capture/ownership checks to obtain a passing report.
- Keep a stopped production context stopped. Expected RED/mutation/refusal fixtures use isolated test values, never a reset of the real package ledger. An actual unexpected production capture/identity/resource failure stops optional work.

Prefer this explicit propagation/reservation over increasing limits, suppressing exceptions, passing zero used bytes, resetting ledgers or rerunning tokenizer research. No source/default/ABI/licence/model/adoption conclusion changes.

## Frozen inputs and fresh evidence

Recheck the 107 explicit rows in the closed SMC frozen inventory plus these six rows: **113 identity rows**, not unique files. Verify the inventory's own identity before following its records. Hash checks do not authorize executing those historical entry points.

| Additional input | Bytes | SHA-256 |
| --- | ---: | --- |
| `data/t17/tokenizer-source-metadata-02/frozen.json` | 20,786 | `86151c8f82d1cfdb05a1dc58c03346ba56364c7afd08ad33e71d1f4091abed17` |
| `data/t17/tokenizer-source-metadata-02/summary.json` | 1,427 | `9a3d928fb4f6ae38f69ba97a495cc562f97d5e23481735f77f2a5b5e6bb3e1e4` |
| `data/t17/tokenizer-source-metadata-02/post-terminal-parent-state.json` | 181 | `6ccd066b6dba53c050636905c22939724fafe85774d2375e963826ccf5b57c60` |
| `data/t17/tokenizer-source-metadata-02/closure-verification.json` | 787 | `b61efb06df3556c4274df67b60c5e539ac210631c94069040a945f7471f6d3e3` |
| `data/t17/tokenizer-source-metadata-02/local-audit-reconciliation.json` | 1,138 | `1d30b372c9af6bd0c214fbff9e3291934b966f7a7e60f4136be8047f692c1c21` |
| `data/t17/tokenizer-retained-source-review-01/controller-source.json` | 3,505 | `67e61e804e4819e91b34eed85a0aea4c18bb3a1d0e6e72949b9f955a34dc71c4` |

Fresh ignored root: **data/t17/tokenizer-closeout-report-fix-01/**. New report: **docs/benchmarks/tokenizer-closeout-report-fix.md**. Both must be absent at entry. No reuse/reset of closed roots. Use the existing isolated Python 3.14/stdlib inspector and reviewed owned code only. Preserve AGENTS/SPEC/project/lock files, six skills, old evaluation scripts and checkpoints.

## Ordered work

| ID | Objective / prerequisite | Acceptance and evidence | Files / status |
| --- | --- | --- | --- |
| RPT1 | Establish the boundary after execution approval | Fresh paths, 113 rows, exact prepaid starts, shared limits and root/state-only bootstrap of frozen gateway/controller | Proposal/ignored entry and identity records. Proposed. |
| RPT2 | Correct the actual reporting path after RPT1 | Meaningful RED, smallest GREEN, mutation caught, exact restoration/final GREEN; parent lease and production controller use the same tested path | Ignored owned copy/wrapper, tests and captures. Proposed. |
| RPT3 | Validate protected closeout after final RPT2 GREEN | Actual corrected controller runs read-only git diff --check and a complete scoped git diff; verify both child/controller exit, EOF/reaping and complete captures; review untracked authored reports separately | Captures, readable measured diff and findings. Proposed. |
| RPT4 | Close/review after completion or hard stop | Recheck preservation, exact scope, links/UTF-8/whitespace/index, all starts/leases and terminal receipt; append a dated SMC follow-up without rewriting its failed history | Findings/root docs/proposal; SMC addendum only. Proposed. |

RPT2 has **at most twelve inert cases** across parent/controller serialization: ordinary-reserve refusal before launch; closure success near the ordinary ceiling; missing/malformed phase; inconsistent/undercharged lease; duplicate/replayed lease; multibyte status plus newline; oversize zero-write refusal; full-limit refusal; child failure distinct from report failure; missing EOF/reap proof; positive actual caller integration; and mutation/restoration. No allocation per component. Synthetic near-limit fixtures are separate from the real package counter. Two supervised test-child invocations maximum; test phases can share one child. Never weaken a failed assertion to finish.

RPT3 checks the **current** reviewed workspace. It does not retroactively make the old SMC controller pass, rerun its last provisional note, or prove model parity. Current preparation-time Git checks also remain distinct from this proposed supervised integration.

## Shared execution limits

- **14 work units:** entry 2, controls 5, Git integration 2, closeout 5. **900 active seconds**, optional cutoff 480, protected closeout 420. Authoring/waits/failures count. One measured approval wait up to 24 hours without intervening work may be excluded.
- **40 owned starts**, optional ceiling 28, twelve protected. Planned: fixed prelude/approved exact commit 12 + two separate bootstrap invocations 4 + identity check 2 + two supervised test children 6 + two supervised Git reads 6 + final verification 2 + terminal receipt 2 = **34**. Six starts are correction headroom, not new investigations. Integration/final checks use protected closeout; no per-test counters or refunds. Enforce these stricter limits before the unchanged gateway's looser historical ceiling.
- **24 MiB explicit read leases**, including 4 MiB receipt allowance; **2 MiB fresh artifacts**; at most twenty immutable local receipts of at most 4 KiB. Retain failed attempts/partial writes. Hash reads of historical evidence do not permit reopening model stores or payloads.
- **32 KiB authored UTF-8 reporting**, 8 KiB protected; reserve upcoming documentation/final reply as well as each child status lease. Ordinary displays at most 1,024 UTF-8 bytes. The two bootstrap JSON bodies are separate, measured exceptions at most 4,096 ASCII bytes each; host allowance at least 8,192 tokens. No evidence-frame expansion or whole-document dumps.
- Local invocation streams stay **32 KiB combined**, concurrently captured through EOF with retained direct child identity/exit/reaping. Checks at most 60 seconds plus 15 for teardown, sequential owned tree. Premeasure final escaped output before stdout; complete capture must precede excerpts. No machine-wide confinement claim.
- Precharge final reply/terminal starts/read lease and reserve a 64 KiB artifact tail before snapshot. Observe the successful terminal return before marking RPT4 accepted; retain immutable parent reconciliation if necessary. A new failure does not authorize another allocation or automatic retry.

Zero public calls, model-manifest/blob/payload reads or stats, model-store enumeration, dependency/model downloads/installs, resolver/pulls, candidate imports/evaluation, native/model services, old worker entry points, pytest/Ruff, global/PATH/policy changes, Git writes beyond a separately approved exact commit, or checkpoint writes. Unit tests may load the hash-verified owned ReportGate definition; no candidate/library initialization.

## Deliverables and requested decision

Preparation changes only this proposal, PLAN, TODO and README, preserving the two existing SMC report/proposal changes. Proposed **six-file planning/results commit**: those four plus docs/proposals/tokenizer-source-metadata-continuation.md and docs/benchmarks/tokenizer-source-metadata-continuation.md. It records SMC as limited, not fully accepted.

After approval, execution may change PLAN/TODO/README, this proposal, the new RPT benchmark report, and append a link/result note to the SMC benchmark report: six result documents. Keep the historical SMC proposal unchanged during execution. No new versioned helper/application code. The new RPT root holds the owned copy/tests/captures/receipts; historical roots remain immutable.

**Requested:** approve that exact six-file commit and RPT1–RPT4, including the reporting-only controller/wrapper change, two inert test children, two read-only supervised Git checks and shared limits. Results commit remains a separate gate. Native readiness remains on hold; no new requirements or adoption decisions are inferred.
