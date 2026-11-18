# T17-IF-LFT — controlled local-file tokenizer trial proposal

## Approval state and readiness

The user approved the four-file [LFC comparison](local-file-tokenizer-comparison.md) commit **`cbfedf3`** and preparation of option A's trial proposal. This approval selects preparation with the **complete declared dependency set**, not installation, a trial-risk exception, native execution or runtime adoption. No code, fixture, execution root, public query or environment change was made during this preparation.

**The native trial is not execution-ready.** Existing static evidence is useful, but exact local-file import/load behaviour, native launch/loader policy, complete executable schedule and the named evidence exceptions remain unsettled. This document provides a bounded **readiness package LFT1–LFT5** for approval now. It also defines the later native-trial acceptance contract and required risk decision. Approving LFT1–LFT5 cannot activate the native phase.

Stage 1 remains Windows 11/16 GB/CPU-only, PDF/XLSX/CSV. Conditional standalone counting remains the direction; Ollama remains the generation/embedding candidate. No CSV application coding, architecture/runtime adoption/G2 closure or stage transition.

## Retained evidence and exact candidate set

The saved Windows target graph has **17 distributions**. Keep it complete; do not omit Hub/HF-Xet because downloading is unused, use `--no-deps`, edit metadata, stub imports, add extras, select a different version or infer a smaller installed footprint.

| Distribution | Version | Retained artifact authority |
| --- | --- | --- |
| tokenizers | 0.23.3 | Cached inspected Windows wheel |
| huggingface-hub | 2.4.0 | Cached inspected wheel |
| hf-xet | 1.8.0 | Acquired/inspected Windows wheel |
| httpx2 / httpcore2 | 2.16.2 / 2.16.2 | Two acquired/inspected wheels; distinct from project HTTPX/httpcore |
| anyio / click / filelock | 4.16.0 / 8.5.1 / 4.2.10 | Three acquired/inspected wheels |
| truststore / fsspec | 0.10.5 / 2026.9.0 | Two acquired/inspected wheels |
| idna / typing-extensions / h11 | 3.20 / 4.16.0 / 0.16.0 | Retained installed metadata, not new wheel clearance |
| packaging / pyyaml / tqdm / colorama | 26.3 / 6.0.3 / 4.70.1 / 0.4.6 | Retained installed metadata, not new wheel clearance |

The graph's Windows/AMD64 facts were labelled assumptions, not a new hardware measurement. Preserve that distinction. A matching version declaration is not native ABI compatibility or an installable lock. See [RRC findings](../benchmarks/remaining-artifact-readiness-continuation.md).

Exact candidate identities include:

- Tokenizers `tokenizers-0.23.3-cp310-abi3-win_amd64.whl`: 2,872,101 bytes, SHA-256 `1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3`.
- Hub `huggingface_hub-2.4.0-py3-none-any.whl`: 857,021 bytes, SHA-256 `42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801`.
- HF-Xet `hf_xet-1.8.0-cp38-abi3-win_amd64.whl`: 3,911,559 bytes, SHA-256 `92188598dedc1e1f5609bd718d4db8687a6c89915553912571e2f587892eecec`.

The other seven acquired wheels' exact filenames/sizes/digests are frozen by the ASR acquisition/inspection records below. The seven installed dependencies require a final reuse/artifact/lock plan; their metadata does not supply missing wheel identities. LFT1–LFT5 cannot install, resolve or acquire those artifacts to fill a gap.

### Existing runtime and tokenizer assets

Retain Ollama **0.40.16**, cached archive SHA-256 `50fcf5ad54277f2fa5d173ebfc93bcb017adbc0c9ef2314daabc96ca9e6aa64e` and the saved 75-file installation inventory. No repeat of the 1.6 GB archive comparison is proposed. Representative existing manifest entries under `.venv/tools/ollama/0.40.16/` are:

| Relative file | Bytes | Saved SHA-256 |
| --- | ---: | --- |
| `ollama.exe` | 41,268,104 | `4ccefcbfecc50fb6526471adabbc20869dd614e29e351120b15083cb174b0b8a` |
| `lib/ollama/llama-server.exe` | 23,944 | `740af7a7897cc7848cc9d8ee58e91889c10341f364c437f9b62bf4e254b4e7ac` |
| `lib/ollama/ggml-base.dll` | 852,360 | `db03afde2e16f420308da15b4cfe635c074de64b63fae5295bd9387e13938f15` |
| `lib/ollama/ggml-cpu-x64.dll` | 1,276,808 | `a18390c75b37c9fe47bba82bb4520eb2d3efb3347fb62d7d777101d4902fa191` |
| `lib/ollama/ggml.dll` | 49,032 | `91c9624eafab84f83e5b3a2fb9c4d782c0488f6c8b41e8c7d6f7faa01a925456` |
| `lib/ollama/libllama.dll` | 4,130,184 | `8831be8f308bfdd5971a56412814a7eebce2dfc4d504b7944e1a676799313c3e` |

