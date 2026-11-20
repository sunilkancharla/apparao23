# T30-N1 — One disconnected Qwen generation/persistence smoke

**Status: approved, prepared and source-sealed; not executed.** The user explicitly approved the reviewed 23-file T30 source/status/handoff commit and this exact T30-N1 package on 2026-11-20. No further project approval is needed for its one operator-disconnected run. T30 implementation is routine-verified; actual chat-purpose runtime/client verification remains pending. The [35-file seal](t30-model-smoke-seal.json) fixes all application sources, `pyproject.toml`/`uv.lock`, this helper and the existing generic T27 meter/supervisor it imports. Importing those utilities does not reopen S1/S2 or use their roots/ledgers/seals. Its allocation and stop conditions below are unchanged.

Use existing project Python/HTTPX, Ollama **0.40.16**, executable SHA256 `4ccefcbfecc50fb6526471adabbc20869dd614e29e351120b15083cb174b0b8a`, and selected **qwen2.5:1.5b-instruct-q4_K_M**, manifest SHA256 `65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b`. The installed v2 manifest matches that identity during preparation. Full executable/manifest/blob size/hash/ancestry checks run before native launch and after generation. No download, install, model replacement, wrapper/build change, OCR, private corpus or new adoption is included.

## Exact work and success gate

1. Create fresh ignored `data/t30-model-01/`; refuse any existing root. Parent and one token-checked/claim-once worker share a fresh `T30-N1` ledger. Both verify the new source seal.
2. Use only inline `Name,Units / North,42 / South,50` in the actual CSV upload/extraction/index store. Index vectors and retrieval are explicitly authored fixture seams; there is no Nomic inference or sqlite-vec DLL load in this run. Actual source/extraction/index metadata and original rechecks remain in the persistence boundary.
3. Provision only a private staging home below that fixture store. Start **one owned Qwen Ollama tree**, verify its exact loopback listener and pinned model, then use actual `ChatService`/`ChatModel` to ask `How many North units?` against the North row's supplied ID `ev_native`.
4. Apply recorded CPU/four-thread/2048-context/64-batch settings, `num_predict=192`, temperature 0.2/top_p 0.9/top_k 20/repeat_penalty 1/seed 42, JSON mode, `stream=false`, `keep_alive=0`. Require complete `done/stop` termination, at most 192 observed generated tokens, valid typed claims and only supplied citation IDs. Require `answered` with the standalone value 42 in at least one claim. This is a smoke-case assertion, not a semantic quality score or proof that every claim is correct.
5. Verify native teardown/free port, post-run assets and complete saved exchange. Close/reopen the fixture store and require the saved answer to match exactly. Retain only bounded scalar result/ledger/output receipts plus ignored fixture scratch. No raw model response or evidence text is printed to receipts.

## Separate finite allocation

At most **64 starts / 12 HTTP attempts / 180 seconds shared parent deadline**, including source/asset checks, controls and ordinary cleanup. Prepay two Python starts plus 16 for the single planned native tree (**18 conservative starts** when admitted); count failed starts and exited native descendants, with no refunds/retry. Positive flow normally uses five HTTP requests (version/tags twice and one chat request). No cancellation tree, second model question or automatic retry is included.

Reuse the reviewed independent parent supervisor: at most 65,536 retained worker-output bytes, 2,000,000 cumulatively charged ledger/result/output bytes and 64,000,000 observed run-root bytes. One runtime home has sampled 16,000,000-byte/4,096-entry guards. Worker result is a fixed small scalar object; no answer/vector dump. Existing-root, source/asset/version/listener/ownership, vector/output/termination, persistence, deadline/clock/output/scratch/resource or uncertain-cleanup failure stops acceptance and preserves the actual ledger. Never reset/resume/delete/reseal a consumed root or allocate a replacement without a new decision.

Native controls remain eight active/16 cumulative sampled job starts, worker-private plus peak-job commit at most 8 GiB, at least 4 GiB available physical RAM, 100-ms observation waits and a stop on measured gaps above 300 ms. Session deadline is at most 84 seconds; complete answer operation is cooperatively bounded to 90 seconds. Parent supervises the worker independently, allowing at most five seconds for kill/wait and two seconds for output settling on forced termination. These trial controls and requested CPU options do not prove strict aggregate RAM, GPU residency, physical-16-GB performance or confinement. The outer parent's private memory remains outside job accounting; sampled guards can observe overshoot after it occurs. Preserve those limitations, exact-input-fit uncertainty and same-account/native-trust assumptions.

A pass establishes only this chat-purpose owned runtime/request/structured-result/persistence bridge with authored retrieval. It does not establish combined real Nomic/sqlite-vec/Qwen retrieval quality, prompt-injection resistance of the model, quote correctness, final support scoring, warm-answer latency, full-scale memory, browser readiness or Stage 1 acceptance. All prior allocations remain closed and unchanged.

## Approved operator handoff — run once while disconnected

Save/read these instructions while connected. The package is approved. Disconnect external networking and run **once** locally:

```powershell
cd F:\document_assistant
.\.venv\Scripts\python.exe -m tests.evals.spikes.t30_model_smoke --execute-approved --offline-attested
```

The flags attest to already granted approval and actual disconnection; they do not switch networking off. No online reply while disconnected is required. Read local `data/t30-model-01/ledger.json` for counters and, after the command returns, `result.json`, `worker-output.txt` and any `parent-stop.json`. Keep the ledger's worker token private. A stop can have incomplete receipts; preserve the root and do not retry even if it fails.

Reconnect after the command returns and say **“T30-N1 finished; please inspect the results.”** I can read the local files directly. Review of those receipts precedes native T30 acceptance/T31 progression; this package alone does not approve another source commit or stage transition.
