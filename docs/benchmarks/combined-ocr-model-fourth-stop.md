# Combined-04 stop: sampling interval exceeded

Recorded 2026-11-14 (Asia/Calcutta), following the user-operated disconnected run of preparation commit `7ca4ee3`. Only sanitized summary, meter and scalar resource-failure receipt were inspected. No raw documents, OCR, prompts, vectors, answers, model logs or private error receipts were opened. No rerun occurred.

## Confirmed result

All four deadline/memory sentinel controls were checked: one of each per OCR engine. The trial stopped during `frozen-corpus-embeddings`, with two embedding attempts and zero scored chat responses. The supervisor reported `ResourceBoundary: Resource boundary: sampling_gap`. The downstream request ended with ReadError after the supervisor stopped the owned server; it is not evidence of external network failure.

The durable resource receipt and final summary contain the same failed measurement packet. The only recorded violation is sampling_gap:

| Measurement | Recorded value | Guard |
|---|---|---|
| Sampling interval | 259.0546 ms | At most 250 ms |
| Available physical RAM | 8.9257 GiB | At least 4 GiB |
| Controller private memory | 29.5156 MiB | At most 512 MiB |
| Owned private memory | 384.2969 MiB | At most 8 GiB |
| Peak job commit | 384.7227 MiB | At most 8 GiB |

The interval exceeded its allowance by 9.0546 ms. This identifies the guard that stopped combined-04, not why the monitoring interval grew. It does not establish that loaded models or the full overlap matrix would fit memory, or retrospectively identify combined-03's lost failure reading. The low retained memory figures describe this early phase only.

Teardown verified true: zero active owned children, owned process reaped, port released, server exit code 125. The user may reconnect under the runner's explicit confirmation. Preserve the started ledger at **60/160 reservations**, **seven API attempts**, **five explicit native roots**, **nine extra native descendants**, **14 observed native processes**. Categories: preparation28, report16, controller3, OCR4, supervisor9, cleanup0. No reset/reseal/retry or reuse of the closed diagnostic allocations.

## Interpretation and next decision

The diagnostics repair achieved its narrow purpose: a specific guard and violating scalar reading survived shutdown. The combined performance/quality evaluation remains incomplete; no chat or OCR/chat overlap measurements exist from this run. T09/T11 acceptance, physical-16-GB feasibility and runtime adoption remain open.

Repeating the unchanged trial can hit the same monitoring boundary. Before another trial, review the monitoring contract: compare preserving the strict 250-ms stop with a separately proposed change that distinguishes target sampling cadence from a hard maximum gap. Any proposed limit must state the resulting blind interval for sampled headroom/controller checks, retain kernel aggregate/worker caps and fail-closed ownership/network/cleanup controls, and include fake timing regressions. Scheduling or monitor-work overhead is a hypothesis, not an established cause. No new timing value, code repair, timing study or native allocation is approved by this results note.

Result documentation is saved for review. Its Git commit requires explicit approval. No application implementation, dependency change, model/OCR adoption or stage transition follows from this stop.
