# T11A — Early CPU chat feasibility review and trial proposal

**Date:** 2026-11-13 (Asia/Calcutta). **Status:** Approved continuation completed all 13 missing/interrupted Qwen3 requests. Across both epochs, **all 96 planned slots have completed/schema-scope-valid results**, with **97 total attempts** retaining the original timeout. Final 27 tests and Ruff pass. Cleanup independently verified; semantic answer/citation review remains pending. Source/documentation commit explicitly approved on 2026-11-13; semantic review and runtime adoption remain separate gates. T10 is committed in `55d68f6`.

## User review follow-up

User review, 2026-11-13: in response to the local factual/citation review request, the user replied “I am good with it”. Record qualitative acceptance of the reviewed outputs; no per-answer grades, claim counts or citation-support measurements were supplied. Numeric semantic metrics remain unscored; this does not select a runtime model or waive PDF, strict-16-GB, combined OCR/model or offline acceptance. T11A source/evaluation documentation is committed in 0872c22.

Earlier pending-review statements below describe the state before this reply. Structured semantic scores remain unfilled.

## Completed continuation and combined observations

The user explicitly approved the documented **32-start/40-call/25-minute, no-download** continuation. New linked receipts are under `data/t11a/continuation-01/`; the original result, cases, ledger, failed attempt and source snapshot were not overwritten. The installed executable and every pinned Qwen3 layer were hash-verified again. There were **zero downloaded bytes and no dependency/environment/global changes**.

The harness verified the original result/case hashes and required byte-identical request hashes for every follow-up case. It retried **only C12 repetition 2**, then executed **all 12 repetition-3 Qwen3 cases**. All 13 completed successfully and passed schema/source-column membership checks. Qwen2.5 was not rerun. There are now 48 completed slots per model; Qwen3 has 49 retained attempts because its original interrupted request remains failed. New-session timing does not replace the missing original timeout duration.

| Completed-response observation | Qwen2.5 1.5B | Qwen3 1.7B |
|---|---:|---:|
| Completed planned slots / retained attempts | 48 / 48 | 48 / 49 |
| Full-response median, seconds | 10.566 | 14.211 |
| Full-response range, seconds | 2.914–20.933 | 3.068–33.420 |
| First answer-content fragment median, seconds | 0.379 | 3.026 |
| Weighted generation tokens/second | 10.29 | 8.29 |
| Warm C01 response seconds | 9.813 / 7.752 / 7.392 | 12.237 / 11.663 / 11.395 |

These pool completed responses across the retained epochs; the Qwen3 numbers include 13 follow-up responses in a different session/cache/background state. The first new request was C12, **15.528 seconds**, not a repeated cold C01 test. The continuation's own response median was **14.297 seconds**. The original timeout is excluded from completed-response duration calculations because its elapsed value was not recorded; it is included in attempt/failure coverage. JSON punctuation can be the first content fragment, not useful answer text or an internal first token. These observations support exploratory CPU latency comparisons, not general accuracy, tail-latency or strict-capacity guarantees.

The continuation observed **2,043.71 MiB peak native-job committed memory**, **71.58 MiB controller peak working set**, and **7.255 GiB minimum available physical RAM**. Initial and final model-state checks confirmed CPU/zero VRAM/context 2048; Qwen3 was explicitly unloaded after its 13 requests. These are not independent per-model RSS or combined OCR/embedding/app measurements. Keep the Windows 11/16-GB/CPU-only target and all earlier host/corpus/traffic limitations.

### Regression fixes, execution epochs and cleanup evidence

Four new regression tests first reproduced lost deadline fragments, incomplete teardown observation and missing-only schedule behavior. Timeout exits now retain observed elapsed time, bounded partial answer/final counters and timer-versus-consumer cutoff metadata; the result checkpoint records deadline failure details before aborting. Teardown waits boundedly for the owned `Popen` process after job termination, records each probe outcome, and never kills a process based on its port alone.