This is not a selected complete DLL load set. Source review must establish the exact CPU backend, loader search policy and launch arguments; no hardware-specific DLL, GPU fallback or global search path is silently chosen. Saved installed/archive agreement is not an independent publisher/build attestation.

The existing publisher asset set is frozen in the combined-reference manifest: Qwen `Qwen2.5-1.5B-Instruct` revision `5fee7c4ed634dc66c6e318c8ac2897b8b9154536` and Nomic `nomic-embed-text-v1.5` revision `541c5a6fadb4da793505a2bb4d3ee910de7f39ea`, 11 data assets in total. The main tokenizer JSON observations are Qwen 7,031,645 bytes/SHA `c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539` and Nomic 711,396 bytes/SHA `d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66`. These are observed local SHA identities with publisher Git-blob/size checks, not independent publisher SHA attestations or proof of cached-GGUF equivalence. No asset payload or model store is read during readiness work.

The native source reference remains b12177 / `6c01da6278ab6c69ed67d9124806b50d2b299ba7` **with Ollama compatibility overlays**, as established by [SV findings](../benchmarks/standalone-tokenizer-validation-design.md). No upstream binary substitution or custom build is proposed.

The retained metadata inventory names cached chat `qwen2.5:1.5b-instruct-q4_K_M`, manifest SHA `65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b`, and embedding `nomic-embed-text:v1.5`, manifest SHA `0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f`. These manifest identities are not GGUF weight digests. LFT4 must supply the exact retained weight/model mapping before calling the native package ready; no model-store inspection is authorized to invent missing evidence.

## Fixed readiness inputs

Verify these 16 byte identities before optional work and at closeout. Historical roots/files remain read-only. Reuse the eight protected project/evaluation/checkpoint identities retained in ALN's `preserved.json`; no checkpoint edits or replacement files. The historical metadata script is a data/design reference only: do not import or execute it or dispatch its old schedule. The SLR helper/control records support response handling, not permission to reopen that epoch.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/proposals/local-file-tokenizer-comparison.md` | 9,544 | `98424d57902584186ddfb4363a8019e19b92bfada9f98937d74645b1b07c066c` |
| `docs/benchmarks/artifact-licence-notice-review.md` | 10,371 | `022b9da33e57f26747e978fe626088f0a05c2399e8f3044ab9519de214b2dbba` |
| `data/t17/remaining-artifact-readiness-02/graph.json` | 323,768 | `9c8cb29e52fc47e9ce1ceae888641184d88bede3234856219f68be95262fbbd8` |
| `data/t17/remaining-artifact-readiness-02/review-details.json` | 204,623 | `1da1c4d4b9c9be19e158cd074a728edd4a1c086e1a4059187998ffc85043fe22` |
| `data/t17/input-fit-tokenizer-static-01/tokenizers-inspection.json` | 6,824 | `c83fd421d2cc548eeda103e1021cd10247420e232d1589569aced9351dd46ca9` |
| `data/t17/input-fit-tokenizer-static-01/huggingface-hub-inspection.json` | 42,937 | `4396cd55d01094d14cd1a1ab606f54f353a9b716f5a1676db0112d1e5331e86c` |
| `data/t17/wheel-artifact-review-02/acquire-result.json` | 3,496 | `5185fb521c89b74afdfa282c6d12433cb7e47b2aab60cd83d1dccbdddfc6ef18` |
| `data/t17/wheel-artifact-review-02/inspect-result.json` | 127,374 | `2b03271be8c491c648ba2d5e31d9fe86cf112d9180bad06788b4e03afdf73141` |
| `data/t17/input-fit-assets-remaining-01/combined-reference-manifest.json` | 13,130 | `baf43ef4e655328b21a1010ffe877cde9ffa2b7f7ab60e6ada7afb9d4853edcb` |
| `data/t17/standalone-static-verification-03/worker-result.json` | 228,420 | `ae114ac9d586bf489d63a34e7392a0588e598622d5132d8eabf5c4b4e259761e` |
| `docs/proposals/input-fit-tokenizer-parity-validation.md` | 6,857 | `3e5c9036d84bb33033864ec0856796ccafe7988c1078b2c6046b727b82fd7d13` |
| `docs/benchmarks/standalone-tokenizer-validation-design.md` | 7,468 | `4c46a1510b14ba8f43d086c95b547ec428f0dcbf39af0ada4a32f6e36e5c0a6e` |
| `docs/proposals/standalone-tokenizer-parity-trial-design.md` | 7,401 | `d22387119f56f447dcc4566198139529fe474d58e04705c3d888369596a8efab` |
| `tests/evals/spikes/input_fit_metadata.py` | 12,114 | `2d47b7c816dba4092c755a4787fee6f394e4bd628a9d77f4829b3da98ed04204` |
| `data/t17/source-licence-review-01/response-helper.js` | 311 | `5c17dcd40c17736ad3932313fcafdcb5df09238f1cd4635c2d24b69f8d70efc9` |
| `data/t17/source-licence-review-01/green-controls.json` | 179 | `2af07df9ff181a7bfb947dcd80a201d7f8a3274ba415b41e4997ac5264cb5792` |

