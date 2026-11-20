# T17-IF-PGC — default-expression review and prelaunch checklist

## Outcome

Planning committed as **`1f94a74`**; the user approved PGC1–PGC6. The bounded retained-evidence review produced **14 frames/five groups/15,119 frame bytes**. One syntax-only pass covered fourteen default-graph Python modules: **5,137 AST nodes, 545 records and 59 deferred body spans**. The original projection gap is narrowed; native/offline readiness is not established.

The [proposal](../proposals/tokenizer-prelaunch-gap-closure.md) defines scope and budgets. Ignored evidence lives under `data/t17/tokenizer-prelaunch-gap-closure-01/`: frozen identities, selector controls, occurrence/selection ledgers, `prelaunch-checklist.json`, verification and terminal receipts. No candidate, service or model ran. Earlier PBF and stopped RBF/RSR roots remain read-only.

## Python findings

The single production pass covered root/implementation initializers, BaseTokenizer, five wrappers and six alias initializers. The two tools/visualizer modules remain deferred. Every original file hash and each recorded node's original line range is retained in `python-occurrences.json`; p01–p03 are the complete three-part admitted summary.

No explicit AST `Call` nodes occur in the projected module/class/default/decorator/annotation expressions. Displayed defaults are literals or literal collections; decorator references include properties/setters and static methods; class bases include Enum and BaseTokenizer. Function bodies were deferred, not counted as import-time calls. All fourteen files lack the inspected future-annotations import; annotation evaluation timing remains interpreter-dependent and was not executed or assumed.

This is **not** an absence-of-side-effects proof. Import resolution, native binding initialization, attribute/subscript lookup, decorator application and class construction can have effects without an explicit call expression in this projection. The scanner covers the tested syntax categories; it is not a Python semantic evaluator or a sandbox. The remaining native-initialization contract is separate from the now-completed syntax projection. No further broad Python role/default scan is recommended on unchanged input.

## Server/control-plane findings

The three full saved response envelopes retain their identities. Source is pinned to llama.cpp `6c01da6278ab6c69ed67d9124806b50d2b299ba7` and Ollama v0.40.16 compatibility projections.

- **Routes:** s02–s03 show POST registration of tokenize, detokenize, apply-template, chat-input-token and responses-input-token endpoints in `server.cpp` lines 184–191. Registration does not establish handler payloads, response IDs, special-token policy or parity with Ollama generation.
- **Authentication/bind:** s01 shows the wildcard-CORS/no-key warning at lines 233–235 and an authentication-error mapping. Neither establishes request authentication enforcement, exact defaults or localhost binding. Those facts remain missing from the reviewed projections.
- **CPU argument:** corrective s07 shows the numeric/automatic/all assignment branch in `common/arg.cpp` lines 2667–2676. Zero is a numeric setting; exact CPU-only packaged execution, device selection and DLL loading remain unverified.
- **Build overlay:** corrective s08 shows compatibility inclusion before source fetching and compatibility sources added to the llama target. Upstream source alone is not proof of the packaged server's complete behavior or load set.

The first server packet admitted some unrelated draft-flag, error-helper and generic “before” context. Those rows are not used to establish missing control-plane contracts. A source-aware corrective packet supplied exact setter/build spans **within the remaining server quota**. Earlier frames and their charged bytes were retained; no quota was refunded. All omitted/matching rows and source coordinates remain in the ledgers. Partial projections cannot establish absence of a feature or stand in for complete handler bodies.

## Finite prerequisite checklist

The data checklist assigns evidence, gate and exact next action to each item:

| ID / question | Current disposition and gate |
| --- | --- |
| G01 — Python projection | Closed for reviewed syntax. Implicit/native effects remain outside that conclusion. |
| G02 — Native initialization/local-file API | Before native launch: establish the pinned binding initialization/local-file contract and exact candidate correspondence. Actual local-only behavior still requires runtime validation. |
| G03 — Bind/auth/routes/request | Route names supported; bind/auth enforcement and handler payload/special-token contracts remain prelaunch source/API gaps. |
| G04 — CPU/DLL/patched reference | Numeric setter and overlay supported. Complete selected DLL/backend/search/launch policy and exact packaged mapping remain prelaunch controls; actual loading is a runtime check. |
| G05 — Graph/ABI/provisioning | Retained graph has seventeen global nodes and seven installed-metadata records. These do not supply a final artifact/reuse/lock/ABI plan. Complete project-venv-only provisioning must be reviewed before installation or a native trial. |
| G06 — Notices/provenance/timing | Existing partial native/vendor/build evidence and Hub/FSSpec metadata-only timing conditions remain binding. Unconditional installation/adoption is not cleared. A trial-only risk exception would need missing evidence and exact permitted actions stated explicitly; none is granted here. |
| G07 — Weight/tokenizer identity | Reviewed static asset/model-manifest claims do not establish exact cached GGUF-weight mapping. It is unverified, not asserted absent. Current scope forbids model-store/payload inspection. |
| G08 — FP/NP coverage | All FP01–FP08 and NP01–NP08 identifiers match the frozen designs. A complete request/settings/start/resource/teardown schedule is needed before launch; actual rendered IDs/BOS/EOS/template/prefix, embedding policy and negative/regression passes are runtime evidence. |
| G09 — Execution/privacy/resources | A future package must define actual host permissions/isolation, local endpoints, owned capture/teardown and shared budgets. This static package is not filesystem confinement or a native network boundary. No previous disconnected-trial exception is inherited. Preserve the approved CPU/latency/memory targets. |
| G10 — Optional paths | Wrapper/training/SPM/visualizer bodies stay deferred unless selected later. This does not remove any mandatory dependency or waive Stage 1 acceptance. |

