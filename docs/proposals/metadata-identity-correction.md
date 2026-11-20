# T17-IF-K — targeted identity correction and one metadata-only attempt

## Status and objective

Proposed, awaiting approval. IF-J findings are committed as `6f1e007`. The [synthetic evidence](../benchmarks/windows-identity-direct-results.md) shows path/fstat ctime disagreement after a controlled edit, while other identity fields agree. The original IF-R refusal's exact differing field is still unknown.

Implement and test a narrow successor metadata reader, then permit one fresh read of the same nine pinned public metadata files if all controls pass. This package explicitly proposes the comparison-policy change below. It does not merely suppress an exception, remove timestamp checks or authorize model execution/application development.

## Exact proposed guard change

1. Before open, retain the checked path's stat. Immediately after open, retain fstat. Compare **device, inode, size, mtime nanoseconds, mode and link count** across those two APIs. Require all compared fields and meaningful device/inode values; missing/invalid evidence refuses admission. Check regular-file/reparse/type rules for both observations. A ctime-only cross-API difference may proceed and must be recorded explicitly.
2. After the bounded read, capture fstat again and rerun the checked path/ancestor inspection. Compare **all seven original fields, including ctime**, between the before/after handle observations and separately between the before/after path observations. Any same-API mutation refuses. Also compare the six cross-API fields after reading. Do not assume every timestamp difference is harmless.
3. Preserve the fixed expected size/digest, bounded read, full ancestry/reparse/type refusal, aggregate charging, per-file durable started/completed/refused progress and one-shot attempt admission. Final digest/length must match the pinned artifact, even if the stat comparisons pass. These observations do not establish race-free filesystem confinement or hostile replacement resistance.
4. Retain local content-free named stat fields/differences and an allowlisted refusal code, such as open-identity mismatch, path mutation, handle mutation, size/digest mismatch or input cap. Preserve sanitized error types. Do not repeat the earlier diagnostic loss by recording only `Boundary`. Keep raw config/system/template findings separate from ordinary logs and progress.

This is a narrowly approved compatibility policy for the investigation if accepted; it is not final application security/adoption. No guard change occurs during proposal preparation.

## Source scope and immutable inputs

At most two new authored files: `tests/evals/spikes/input_fit_metadata_corrected.py` and `tests/evals/spikes/test_input_fit_metadata_corrected.py`. Leave all IF-R/IF-I/IF-J aids and closed records byte-identical. The successor may reuse the old aid's finite path/type checks, bounded receipt writer and fixed inventory by compiling its exact hash-verified authored bytes under a non-main module name. Do not execute its old controller/worker/read routine or old main dispatch. Its pinned source SHA256 is `2d47b7c816dba4092c755a4787fee6f394e4bd628a9d77f4829b3da98ed04204`. Keep the new read/comparison logic and explicit fresh-worker dispatch cohesive; no additional launcher framework or dependency.

Use existing base `F:/Python/Python314/python.exe -I -S -B` and project Ruff. No venv redirector, installation, global/PATH change or evaluated native import. Reading/sealing authored aids and the interpreter is distinct from the following model-metadata quota.

Only `data/ollama/models` may supply model metadata. Reuse the **exact nine paths, digests and sizes** in the committed IF-R inventory and [IF-S report](../benchmarks/input-fit-static-review.md): Qwen/Nomic manifests plus Qwen config/system/template/license and Nomic config/parameters/license, declared total26,739bytes. No mutable-tag substitution, weights/GGUF parsing, tokenizer loading, other model stores or user/private saved content. Never fetch missing assets.

Each metadata read is at most64KiB+1; reject >64KiB and enforce1MiB aggregate conservatively, including failed attempts. Retaining a full65,537-byte charge per attempted file is acceptable; nine such charges total589,833bytes. Per-file identity/hash/length/progress must persist before advancing. Extracted public metadata findings stay local, with only necessary non-content summaries in the authored report.

## Test-first acceptance

Use mocked stat/file/process/clock/receipt boundaries and the recorded IF-J values. Required cases:

- Cross-API ctime-only disagreement passes the stat stage while being recorded; the old seven-field cross-API comparison would reject the same fixture. Ctime change within either API refuses, as do cross-API device/inode/size/mtime/mode/link changes, missing identity fields and unsuitable file types.
- Ancestor traversal/outside/reparse refusal, changed handle/path, oversized/aggregate reads and wrong digest/size still prevent success; invalid input must not reach the real reader. Receipt failure prevents advancement and ordinary logs contain no metadata contents.
- Fresh-root/meter/claim/time/output admission, second-attempt refusal, malformed output, timeout, failed kill/reap and cleanup uncertainty fail closed. Use fake negative controls only; no actual extra child or data fixture.