## LFT1–LFT5 readiness package — proposed, not yet authorized

This is one sequential package with internal review points, not five separate task-start approvals. No candidate payloads/imports, native executable/library loads, model calls, dependency acquisition/installation, resolver, environment/PATH change or runnable user handoff. Public source text is data only. Existing graph/archive/control/model suites stay closed.

| ID | Objective / prerequisites | Acceptance / verification | Status |
| --- | --- | --- | --- |
| LFT1 | Bootstrap/freeze after package approval | Fresh root/shared accounting; 16 fixed/eight protected identities; complete 17-node candidate set and unresolved artifact roles recorded; literal command/data boundaries | Awaiting approval |
| LFT2 | Local-file API/reference source review after LFT1 | Pinned import/file-loading and CPU-reference/request/loader contracts verified or explicitly unknown; no remote identifiers/download/code path assumed safe; exact source notes retained | Pending |
| LFT3 | Test-first readiness/reporting validator after LFT2 | Meaningful behavioural RED, smallest GREEN and caught mutation; fake-only manifest/admission/report-reserve/ownership controls; focused tests and final Ruff pass, or stop with full diagnostics | Pending |
| LFT4 | Finite trial manifest/schedule design after LFT3 | Every FP01–08/NP01–08 group mapped; exact future installation/asset/runtime/request/ownership entries and call/start/resource schedule, or explicit missing fields; no guessed readiness | Pending |
| LFT5 | Decision and completion/stop closeout | Non-null summary, actual/reserved counters, owned exits, preservation/scope/links/whitespace/diff/index review; clear ready/blocked verdict and exact exception/next decision, no native activation | Pending |

If LFT2 cannot justify an indispensable reference/loader contract, skip new validator authoring that depends on it and close out with alternatives. Source-only readiness work does not need an exception to execute candidates because none may run. Routine edits/tests/review/documentation inside the approved package need no repeated permission; significant scope changes do.

### Pinned source-text boundary

At most **four web calls/12 explicit targets**, including failed requests/finds/clicks. Start with Tokenizers commit `301277072263fb3830eb66eec7e47adadf76f1dc`: `bindings/python/py_src/tokenizers/__init__.py`, `bindings/python/py_src/tokenizers/implementations/base_tokenizer.py`, `bindings/python/src/tokenizer.rs`, `bindings/python/src/lib.rs`, `tokenizers/src/tokenizer/mod.rs`. Only relevant files need be fetched. These are candidate paths, not assertions that each file exists or has been reviewed.

Only to close a concrete unresolved runtime contract, inspect the pinned native `tools/server/server.cpp`, `server-context.cpp`, `server-common.cpp`, `common/arg.cpp`, or Ollama v0.40.16 `llm/server.go`, `llama/compat/compat.cmake`, `llama/server/CMakeLists.txt`, within the same 12-target allowance. Reuse SV observations rather than repeat source mapping. Hosts: GitHub/raw.githubusercontent.com for these exact repositories/revisions only; no broad search, mirror, archive/clone, build, native HTTP helper, dependency-source crawl or repeat ALN licence queries. Missing text stays unknown.

Use the already tested SLR response ordering and UTF-8 arithmetic: raw result stored immediately after await, then serialized size admission, full structured local persistence and byte/JSON/SHA verification, then excerpts. No TextEncoder/Buffer/Node assumptions, public-text shell interpolation or silent truncation. Oversized/unretained responses cannot support new claims. This temporary recovery storage is not a durable session checkpoint.