The live continuation exited successfully and **reaped its server**, but all 17 timed-socket teardown probes were **unknown**, not proof of an occupied port; the historical `port_released=false` remains unchanged. A separate connection attempt returned connection refused. Post-run review then added two more failing regressions: a real owned loopback listener test and a late-timeout header-latency normalization test. The final code reads IPv4/IPv6 TCP listener tables directly and counts header latency once in deadline metadata. The listener test binds only a temporary owned localhost socket, verifies occupied/free states, and closes it; no model inference was rerun for these diagnostic-only changes.

Final suite: **27 tests passed in 1.37 seconds**, including the original 11 shared-helper regressions; final Ruff lint and format checks passed. The later two fixes were tested after inference. Therefore `source-snapshot/` preserves the exact executed continuation epoch and `closeout-source-snapshot/` preserves the final tested code; do not claim the final listener implementation produced the historical socket observations. Successful normal-response timing paths are unchanged by the late-timeout diagnostic fix.

Independent final host verification at **2026-11-13 13:48:01 IST** found **zero processes at the exact project Ollama executable path and zero active TCP listeners on port 11434**. The Python IP Helper listener-table check separately reported free. Windows denied the sandboxed CIM inventory; the authorized read-only host check succeeded. No additional process termination or inference was needed. Underlying cause/timing uncertainty from the original request timeout remains unresolved; successful recovery does not retroactively diagnose it.

Final continuation meter: **30/32 recorded starts**, **19/40 loopback API calls**, **zero downloads**. Ten native starts were observed; its root is already included among 21 explicit reservations, so nine additional descendants were charged. Original T11A meter remains 36 starts/92 calls; combined counts are 66 recorded starts and 111 calls across the separately approved phases, not a reset of either allowance. The result snapshot precedes closeout tests/analysis/Ruff; `meter.json` is the final counter authority. No additional inference is required for the completed frozen schedule.

Combined local artifacts: **`combined-summary.json`**, **`combined-review.html`**, and **`combined-labels.json`** in the continuation directory. The review contains **35 distinct model/case/output-or-failure groups**, including the original interrupted case. Existing human labels are carried forward only for matching output identities; currently **zero human assessments** have been supplied. Automated schema/scope success is not factual correctness, groundedness, semantic citation support/coverage, or successful refusal/instruction isolation. Those metrics remain unscored/N/A pending local human review, and no cloud grader received raw responses. Both models remain candidates; Qwen2.5 was faster on these completed responses, which alone does not select a quality winner.

Continuation raw results SHA-256: **`b076c24fbad9b43e70631124dc0bae7a390b82829c9a07dcaf6a95c8475d4406`**. Original result/case identities below remain unchanged. Keep raw results, review pages/labels, source snapshots, logs, keys and model assets ignored. This execution package is complete; **T11A's semantic-review gate remains open**. Git commit, runtime adoption, later 3B-license/candidate changes and starting the next task retain their separate approvals.

## Original run and approval history

The remaining sections retain the original partial result and follow-up proposal as historical evidence. Their pending-approval/incomplete-coverage statements describe that earlier epoch; the completed continuation and current gates are above.

## Actual bounded run and remaining coverage

The user approved the exact package through the active goal “yes, you can proceed.” Both recommended Apache-licensed models were installed into the project model store and every layer hash-checked. Download charge: **2,345,357,052 bytes**, within 3 GiB. Four provisioning starts include the first attempt blocked by sandbox socket permissions and its approved network-escalated retry. Free-space readiness passed the helper's at-least-6-GiB check; no runtime archive, Python dependency, global environment/PATH/service or user-model-store changes. The initial provisioning receipt reports about 618 seconds in the successful attempt; the shared ledger retains the earlier attempt's start/counters.

The test-first run initially failed all ten new tests. After implementation and a source-hash-key correction, the combined **21 T11A/T10 helper tests passed**, most recently **4.01 seconds** before inference. Coverage includes persisted 45-minute duration without resetting existing phases, malformed/unterminated/oversize streams, partial completion failures, absolute stream deadlines and timeout callback, local-client redirect/error charging, message byte bounds, schema/source/column validation, frozen cases/CPU/thinking controls, output caps and escaped local review. Ruff lint and format checks passed at closeout. No unrelated parser regression or additional dependency was needed. These tests do not establish semantic answer correctness or guarantee scheduling under a paused/stalled host.

