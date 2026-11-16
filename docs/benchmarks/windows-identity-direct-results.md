# T17-IF-J — synthetic comparison completed; cross-API timestamp difference observed

## Outcome — 2026-11-16

The user approved the [IF-J package and direct-command boundary](../proposals/windows-identity-direct-controller.md), with proposal commit `a084243`. Host preflight passed,22fake tests and Ruff passed, a targeted mutation was caught, and the sole synthetic probe completed. Its owned process exited0 and was reaped. No policy setting changed and no model/user content was read.

The probe demonstrates a **cross-API `st_ctime_ns` difference after a controlled same-file edit**. It supplies a concrete compatibility lead for the [earlier metadata refusal](input-fit-inspection-results.md), but does not retrospectively identify that refusal's exact differing field: the earlier receipt did not retain the fields. No metadata guard was changed or runtime adopted.

## Host capability and source reuse

The approved limited preflight reported all five execution-policy scopes as`Undefined`, language mode`FullLanguage`, successful literal marker submission and successful construction/disposal of ProcessStartInfo/Process objects without starting a process. These observations established the capabilities needed for this direct-command trial; they do not assert that saved-script execution was permitted or that policy was unrestricted generally.

The controller was submitted as literal reviewed PowerShell commands. Exact text is archived at `data/t17/windows-identity-02/controller.txt`; it was not invoked/evaluated as a saved script. No execution-policy override, registry/PATH change, Invoke-Expression or ScriptBlock.Create was used. No host permission denial occurred.

[New bootstrap](../../tests/evals/spikes/windows_file_identity_followup.py) verifies the original authored probe hash, compiles exactly those bytes under a non-main module name, and explicitly binds its probe/persistence globals to the fresh02root. The old aid and tests remain byte-identical. The bootstrap checks the active allocation, controller claim, remaining time/output allowance and exclusive probe claim; it does not execute the old command or old `__main__` dispatch.

## Verification before the real trial

The [new tests](../../tests/evals/spikes/test_windows_file_identity_followup.py) cover fresh-root binding of both probe and persistence, wrong root, closed/missing/unclaimed meter, time/output/claim refusal, second-probe claim failure, changed source hash, missing-source failure and probe-error propagation. They also run the unchanged14fake probe tests. No real negative-control child or additional data fixture ran.

Commands actually executed:

```powershell
& 'F:/Python/Python314/python.exe' -I -S -B tests/evals/spikes/test_windows_file_identity_followup.py
.\.venv\Scripts\ruff.exe format tests/evals/spikes/windows_file_identity_followup.py tests/evals/spikes/test_windows_file_identity_followup.py
.\.venv\Scripts\ruff.exe check tests/evals/spikes/windows_file_identity_followup.py tests/evals/spikes/test_windows_file_identity_followup.py
& 'F:/Python/Python314/python.exe' -I -S -B tests/evals/spikes/test_windows_file_identity_followup.py mutation
```

Initial red was the expected missing-bootstrap import error. Green:22tests passed0.005s, Ruff lint passed and both files formatted. An in-memory mutation disabled the root refusal; its focused test failed as expected in0.002s/exit1. Live source bytes were not mutated. All checks preceded the sole real probe. Final formatting/whitespace/document/preservation checks accompany closeout; no historical native suite was rerun.

## Actual synthetic observations

One32-byte fixture was exclusively created below `data/t17/windows-identity-02/`. The probe observed it unchanged, modified its first byte once, flushed/closed it and observed it again. Sixteen explicit stat/lstat/fstat operations,64actual bytes read and130conservatively charged read bytes remain below32operations/4KiB. No second fixture or probe was created.

| Comparison | Observation |
|---|---|
| Original path lstat versus open-handle fstat |All seven IF-R identity fields equal |
| Original stat versus lstat |All ten recorded fields equal, none missing |
| Original before/after read, same API |Both handle and path comparisons equal |
| Modified path versus handle |Only `st_ctime_ns` differs among the seven identity fields |
| Original versus modified path observations |Only `st_mtime_ns` differs among all ten recorded fields |
| Content control |Hash changed; size remained32bytes |

For this fixture, original birth time and both original ctime readings were`1794793834047820600ns`. After modification, the path's ctime remained that value while fstat's ctime was`1794793834069902300ns`; the modified path's mtime was also the latter value. Thus the original seven-field cross-API tuple can disagree for a valid, deliberately edited file even when other identity fields agree. This is an observation on this interpreter/filesystem, not a universal Windows identity rule or proof of resistance to hostile replacement/races.

The content hashes were:

- Original:`f1d4419693a42e3c6576096186243fdca5a87c32bceb5c6b2f3f8f3d66b89cbe`.
- Modified:`5b07018a1dbca49433b4bf011dcbe821026c5f9872ff79a58dd7c5a179bf9fcd`.

Exact field snapshots/comparisons and source/platform identity are retained in the ignored `receipt.json`. The observed case does not require choosing which API's ctime is authoritative. No broader timestamp, hard-link, reparse, replacement or filesystem-security acceptance was performed.

## Owned exit and artifacts

The controller sealed the original probe, new bootstrap/tests and existing base interpreter, consumed its durable single-attempt claim, and launched the explicit base-Python argument vector. The sole owned probe PID43884 exited0/reapedtrue; controller elapsed0.3430525seconds, stdout23bytes, stderr0. The10-second timeout did not fire; no kill/reap failure was induced or measured. Handles were disposed after verified exit. Full tool return/session/exit fields are retained in `execution.json`; no active session remains or was lost. No host-wide process inventory or kernel descendant-count claim was made.

| Sealed artifact | SHA256 |
|---|---|
| Original probe |`7c62c7e58d7bb4e7fbd9501390e2dfbf6b97d560c99425db50003a2348775856` |
| New bootstrap |`8f4c0fb0ee0020113f3a0c6217ae619629cc75c82be5970d45b479fafefccee0` |
| New tests |`d1816d302863838b4d6165a6694f23a88c30edd9b3b28a686218bc92d0928feb` |
| Base Python |`03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38` |

## Review, accounting and next decision

Fresh ignored meter persisted64prepaid units(48normal/16protected),1,200active seconds and1MiB outputs before optional work. Thirteen specification/rules/lock/source/closed-receipt identities were frozen and rechecked before launch. Every orchestration/shell/preflight/test/lint/mutation/controller/probe/report action shares the reservation manifest; it is not a kernel process-start counter. Full phase reservations remain retained without refund. Final time/output/link/preservation/seal evidence and closed completed status are recorded in the meter. No old allocation was reset and no trial retried.

The security review preserves exact source hashes, fixed fresh-root admission, one-shot claims, explicit owned-process cleanup and content-free ordinary output. This connected stdlib/synthetic-only boundary provides no filesystem/outbound confinement or new kernel RAM-cap guarantee. There were no model-store/private-document reads, candidate native loads, inference, services, network/download/installation, guard edits or G2/app adoption. Fake-control evidence and a successful synthetic comparison do not establish model input fit or16GB CPU-only acceptance.

**Next recommendation:** propose a narrow metadata-reader correction that separates cross-API stable identity comparisons from same-API mutation checks, retaining expected size/hash, reparse/type/path checks and failure behavior. Test the observed ctime difference without silently treating all timestamp differences as harmless. A new metadata attempt, any guard-policy change and its exact acceptance require a separate concrete package; none are authorized by this report.

Seven new source/results files are presented for separate commit approval: bootstrap/tests, this report, PLAN, TODO, README and checkpoint. Existing [IF-I](windows-file-identity-results.md), IF-R sources/evidence, SPEC/AGENTS/dependency pins and all model files remain unchanged.
