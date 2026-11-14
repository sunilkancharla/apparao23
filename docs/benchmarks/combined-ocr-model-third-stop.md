# Combined-03 stop: resource boundary during corpus embeddings

Recorded 2026-11-14 (Asia/Calcutta). Executed preparation source is committed as `d9a2792`; its source/launcher hashes matched the existing seal before commit. Only sanitized summary, meter, receipt names and memory observations were inspected. No raw corpus, prompts, vectors, OCR, answers or private error receipt was read into tools.

All four timeout/memory controls completed and were checked. Execution reached `frozen-corpus-embeddings`, recording three embedding attempts and zero scored chat responses. It stopped with ReadError after the supervisor reported `RuntimeError: Memory/headroom/sampling boundary`. This indicates the resource supervisor stopped owned inference; the read failure is a downstream connection symptom, not evidence of a new external-network fault.

Teardown was verified: zero active owned children, owned process reaped, trial port released. Preserve combined-03 at56/160 reservations, eight API attempts, five explicit native roots and nine extra observed descendants. Do not reset/reseal/rerun this started ledger. Prior stopped runs and fake diagnostic/repair epochs remain separate.

## What the retained observations establish

There are66 saved successful observations. Minimum free physical RAM was8.9483GiB; maximum controller private memory30.129MiB, owned private memory0.37677GiB and kernel peak job commit0.37677GiB. Maximum retained sampling gap was0.18481s. These retained readings are within their approved limits; they are not the reading that caused the stop.

The observer calls check_resources before appending an observation. A failed observation is therefore lost, while the exception combines low free RAM, controller/aggregate memory and >0.25s sampling-gap failures into one generic message. Consequently the exact trigger is unknown. A scheduling gap is plausible given the retained memory headroom, but cannot be confirmed; a sudden failed memory reading is not excluded by earlier good samples. Do not alter caps or polling policy based on this incomplete record.

## Proposed next step, not approved

Use a bounded24-start/10-minute fake-only diagnostic/reporting repair to preserve the violating scalar reading and distinguish each resource check before owned teardown. Verify all failure categories, exact threshold edges, durable failed-sample capture and unchanged guard/cleanup behavior; no new OCR/model inference, download, installation, threshold change or native continuation. Present its evidence before considering another offline package or a sampling-policy decision.

Preparation commit approval covered the eight reviewed preparation files only. This results note and updated stopped-state documentation are uncommitted pending their own gate; no runtime component is adopted.
