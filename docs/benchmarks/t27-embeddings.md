# T27 — Pinned local embedding client and synthetic verification

Date: 2026-11-20 (Asia/Calcutta). The user's instruction to proceed to the next step after T26 commit `f7f0a90` authorizes T27 client implementation against the approved G2 component selection. Transport (A), pinned embedding/vector behavior (B), and synthetic loopback/review (C) were implemented sequentially using the previously verified repository implementation, TDD, security, quality and documentation workflows. The user explicitly approved the reviewed T27 client closeout and ten-file Git commit on 2026-11-20. **Production owned-service integration and the separately authorized actual-model smoke remain unimplemented/unrun.** T27 is not marked fully complete, T28 is unstarted and CP10 remains open.

## Implemented client boundary

`app/ollama.py` adds an async HTTPX session bound to a validated integer port at literal `127.0.0.1`. Inherited proxy settings are disabled, redirects are refused, and the route allowlist is limited to version/tags reads and the embed request. There is no DNS hostname, configurable remote URL, pull/install route, fallback model or process launch. The client never attaches merely because a port answers.

Every exchange checks a trusted caller-supplied `ownership_check` before sending and after receiving. An omitted check, a non-None return, or an expected ownership failure refuses access as `OLLAMA_OWNERSHIP_UNVERIFIED`. The callback must establish the caller's pinned owned process/model store and active shared heavy-job lease. **The callback is an integration seam, not evidence that production process ownership or global scheduling has been implemented.** Only test owners are supplied in this task. There is no change to application startup, storage, browser routes, health or readiness.

| Boundary | Implementation |
|---|---|
| Serialized request | At most 65,536 UTF-8 bytes |
| Retained response | At most 262,144 observed bytes, checked while reading as well as against a declared Content-Length |
| Wire format | Uncompressed UTF-8 JSON object; reject duplicate keys, invalid numeric constants, malformed JSON, unexpected media/encoding or an error object |
| HTTP status | Only 200 succeeds; 400 input rejection, 404 missing model and other statuses map to fixed safe codes |
| Time | Default 90 seconds, configurable only within `(0,90]`; cooperative deadlines cover each exchange and the entire embedding batch, including identity checks |
| Retry/parallel work | No automatic retry; one embedder refuses busy calls rather than queueing; transport keeps at most one connection |

These are internal request/work bounds, not changes to approved upload/count/storage limits or evidence of target-machine performance. Reading/parsing and trusted synchronous owner checks must remain bounded/cooperative. HTTP timeout/cancellation does not kill native inference, prove model unload or stop descendants; the future owner must coordinate cancellation/termination and retain honest pending state. Errors expose only fixed codes, without upstream text, source content, paths or private URLs. This backend seam is not a browser API or a document permission check.

## Pinned embedding space and output

`app/retrieval/embeddings.py` adds `Embedder.documents(chunks)` and `Embedder.query(text, query_id)`. A document batch accepts one through eight T26 `Chunk` values, rejects duplicate chunk IDs, and preserves order/source IDs/text hashes. The query path accepts nonblank valid Unicode within the approved provisional 512 UTF-8 byte guard. It never trims, truncates or silently rewrites the question. The caller owns query IDs and document eligibility.

| Identity/setting | Client value |
|---|---|
| Runtime | Ollama `0.40.16` |
| Model | `nomic-embed-text:v1.5` |
| Manifest SHA256 | `0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f` (reused from existing diagnostics inventory) |
| Dimensions | 768, without dimension reduction |
| Document / query prefixes | `search_document: ` / `search_query: `, prepended once to unchanged input |
| Provisional options | `num_gpu: 0`, `num_thread: 4`, `num_ctx: 2048`, `num_batch: 64` |
| Overflow | `truncate: false`; any explicit non-false `truncated` response flag is refused |
| Retention request | `keep_alive: 0` requests release after the batch; actual unload/warm latency is not verified |
| Vector representation | All 768 finite numeric components, stable local L2 normalization `l2-f64-1`; reject booleans/strings, zero vectors and unrepresentable numbers |

Runtime version and exact selected tag/digest are checked before evidence is sent and again before a batch is returned. Duplicate matching tags, wrong digest, absent model or changed post-request identity refuse results. These HTTP observations are not executable/model-layer hash verification, atomic protection against hostile tag swapping, or a substitute for an owned immutable model store. The future owner must provide those prerequisites; current G2/T17 accepted trust/input-fit/resource limitations are unchanged.

Immutable `EmbeddingBatch` and `Embedding` dataclasses return the complete ordered batch with kind, source IDs, unprefixed text hashes, vectors, model/digest/runtime/dimension metadata, normalization version and a deterministic `space_id`. The space hash covers the paired prefixes, artifact/runtime identity, dimensions, options and normalization, so future indexes can reject incompatible spaces. Per-input vectors are checked before any batch is returned; a bad later vector cannot publish a successful prefix. Scaling before computing the norm avoids overflow for large finite components and loss of normalization for subnormals. No vectors/chunks are persisted yet.

