# T27-S2 — Approved disconnected smoke handoff

**Status: executed, passed and closed, 2026-11-20.** The operator completed R1-D of the approved [T27-R1/S2 package](t27-preflight-correction.md), then requested review. [S2 results](../benchmarks/t27-runtime-smoke-02.md): two document/one query vectors, positive/cancellation cleanup and released port; final 34 charged starts, 10 calls, no stop. Preserve its root/receipts/seal; **the command below is historical and must not be repeated**. The operator supplied offline attestation locally and reconnected afterward; no offline chat confirmation was needed.

## Fixed identity and allocation

The [S2 source seal](t27-runtime-smoke-02-seal.json) pins 25 application/helper/configuration files and still matches after the run. Both parent and worker checked it before native construction. The preserved ignored root is **`data/t27-runtime-smoke-02/`**; its existence prevents reuse. S1 remains closed, with its original root/receipts/seal unchanged. Default/S1 execution is refused; S2's explicit package selected its distinct ledger/root. There is no root/port/model override in the historical command.

Use existing project Python/HTTPX and `.venv/tools/ollama/0.40.16/ollama.exe`, SHA256 `4ccefcbfecc50fb6526471adabbc20869dd614e29e351120b15083cb174b0b8a`. Only existing Nomic `nomic-embed-text:v1.5`, manifest SHA256 `0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f`, full 768 dimensions and the approved CPU/four-thread/2048-context/64-batch/prefix settings are used. Real preflight rehashes approved executable, manifest and config/layers with size/ancestry checks. No install, download, model substitution, private corpus, OCR or answer generation is included.

The fresh S2 native allocation is independent of closed S1 and routine R1 tests: **64 starts, 12 HTTP attempts, 180 seconds shared parent deadline plus at most 5 seconds kill/wait and 2 seconds output settling**, 2,000,000 retained charged output/ledger bytes and 64,000,000 observed run-root bytes. Two Python starts are prepaid and 16 starts per native tree; exactly one positive tree and one cancellation tree are planned, with no retries/refunds. Eight active/16 cumulative sampled tree guards, worker-private-plus-peak-job at most 8 GiB and at least 4 GiB physical availability, 100-ms observation waits/300-ms gap stop, and sampled 16,000,000-byte/4,096-entry homes carry forward unchanged. The outer supervisor's private memory is not included in job accounting; strict aggregate/physical-16-GB proof remains unverified. Sampled TCP/files/memory checks do not guarantee confinement or prevent every transient overshoot.

The positive flow embeds the two authored CSV rows `Name,Units / North,42 / South,50` and one query, validating finite normalized 768-dimensional vectors and matching space IDs. It requires owned listener/job membership and verified zero-member teardown/free port. A second owned session is deliberately cancelled after listener admission and must also release ownership, admission and port. Port **127.0.0.1:11435** must be free; never kill/adopt an unrelated service to make it available. Stop on any asset/source/ownership/resource/deadline/output/cleanup mismatch; preserve receipts and do not retry, reset, reseal or delete a run root. Full controls/stop conditions are in the approved R1 package and the [historical S1 control description](t27-runtime-smoke.md); the S1 command is closed and must not be used.

## Historical one-run instructions — closed; do not repeat

The operator followed the instructions below once. They are retained for audit, not for another execution:

```powershell
cd F:\document_assistant
.\.venv\Scripts\python.exe -m tests.evals.spikes.t27_runtime_smoke --package T27-S2 --execute-approved --offline-attested
```

The flags attest to the already granted approval and your actual disconnection; they do not switch networking off. The command does not alter network settings or require online chat. It prints a local passed/failed summary when it finishes. Its parent supervises the worker under the deadline above; this is not an end-to-end answer-latency claim.

To inspect progress while it runs, use a second local PowerShell window:

```powershell
Get-Content F:\document_assistant\data\t27-runtime-smoke-02\ledger.json
```

Read counters locally; do not edit the ledger or publish its worker token. If the file is briefly being written, wait and read it again without restarting the smoke. Once the original command returns, read the result and any parent stop record:

```powershell
Get-Content F:\document_assistant\data\t27-runtime-smoke-02\result.json
Get-Content F:\document_assistant\data\t27-runtime-smoke-02\parent-stop.json -ErrorAction SilentlyContinue
```

A failure before worker handoff can leave a stopped ledger without `result.json`; preserve the directory and terminal message. A failure after worker handoff can have `parent-stop.json`; `not_started` means corroborated asset failure before native admission, while `unverified` requires cleanup review. Neither a nonzero exit nor a stop record is acceptance. **Run only once, even if it fails.**

The operator reconnected and requested inspection. [Receipt review](../benchmarks/t27-runtime-smoke-02.md) confirms bounded T27 native success; T28 indexing is next and unstarted. No screenshot, token or online reply during disconnection was needed. This result does not establish final resource/quality acceptance, runtime autostart, application readiness or a stage transition.