The saved runtime worker record has a stopped status; successful earlier static observations are not a new runtime pass. The saved 75-file inventory is not a complete chosen DLL load set. The combined asset record's static-identity status does not prove cached-weight/tokenizer equivalence. Original [controlled-trial prerequisites](../proposals/controlled-local-file-tokenizer-trial.md) and [local-file comparison](../proposals/local-file-tokenizer-comparison.md) remain authoritative for these distinctions.

## One recommended next direction

Prepare **one finite pinned-source plus local-metadata request** for the remaining facts. Do not repeat the unchanged wheel/archive/role review or expand optional helpers.

| Fact needed | Target for the next proposal; no access authorized here |
| --- | --- |
| Binding initialization/local-file boundary | Tokenizers commit `301277072263fb3830eb66eec7e47adadf76f1dc`: `bindings/python/src/lib.rs` and only necessary tokenizer/core context. Candidate path existence must be checked rather than assumed. |
| Handler payload and HTTP enforcement | Pinned llama.cpp `tools/server/server-context.cpp`, relevant `server-common.cpp` context and the actual HTTP bind/auth implementation. `tools/server/server-http.cpp` is an **unverified candidate path**, not a reviewed file. |
| CPU/reference launch and loader policy | Ollama v0.40.16 `llm/server.go` and necessary compatibility/build context. Retain overlays; no upstream-binary substitution, custom build or large archive repeat. |
| Exact weight/model/tokenizer mapping | Separately bounded local metadata-only evidence, with explicit paths/privacy limits. No model payload read, model-store access or acquisition is approved by this report. |

The next proposal must name calls/targets/read limits and close with supported or precisely missing facts, without automatically widening research. Compare this with holding standalone-tokenizer work, which requires a separate input-fit direction, or preparing a concrete trial-only residual-risk proposal after indispensable facts/actions can be stated. A generic waiver or native trial now is not recommended. Any later risk acceptance, runtime adoption/G2 and stage transition remain distinct user decisions.

## Controls and closeout

Entry verified **89 identity rows**, including carried protected inputs and six previously reviewed skill files. Parent smoke plus duplicate, undercharge, stopped-state, start-cap and zero-write report controls passed; prepaid prelude accounting is separate from the gateway subgraph.

Test-first controls reproduced deferred function-body misclassification, then passed **fourteen inert cases**, caught the deliberate mutation and passed again after exact owned-source restoration. The unchanged formatter handled exact escaped-byte boundaries and zero-write refusal through the actual packet/reader path. No pytest/Ruff or application suite ran; these are owned inspection controls, not native or product tests.

The checklist check confirmed all sixteen frozen FP/NP groups and packet quotas: Python **4,346**, server including correction **7,315**, readiness **3,458** bytes. Selected occurrence/selection data total **135,809 bytes**; one production candidate parse only. No source capture was truncated or falsely described as a complete source file. Server selection quality was corrected without hiding its first packet.

Final closeout verifies preserved identities, exact authored scope, local links, UTF-8/whitespace, readable tracked/new-file changes, empty index, control/frame integrity and known owned exits. Exact reserved/observed starts, time, explicit reads, measured artifacts and terminal-tail accounting are retained in the local receipt. Optional work finished at **34 reserved starts**; no unapproved work uses the remaining allowance.

No public calls, downloads, installation/resolver, candidate import/evaluation/executable compilation, native/model/service run, wheel/archive/model/tokenizer payload read, model-store inspection, global change or checkpoint write occurred. There is no newly usable application feature or runtime adoption. Five result documents await review/commit; the next request package is not yet authorized.