### Test-first scope and permitted authored files

Only after execution approval, permit `tests/evals/spikes/local_file_trial_readiness.py`, `test_local_file_trial_readiness.py` and `local_file_trial_cases.json`. The helper validates a **data-only future manifest/schedule and reporting admission**, not an application tokenizer or native launcher. No candidate import, fake success implementation or hidden execution mode. Do not run third-party skill scripts or spawn subagents. Read the verified incremental/TDD/security/review skills before implementation.

Use at most 48 authored small synthetic case definitions covering missing/mismatched IDs, local path/URL refusal, unsupported branches, required graph omissions, unknown context/overhead, capacity equality/overflow, drift/replay/cancellation/ownership/teardown states and immutable manifest decisions. Carry all frozen FP/NP groups into the future manifest; fake results never count as native passes.

Specifically reproduce ALN's reserve failure with a behavioural RED: an optional display would leave fewer than 16 KiB for closure and must be refused **before emission**. GREEN must cover exact UTF-8 boundary/over-cap cases, multibyte JSON, closure admission, immutable shared counters and caught mutation of the reserve check. Test the same reporting-admission function that the parent uses; an unused tested helper is insufficient. Raw native streams go to bounded retained capture; only admitted scalar status/excerpts may be displayed. Failed precharge stops the operation, not just its preview.

### Shared readiness limits

Fresh ignored root **`data/t17/local-file-trial-readiness-01/`**; refuse existing/reparse roots. A single parent reserves before every operation, including tests, negative/mutation controls, shell/Git/worker failures and partial captures. Never reset old roots or renew their unused limits.

| Resource | Proposed limit / accounting |
| --- | --- |
| Work/time | 64 units: bootstrap 6, source review 12, validator/tests 20, schedule/decision 10, protected closeout 16. At most 1,800 active seconds; optional cutoff 1,200, 600 reserved for closeout. Public review must start by 600 or report not started. |
| Owned starts/checks | 48 combined prepaid starts, actual separately recorded. At most six focused pytest invocations and four Ruff invocations, including RED/negative/regression/final checks; no extra historical suites. Reserve final tests/lint before refinements. |
| Source/reads/artifacts | Four calls/12 targets; 512 KiB serialized response each/2 MiB aggregate; 64 MiB explicit read leases including 4 MiB receipts; 16 MiB total retained artifacts/diagnostics/fixtures. No candidate/asset payload reads. |
| Reporting | 64 KiB author-controlled UTF-8 displayed text, with **16 KiB protected for closure**, at most 3,000 bytes per display. Before optional display require `used + proposed <= 48 KiB`; closure may use the full remaining ceiling. Retain actual cumulative count; platform-generated tool envelopes/fetch buffering are outside this measurement. |
| Native captures | Combined stdout/stderr at most 32 KiB per invocation, captured concurrently to EOF, never echoed before admission; over-cap is failure, not silent truncation. At most 120 seconds plus 15-second owned teardown per test/check child; other shell checks at most 60 seconds plus 15. |
| Receipts | At most 48 explicitly numbered immutable receipts, each at most 4 KiB, included in shared read/artifact limits; non-null completion/stop summary and ownership evidence. |

Use only existing project `.venv` pytest 9.2.0/Ruff 0.17.5 and interpreter, with verified local versions; no provisioning to repair a missing tool. Isolated stdlib metadata checks may use the existing `F:/Python/Python314/python.exe -I -S -B`. No policy bypass or global changes. Source controls can run in-process; every actual native child/start remains counted. No arbitrary subprocesses, candidate imports, network calls from tests or real model processes. Verify invocation syntax/capture in the same allowance before running checks; don't bypass host policy.

Stop optional work on failed required GREEN, identity drift, unsafe input, capture/accounting/ownership failure, exhausted allowance/cutoff, host denial or missing indispensable source contract. Ordinary test-first implementation corrections remain inside the six-suite/four-Ruff caps; no automatic real-source request retry or unmetered orchestration correction. Up to two measured host approval waits, cumulative 24 hours with no intervening model work, may be excluded; authoring/tool time counts. Close out even if readiness is blocked. Conservative reservations are not actual OS I/O, memory or process confinement measurements.

## Later native trial — contract only, no execution permission

LFT4 must produce a reviewable manifest with no unknown executable-critical field. It must identify exact cached model/GGUF/runtime/DLL/asset paths and hashes, source/settings/rendering identities, CPU-only flags, local endpoints/authentication, loader search policy, process birth/handle ownership, permitted children, bounded readiness polling and teardown deadlines. Do not discover private ports, attach to unrelated Ollama, use remote model identifiers, substitute an upstream binary or invent working commands from this design.