Optional `prompt_eval_count` must be a nonnegative integer or absent. It records completed work only. `truncate: false` and byte guards do not establish exact pre-request token fit or prove an unreported truncation did not occur. No unsupported count-only endpoint, tokenizer dependency, input-fit investigation restart or silent alternative model is introduced.

## Verification and review

Initial tests failed because `app.ollama` did not exist, then the first eight embedding cases passed after implementation. Additional negative controls exposed acceptance of a reported truncation flag and an unsanitized surrogate-encoding error; both were corrected. Numeric controls cover huge integer conversion, NaN/infinity/boolean/string/zero/wrong-dimension vectors and extreme finite normalization. One initially oversized integer fixture hit the transport-size cap; it was narrowed to a single huge component to exercise vector validation within that cap. Focused Ruff findings were corrected before final checks.

There are **56 new cases**: **54 unit cases** across `test_embeddings.py`/`test_ollama.py` and **two integration cases** in `test_local_embeddings.py`. They cover model/runtime/digest/prefix identity, source ordering/hash linkage, invalid input, changed post-inference tags, complete-batch refusal, response size/media/JSON/status failures, blocked remote routes/redirects, absent/lost ownership, deadlines, busy refusal, cancellation and reusability.

The integration fixture binds a synthetic HTTP server to an OS-selected loopback port in the pytest controller. It embeds two authored CSV-record chunks and one query through actual HTTPX sockets, with an unusable inherited proxy and empty NO_PROXY, and verifies the document/query payloads and matching spaces. Another test confirms a running unowned synthetic server receives zero requests. Each fixture shuts down/closes its server and joins its thread. **This is real HTTP transport testing with fake vectors, not actual Ollama/model integration, quality evaluation, CPU/native memory proof or strict disconnected-runtime acceptance.** No private document or historical sample was read.

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest tests/unit/test_embeddings.py tests/unit/test_ollama.py tests/integration/test_local_embeddings.py -q -rP -p no:cacheprovider
.\.venv\Scripts\python.exe -m pytest -q -rP -p no:cacheprovider
.\.venv\Scripts\ruff.exe check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration
.\.venv\Scripts\ruff.exe format --check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration
git diff --check
```

Focused result: **56 passed in 1.07 seconds**, controller only / zero retained factory-artifact or child-output bytes. Final full suite: **329 passed, 1 skipped, 1 warning in 38.34 seconds**. The skip remains the Windows symlink-permission control; the warning remains Starlette's HTTPX test-client deprecation. Ruff lint passed and **39 files** passed formatting. Shared final suite meter: **13/64 starts; 263,388/2,000,000 retained factory-artifact/child-output bytes**, under the existing 120-second admission/child boundary. All prior regression/control children use the same meter; the new synthetic servers add threads, not child processes. This does not meter every HTTP buffer/database byte or authorize a new native run.

Quality/security review temporarily inverted the model-digest equality guard. The wrong-digest control failed because the mutant accepted it; the original source was restored byte-for-byte, matching Git object hash `bd27cfaa0b38d8634d12d1a00a3db827fbf3b5bc`. The final full suite ran after restoration. Review traced trusted ownership versus transport identity, proxy/redirect isolation, response bounds, safe errors, source/version linkage, stable normalization, cancellation and all-or-nothing batches. There is no outstanding required finding in this client subset; production owner/global-lease/native termination remain explicit unimplemented prerequisites.

## Public references and remaining gates

The [Ollama embed API](https://docs.ollama.com/api/embed) documents text-array input, the truncate option and returned vectors/counts. The [tags API](https://docs.ollama.com/api/tags) documents model names/digests. The [Nomic publisher card](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) documents the distinct retrieval prefixes and 768-dimensional representation. Version reads/options also match the retained T10/T11 ordinary API calls; historical trial helpers were inspected, never executed. Public documentation requests included only public project/model names. No document, prompt, embedding or answer content was sent externally; no download/install/model execution occurred.

Before live embedding work, implement and verify the production owned-service lifecycle and shared heavy-job lease, including pinned local assets, collision refusal, abandoned-work cleanup and teardown. Then obtain the separately scoped actual-model smoke authorization with finite shared start/time/output/resource boundaries. **No such native package was prepared or authorized here, and no historical trial ledger may be reused.** The client alone does not close that runtime gate or make the app ready. No new model/dependency/architecture selection, target-machine proof or stage transition is claimed. T28 and CP10 remain open.

Ten reviewable files: the two client modules, three test files, README, PLAN, TODO, contracts and this report. Complete readable tracked/new-file diff: `data/reviews/t27.diff`. Generated review/test artifacts stay ignored; unrelated untracked user files are preserved. The approved commit includes only these ten reviewed files; runtime/generated artifacts and unrelated user files are excluded. Only closeout documentation changed after the final suite. `/status` and `/compact` are not exposed in this host and were not run. No session checkpoint or session summary was created/updated.
