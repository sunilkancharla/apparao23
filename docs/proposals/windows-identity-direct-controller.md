# T17-IF-J — host preflight and one direct-controller synthetic trial

## Status and objective

Proposed, awaiting approval. IF-I source/results are committed as `c94d6da`. The [previous attempt](../benchmarks/windows-file-identity-results.md) was refused while loading its saved PowerShell script, before any probe or fixture existed. The underlying file-identity difference remains unknown.

First establish whether the host permits the required direct commands and process-control objects. Only if it does, prepare and run one fresh synthetic comparison using the existing tested probe logic. Do not reopen `windows-identity-01`, change the metadata guard or inspect model files.

## Exact invocation and authority boundary

The proposed change is to submit a **literal, reviewed controller command directly through the PowerShell tool**, rather than invoke a saved `.ps1`. Archive the exact command text/hash locally for review, but do not load/evaluate that archive with `Invoke-Expression`, `ScriptBlock.Create` or a shell wrapper. No `Set-ExecutionPolicy`, `-ExecutionPolicy Bypass`, `Unblock-File`, policy/registry modification or global/PATH change is permitted.

After package approval and fresh accounting, read only `Get-ExecutionPolicy -List` and `$ExecutionContext.SessionState.LanguageMode`; record their small scalar results locally. Test direct literal-command submission with a fixed content-free marker and construction/disposal of `System.Diagnostics.ProcessStartInfo`/`Process` objects **without starting a process**. This is host-capability evidence, not permission to override a managed restriction. If the host refuses the required command/object, stop before implementation/trial. Use native host permission prompts when required; a denial is a stop, not permission to find another route. No broad process/environment/user inventory.

The eventual controller retains the existing boundary: fixed base executable/arguments, `UseShellExecute=false`, `CreateNoWindow=true`, one retained owned `Process`,10-second post-creation wait and5-second owned kill/reap verification. Creation delay is not claimed covered. Save prelaunch/running/exit/cleanup receipts; no basename/PID discovery or attachment. Capture at most the intended small status/error packet, reject >4KiB or unexpected stderr/nonzero exit. Bounds rely on the sealed known probe; they are not a general malicious-child RAM limiter. Dispose handles only after verified exit. Retain full tool/session/exit fields and stop on unknown cleanup.

## Sources and fresh run

- Preserve both existing `windows_file_identity.py` and `test_windows_file_identity.py` byte-for-byte. Expected SHA256: probe `7c62c7e58d7bb4e7fbd9501390e2dfbf6b97d560c99425db50003a2348775856`; tests `4d4e9d17d716d16d2fba0a6f004b479af5f7129c36c001f53ca448e96832440f`. Preserve IF-I's closed meter/execution/controller text and prior IF-R evidence.
- At most two new authored files: `tests/evals/spikes/windows_file_identity_followup.py` and `tests/evals/spikes/test_windows_file_identity_followup.py`. The first is a small explicit bootstrap, not a duplicate probe or new launcher framework. Load only the verified authored probe module by its exact local path without triggering its old `__main__` dispatch; bind its `RUN` to the single approved fresh root, then call its unchanged `probe`/`persist` functions. Test this binding and refuse old/outside roots. Do not edit old source, use environment-selected paths or run an old command.
- Fresh ignored root **`data/t17/windows-identity-02/`**. Bootstrap must enforce that root's active meter, single attempt claim and remaining clock/output allowance before calling the reused probe. Controller seals old probe, both new aids and existing base interpreter before launch. No trial starts unless all prerequisites/checks pass.
- Existing `F:/Python/Python314/python.exe -I -S -B` and project Ruff only. No installation/new dependency/evaluated native import. Reuse the original one <=64-byte synthetic fixture definition, at most4KiB fixture reads and32stat operations, unchanged/read/one-byte-modified observations and exact missing/differing fields. One real probe only, no actual negative-control child or extra data fixture.

No model-store/user-document/private-output read, tokenization, inference, service/API/network/download/OCR/parser/vector loading. Connected stdlib/synthetic-only boundary; no filesystem/outbound confinement or new kernel RAM-cap claim. No guard repair, tokenizer choice, input-fit acceptance, G2 or application adoption.

## Ordered tasks and acceptance

| ID | Objective / prerequisite | Acceptance and verification | Status |
|---|---|---|---|
| IF-J1 |After approval, initialize preservation/accounting and perform the limited host preflight |Full prepaid clock/manifest first; policy/language-mode/capability receipts; no child/fixture; refuse missing/denied capability |Pending approval |
| IF-J2 |After J1 passes, test-first bootstrap/binding/admission |Meaningful red, passing new tests plus existing14fake tests/Ruff; in-memory admission mutation caught; old source hashes unchanged |Pending J1 |
| IF-J3 |After J2/seals/literal-controller review, one fresh synthetic probe |Exact fields/differences and modification observations or partial stop; full result/verified owned exit; no old run touched |Pending J2 |
| IF-J4 |After J3 or any stop, review and close |Document observed versus unknown Windows behavior, preserve hashes/links/diff/budgets/checkpoint and request results commit; no silent guard adoption |Pending J3 |

New tests must cover wrong/closed/missing root or meter, second-attempt refusal before probe invocation, changed source hash, binding both probe/persistence to02, and failure propagation without success. Mock process/clock/file controls; real timeout/negative workers remain excluded. Existing14tests are fake-only and share this allocation. Routine corrections/tests/review inside the approved package need no additional task-start permission.

## Shared budget and stop rules

**64prepaid conservative execution units:48normal/16protected**. Manifest: initialization/preservation4, host preflight4, test-first bootstrap12, green/lint/mutation8, controller/trial8, reporting4, review/close8, protected16. Cover every orchestration/tool/shell/test/lint/mutation/controller/probe/observed-helper/report/cleanup action, not only the adapter. No refunds, old-meter resets or silent new phases. Separately approved Git actions are outside this epoch.

**1,200active seconds**, **1MiB new source/generated receipts/outputs**; persist before optional work. At least60seconds plus required normal units/output headroom must remain before launch. One real probe; one64-byte data fixture/4KiB reads/32stat operations; no extra actual discovery/timeout child. Preflight failure stops before implementation; any real guard/receipt/tool/exit/cleanup/limit failure stops without retry or fallback. Protected capacity is only for termination, preservation and partial reporting, never new research/implementation/trial.

## Deliverables and approval

Two new bootstrap/test aids, `docs/benchmarks/windows-identity-direct-results.md`, and focused PLAN/TODO/README/checkpoint updates. No changes to SPEC/AGENTS/dependency pins or old sealed aids. Distinguish literal-command capability, fake tests, actual stat observations and unproven identity/security guarantees.

Approve this exact IF-J package, the explicit direct-command execution boundary and separately the five proposal/status documents' commit. Later source/results commits, metadata-guard changes, renewed model-metadata inspection and G2/application work remain separate decisions.