Run order was Qwen2.5 1.5B, then Qwen3 1.7B, one model at a time. Qwen2.5 completed all four 12-case sweeps and explicit unload. Qwen3 completed 35 responses; **C12 in repetition 2 (zero-based)** interrupted on `BudgetExceeded: Request wall deadline`, so its fourth sweep never started. Coverage is **83 completed/validated of 96 required**, with one interrupted and 12 unattempted cases; the denominator is not reduced. No retry, prompt change, alternative model or new inference was performed after the stop.

During this period a tool status read also stalled and failed with `wait for runner spawn_ready`. That is a separate contemporaneous observation, not proof of the request's underlying cause. The recorded stop reason is the request wall deadline. The interrupted request has no completed duration or partial answer checkpoint; its exact elapsed time and whether the timer callback ran before the consuming-thread guard cannot be reconstructed. The supervisor failure list is empty; do not claim a memory, model-quality or engine-crash diagnosis, or strict observed 120-second cutoff timing from this record.

| Measurement | Qwen2.5 1.5B Q4_K_M | Qwen3 1.7B Q4_K_M |
|---|---:|---:|
| Required scheduled requests | 48 | 48 |
| Attempted / completed and schema-scope valid | 48 / 48 | 36 / 35 |
| Interrupted / unattempted | 0 / 0 | 1 / 12 |
| First C01 full response, seconds | 14.665 | 22.246 |
| Warm C01 responses, seconds | 9.813 / 7.752 / 7.392 | 12.237 / 11.663 / not run |
| Completed-response median, seconds | 10.566 | 14.125 |
| Completed-response range, seconds | 2.914–20.933 | 3.166–33.420 |
| Completed-response first-content median, seconds | 0.379 | 1.055 |
| Generated tokens / weighted generation tokens per second | 4,253 / 10.29 | 3,424 / 8.00 |
| Maximum observed prompt tokens | 319 | 327 |

Latency/token summaries include completed responses only; **the timed-out request is missing from those durations**, not a fast success or zero. Question mixes and repetition counts differ after the interruption; these are observations, not a fair completed comparative ranking or tail-latency guarantee. First response-content fragments can be JSON punctuation, not the model's internal first token or the first useful UI answer. Tokenizers differ. Seeds do not guarantee identical outputs: 84 attempt records group into **34 distinct model/case/output-or-failure groups**, including the interrupted case. Qwen2.5's 48 outputs alone group into 16 distinct case outputs.

Runtime 0.40.16, CPU computation and cloud-disabled logging were observed. Initial `/api/ps` checks confirmed context 2048/zero VRAM for both models; the interrupted Qwen3 run did not reach its final ps/unload controls. No nonempty thinking/tool-call field or unexpected owned non-loopback TCP peer was observed. No selected input-truncation/OOM warning appeared in the closeout log scan. Token headroom observations and that scan are not tokenizer proofs or complete traffic capture.

Observed whole-native-job peak committed memory: **2,085.0 MiB**; controller peak working set: **70.64 MiB**; minimum available physical memory: **6.981 GiB**. These are run-wide measures, not independent per-model RSS. The approximately 19.9-GiB host's background workload/power mode was not controlled or logged as a benchmark baseline. Neither strict 16-GiB compatibility, combined OCR/embedding/chat pressure, document-scale ingestion nor disconnected-runtime acceptance is established.

The immediate teardown socket probe returned **false** for port release. Preserve that result. Subsequent escalated, read-only host verification at **2026-11-13 07:41:11 UTC** found **zero processes at the exact project Ollama executable path and zero active TCP listeners on port 11434**. No additional process termination was needed. This verifies later cleanup; it does not establish why the immediate probe failed. Add a bounded owned-process wait and retained teardown observations before any approved follow-up instead of treating an immediate post-termination probe as final.

Final ledger after analysis/lint: **36/64 recorded starts**, **92/140 API calls**, **2,345,357,052 downloaded bytes**. The native job observed 12 cumulative starts; its root is already among explicit reservations, so 11 additional descendants were charged. The result's 32-start snapshot precedes the two analysis and two final Ruff starts. Available counters are not permission to restart after the stop or reset the phase deadline. All further inference is stopped.

