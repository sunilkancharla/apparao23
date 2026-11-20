# T10 — Local embedding comparison and retained trial limitations

**Date:** 2026-11-13 (Asia/Calcutta). **Status:** Approved provisioning and bounded two-model comparison complete, including the explicitly approved continuation without `/goal`. Original failure/accounting limitations are retained below. Source commit explicitly approved after result review; no runtime adoption. Combined pressure, larger coverage and disconnected-runtime validation remain future gates.

## Continuation results and recommendation

The user explicitly approved the documented additional allocation. In `data/t10/continuation-01/`, a separate persistent ledger links the original run's hash/counters and records the original actual-count uncertainty. No original result or ledger was overwritten. Three new tests first failed, then all **11 focused tests passed**, including continuation-limit persistence/no-download enforcement, native overshoot persistence without double charging, and saving the supervisor reason before job closure. The final focused suite passed **11 tests in 1.14 seconds**. Ruff formatting/lint passed before a hash-literal correction; no additional Ruff process was started after the allocation was consumed.

An initial continuation preflight stopped before native startup because the copied expected result hash contained an extra character. Comparison with the unchanged original receipt identified the transcription error. The corrected 64-character hash matches the original, and that failed helper's two starts remain charged. The next attempt verified executable/both weight hashes, checked the frozen corpus against run-01, and completed Nomic's four retrieval passes, 32 single-input calls, HTTP 400 over-limit rejection, unload and lexical control. All vectors were checked for 768 dimensions, finite components and usable norms. CPU logs and `/api/ps` confirmed zero VRAM and context 2048; no supervisor failure occurred. The owned job was closed and loopback port release verified.

| Measurement | EmbeddingGemma 300m BF16, original run | Nomic v1.5 F16, continuation |
|---|---:|---:|
| First corpus/query pass, seconds | 7.432 | 5.556 |
| Warm passes, seconds | 5.308 / 5.233 / 5.772 | 5.932 / 6.256 / 5.785 |
| Mean recall@5, every pass | 1.00 | 1.00 |
| Mean precision@5, every pass | 0.25 | 0.25 |
| 32 batch-one requests, total seconds | 5.342 | 4.630 |
| Run-wide peak native job commit, MiB | 815.62 | 462.83 |
| Model weight layer, bytes | 621,867,104 | 274,290,656 |
| Minimum available physical RAM, GiB | 7.75 | 8.26 |

Nomic evaluated 1,237 input tokens per corpus/query pass versus Gemma's 1,772; their tokenizers differ, so these are not interchangeable throughput units. Each pass has 32 documents and 12 queries in batches of four. Memory is whole native-job commit, not a per-model RSS comparison: the original run also attempted a Nomic load. Sessions/OS caches/background pressure differ. First passes are not controlled cold-cache trials. Neither the smaller weight layer nor first-pass timing proves Nomic is universally faster; its warm passes were slower on this sample.

The lexical control achieved **mean recall@5 0.9583** on the identical 12 variants. It missed one of Q03-v2's two required sources; both embedding candidates retrieved both. These closely related CSV lookup variants are a feasibility sample, not a general semantic benchmark. No generation/refusal score, supported answer probability, PDF/OCR/XLS quality, long-context robustness, 100 MB file-scale claim or persistent vector-index footprint is established. Q05/Q06 diagnostics were not implemented/scored; ambiguous/unanswerable answer behavior remains in the broader evaluation and T11A/T11/T16.

**Recommendation for later adoption review:** carry **Nomic v1.5 as the leading embedding candidate** because this small set shows equal retrieval coverage with a smaller weight layer, lower observed native-job peak and Apache 2.0 terms. Retain EmbeddingGemma as the evaluated alternative. This is a recommendation, not a runtime default or an adoption decision. T11/T12 must evaluate combined model/OCR pressure, retrieval/storage behavior and model-change reindex/version semantics; T16 must approve wider quality thresholds before G2 selection. The 16 GB CPU-only target is unchanged; neither run on this approximately 19.9 GiB host certifies strict target-capacity acceptance.