Require meaningful red before implementation, passing new tests **and existing20fake IF-R controls**, Ruff, and a caught in-memory mutation of a same-API ctime check or cross-API identity refusal. Do not weaken/remove existing tests or modify sealed live source for mutation. No new real synthetic fixture or model-token-count test is needed for this package.

## One actual attempt and execution boundary

Fresh ignored root **`data/t17/input-fit-corrected-01/`**, created only after approval. Submit the reviewed controller as literal PowerShell commands using the demonstrated IF-J method; archive exact text/hash but do not invoke a saved script/eval or change execution policy. Preserve native host permission prompts and stop on denial. Before launching, verify old hashes, controls and seals for the base interpreter, reused old source and both new aids; consume durable controller/worker claims.

Launch one explicit base-Python worker only, with no descendant-spawning path, using a retained owned Process, `UseShellExecute=false` and `CreateNoWindow=true`. Wait at most30seconds after successful creation; on timeout kill that exact child and verify exit within5seconds. Creation delay is not covered. Save launch/running/result/cleanup receipts and retain full tool/session/exit fields; do not infer exit from empty output or attach by name/PID/port. Dispose only after verified exit. Intended worker stdout/stderr is a fixed small status/error packet; reject >4KiB, unexpected stderr/nonzero exit or incomplete completion. This is not a general malicious-child RAM limiter.

Connected **stdlib/public-metadata-only**, no filesystem/outbound confinement or new kernel RAM-cap claim. No model/native dependency load, inference, service/API, parser/OCR/vector extension, network/download/install, tokenizer choice or larger context. Any guard/persistence/output/exit/cleanup/limit failure stops without retry, fallback, policy change or old-allocation reset.

## Ordered tasks and shared allocation

| ID | Objective / prerequisite | Acceptance and evidence | Status |
|---|---|---|---|
| IF-K1 |After approval, initialize fresh accounting and preserve earlier evidence |Full manifest/clock before optional work; old IF-R/I/J source, closed meters/selected receipts and rules/spec/lock hashes |Pending approval |
| IF-K2 |After K1, test-first targeted comparison/read correction |Meaningful red, required new+20legacy fake tests/Ruff and caught mutation; exact comparison policy preserved |Pending K1 |
| IF-K3 |After K2/seals/controller review, one actual pinned metadata worker |Nine verified files with named identity evidence/local findings or honest partial stop; full result and verified owned exit |Pending K2 |
| IF-K4 |After K3 or stop, assess metadata/remaining input-fit gates and close |Separate verified bytes/declarations/inference/unknown runtime behavior; links/diff/hash/budget/checkpoint evidence and separate results-commit request |Pending K3 |

**80prepaid conservative units:64normal/16protected**. Manifest: initialization8, red/test authoring12, implementation8, green/lint/mutation10, controller/trial10, reporting6, review/close10, protected16. Include every orchestration/tool/shell/test/lint/mutation/controller/worker/observed-helper/report/cleanup action; no adapter-only counter claim, refunds or hidden resets. Separately approved Git actions remain outside this epoch.

**1,200active seconds**, **2MiB total new source/receipts/generated outputs**. Persist clock/manifest before optional preparation; charge conservatively across interruptions. No real worker unless controls/seals pass and at least60seconds plus required units/output headroom remain. One actual worker, zero actual negative-control workers/new data fixtures. Metadata64KiB/file,1MiB total; intended worker output4KiB. Stop if a required phase cannot cover its remaining steps. Protected capacity is solely for termination, preservation and partial reporting, never new research/implementation/trials.

## Deliverables and approval requested

Two new aids, `docs/benchmarks/metadata-identity-correction-results.md`, focused PLAN/TODO/README/checkpoint and dependency/input-fit cross-references only where actual evidence warrants them. Metadata contents alone cannot prove actual rendering/tokenizer parity, effective context,192-token output reservation, model quality/resource acceptance, native trust or G2 readiness. No end-user app/runtime adoption follows.

Approve the exact IF-K package, explicit comparison-policy/execution boundary and separately the five proposal/status documents' commit. One package approval covers its routine ordered edits/tests/read/review without repeated step approval. Later source/results commits, adapter/native validation, dependencies, G2/application implementation and stage transitions retain separate gates.
