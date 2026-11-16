# T17-IF-I — controls passed; host refused saved controller

## Outcome — 2026-11-16

The user approved the [IF-I package](../proposals/windows-file-identity-investigation.md) and its five-document commit, `16d6f97`. The two new standard-library aids passed14focused tests and Ruff; an in-memory mutation that suppressed differing fields was caught. The subsequent saved PowerShell controller invocation was rejected by the host before its script executed.

**No synthetic probe ran, no fixture was created and no actual stat/fstat comparison was obtained.** The original Windows identity mismatch remains unexplained. There was no model-store read, metadata retry, guard change, dependency/model/native execution, service, installation, download or network request. Existing IF-R and earlier evidence remain unchanged. The new allocation is closed without retry.

## Authored controls and verification

- [Probe aid](../../tests/evals/spikes/windows_file_identity.py) preserves the seven IF-R identity fields plus available Windows attributes, reparse tag and birth time. Each field retains an explicit presence marker. It reports differences rather than normalizing them into equality. Its intended real path exclusively creates one <=64-byte owned file, captures unchanged/read observations, modifies one byte, and records changed observations/hash with32stat and4KiB aggregate-read caps.
- [Fake tests](../../tests/evals/spikes/test_windows_file_identity.py) cover missing versus zero values through JSON, differing/equal/missing comparisons, outside/traversal/existing/reparse fixture refusal, stat/read caps, oversized or unexpected contents, size/hash-change reporting, fixture failure and receipt-write failure. They create no real fixtures or children.
- A short reviewed controller was authored only under ignored `data/t17/windows-identity-01/run.ps1`. It specifies the fixed base Python executable/arguments, a retained owned process,10-second wait/5-second kill-reap path, content-free output checks and durable attempt state. Its seal/launch/timeout/cleanup paths **were not exercised**, because script loading was refused. It is withdrawn with this closed allocation.

Commands actually executed:

```powershell
& 'F:/Python/Python314/python.exe' -I -S -B tests/evals/spikes/test_windows_file_identity.py
.\.venv\Scripts\ruff.exe format tests/evals/spikes/windows_file_identity.py tests/evals/spikes/test_windows_file_identity.py
.\.venv\Scripts\ruff.exe check tests/evals/spikes/windows_file_identity.py tests/evals/spikes/test_windows_file_identity.py
& 'F:/Python/Python314/python.exe' -I -S -B tests/evals/spikes/test_windows_file_identity.py mutation
```

Expected red: `ModuleNotFoundError` before the aid existed. Green:14tests passed0.010s, Ruff lint passed and both files were formatted. The controlled mutation replaced the differing-field condition with false in an in-memory copy; its focused test failed as intended in0.002s, exit1. The live source was not mutated. A subsequent docstring correction changes no behavior; final format/lint/whitespace/preservation/link checks accompany closeout. No historical/native suite or real timeout control ran.

## Host refusal and absence of a probe

Attempted once:

```powershell
& 'F:\document_assistant\data\t17\windows-identity-01\run.ps1'
```

The tool returned exit1 after0.7626465seconds with `PSSecurityException`/`UnauthorizedAccess`, stating that running scripts is disabled. The complete result, including exit fields, is retained locally as `execution.json`. This is a script-loading refusal, not a failure of the Python probe or the file-identity guard.

The controller did not reach its first statement, artifact-sealing code, attempt claim or process creation. Read-back confirms no `ready.json`, `attempt.claim`, `controller.json`, `fixture.bin` or `receipt.json`. The shared meter therefore retains `probe_attempts:0`. No owned probe process was created and no teardown was required; there is no successful timeout/kill/reap measurement to claim. No active tool session was returned or lost.

I should have established that the saved-script invocation was permitted before making it the sole execution path. The error does not identify whether machine, user or another policy source set the restriction; no policy discovery/change or alternative invocation was attempted. No execution-policy bypass, escalation/retry, inline replacement, reseal, broader process lookup or renewed model inspection followed.

## Evidence, limits and handoff

Fresh ignored record: `data/t17/windows-identity-01/meter.json`. Before optional work it persisted48prepaid units(36normal/12protected),900active seconds and1MiB outputs. Eleven prior identities cover AGENTS/SPEC/pyproject/lock, both IF-R aids and IF-R meter/progress/ready/controller/execution receipts. No closed record was reset. Full phase reservations are retained, including the refused invocation; protected capacity covers only final preservation/reporting, not another attempt. Final elapsed/output/hash/link counts and closed status are stored in the meter.

This connected standard-library/synthetic-only package has no filesystem/outbound confinement or new kernel RAM-cap claim. Its intended controller/output/fixture limits do not establish general hostile-process confinement. There are0real probe starts,0generated data fixtures,0fixture reads/stat observations and0candidate/native calls. Fixture handling and field comparisons have fake-test evidence only; runtime validity remains unproven.

**Recommendation:** establish a host-permitted invocation for the reviewed bounded controller before a separately approved fresh synthetic trial. Keep its intended process ownership, timeout, read/stat/output and no-model boundaries. Do not change machine/user policy or silently treat an alternative invocation as already validated. No follow-up package is implemented or approved here.

Seven source/results files are presented for a separate commit: the two aids, this report, PLAN, TODO, README and checkpoint. The exact model-metadata guard, tokenizer/rendering/input-fit method, native trust, G2 and end-user app remain unchanged and unresolved. [IF-R evidence](input-fit-inspection-results.md) remains the source for the earlier file refusal.