Final continuation ledger: **24/24 process starts, 82/100 loopback API calls, zero downloaded bytes**. Thirteen explicitly reserved starts include Python launcher/interpreter pairs, Ruff and the native server root; the native job observed 12 cumulative starts, of which 11 additional descendants were charged. Infrastructure PowerShell/tool-host processes are outside the experimental-child count. The result snapshot records 22 starts before the final test pair; the final meter records 24. About 200 seconds elapsed from first test-phase start to final test reservation, followed by the 1.14-second suite, within 30 minutes. Outputs measured **272,998 bytes** after analysis, below 64 MiB. There is no remaining process allowance; reproduction requires a new explicit allocation, not resetting either ledger.

The controller peaked at **40.72 MiB working set** in the continuation. No unexpected non-loopback native TCP peer was observed during sampled checks; HTTPX used only loopback with proxy inheritance disabled and cloud was disabled. This was **not an externally disconnected run or complete packet/UDP capture**. Stage 1 offline/combined validation remains required before corresponding capability/adoption claims. Historical stop cause/final actual process total from run-01 remain unknown; this successful continuation does not repair that evidence retroactively.

Ignored continuation receipts include `meter.json`, `corpus.json`, `results.json`, `post-analysis.json`, engine logs and test outputs. Result: **85,043 bytes**, SHA-256 **`2d52f981032c2ae22ae744ef50812e4193e4ec8fcd50baf079148d31f49ed3da`**. The three authored helper files and sanitized reports are reviewable; weights, keys, raw source-derived corpus/results and logs remain ignored. No packages, model assets or application features were added during this phase. Next proposed package: T11A exact chat-candidate review, with separate execution/provisioning approval.

## Original run — measured outcome and stopping point

The approved ZIP's hash matched. Its 80 entries expanded to **2,267,275,279 bytes**, with member paths/duplicates/symlinks checked. Ollama is installed at `.venv/tools/ollama/0.40.16/ollama.exe`; both pinned models' manifests and all layers were hash-verified in `data/ollama/models`. Charged download: **2,515,473,387 bytes**, including a conservative extra 1 MiB after an interrupted ledger write. No Python packages/lockfile changes, global installation, persistent PATH/service changes or user-store modifications were made.

CPP_HTTPLIB, GO, LLAMA_CPP and LLAMA_CPP_VENDORS notices were inventoried in ignored `native-notices.json`. Additional vendor/dependency terms apply; this is not complete redistribution/security certification. Gemma's custom terms remain distinct from Nomic's Apache 2.0 license. Runtime key/config state was created under the project-isolated home; keep keys/raw receipts out of Git.

Runtime version **0.40.16**, cloud-disabled logs and CPU computation were observed. Gemma's loaded-model state reported zero VRAM and context 2048. Each pass used 32 CSV-derived passages and 12 frozen variants of Q01–Q04, including Q03's two-source gold; these are not 12 independent business scenarios.

| Gemma pass | Corpus/query elapsed seconds | Mean recall@5 | Mean precision@5 |
|---|---:|---:|---:|
| First load (OS cache uncontrolled) | 7.432 | 1.00 | 0.25 |
| Warm 1 | 5.308 | 1.00 | 0.25 |
| Warm 2 | 5.233 | 1.00 | 0.25 |
| Warm 3 | 5.772 | 1.00 | 0.25 |

Each pass reported 1,772 evaluated input tokens. Eight single-input requests repeated four times took **5.342 seconds total**. The over-limit request with truncation disabled returned HTTP 400; unloading succeeded. Precision uses five returned passages and one or two required gold passages, so gold-set size limits this metric. These scores do not establish answer accuracy or broad retrieval quality.

Observed run-wide peak native job committed memory: **815.62 MiB**; peak controller working set: **40.75 MiB**; minimum available system memory: **7.75 GiB**. Committed memory and working set are different measures. This approximately 19.9 GiB host does not establish strict 16 GiB compatibility or combined chat/OCR feasibility.

Nomic's first batch ended in `httpx.ReadError`/connection reset. The supervisor closed the owned native job; port 11434 was released. **Stop cause remains unresolved:** the watchdog failed to persist its exception/reason. The last successful memory observations were within guards. Ledger: **39/40 recorded process starts, 84/200 calls**. A native-child charge could have been rejected before persisting the observed count, so final actual starts and strict 40-start compliance cannot be established. No further experimental processes were started after this gap was identified. The lexical control, scheduled after both models, was not reached. There is no comparative recommendation or completed disconnected-runtime validation. TCP-peer observations are not packet capture or proof of absent traffic.

