# T17-IF-L — counting-adapter primary-source review

## Outcome — 2026-11-16

Approved [IF-L package](../proposals/input-fit-adapter-review.md), proposal commit `0a3a709`. Completed12visible web calls/32explicit targets and a [concrete comparison](../proposals/input-fit-adapter-comparison.md). Recommend investigating runtime-rendered text plus a matching standalone tokenizer first, conditionally on artifact and parity validation. This is a design recommendation, not adapter selection, installation, runtime adoption or proof of exact fit.

No executable/source was changed or run as a candidate; no full tokenizer/vocabulary, wheel, weights or code archive was downloaded. No model/API/service/inference, cached prompt/template, private document/output or model-store read occurred. Existing [IF-K metadata](metadata-identity-correction-results.md) supplied the cached identities. No new application tests or benchmarks were appropriate for this documentation-only review.

## Pinned runtime evidence

The inspected v0.40.16 registration lists generation/chat/embedding and management/cloud operations but establishes no public `/api/tokenize`. Debug branches return rendered text/image count rather than an exact count; do not infer that debug rendering is load-free or non-native. Public count-only support remains unestablished. [Routes](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/server/routes.go), [request/debug types](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/api/types.go).

The runtime distinguishes Go-rendered completion from native chat-template handling. Internal `Tokenize` sends `add_special=false`; completion preprocessing can tokenize with true. Context/truncation code reserves a slot in one path; this is not a complete192-output/EOS accounting proof. Owned internal port/process access exists in source, not as an adopted public application interface. [Tagged llama-server wrapper](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/llm/llama_server.go).

Prompt construction can render using a selected renderer or the cached template; its truncation loop compares input length to context rather than proving the application's output reservation. The internal interface exposes template/tokenizer/context/process operations and requested context may be clamped to training context. [Prompt construction](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/server/prompt.go), [runtime interface](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/llm/server.go).

**Inference:** using runtime-rendered text avoids reproducing its Go template independently, but only a parity test can establish that this text and the chosen tokenizer represent the actual generation path. No assumption that debug, raw completion and normal chat are interchangeable is justified. Runtime tag/source evidence also does not attest the installed binary/vendor build by itself.

## Model-side provenance and tokenizer requirements

Qwen's publisher repository lists tokenizer/configuration assets. Its tokenizer config identifies Qwen2Tokenizer, disabled automatic BOS, explicit chat delimiters/EOS and a generation-prompt template. The file page reports last-change commit `5fee7c4ed634dc66c6e318c8ac2897b8b9154536`; that is not a frozen/hash-verified complete tokenizer asset set or proof of cached GGUF equivalence. [Publisher model](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct), [configuration](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/blob/main/tokenizer_config.json), [observed commit](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/commit/5fee7c4ed634dc66c6e318c8ac2897b8b9154536).

Nomic's configuration identifies BertTokenizer, lower-casing and CLS/SEP tokens with8192declared model maximum. Its config page reports last-change commit `541c5a6fadb4da793505a2bb4d3ee910de7f39ea`. The model card requires the task prefixes already recorded for query/document embeddings. It includes framework/custom-code examples; no permission to run repository code follows. [Configuration](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5/blob/main/tokenizer_config.json), [commit](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5/commit/541c5a6fadb4da793505a2bb4d3ee910de7f39ea), [publisher model card](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5).

The listed asset repositories were inspected as metadata only: [Qwen files](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/tree/main), [Nomic files](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5/tree/main). Neither full tokenizer payload was fetched or hashed. Model-family/name agreement does not prove normalization, special-token or token-ID parity with the cached quantized artifacts. Complete revision/artifact pinning remains an acquisition-review requirement.

## Standalone implementation candidate — not selected

PyPI lists Tokenizers0.23.3, Python>=3.10 and Windows wheels. The regular-ABI candidate observed is `tokenizers-0.23.3-cp310-abi3-win_amd64.whl`, displayed2.9MB, SHA256`1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3`. This is registry metadata, not downloaded-byte verification or a Python3.14 import test. Release date displayed:2026-10-09. [Observed release/file page](https://pypi.org/project/tokenizers/).

The observed publishing source commit is `301277072263fb3830eb66eec7e47adadf76f1dc`. Its Python project declares `huggingface_hub>=0.16.4,<3.0`, a PyO3 extension and Maturin build backend; repository license text is Apache2.0. Rust/native and hub transitive review is therefore required even for a tokenizer-only candidate. [Pinned project metadata](https://raw.githubusercontent.com/huggingface/tokenizers/301277072263fb3830eb66eec7e47adadf76f1dc/bindings/python/pyproject.toml), [license](https://raw.githubusercontent.com/huggingface/tokenizers/301277072263fb3830eb66eec7e47adadf76f1dc/LICENSE), [publisher repository](https://github.com/huggingface/tokenizers).

The project documents loading a local tokenizer file, which is a possible offline API path, not proof of this package's full outbound behavior. No cloud/hub download at runtime is acceptable. Exact hub/transitive versions, wheel payload/RECORD/notices, advisories, installation footprint and actual CPU/RAM/latency remain unreviewed/unmeasured; no source build or implicit Transformers/Torch adoption is proposed. [Observed local-file API example](https://pypi.org/project/tokenizers/).

## Gaps and decision

The source review supports comparing the routes but does not establish a working adapter. Required evidence remains: full matching tokenizer asset identities, cached-GGUF provenance/parity, actual renderer branch, special-token policy, effective usable context and output/EOS accounting. The internal route additionally lacks a demonstrated trusted endpoint handoff from the owned controller; an internal GetPort method is not an external Python integration contract. No port/log scanning or arbitrary attachment is authorized.

Prefer a later bounded **artifact/dependency review and parity-validation design** for runtime-rendered text plus a standalone tokenizer; retain the internal route as an alternative if the first cannot prove parity. Selection, exact provisioning and any native trial require explicit decisions. The comparison specifies future acceptance cases without preparing code, fixtures, runners or trial permits. G2, native notice/advisory reconciliation and16GB CPU-only/resource/format acceptance remain open.

## Accounting and verification

Fresh ignored `data/t17/input-fit-adapter-review-01/meter.json` prepaid64units(48normal/16protected),1,200seconds and2MiB local outputs before optional work. Eleven rules/spec/lock/source/closed-receipt identities were captured. All12calls/32targets were prepaid in full before research; the exact submission ledger/reference-to-URL map is persisted in `research-ledger.json`. Failed/duplicate/navigation/find requests count; provider-internal fetches/redirects/bytes/RAM are opaque. All32targets were consumed; no further research is permitted in this epoch. The first call requested a long response instead of the planned concise/medium size; the remaining11used medium. No additional calls or asset permissions were inferred from that deviation.

Research used24reserved units for12orchestration wrappers/12web invocations. Design/review/close steps share their own prepaid blocks; no adapter-only start counter or refunds. Protected capacity is only for final preservation/reporting. Final local links/diff/old hashes/elapsed/output and closed status are recorded in the meter. No application tests, vulnerability scan or runtime benchmark ran; no host /status or /compact invocation is claimed.

Eight source-review/design/status documents await separate commit approval. SPEC/AGENTS/dependency pins and all old sources/meters/model assets remain unchanged. This public-source review does not establish filesystem/outbound confinement or a kernel memory boundary.