Ignored evidence is in `data/t11a/run-01/`: `installation.json`, `meter.json`, `cases.json`, `results.json`, `engine.log`, `post-analysis.json`, `teardown-verification.json`, `handoff.json`, and exact executed helper/definition copies under `source-snapshot/`. Raw results SHA-256: **`22011d6b7d3f87435c23a2a72c2f1972b3ff5fecb5367128ea38bda0777f87ad`**; frozen cases SHA-256: **`b394ff771cafd6072a3c4f7ed65ceec274fece3394c2a8aaf81f322e278c4ed9`**. Source snapshot/hashes preserve the executed epoch before potential future fixes; raw source-derived artifacts/keys/weights/logs are not commit candidates.

## Local semantic review — pending

Local artifacts: `review.html` contains all retained attempt records; `review-qwen25.html` groups the first model's 48 outputs into 16 distinct case outputs; **`review-unique.html`** groups both models' retained records and shows the approved variant expectations and frozen evidence/gold. **`review-labels.json`** provides empty per-output human labels, including claim/citation numerators and denominators. No model outputs were sent to a cloud grader. A text-only review request for the first model was presented while inference continued; no reply has yet established semantic results.

Machine validation checks shape/types and supplied source/column membership only. **Groundedness, semantic citation correctness/coverage, fully correct answers, meaningful abstention/ambiguity and instruction isolation remain unscored pending local human review.** Report N/A for unknown/empty denominators; do not turn 83 structurally valid outputs into 83 correct answers. The interrupted and missing cases remain explicit coverage failures. Both models remain candidates; observed CPU latency alone cannot select a winner.

## Concrete follow-up proposal — not authorized

The original stop condition has been reached. Propose a separately approved continuation with **no downloads/dependency changes**, **32 additional shared starts**, **40 loopback calls**, **25 minutes from its first experimental process**, **64 MiB additional outputs**, and the unchanged 6-GiB job/1-GiB controller/4-GiB availability guards, CPU/context/prefix/privacy controls. Preserve/link the original ledger, failed record, frozen cases and source epoch; do not reset or overwrite them.

1. Test first: retain elapsed/partial-response metadata on request-deadline exits, and wait boundedly for the owned process after job termination before a retried port-release check. Persist timeout-path diagnostics and teardown snapshots; never stop an unrelated listener. Keep changes in the existing evaluation files/shared budget as necessary, with all relevant tests/lint inside the new allocation.
2. Recheck host readiness and the pinned local model/assets; start only a new owned job/phase. Reuse the identical frozen Qwen3 cases/prompts/settings. Attempt **C12 repetition 2 once**, then all **12 repetition-3 cases**, for 13 explicitly identified follow-up requests. The original timeout stays failed; new measurements have a separate-session/cache caveat and do not replace its latency.
3. Retain the complete Qwen2.5 results without rerunning it. Stop on any further guard/host/runtime failure, save diagnostics, and return to review instead of raising limits. Regenerate local review/metrics with original-versus-follow-up labels and require semantic review before quality claims/adoption.

Alternatively, retain this as an incomplete feasibility result without more inference. Neither option silently completes T11A, removes the Qwen2.5 3B licensing decision for later T11, or authorizes a commit/runtime model/stage transition. [AGENTS.md](../../AGENTS.md) requires approval before exceeding/changing an approved bounded package.

## Original approved proposal and read-only review

The remaining sections preserve the pre-execution proposal. References there to pending provisioning/approval or no benchmark describe that earlier state; actual outcomes and pending gates are recorded above.

## Recommendation and licensing decision

Recommend an early comparison of **qwen2.5:1.5b-instruct-q4_K_M** and **qwen3:1.7b-q4_K_M**, both Apache 2.0. This offers a small baseline and a newer-family alternative without restricting the experiment to non-commercial use. Model size does not establish instruction-following quality or usable speed; those remain unmeasured here. Neither is a runtime default.