Before inference, **8 focused tests passed (1.06 seconds)** and Ruff checks/formatting passed. Coverage included shared exhaustion, deadlines/download/memory guards, local-only client/error charging, vector validation, ledger retry/recovery, corpus/gold preservation and empty native-job accounting. A test first reproduced the Windows `PermissionError`; replacement now retries and pending charges recover conservatively. This did not cover the later watchdog-diagnostic gap. Tests were not rerun after the allowance became insufficient.

Ignored receipts: `data/t10/run-01/installation.json`, `archive-inspection.json`, `native-notices.json`, `meter.json`, `corpus.json`, `results.json`, `post-analysis.json` and engine logs. Raw result: **104,047 bytes**, SHA-256 **`5a2c9f5e6316205d162ef2bc99d6b0316deee06ee945d5cea0451c7fa8eddab3`**. Preserve original failure/meter. Only sanitized reports and the three authored evaluation files are candidates for a later approved commit.

## Approved continuation allocation — historical proposal

The original allowance could not accommodate another Python launcher/interpreter pair; its deadline could not be silently reset. The user approved the following separately recorded phase, preserving run-01 unchanged; its completed results are above:

1. Test first and fix watchdog-reason persistence and observed native-start accounting, including rejected charges, within the existing three helper files. Distinguish reserved and observed counts. This cannot reconstruct the original missing count.
2. Permit **24 additional process starts**, shared across helper/test/lint/native descendants/retries; **100 additional loopback calls**; **30 minutes from the first continuation experimental process**; **64 MiB additional outputs**. Link the new phase ledger to the original 39 recorded starts/84 calls. Polling observes native starts after creation: retain any overshoot and stop, without claiming preemptive enforcement.
3. **No downloads or dependency changes.** Reuse pinned installed assets and original CPU/context/prefix settings, 6 GiB native-job/1 GiB controller caps, 4 GiB available-memory guard, local/cloud-disabled isolation and owned-process teardown. Preserve completed Gemma measurements rather than rerunning inference.
4. Complete Nomic's four corpus/query passes, batch-one subset repetitions, over-limit and unload controls; run the lexical control on the identical frozen corpus. Compare against retained Gemma results with separate-session/cache caveats. Stop with incomplete coverage if the allocation is insufficient. Unrelated parser regressions are unnecessary for these isolated helper changes.
5. Update reports/status, review the diff and request a separate Git decision. Runtime model adoption and T11A remain separate gates.

The explicit additional approval followed [AGENTS.md](../../AGENTS.md)'s shared-budget instruction: “never silently reset an exhausted trial budget.” No future extension or runtime adoption is implied.

## Original approved package and pre-provisioning review

The remaining sections preserve the historical proposal. References below to pending approval or unverified installation describe the earlier review; the outcome above is current.

## Local inventory and limits

Ollama was not on PATH, no Ollama process was visible, and the checked per-user `AppData/Local/Programs/Ollama/ollama.exe` path was absent. Proxy-disabled HTTPX GETs to `127.0.0.1:11434/api/version` and `/api/tags` returned ConnectError, also outside the sandbox. This establishes no usable service at that endpoint, not an exhaustive installation search.

The conventional `.ollama/models` directory exists. Its older `manifests` path yielded no entries; a deeper bounded inspection found **two manifests-v2 and two metadata records** for embeddinggemma and qwen2.5:3b. The embedding weight digest matches the public candidate below. No model weight files appeared in that inspected directory tree; cached metadata alone is not proof of available weights, integrity, version compatibility or inference. Do not reuse, move, uninstall or alter anything outside the project. Any additional installation/asset locations remain unverified.

Observed F: free space outside the sandbox: **36,935,553,024 bytes (~34.4 GiB)**, a changing snapshot. The sandbox drive query returned unavailable/blank capacity, not a reliable zero-free-space result. Prior hardware inventory reports i5-8250U/4 cores/8 threads and approximately 19.9 GiB physical RAM plus MX150; the user explicitly retains the **Windows 11, 16 GB, CPU-only target**. Do not use the GPU/additional RAM as acceptance capacity. This review ran no capacity/performance test.

