# T17-IF-I — synthetic Windows file-identity investigation

## Status and question

Proposed, awaiting approval. IF-R source/results are committed as `9a72136`. Its [closed attempt](../benchmarks/input-fit-inspection-results.md) refused the first path/open-handle identity comparison before reading content; the individual differing fields were not retained. Do not infer corruption, replacement or a native-library defect.

Determine which fields from `Path.lstat()`, `Path.stat()` and `os.fstat()` agree or differ for **one newly authored synthetic file** on the existing Windows interpreter/filesystem. Preserve the values needed to explain the comparison. This investigation does not repair or relax the metadata guard, prove protection against hostile replacement, or authorize another model-metadata attempt.

## Exact scope

- At most two new authored files: `tests/evals/spikes/windows_file_identity.py` and `tests/evals/spikes/test_windows_file_identity.py`. Keep the snapshot/comparison/probe logic small and cohesive. No edits to the sealed IF-R aids or older helpers.
- Existing base `F:/Python/Python314/python.exe -I -S -B`, standard library only; project Ruff for these two files. No installation, interpreter/global/PATH changes, new dependency or candidate-native import.
- After controls pass, generate exactly one fixed synthetic `fixture.bin`, at most64bytes, exclusively below fresh ignored `data/t17/windows-identity-01/`. No existing user/model files as fixtures. Read at most4KiB total from that fixture; at most32stat/fstat operations. Generated controller/receipts are separate from this one data fixture.
- Capture the seven fields used by IF-R: device, inode, size, modification nanoseconds, change-time nanoseconds, mode and link count. Also record available Windows attributes/reparse tag/birth-time fields, with explicit missing-field markers rather than fabricated zeroes. No document text, user paths, environment dump or process inventory.
- In one probe, capture path stat/lstat and open-handle stat before/after a bounded fixture read, then close the handle. Record exact field differences and their equality/inequality; do not assume every difference signals replacement. Perform one predetermined same-file one-byte modification, flush it, reopen and record changed observations/hash. This control establishes only the changes actually observed, not universal detection of all mutations.
- Save small JSON snapshots, comparisons, fixture hash/size, Python/platform identity and completion/failure receipts under the fresh root. Print only a small content-free status packet. Output is data; no execution of fixture or third-party instructions.

No reads below `data/ollama/`, no other model stores, private saved outputs or user documents. No model/tokenizer/parser/OCR/vector extension/service/API/inference/network/download activity. No reuse/reset/retry of any closed allocation. No application implementation, exact token-count adapter or runtime adoption.

## Test-first and real-execution boundary

First write focused tests using fake stat structures and mocked file/receipt boundaries. Prove that differing/missing fields survive serialization, changed size/hash is reported, invalid/outside/reparse/existing fixture paths refuse creation, bounded reads refuse excess, and fixture/receipt failures cannot report success. Initial meaningful red, passing tests and Ruff are prerequisites to the real probe. Mutate one comparison/refusal condition in an in-memory copy and require its focused test to fail; leave sealed live bytes unchanged. No actual negative-control worker or extra real fixture is permitted.

After checks, seal the two aids and base interpreter and execute **one** actual probe. A short reviewed PowerShell controller may be generated inside the ignored root: explicit fixed executable/arguments, `UseShellExecute=false`, `CreateNoWindow=true`, retained `System.Diagnostics.Process` object, no process-name lookup. After successful creation wait at most10seconds; if it has not exited, kill that exact owned process and verify exit within5seconds. Persist launch/exit/cleanup status. Process-creation delay itself is not covered by the wait timer. Dispose owned handles after verified exit; unknown cleanup is a stop, never success. The probe contains no descendant-spawning path; any observed console-helper overhead must be charged, not ignored.

Keep stdout/stderr intentionally small through the sealed probe's fixed status/error packets; reject output over4KiB and unexpected stderr/nonzero exit. This is not a general hostile-child memory limiter. Retain the complete tool result and session identifier when a call yields; empty output is not exit evidence. Do not add another launcher framework or Windows Job Object experiment.

This is a connected **stdlib/synthetic-data-only** boundary, with no filesystem/outbound confinement or new kernel RAM-cap claim. It grants no connected execution permission for evaluated model/native dependencies. Any real-probe failure, guard/receipt error, unverified exit or exhausted limit stops further investigation; report partial results without retry.

## Ordered tasks and checkpoints

| ID | Objective and prerequisite | Acceptance / evidence | Status |
|---|---|---|---|
| IF-I1 |After approval, initialize fresh accounting and preserve previous evidence |Full manifest/clock persisted before optional work; IF-R meter/progress/ready/controller/execution and both aids, AGENTS/SPEC/lock hashes captured |Pending approval |
| IF-I2 |After I1, implement snapshot/comparison and safe probe test first |Expected red; passing focused tests/Ruff; caught in-memory mutation; no real fixture/probe yet |Pending I1 |
| IF-I3 |After I2/seal/controller review, one synthetic probe |Exact stat-field values/differences and modification observations or partial stop; fixture/operation limits; full exit/cleanup receipt |Pending I2 |
| IF-I4 |After I3 or stop, review and close |Explain observed mismatches versus unknowns; document candidate guard implications without adoption; verify hashes/links/diff/budgets and request results commit |Pending I3 |

The internal checkpoint after I2 is checks-based and covered by package approval; no repeated routine-edit/test approval. The closeout decision is separate: accepting a guard change or permitting another metadata run requires a new concrete package.

## Shared allocation and stops

Fresh root `data/t17/windows-identity-01/`, created only after approval. **48prepaid conservative local execution units:36normal/12protected**, covering orchestration, shells, tests/lint/mutation, controller, probe, any observed helper, reporting and cleanup. Manifest: initialization4, test authoring4, red4, implementation4, green/lint/mutation6, real probe4, report4, review/close6, protected12. No phase refunds or silent resets; preserve the whole reservation manifest. Separately approved Git actions stay outside this investigation epoch.

**900active seconds** including authoring/tool waits/checks/reporting; **1MiB total new source/receipts/generated outputs**. Persist the clock before optional work and charge conservatively across interruptions. Reserve stopping/reporting capacity before launch. No real probe starts unless controls/seals pass and at least60seconds plus sufficient units/output headroom remain. Maximum one real probe; one64-byte fixture/4KiB reads/32stat operations. Stop at the first real failure or exhausted normal block; protected capacity is only for owned termination, preservation and partial reporting. No additional research/implementation using protected slots.

## Deliverables and approval requested

Two aids, `docs/benchmarks/windows-file-identity-results.md`, and focused PLAN/TODO/README/checkpoint updates; dependency references only if warranted. Explain which fields were observed to differ, which observations support a future comparison design, and what remains unproven. Retain exact artifact identities and all old evidence unchanged. No secure-erasure, model-correctness, input-fit or16GB resource-acceptance claim.

Approve this exact IF-I package/execution boundary and separately the five proposal/status documents' commit. Later source/results commits, guard changes, any renewed metadata inspection and G2/application implementation retain their own gates.