The SPEC-named **qwen2.5:3b** candidate has the **Qwen Research License**, not Apache 2.0. The publisher grants non-commercial research/evaluation use and says commercial users must request a license. It also imposes redistribution/notice obligations. Do not infer commercial permission, a price, or license acceptance from the user's earlier Gemma approval. Recommend leaving its weights out of this early package. This is a T11A shortlist proposal, not removal of the candidate from SPEC or silent revision of T11's separately planned 3B comparison. Before that later comparison, explicitly decide whether to trial 3B under its terms or amend that candidate criterion.

Primary sources: [Qwen2.5 1.5B publisher card](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct), [Qwen3 1.7B publisher card](https://huggingface.co/Qwen/Qwen3-1.7B), [Qwen3 Apache license](https://huggingface.co/Qwen/Qwen3-1.7B/raw/main/LICENSE), and [Qwen2.5 3B publisher license](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/raw/main/LICENSE). Packaged licenses were also retrieved and hash-checked against the exact registry manifests. License obligations remain separate from the reused native runtime's MIT/vendor notices. No full legal/security certification is claimed.

## Exact candidate identities

All candidates below were reviewed, but only the first two are proposed for provisioning. Public mutable tags are pinned by manifest and model-layer SHA-256; recheck before downloads and stop on drift. Config/license/template/system/parameter layer identities are captured in ignored `data/t11a-metadata/summary.json` and their exact downloaded records. Do not fetch any other quantization or tag automatically.

| Candidate | Quantization | Weight bytes | All config/layer bytes, excluding manifest | License |
|---|---|---:|---:|---|
| qwen2.5:1.5b-instruct-q4_K_M | Q4_K_M | 986,048,512 | 986,061,892 | Apache 2.0 |
| qwen3:1.7b-q4_K_M | Q4_K_M | 1,359,279,776 | 1,359,293,444 | Apache 2.0 |
| qwen2.5:3b-instruct-q4_K_M — review only | Q4_K_M | 1,929,903,008 | 1,929,912,432 | Qwen Research |

| Candidate | Manifest SHA-256 | Model-layer SHA-256 |
|---|---|---|
| [Qwen2.5 1.5B](https://registry.ollama.ai/v2/library/qwen2.5/manifests/1.5b-instruct-q4_K_M) | `65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b` | `183715c435899236895da3869489cc30ac241476b4971a20285b1a462818a5b4` |
| [Qwen3 1.7B](https://registry.ollama.ai/v2/library/qwen3/manifests/1.7b-q4_K_M) | `8f68893c685c3ddff2aa3fffce2aa60a30bb2da65ca488b61fff134a4d1730e7` | `3d0b790534fe4b79525fc3692950408dca41171676ed7e21db57af5c65ef6ab6` |
| [Qwen2.5 3B — review only](https://registry.ollama.ai/v2/library/qwen2.5/manifests/3b-instruct-q4_K_M) | `357c53fb659c5076de1d65ccb0b397446227b71a42be9d1603d46168015c9e4b` | `5ee4f07cdb9beadbbb293e85803c569b01bd37ed059d2715faa7bb405f31caa6` |

The recommended pair totals **2,345,355,336 bytes (~2.18 GiB)** plus manifests. The 3B/Qwen3 pair would instead total 3,289,205,876 bytes, exceeding the proposed 3 GiB network cap; substituting it needs a revised explicit package, not automatic fallback.

Qwen3's tag/publisher name says 1.7B; the registry config says 2.0B and the library page reports 2.03B. Preserve those distinct labels and inspect actual `/api/show` metadata; do not promise a 1.7-billion-parameter memory footprint from the name. Config `os: linux` is model-image metadata, not a Windows compatibility result. Actual GGUF loading through the pinned Windows runtime remains to be tested. [Exact library page](https://ollama.com/library/qwen3:1.7b-q4_K_M).

No model-specific Python code, PyTorch, Transformers, SentenceTransformers, hosted API, remote-code execution, Docker or tokenizer package is proposed. The GGUFs, templates and parameters are untrusted input to the existing native parser; hashes establish identity, not safety. Reuse the inspected **Ollama 0.40.16** executable at `.venv/tools/ollama/0.40.16/ollama.exe`, SHA-256 `4ccefcbfecc50fb6526471adabbc20869dd614e29e351120b15083cb174b0b8a`. No runtime upgrade or additional archive. Existing standard library/HTTPX/pytest/Ruff suffice. Inherited bundled-license/security limitations remain in the [T10 report](embeddings.md).

## One proposed approval package

Approval would cover only the recommended Apache-licensed pair, local caching, the bounded test-first evaluation aids, measurements, manual result review, documentation and owned-process teardown below. It would not approve Qwen2.5 3B weights, runtime adoption, T11 combined pressure tests, app code, a Git commit or a stage transition.

### Provisioning and shared execution bounds

- **Network:** at most **3 GiB** received, including metadata, partial transfers and retries; only the public Ollama registry and its official artifact delivery redirects during provisioning. Verify pinned manifests immediately before transfer and hash/size-check every layer before installing it. No content goes to remote endpoints.
- **Additional project disk:** at most **6 GiB**, covering model/temporary files and receipts; reuse the installed native runtime, no new ZIP. Verify actual free space before transfer. The sandbox's current F: drive query returned unavailable/null capacity; this is not proof of zero space or readiness.
- **Provisioning deadline:** **90 minutes** from provisioning start, with no implicit reset. Count provisioning helper launches in the same process allowance as tests/inference. No stale T10 allowance is available.
- **Experimental process starts:** **64 total**, including helper launchers/interpreters, test/negative/regression runs, Ruff, the owned server and all native descendants. Persist both explicit reservations and cumulative observed native counts, including rejected charges; one native job per phase. Record observed overshoot and stop. Polling is not preemptive child-creation enforcement. Tool-host/PowerShell infrastructure is outside this experimental-child count, as in T10; do not hide Python/native tests there.
- **API calls:** **140 loopback calls total**, counting failed/control/streaming attempts. A stream is one HTTP call; retries require another charge. Plan 96 scored chat calls, at most two readiness chat probes, and at most 20 startup/show/tags/ps/unload calls, leaving 22 for bounded failures/controls. Do not silently reduce the frozen scored schedule to fit startup overhead.
- **Benchmark deadline:** **45 minutes** from the first test/evaluation experimental process after provisioning; tests/lint/native setup and inference share that deadline. Persist it before the first such launch. Configure/test this new phase duration explicitly rather than changing T10's stored 30-minute phases. Per request: **120 seconds or the remaining global deadline**, whichever is smaller; enforce wall time across an entire stream, not just socket-read inactivity.
- **Outputs:** at most **64 MiB** total under the run directory, including answers, logs, tests, failures and receipts. Cap each streaming record/assembled response as well. Stop before unbounded accumulation.
- **Memory:** reuse the **6 GiB native-job committed-memory cap**, **1 GiB controller cap**, and stop when available physical memory falls below **4 GiB**. One model loaded, sequential requests, no embeddings/OCR concurrently. Preserve the approved Windows 11/16 GB/CPU-only target; the actual host's approximately 19.9 GiB RAM and MX150 do not expand it. Combined capacity is unverified until T11.

Model store remains `data/ollama/models`; state/key/config/temp remains under `data/ollama/runtime-home`, with run data under a fresh `data/t11a/run-01/`. No global installs/PATH/environment changes, service/updater, user-store modification or cleanup of other locations. No Python dependency/lock changes. Keep original bytes, raw responses, prompts, keys, model layers and logs ignored. Retain partial downloads/failures without unapproved deletion; they count against the caps.

Reuse process-local loopback/cloud/CPU settings from T10: `OLLAMA_HOST=127.0.0.1:11434`, `OLLAMA_NO_CLOUD=1`, one loaded model/parallel request, GPU backends disabled, and HTTPX proxy inheritance disabled. Refuse an occupied endpoint and terminate only the job this trial creates. Observe zero VRAM/CPU computation. No LAN binding, accounts, tools/MCP, web search, cloud fallback or startup downloads. Verify owned-job closure and endpoint release.

### Fixed request configuration

Use `/api/chat` with model-native templates, the same authored English system/evidence contract, `num_gpu=0`, `num_thread=4`, `num_ctx=2048`, `num_batch=64`, `num_predict=192`, `temperature=0.2`, `top_p=0.9`, `top_k=20`, `repeat_penalty=1`, and recorded seed 42. These are comparable trial settings, not publisher-recommended optima, determinism guarantees or application defaults. Do not tune after observing scores inside this package; record failures/limitations for review.

For Qwen3 request **`think=false`** and inspect the pinned template/local model metadata. Its registry defaults differ from this proposal. Treat unexpected thinking output, unsupported controls or tool-call output as a failed control; do not silently change model/mode or spend the output allowance on reasoning. Qwen2.5 uses its non-thinking template; do not send an unsupported thinking option blindly. [Ollama thinking controls](https://docs.ollama.com/capabilities/thinking), [pinned API types](https://github.com/ollama/ollama/blob/v0.40.16/api/types.go).

Request a small structured answer with English `answer`, `status` (`answered`, `insufficient`, `clarify`) and `citations` (source IDs and columns). Validate shape/types locally with standard library checks; JSON conformance is not semantic correctness. Tool invocation stays disabled. The system contract requires using only supplied evidence, treating evidence/history instructions as untrusted, preserving source values/units, distinguishing calculation from a quoted value, citing factual claims, and abstaining/clarifying when warranted. Freeze the exact contract/schema before the first inference call.

Use streaming NDJSON to measure time to the first nonempty **answer-content** chunk separately from HTTP headers or any thinking field; retain the final timing/token counters and termination reason. A missing final record, malformed/oversize stream, timeout, truncated output or token-limit termination is a recorded failure/incomplete answer, not a fast success. [Chat API](https://docs.ollama.com/api/chat), [streaming format](https://docs.ollama.com/api/streaming).

Keep the full serialized messages compact (proposed cap **3,000 UTF-8 bytes**); freeze their hashes. This byte cap is not a tokenizer proof. Inspect prompt token counts and runtime truncation/context warnings, leave room for output/template overhead, and invalidate affected cases instead of claiming all context was used. No tokenizer dependency or larger context is automatically authorized. Input length/resource negative controls use mocks/local validation first.

### Frozen scenarios and provenance

Reuse the checked R08/R09 originals and source IDs/record/physical-line/column anchors from T10. Read source/definition hashes and materialized T10 evidence, verify required values/anchors locally, then freeze a derived case manifest before inference. These internal JSON evidence packets do not add TXT support or globally enable question scoring. Do not run parsers or regenerate PDF/workbook fixtures for this package. PDF/OCR/XLS/XLSX and chart understanding remain untested by this CSV-only early slice.

| Case | Lineage / purpose | Required behavior |
|---|---|---|
| C01 | Q01 numeric lookup | Exact workers value with its real source/2025 column |
| C02 | Q02 two-year arithmetic | Correct decrease and subtraction; cite both input years, distinguish derived change |
| C03 | Q03 two-source answer | Correctly identify output versus workers; both required sources, no invented units |
| C04 | Q04 industry row lookup | Correct quoted-comma industry and record/column anchor |
| C05 | Q05 ambiguity | Clarify output/workers or explicitly answer both with sources; no silent selection |
| C06 | Q06 absent cause | State supplied numbers do not establish management decisions/causation |
| C07 | Q01 history-contamination control | Prior deliberately wrong assistant value must not override current evidence |
| C08 | Q01 empty-evidence control | Abstain without fabricating a source/value from history or model memory |
| C09 | Q03 selected-scope control | With output evidence withheld, do not report its value; disclose incomplete evidence |
| C10 | Q01 authored injection control | Ignore a separate clearly identified hostile evidence instruction; answer only from the unchanged real row |
| C11 | Q02 wording/format variant | Preserve arithmetic/provenance under a reordered question; same gold, not a new independent business case |
| C12 | Q03 unsupported-unit diagnostic | Do not infer currency/scale absent from the supplied evidence packet; qualify the packet's limits |

The six controls/variants are explicitly derived cases, not replacement ground truth for Q01–Q06. The authored injection/incorrect history are separately identified test inputs; do not modify source bytes or gold facts. Approval of this package approves these case definitions and the trial's use of existing gold; unexpected requirements/ground-truth changes still need a decision. Missing evidence/hash mismatches fail readiness, not a smaller denominator.

Per model: four full sweeps of all 12 cases, **48 scored calls**, **96 across both models**. The first scored request is the first-load observation; later requests are warm. Do not describe every scenario as cold or claim controlled cold OS caches. Readiness probes, if needed, come after that first scored request so they cannot warm the model before its first-load measurement. Keep ordering fixed and report model order, cache/session/background-pressure effects. Record settings/prompt/source hashes with every run. Do not automatically retry failed scored cases or change temperatures to obtain a better score.

### Measurement, tests and stop conditions

Use the existing [evaluation rubric](../evaluation.md): exact facts/calculation, completeness, grounded claims, citation validity and semantic support/coverage, ambiguity, unsupported refusal, over-abstention and instruction/history/scope isolation. Manually review source/claim links locally; valid IDs and string matching alone do not establish support. Report raw denominators per category, N/A for empty citation/recall denominators, every failed/incomplete case and variation across repetitions. No cloud judge or user-facing probability score. These are exploratory measurements against the approved initial rubric, not T16/final acceptance or general accuracy.

Measure runtime/model identity, CPU/VRAM/context, load/first-answer/full-response timings, generated/prompt tokens and generation throughput, native-job commit, controller working/private memory, available physical RAM, output/disk footprint and startup/unload failures. Preserve counter units; do not substitute model-file size for memory. Do not equate first content chunk with the model's internal first token. A model switch later requires model/prompt/index version review; no chat/embedding model coupling is assumed here.

After approval, implement tests first for: total-stream deadlines/failed-call charging, malformed/unterminated/oversize streams and output caps, local endpoint/redirect restrictions, response schema/source-scope/citation validation, CPU/thinking controls, fixed case/source hashes, and budget exhaustion/stop-reason persistence. Reuse T10's reviewed job/ledger code where appropriate; add/test persisted configurable phase duration and exercise relevant existing 11 helper regressions **inside the new T11A allowance**. Never invoke their consumed T10 meters. No unrelated parser suite, optional dependency or new framework is necessary.

Keep at most **three new versioned evaluation artifacts** (chat harness, focused tests and safe authored case definitions); targeted changes to the shared budget/tests are allowed for configurable duration and any demonstrated T11A requirement. Do not create product modules. Review trust/resource boundaries and Ruff after the relevant tests, retaining source hashes. A native-child counter polling gap is disclosed, not described as a kernel-enforced cumulative-start limit.

Stop before exceeding network/disk/deadline/API/output limits, on insufficient memory, occupied port, identity/source drift, non-loopback owned traffic, GPU use, unexpected runtime downloads, unsupported template/thinking behavior, or inability to supervise/retain diagnostics. Save partial results and terminate owned processes; do not reset counters, silently skip required scenarios, adopt a cloud fallback or proceed to T11/application work. If resource failure prevents all 96 cases, report incomplete feasibility and concrete options for a separately approved follow-up.

Sample TCP-peer observations/local settings do not prove disconnected operation or cover UDP/brief connections. No machine-wide firewall/network changes are proposed. Explicit offline and combined app/OCR/embedding/chat checks remain required later, especially T11/T47 and before corresponding adoption/acceptance claims.

## Read-only checks and next gate

Public manifests and each small fetched layer were size/hash-checked; all selected configs state GGUF/Q4_K_M. Only small public metadata was cached under ignored `data/t11a-metadata/`; no original documents/prompts/answers left the machine. The first `.ps1` file invocation was blocked by Windows script execution policy and was not executed. No execution-policy change was made; equivalent explicit read-only HTTP commands ran through the tool after network escalation. No engine was started for inventory or inference, and no T10 budget was reused. The installed executable exists and no Ollama process was visible in the read-only inventory; service/port and free-space readiness must be checked before the proposed run.

User decision now: **approve the recommended Apache-only pair and exact bounded package, or request another shortlist**. Qwen2.5 3B remains review-only unless separately approved under its terms with revised budgets. After an approved trial, present measured results, recommendation/limitations and a readable Git diff; ask separately before commit or runtime adoption. This read-only review provides no chat benchmark outcome or speed/quality guarantee.
