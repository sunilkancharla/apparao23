# T17-IF-K — corrected metadata inspection completed

## Outcome — 2026-11-16

The user approved the [exact IF-K comparison policy and execution package](../proposals/metadata-identity-correction.md), committed as `c4dff2d`. The successor reader passed30fake tests/Ruff and a caught same-API timestamp mutation. Its sole metadata worker then verified all nine pinned files,26,739actual bytes, and exited0 with reap verified.

All nine files exhibited a path/open-handle ctime difference while passing the six compatible cross-API fields and the seven-field before/after checks within each API. The former seven-field cross-API comparison would reject these current observations. This confirms the compatibility issue for the current files; the original IF-R receipt still cannot retrospectively identify its exact differing field.

No weights, model/tokenizer/native dependency, user documents, saved prompts/answers, service, inference, network/download or installation was accessed/executed. The original IF-R/I/J aids and closed records remain unchanged. This closes the missing metadata inspection; it does **not** establish exact token counting, runtime rendering/context/output parity, native trust, G2 or an end-user app.

## Corrected guard and verification

[Successor aid](../../tests/evals/spikes/input_fit_metadata_corrected.py) reuses only the exact hash-verified old authored module's finite path/type/receipt/inventory helpers, under a non-main module name. It does not dispatch the old reader/controller/worker/main. New logic compares device/inode/size/mtime/mode/link count across APIs, but retains ctime in separate before/after handle and before/after path comparisons. Missing/meaningless identity, unsuitable type/reparse, changed stable fields, same-API mutation, size/digest mismatch and caps still refuse.

Exact named observations/differences are retained locally before the read, with started/completed/refused state and allowlisted refusal codes. Expected digest/size and bounded-read/aggregate/path checks were preserved. Observed stat stability and pinned hashes are not race-free filesystem confinement or general hostile-replacement guarantees.

[New tests](../../tests/evals/spikes/test_input_fit_metadata_corrected.py) add10targeted tests to the unchanged20IF-R fake controls. They cover the demonstrated ctime-only cross-API pass, same-API handle/path ctime refusal, changes to each cross-API field, missing/meaningless identity, digest/size/oversize/aggregate refusal, invalid paths, receipt failure and fresh-root/meter/claim/time/output admission. Existing fake controls cover ancestry/reparse and owned-process/error/timeout/kill/reap behavior; the real direct PowerShell timeout/failure paths were not induced.

Commands actually executed:

```powershell
& 'F:/Python/Python314/python.exe' -I -S -B tests/evals/spikes/test_input_fit_metadata_corrected.py
.\.venv\Scripts\ruff.exe format tests/evals/spikes/input_fit_metadata_corrected.py tests/evals/spikes/test_input_fit_metadata_corrected.py
.\.venv\Scripts\ruff.exe check tests/evals/spikes/input_fit_metadata_corrected.py tests/evals/spikes/test_input_fit_metadata_corrected.py
& 'F:/Python/Python314/python.exe' -I -S -B tests/evals/spikes/test_input_fit_metadata_corrected.py mutation
```

Expected red: missing successor import before implementation. Green:30tests passed0.063s, Ruff passed and both files formatted. The in-memory mutation removed ctime from same-API comparisons; its focused test failed as intended in0.005s/exit1. Live sealed source was unchanged. No actual negative-control child or new data fixture ran. Final format/whitespace/document/preservation checks accompany closeout.

## Verified bytes and hashes

Only the fixed public inventory below `data/ollama/models` was read. Each file passed expected size/hash, before/open/after observations and durable completion progress. The raw public findings are separate from content-free progress in the ignored run root; system/template text was not printed into ordinary logs.