The provisional envelope inherited from the staged design is at most 60 active minutes, 64 combined owned starts and 256 local HTTP transactions, including health/render/reference/generation/control/cleanup requests. At most 24 chat and 12 embedding positive case instances plus 16 explicit negative/control instances; cold/warm repetitions must be named within those counts. Expand the actual per-case operations and totals after source verification; this ceiling alone is not a valid executable schedule. No native permission follows if the complete required matrix cannot fit.

Preserve every FP01–08 and NP01–08 requirement: complete actual rendered input, exact token IDs/counts and special-token policy; separate Nomic query/document normalization/prefix/CLS/SEP; context/output/EOS and equality semantics; eight packing candidates without extra inference; drift, scope, cancellation and refusal checks; disconnected cold/warm loading and complete answer path. Post-generation usage is supplementary, not preflight proof. Unknown overhead cannot become zero. Keep provisional 2,048 context/192 output and R01 limits unchanged pending their existing validation gates.

One heavy workload at a time; target warm complete answer within 30 seconds, hard answer timeout 90 seconds, at most 8 GiB total across owned app/workers/Ollama and at least 4 GiB available RAM. These remain targets on the unchanged 16 GB CPU-only specification, not demonstrated capacity. A larger-memory host result alone cannot establish target acceptance. Measure all owned/native children, not just the adapter.

Before native execution, explicitly choose a reviewed enforceable host/privacy boundary. A physical-disconnection-only synthetic run with no filesystem confinement would need its own plainly stated user acceptance and disconnection-through-verified-teardown procedure; it is not granted here. No silent network reconfiguration, cloud fallback or automatic downloads. Exact local assets only, synthetic inputs only, no documents, content telemetry or payload logs. Fully stop/reap the owned model before starting its reference, then stop the reference before generation cross-check; uncertain ownership/teardown stops the trial without retry.

## Named exception and decisions still required

| Unresolved evidence | What a future trial-only exception would need to say | What it cannot waive |
| --- | --- | --- |
| Tokenizers/native vendor notices; HF-Xet compiled/vendor scope | Acknowledge these exact gaps for the named candidate artifacts and specific controlled installation/import/load actions | Notice obligations, unrestricted redistribution, a claim of compliance or runtime adoption |
| Wheel/build-source linkage; Hub/FSSpec source-role conditions | Name publishing versus release/build roles and the limited trial action accepted despite missing independent linkage | Existing adoption conditions or an assertion that builds were independently verified |
| Publisher tokenizer SHA unavailable; observed SHA/Git identity and GGUF equivalence | Distinguish observation from publisher attestation; permit only exact existing files if accepted | Identity checks, source matching, empirical tokenizer/model parity or drift refusal |
| Seven reused installed dependencies and final provisioning set | Supply an exact project-venv reuse/install/lock plan and any remaining artifact assurance gap | Required dependencies, reviewed source/version choices, global isolation or truthful lockfile |

No exception is presumed approved. A future exception must be specific, rather than a broad waiver of safety or product requirements. Missing loader/oracle correctness, an unknown execution manifest, unsafe host boundary, inadequate capture or failed teardown are readiness blockers, not proposed exceptions. No package/model/runtime adoption follows from a trial-only decision.

**Decisions after LFT1–LFT5:** whether evidence supports the exact native package; whether to accept the narrowly named trial-only gaps; whether to approve project-venv provisioning/native execution and its host boundary. Review actual results separately for runtime adoption/G2 and any stage transition. If blocked, present one consolidated decision/alternative; do not automatically start another identical research continuation.

## Deliverables and requested approval

Preparation touches only this proposal, PLAN, TODO and README. Readiness execution may author the three named evaluation files and at most seven closeout/design documents: this proposal, new `docs/benchmarks/local-file-trial-readiness.md`, new `docs/proposals/local-file-native-trial-package.md` **only if a concrete package can be supported**, `docs/dependencies.md`, PLAN, TODO and README. Record a blocked verdict instead of an empty/runnable-looking native package. Preserve SPEC/AGENTS/project/lock, existing parity/evaluation sources/manifests, old roots/reports/proposals, historical checkpoints and unrelated user files.

**Requested now:** the four-file planning commit and **LFT1–LFT5 readiness work only**, under the limits above. This does not approve any residual-risk exception, installation/download of candidates, native/model execution, runtime adoption or stage transition. No session-checkpoint file is created or updated.
