# T17-IF-SV — standalone reference design findings

## Outcome — 2026-11-16

Approved [SV package](../proposals/standalone-tokenizer-validation-design.md), proposal commit `68a878c`. **A directly owned bundled runner is a credible source-level validation reference candidate for the standalone tokenizer.** Exact installed artifacts, release provenance and empirical parity remain unverified; no execution-ready trial or runtime adoption follows. This advances the design beyond the earlier unresolved external handoff: a future test controller would start its own reference process, not discover Ollama's private port.

Eight web calls/twenty-four targets exhausted the approved research ceiling. One missing `.gitmodules` returned404 and one GitHub ref API URL was inaccessible; both charged without retry. A distinct release/commit page established the native revision. No local binary/model inspection, installation, download of payloads, code/helper/test generation, native process, API or inference occurred.

## Build mapping and source evidence

| Primary source | Verified source observation | Limit |
|---|---|---|
| [Ollama v0.40.16 root CMake](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/CMakeLists.txt) |Native server build is a separate subproject |Not an installed binary attestation |
| [Runner CMake](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/llama/server/CMakeLists.txt) |Reads LLAMA_CPP_VERSION, fetches upstream and applies compatibility integration; enables native server, disables CURL/OpenSSL/subprocess build options |Source configuration is not proof of runtime confinement or shipped DLL inventory |
| [LLAMA_CPP_VERSION](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/LLAMA_CPP_VERSION), [release](https://github.com/ggml-org/llama.cpp/releases/tag/b12177), [commit](https://github.com/ggml-org/llama.cpp/commit/6c01da6278ab6c69ed67d9124806b50d2b299ba7) |Native tag b12177 maps to full commit `6c01da6278ab6c69ed67d9124806b50d2b299ba7` |Tag/source mapping alone does not authenticate local binaries |
| [Compatibility README](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/llama/compat/README.md), [compat.cmake](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/llama/compat/compat.cmake) |Ollama links its compatibility sources and loader patches; transformations can affect metadata |A generic upstream binary is not an equivalent substitute |
| [Native server registration](https://raw.githubusercontent.com/ggml-org/llama.cpp/b12177/tools/server/server.cpp), `server_register_routes` |Registers tokenize/template/properties and count-only chat routes; explicit-model instance differs from router mode |No public Ollama count endpoint or verified installed behavior implied |
| [Native request implementation](https://raw.githubusercontent.com/ggml-org/llama.cpp/b12177/tools/server/server-context.cpp), `post_tokenize`, `handle_completions_impl`, embedding handler |Token endpoint exposes IDs with explicit special-token flags; text generation and embeddings use shared input preparation with special insertion/parsing |Must validate the actual selected Ollama preprocessing, model metadata and context/output policy |
| [Immutable native helpers](https://raw.githubusercontent.com/ggml-org/llama.cpp/6c01da6278ab6c69ed67d9124806b50d2b299ba7/tools/server/server-common.cpp), `tokenize_mixed`, `tokenize_input_subprompt` |Plain strings pass through the shared tokenizer helper; token arrays take a different path |Test allowed plain-text shapes only; no synthetic token-array shortcut |

The pinned [server documentation](https://raw.githubusercontent.com/ggml-org/llama.cpp/b12177/tools/server/README.md) describes token IDs, separate insertion/parsing flags and properties including context/build information. Those observations support designing a reference; they do not prove safety, renderer equivalence, an exact EOS margin or the model identity returned by a running process. Medium web responses sometimes returned extensive matching context; no long response was requested and no source dump was echoed through shell reporting.

## Credible route and unresolved gates

The [staged validation design](../proposals/standalone-tokenizer-parity-trial-design.md) keeps production counting standalone and Ollama responsible for generation/embedding. A later controller would use the exact same verified packaged native executable/DLL set as a temporary reference with explicit local model path, CPU-only settings and a directly retained process identity. It must reject wrong binary/model/options/socket ownership, router/autoload/remote/tool/media paths and unexpected child processes. No custom build is assumed necessary.

Local artifact identity and all native license/advisory/provenance reviews are still blockers. Source equivalence must include Ollama compatibility overlays and actual runtime rendering/BOS preprocessing, not merely upstream tokenizer IDs. Context clamp, reserved output/EOS, truncation/shift and model drift require evidence; unknown overhead remains unavailable. Native chat count routes are candidates, not automatically equivalent to the selected Ollama branch. Embedding prefixes/normalization/CLS/SEP require their own checks.

Sequential heavy workloads are proposed: capture approved synthetic rendering under a frozen identity, fully tear down the owned model process, then start the reference with the same verified identities, then tear it down before any generation comparison. At every phase boundary reverify source/settings/artifacts and reject drift. This reduces simultaneous loading by design but proves neither16GB fit nor production lifetime binding. Runtime publication/identity controls remain separately testable requirements.

## Tasks and next step

- SV1 completed: clock/full64unit accounting/report reservation before inspection;36prior identities frozen and older preservation checked.
- SV2 completed as conditional source feasibility: pinned build/native revision, compatibility overlay, token/reference operations and effective text-token helper path identified within eightcalls/24targets.
- SV3 completed as draft design only: exact-artifact/dependency gates, staged ownership, synthetic matrix and proposed shared boundaries documented; no executable trial permission.
- SV4 completed as review handoff: findings/status/checkpoint and preservation/link/diff/budget closure retained locally. Eight authored findings/design/status files await separate commit approval.

**Recommend next: prepare bounded static verification of the existing packaged runner/DLL identities and outstanding standalone dependency/native/provenance gaps.** No installation or loading until that evidence supports an exact trial package. Do not revisit the closed public-API search, substitute an upstream binary or broaden runtime versions. Trial design limits are proposals, not permission to run it.

No application tests/Ruff were appropriate for this source/document review. Controlled output was conservatively precharged in4096byte blocks and bounded summaries measured before emission; initial allowance includes bootstrap/Git/error output. Final research/preservation/time/artifact/reporting counters are in ignored `data/t17/standalone-validation-design-01/closeout.json`; no old allocation reopened. Stage1/G2, unchanged16GB CPU-only, formats/OCR/privacy, provisional2,048context192output/R01 and chart deferral remain binding.
