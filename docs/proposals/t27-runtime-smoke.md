# T27-S1 — Bounded owned-runtime and embedding smoke

**Status: executed and closed, 2026-11-20 - failed before native launch.** [S1 receipts/diagnosis](../benchmarks/t27-runtime-first-stop.md): `OLLAMA_ASSET_UNAVAILABLE`, 2 charged Python starts, 0 HTTP calls, no native reservation. The verifier used the wrong model-store path. Preserve this root/ledger/seal; its command is withdrawn and no retry is authorized. The user approved a [focused correction/fresh S2 package](t27-preflight-correction.md) on 2026-11-20; S1 remains closed. This is the separate native execution package required to finish T27 after client commit `ae1f611`. The user's instructions to proceed authorized owner implementation and preparation; no real-model execution has occurred in that work. [Implementation and fake-only verification](../benchmarks/t27-runtime-owner.md). The user explicitly approved both the source commit and this exact native execution package. This does not establish native results, runtime acceptance or a stage transition.

## Fixed scope and artifacts

Use the existing project `.venv` Python/HTTPX and **Ollama 0.40.16**, executable `.venv/tools/ollama/0.40.16/ollama.exe`, SHA256 `4ccefcbfecc50fb6526471adabbc20869dd614e29e351120b15083cb174b0b8a`. Use only the existing `data/ollama/models` **nomic-embed-text:v1.5**, manifest SHA256 `0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f`; verify its config/layer sizes/hashes using existing diagnostics before both sessions and after the run. No installation, download, model change, native dependency/build/source-evidence investigation or private corpus access is included.

The [source seal](t27-runtime-smoke-seal.json) pins 25 application/helper/configuration files, including the two new runtime modules, the worker and `pyproject.toml`/`uv.lock`. Both parent and worker reject source drift before native construction. This is an accidental-drift check, not protection against a hostile same-account operator changing both code and seal.

Run once in fresh ignored `data/t27-runtime-smoke-01/`. Refuse an existing root; never reset, resume or delete it. Parent and one claim-once worker share its ledger. Preserve success/failure/interruption evidence and do not reuse any historical trial allocation.

## Ordered operations

1. The approved parent creates the fresh root and precharges itself and its worker. Validate the source seal, then launch exactly one hidden project-Python worker with bounded output and an independent outer wall deadline.
2. Positive session: reserve one 16-start native-tree allocation before constructing its job. Verify assets, home capacity and free port **127.0.0.1:11435**; launch the exact `serve` executable with atomic job membership, suspended/hidden startup and the explicit CPU/local environment. Verify root-handle membership and the exact root's IPv4 loopback listener before HTTP.
3. Normalize only inline authored CSV `Name,Units / North,42 / South,50` with the existing CSV/T26 transform. Send one two-document embedding request and one query embedding request through the pinned client. Verify both 768-dimensional finite normalized document vectors, the query vector, matching space identity and complete counts. No answer generation, retrieval score or accuracy threshold is introduced.
4. Terminate/reap the owned tree, check zero job members and free loopback port. Start the second, separately prepaid owned tree and deliberately cancel its session after listener admission, without sending model input. Verify owned-tree teardown, global-slot release and free port again.
5. Recheck assets, retain only bounded scalar status/identity/count evidence and the ledger, then close storage and the worker. Retain runtime-home scratch as ignored temporary artifacts; do not recursively clean unknown files. Parent preserves bounded worker output and marks any failed/expired worker stopped, with native teardown unverified after hard worker termination.

## One shared allocation

| Limit | Exact package boundary |
|---|---|
| Starts | Maximum 64 including parent, worker and all native descendants/failed attempts; 2 Python starts prepaid, plus 16 per native tree (34 conservative charged starts if both phases are admitted). Failed reservations are not refunded. Kernel cumulative starts include already exited descendants. |
| Native jobs | Exactly two planned trees; eight active processes/job and a sampled guard of 16 cumulative starts/tree. Observed excess is charged, retained and stops further phases; the active cap is not a hard cumulative-start cap. |
| HTTP | At most 12 attempts for the entire package, charged before sending, including metadata/errors; positive flow normally uses 10. No retries, pull endpoints or remote URLs. |
| Wall time | 180 seconds shared from parent-ledger creation, including source/asset checks, controls and ordinary cleanup. Parent kills/reaps its owned worker on expiry; allow at most 5 seconds for that kill/wait and 2 seconds for output-thread settling. No automatic continuation. |
| Runtime session | At most 84 seconds before teardown, reserving cleanup time within the earlier 90-second answer target; owned-tree termination/wait is bounded separately. This smoke is not an end-to-end answer-latency pass. |
| Memory | Job commit ceiling is 8 GiB minus embedding worker's admission-time private commit; sampled peak-job plus current worker commit must remain at most 8 GiB, with at least 4 GiB physical availability. The extra supervising parent's private commit is not part of this job accounting; strict aggregate/physical-16-GB proof remains unverified, not silently passed. |
| Observation | Independent thread waits 100 ms between checks; a measured inter-check gap above 300 ms stops the tree. Memory, TCP and scratch limits are sampled; they cannot prevent every transient overshoot/first packet. |
| Files/output | 64,000,000 observed bytes/run root; 16,000,000 bytes and 4,096 entries/runtime home; root scan at most 10,000 entries. At most 2,000,000 cumulatively charged retained report/ledger/output bytes, including an upfront 65,536-byte worker-output reservation. Each result is at most 65,536 bytes. No model/prompt/vector dump or engine stdout capture. |
| CPU/settings | Existing provisional CPU controls (`num_gpu=0`, four threads, 2048 context, internal batch 64), 768 dimensions, distinct document/query prefixes, `truncate=false`, `keep_alive=0`. Requested CPU settings/unload are not independent execution/GPU-residency proof. |

These are the approved S1 **trial** limits and explicit measurement limitations, not new product upload/resource limits or acceptance of the runtime. Stop on asset/source/ownership mismatch, wrong listener, unexpected non-loopback owned TCP peer, expired/exhausted meter, memory/headroom/scratch/cadence failure, malformed vectors, failed cleanup or unexpected native behavior. Preserve actual counters and errors; do not weaken controls, rerun, reseal changed sources or allocate another root without a new decision. Kernel cumulative-start and filesystem guards may observe an overshoot after it occurs; retain and report it as a failure rather than a pass.

## Historical disconnected handoff - closed; do not repeat

The operator must disconnect external networking and attest to it. The flag is an operator attestation, not an automatic network-confinement test. The watcher observes TCP, not a firewall or UDP/DNS confinement; no private documents enter this smoke. The launcher never changes network settings, global installations, PATH or another service. If port 11435 is occupied, stop without killing/adopting its owner.

The operator ran the following command once from `F:\document_assistant`. It is preserved for audit and **must not be repeated**:

```powershell
.\.venv\Scripts\python.exe -m tests.evals.spikes.t27_runtime_smoke --execute-approved --offline-attested
```

The helper refuses without both flags. Read `data/t27-runtime-smoke-01/result.json`, `ledger.json` and any `parent-stop.json`; a nonzero exit/stop record is not acceptance. Do not run the command a second time. The Python worker ran and was reaped, but native Windows Job Object/model behavior remains unvalidated because S1 stopped at asset preflight; fake tests are not native evidence. After verified teardown the operator may reconnect and share the non-sensitive outcome for review. No stage transition, chat-model/OCR run, application autostart or T28 implementation is included.