## Exact native Ollama artifact

Recommend the official **Ollama v0.40.16** standalone Windows x64 ZIP, released 2026-11-09, instead of the desktop installer/service. [Release API](https://api.github.com/repos/ollama/ollama/releases/tags/v0.40.16), [release page](https://github.com/ollama/ollama/releases/tag/v0.40.16), [Windows distribution documentation](https://docs.ollama.com/windows).

- Artifact: `https://github.com/ollama/ollama/releases/download/v0.40.16/ollama-windows-amd64.zip`
- Bytes: **1,618,244,995** (~1.51 GiB). SHA-256: `50fcf5ad54277f2fa5d173ebfc93bcb017adbc0c9ef2314daabc96ca9e6aa64e` (GitHub release metadata).
- Core license: [MIT at the pinned tag](https://github.com/ollama/ollama/blob/v0.40.16/LICENSE); bundled engine/GPU/native components have additional notices to inventory from the exact ZIP before execution/adoption. No Rust/Go compiler, GPU driver or optional ROCm/MLX archive is proposed. A CPU-only target does not make the published archive CPU-only or remove its bundled dependencies.
- Proposed location: `F:/document_assistant/.venv/tools/ollama/0.40.16/`; cache/archive inside `.venv/.cache/ollama/`. This is a native executable alongside the project environment, **not a Python package**. Existing Python dependencies/uv.lock need no change.
- Model store: `F:/document_assistant/data/ollama/models`; isolated process home/config/key/log/temp state under `data/ollama/runtime-home` and the run directory. Verify all generated state stays there. No writes to the existing user model store, persistent user environment/PATH or Windows services; no desktop updater installed.

Compatibility is proposed from the publisher's Windows support and x64 artifact, not verified locally. Verify archive hash before opening, constrain extracted members/paths and expanded size, inspect notices/native layout, then smoke the exact binary. Stop on unexpected native assets, execution failure, additional downloads or artifact drift. Core MIT does not by itself settle all bundled licenses/security; no complete vulnerability audit or runtime-offline claim exists yet.

## Exact embedding candidates

| Candidate | Weight format / bytes | License / reason to compare |
|---|---|---|
| embeddinggemma:300m | BF16, 307.58M metadata; **621,867,104 bytes** | Google's custom Gemma Terms, not MIT/Apache; small on-device candidate already named in SPEC |
| nomic-embed-text:v1.5 | F16, 137M metadata; **274,290,656 bytes** | Apache 2.0 per model card and packaged license; smaller English retrieval alternative |

Sources: [EmbeddingGemma publisher card](https://huggingface.co/google/embeddinggemma-300m), [Gemma terms](https://ai.google.dev/gemma/terms), [Nomic publisher card](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5), and the public Ollama registry manifests linked below. Model licensing is separate from the Ollama executable license. Preserve exact license records. Gemma has usage restrictions and redistribution obligations; trial approval must include reviewing/agreeing to its terms. No paid license is proposed and no terms acceptance is inferred from this read-only review. Later deployment/distribution needs its own license review.

Public registry identities fetched and hashed locally (no weights):

| Record | SHA-256 |
|---|---|
| [embeddinggemma:300m manifest](https://registry.ollama.ai/v2/library/embeddinggemma/manifests/300m) | `85462619ee721b466c5927d109d4cb765861907d5417b9109caebc4e614679f1` |
| EmbeddingGemma weight layer | `0800cbac9c2064dde519420e75e512a83cb360de3ad5df176185dc69652fc515` |
| EmbeddingGemma license layer | `1adbfec9dcf025cbf301c072f3847527468dcfa399da7491ee4a1c9e9f1b33e9` |
| [nomic-embed-text:v1.5 manifest](https://registry.ollama.ai/v2/library/nomic-embed-text/manifests/v1.5) | `0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f` |
| Nomic weight layer | `970aa74c0a90ef7482477cf803618e776e173c007bf957f635f1015bfcfef0e6` |
| Nomic license layer | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |

Tags are mutable. Revalidate the pinned manifest immediately before provisioning; stop for any digest/size drift and verify all downloaded layers before loading. Do not silently accept a newer tag. The ignored metadata receipt contains config/parameter digests too. Registry config `os: linux` describes the model image metadata; it is not evidence that the GGUF runs on this Windows artifact—verify actual compatibility.

EmbeddingGemma's registry parameters specify num_ctx=2048; Nomic's specify num_ctx=8192 although its library page advertises 2K. Do not silently resolve that discrepancy by assuming the larger context works. Inspect local `/api/show`, use a **common proposed 2048-token trial context**, set `truncate=false` and test over-limit rejection. Verify actual token limits/response dimensions; do not infer them from names. Model cards describe 768-dimensional embeddings; initial comparison keeps full dimensions, with no truncation/compression experiment.

Use the publisher's distinct retrieval prompts: EmbeddingGemma query `task: search result | query: ...` and document `title: none | text: ...`; Nomic query `search_query: ...` and document `search_document: ...`. Inspect pinned model/runtime handling to avoid adding prompts twice. Do not copy upstream examples using hosted Nomic APIs, `trust_remote_code`, PyTorch or SentenceTransformers: this proposal uses GGUF through local Ollama and already installed HTTPX/standard library only.

Alternative no-new-model baseline: a small deterministic lexical ranker over the same evidence helps expose obvious retrieval failures. This is a benchmark control, not a replacement for the required local embeddings. Larger models, additional quantizations and dimension reduction require another package; none is automatically selected for quality claims.

## Proposed single approval package

Approval covers the exact artifact/two pinned candidates, license review, isolated setup, necessary small test-first benchmark helpers, safe authored CSV-derived passages, startup/teardown, measurements and limits below. It does not approve chat weights/T11A inference, runtime adoption, global changes or Git commit.

### Provisioning budget and isolation

The ZIP plus two weight layers total **2,514,402,755 bytes (~2.34 GiB)**, excluding small configs/licenses/TLS overhead. Propose at most **3 GiB downloaded**, **12 GiB additional disk** (archive, native extraction, weights and temporary assets), and **90 minutes provisioning wall time**. Inspect ZIP entries before expansion; cap native extraction at 8 GiB and stop before exceeding the shared disk allowance. Do not partially install a different build or fetch optional GPU archives to fit the cap. Verify free space first; retain receipts and do not delete unrelated files. If native extraction cannot fit, return the concrete alternatives for review.

Start only the project-owned CLI server, hidden, with process-local environment (no persistent system/user changes): `OLLAMA_HOST=127.0.0.1:11434`, `OLLAMA_MODELS` at the project store, `OLLAMA_NO_CLOUD=1`, `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_MAX_LOADED_MODELS=1`. Isolate the child process's USERPROFILE/config/temp paths under project data and verify generated keys/state; do not repurpose PowerShell's HOME variable. Refuse to start if port 11434 belongs to an unrelated process. Never stop/modify another Ollama instance.

CPU settings: `CUDA_VISIBLE_DEVICES=-1`, `HIP_VISIBLE_DEVICES=-1`, `OLLAMA_VULKAN=false`, `OLLAMA_IGPU_ENABLE=false`; request `num_gpu=0`, `num_thread=4`, `num_ctx=2048`, `num_batch=64`. These are proposed experimental settings, not final defaults. Observe local process/model state (including zero VRAM/CPU processing) and fail the CPU-only gate if acceleration is used. The pinned [runtime environment definitions](https://github.com/ollama/ollama/blob/v0.40.16/envconfig/config.go), [GPU guidance](https://docs.ollama.com/gpu) and [local FAQ](https://docs.ollama.com/faq) support reviewing these controls; actual operation remains unverified.

Use one supervised process tree with a **6 GiB committed-memory cap**, controller at most **1 GiB**, one model loaded and sequential requests. Sample process tree/system memory and stop if available system memory drops below **4 GiB**, if the tree cannot be bounded, or if memory pressure prevents reliable measurements. These are initial trial safeguards, not a claim that this approximately 20 GiB host demonstrates strict 16 GiB compatibility. Reserve at least 4 GiB of the target's 16 GiB for OS headroom in the feasibility assessment and report observed application/model usage; later chat/OCR combined testing remains required.

Keep outbound content processing disabled. Provisioning can contact the named official distribution/registry endpoints and their artifact delivery redirects; model inference uses only loopback with HTTPX `trust_env=False`. No cloud model names/accounts, web-search endpoint, telemetry exporter or automatic runtime downloads. Confirm cloud-disabled logs without sensitive payload logging; inspect network/offline behavior after assets are present. Local-only settings are not by themselves proof of absent traffic.

### Benchmark definition and shared limits

Before any engine execution, implement/review **one shared run meter** covering setup/engine/runner/test/regression process starts, API calls, model loading, negative controls, retries, output and deadlines. No separate unmetered regression suite. Test budget exhaustion with mocks first; reuse no expired T07 meter. Propose at most **40 process starts**, **200 loopback API calls total** (embedding and control calls), **30 minutes benchmark wall time**, **120 seconds/request or remaining global time**, and **256 MiB benchmark outputs**. Engine subprocesses count, not just the Python wrapper. Fail closed on any unmetered child or budget exhaustion; stop only this package's processes and retain failures. Provisioning transfers have the separate network/time bounds above.

Corpus proposal: at most **32 deterministic English passages** derived locally from the already approved CSV sample/fixture definitions, carrying original dataset/document identity, record/column/header and physical-line anchors. Freeze selected source/definition hashes and required passage/query IDs before running. Preserve raw values and do not invent units/causes. These are internal JSON evidence records, not reintroducing TXT file support. No PDF/OCR/XLSX/XLS serialization or new parser is needed for this fixed-evidence embedding spike.

Query proposal: **12 frozen retrieval queries**, consisting of existing answerable CSV questions and reviewed wording variants anchored to Q01–Q04; include Q03's two-source gold. Record original IDs and variant lineage; do not change original question gold or claim 12 independent business scenarios. Evaluate Q05 ambiguity and Q06 absent-cause relevance only as diagnostics, not as embedding-model answer/refusal scores. Freeze the required set; unavailable evidence fails readiness instead of shrinking the denominator.

For each model: one first-load corpus/query pass plus three warm repetitions using batches of four; compare batch-one throughput on an eight-input subset with the same repetitions if the shared call/time budget permits. Full proposed schedule is 88 batched calls plus 64 single-input calls across both models, leaving 48 of 200 for bounded setup/negative/unload observations. All controls and failed calls count. If the frozen schedule would not fit after startup checks, stop and report incomplete coverage rather than silently omitting it. First load is not a guaranteed cold OS cache; unload/model-switch and repeated timings must be explicit.

Measure validated finite vector dimensions/norms, prefix consistency, over-limit input behavior, document/query batch throughput, load/end-to-end timing and peak process/system pressure. Use deterministic cosine reference search and report recall@5/precision@5 with gold source anchors, including both sources for multi-file questions; compare the lexical control. Report exact counts and N/A where applicable. Track raw failures/variation; this tiny sample is not general retrieval accuracy, user-facing correctness probability, or generation quality. Do not enable global question scoring flags or select a runtime model automatically.

Keep helpers small (at most three T10 evaluation files), version only safe definitions/code/sanitized reports, and leave originals, weights, model state, embeddings and raw prompts/results ignored under project data. Routine budget/client tests mock Ollama. After local/offline smoke, terminate only the owned server tree and confirm the loopback port is released. T11A will separately review exact chat candidates/artifacts; T11 later measures combined chat/OCR/embedding pressure before adoption.

## Review outcome and remaining gates

Recommend this bounded two-candidate comparison with the standalone native distribution. No packages need adding to pyproject/uv.lock. The material decisions for the user are the approximately **2.34 GiB payload**, **12 GiB disk allowance**, project-contained native/model locations and **EmbeddingGemma's custom license terms**. If those terms are unwanted, explicitly revise the candidate set; do not silently skip the SPEC-named candidate or substitute a cloud service. The read-only review cannot rate speed/quality or choose a winner. T10 remains in progress until approved provisioning and actual measurements, followed by result/Git review and eventual G2 adoption.
