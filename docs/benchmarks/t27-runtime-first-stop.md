# T27-S1 — Preflight stop and model-store path diagnosis

Date: 2026-11-20 (Asia/Calcutta). The operator ran the approved disconnected T27-S1 command and requested review of its local results. This review reads existing receipts, sealed code and selected public-asset identities/metadata only. It does not rerun the smoke, change its root/ledger/seal, start a service, download/install assets or implement a repair. The repository quality/documentation workflows were applied to the review. T27/CP10 remain open; T28 is not authorized by this failed run.

## Outcome

`data/t27-runtime-smoke-01/result.json` reports **failed / `OLLAMA_ASSET_UNAVAILABLE`**. The final ledger is stopped, with **2 charged Python starts, 0 HTTP calls, an empty native-observed map, and 69,497/2,000,000 retained charged bytes**. The two starts cover the parent and worker; no 16-start native-tree reservation was admitted. Neither the two-document embedding request nor the query nor cancellation-control tree ran. No vector/model/CPU/resource/offline acceptance result was produced.

The worker output repeats the same fixed failure code. `parent-stop.json` confirms `worker_reaped: true` but labels native teardown `unverified`. That generic field is written for every nonzero worker result. Here, sealed control flow and the empty native reservation map place failure in `_verify_assets()` before the native process factory: **no Ollama process was launched by this run**. The field is not evidence of an orphaned model process. Future reporting should distinguish a proven pre-launch stop from uncertain teardown after a native launch/hard worker kill.

Source verification still matches the 25-file S1 seal. The run root contains the initialized SQLite/upload-store scaffolding and empty positive-session profile directories; it is preserved without cleanup/reset. A stopped S1 allocation is closed even though most of its allowance was unused.

## Confirmed cause

`app/diagnostics.py::_model()` constructs:

```text
data/ollama/models/manifests/registry.ollama.ai/library/nomic-embed-text/v1.5
```

That file is absent. The installed selected-runtime layout instead contains:

```text
data/ollama/models/manifests-v2/ollama.com/library/nomic-embed-text/v1.5
```

The actual 708-byte manifest hashes to the approved identity `0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f`. The 41,268,104-byte executable hashes to approved SHA256 `4ccefcbfecc50fb6526471adabbc20869dd614e29e351120b15083cb174b0b8a`. The existing historical helper `tests/evals/spikes/combined_trial.py` already uses the installed `manifests-v2/ollama.com/library` layout; it was inspected, not executed.

| Referenced Nomic artifact | Expected bytes | Observed bytes |
|---|---:|---:|
| Config | 420 | 420 |
| Model weight | 274,290,656 | 274,290,656 |
| License | 11,357 | 11,357 |
| Parameters | 17 | 17 |

All four blobs are present at the expected sizes. Their full contents were not rehashed during this review; the fresh corrected preflight must verify them before a later native launch. The evidence identifies a verifier path bug, not a reason to select/download another model. The same canonical diagnostic function serves other selected-model checks, so its correction needs coverage for both selected model identities without changing their pins. Fake tests failed to expose this real-layout mismatch because runtime-owner tests injected an asset verifier.

## Preserved receipts

Raw receipts stay local and ignored. The worker correlation token is excluded from this report.

| Receipt | Bytes | SHA256 |
|---|---:|---|
| result.json | 288 | `e8d1a8867f9f8e0ad876d14de53d490974affb540705f0c4f631ac1c34d9ee32` |
| parent-stop.json | 76 | `5246a329807eb87f0fed84a836f44290027e309d8a3bea6b4ace867c240f8408` |
| ledger.json | 200 | `ca0c962816b60355b15344f8e932fc483e678faf83e9e429ef53a3e32f74e76f` |
| worker-output.txt | 79 | `0bd240c8918df9163acc8ef5dc90d8bac86666caf722a8b11225ae6b90897573` |
| worker.claim | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## Recommended next step

Proceed with the approved [focused T27-R1 correction and fresh S2 package](../proposals/t27-preflight-correction.md): reproduce the installed layout in a small fixture, correct version-specific lookup without weakening hashes, expose the safe failing component, distinguish pre-launch status, then validate one new sealed S2 run under a fresh explicit allocation. Preserve S1 exactly. T28 indexing should follow successful native ownership/embedding/cancellation evidence rather than treating this preflight failure as a model test.

This is a read-only results review with documentation/consistency checks; no application tests or inference were run for it. The prior **365 passing tests** remain fake/routine evidence from implementation, not a passing S1 result. The results review itself authorized no repair/native execution. The user subsequently explicitly approved T27-R1/S2 and the six-document review/proposal commit on 2026-11-20; execution must remain within its allocations and operator-disconnected handoff. Readable diff: `data/reviews/t27-runtime-first-stop.diff`. No session checkpoint/summary or unrelated user file was changed.