| Role | Verified bytes | SHA256 |
|---|---:|---|
| Qwen manifest |857|`65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b` |
| Nomic manifest |708|`0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f` |
| Qwen config |487|`377ac4d7aeefd5b870c9fccff9a6d4df36901d99fe3277c2f755bc401601ba1c` |
| Qwen system |68|`66b9ea09bd5b7099cbb4fc820f31b575c0366fa439b08245566692c6784e281e` |
| Qwen template |1,482|`eb4402837c7829a690fa845de4d7f3fd842c2adee476d5341da8a46ea9255175` |
| Qwen license |11,343|`832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e` |
| Nomic config |420|`31df23ea7daa448f9ccdbbcecce6c14689c8552222b80defd3830707c0139d4f` |
| Nomic parameters |17|`ce4a164fc04605703b485251fe9f1a181688ba0eb6badb80cc6335c0de17ca0d` |
| Nomic license |11,357|`c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |

Actual bytes26,739; conservative charge589,833=9×65,537of1,048,576allowed. The unused part of each possible read charge was not refunded. No model weight was read/rehashed/parsed and no missing asset fetched. Reading the generated findings for review is separate from rereading the model-store files; there was only one actual worker/metadata pass.

## Metadata findings and what they do not prove

| Verified local metadata | Implication / remaining limit |
|---|---|
| Qwen config declares gguf, familyqwen2,1.5B,Q4_K_M |Pins the declared configuration; actual weight/tokenizer bytes were not inspected |
| Qwen has separate system and1,482-byte template layers |Exact rendering must account for both; byte length is not token count |
| Template references Messages/System/Prompt/Response/Role/Content and tool-related fields; contains im-start/im-end markers |Serializer/role/assistant-prefix/special-token parity matters; this does not enable tools or prove which branches the runtime uses |
| Nomic config declares gguf,nomic-bert,137M,F16 |Embedding tokenizer/config remains separate from the chat model |
| Nomic parameters contain `num_ctx:8192` |Observed artifact parameter only; effective runtime context/fit was not measured and provisional application limits are unchanged |
| Both config layers contain amd64/linux labels |Artifact declarations, not a fresh Windows binary compatibility result |
| Both verified license layers contain Apache License/Version2.0 markers |Local notice evidence only; no legal clearance or reconciliation of every native/vendor/transitive notice |

No tokenizer artifact/version or exact application-facing count-only operation was selected. The public metadata does not establish Nomic prefix handling, special-token IDs, actual renderer settings, effective context, output/termination overhead or representative multi-file/resource behavior. The provisional2048context/192output and R01 byte/packing settings remain unchanged, not adopted by this inspection.

| Adapter direction | Remaining work before a decision |
|---|---|
| Exact renderer plus matching tokenizer |Pin matching tokenizer artifacts/dependencies/license and verify template/role/special-token parity, offline behavior and cost |
| Owned runtime's internal count operations |Review endpoint/process ownership and lifecycle, exact rendering/tokenization parity, native trust and resource boundary; no internal port attachment is authorized |
| Public count-only API |Still not established by the carried-forward public-source review; do not invent an endpoint |
| Byte guards or truncation refusal alone |Remain insufficient to prove exact input/output-headroom fit |

**Next recommendation:** prepare a bounded adapter-design comparison using these verified identities and the existing pinned runtime source evidence, then obtain an explicit adapter/trust decision before provisioning or native validation. No additional public research, tokenizer download, internal-runner call or application code is authorized by this report.

## Owned completion, accounting and handoff

Literal reviewed PowerShell controller text/hash is archived in `data/t17/input-fit-corrected-01/controller.txt`; no saved-script invocation/eval/policy change occurred. It sealed base Python, old authored helper and the two new aids, consumed one-shot controller/worker claims and launched one explicit base-Python worker. PID33352 exited0/reapedtrue; elapsed0.7618728seconds, stdout33bytes/stderr0. The30-second deadline did not fire; handles were disposed after verified exit. Full tool/session/exit fields are retained in `execution.json`. No active session/worker remains; no process-name discovery or kernel descendant-count claim.

New aid SHA256:`6a3681d07ba0c8b22e526141702f7f8dab3ae165f02c6dd3d00086b227e89dfb`; new tests:`96f2ba6dd47c996b67ccae65e23548a7a74c4d0df1d84ce99ab676ba1f5de05a`. Reused helper:`2d47b7c816dba4092c755a4787fee6f394e4bd628a9d77f4829b3da98ed04204`; base Python:`03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38`.

Fresh meter persisted80prepaid units(64normal/16protected),1,200active seconds/2MiB outputs before optional preparation. Sixteen prior rules/spec/lock/source/closed-receipt hashes were frozen and rechecked. All orchestration/tools/shells/tests/lint/mutation/controller/worker/report actions share the conservative reservation manifest; no adapter-only start counter or refund. Final elapsed/output/links/preservation/seals and closed completed status are stored in the meter. No old epoch was reset or retried.

Connected stdlib/public-metadata-only execution provides no filesystem/outbound confinement or new kernel RAM-cap guarantee. Metadata verification and fake controls do not establish model accuracy,16GB CPU-only acceptance, native advisory/notice clearance or G2 adoption.

Nine source/results documents/aids are presented for a separate commit: two aids, this report, dependency/input-fit references, PLAN, TODO, README and checkpoint. Model files, prior evidence and SPEC/AGENTS/dependency pins remain unchanged.
