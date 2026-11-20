# Standalone tokenizer parity — staged trial design, not execution approval

## Readiness

Draft produced under [IF-SV](standalone-tokenizer-validation-design.md), based on [source findings](../benchmarks/standalone-tokenizer-validation-design.md). Not an executable bounded trial package. Missing exact local runner/DLL manifest, native notices/advisories/provenance closure, standalone dependency graph approval and installed/offline API evidence prevent provisioning or trial execution. Do not install, build, launch a model or prepare a runnable handoff from this document.

Use only the already pinned Ollama/model/publisher-tokenizer identities. Native reference source candidate: upstream b12177 / `6c01da6278ab6c69ed67d9124806b50d2b299ba7` **plus Ollama v0.40.16 compatibility sources and patches**. The actual reference must be the verified packaged runner used by the selected runtime, not a freshly fetched upstream binary. No new custom build assumed.

## Prerequisites before any executable trial proposal

1. Static binary/DLL inventory with exact paths/hashes/sizes, expected Windows CPU build, package/source mapping and native licenses/advisories. Verify allowed loader search paths; no global/PATH change or unreviewed DLL fallback. No native loading during static review.
2. Full required standalone dependency/artifact review, local-only loading contract and approved project-venv provisioning. Existing two wheels are observations, not installation approval. No remote tokenizer/model loading, custom code, cloud fallback or package extras.
3. Identify exact selected Ollama rendering branch, generation-specific preprocessing/BOS policy, Nomic prefix/normalization/boundary tokens and effective context/output/EOS semantics. Explicitly bind render/count/generate/settings/evidence identities and fail closed on unknowns. A generic native count endpoint cannot settle a different rendering branch.
4. Approve a finite authored synthetic corpus, exact cases/schedule, fake tests, native request/start/time/artifact/memory limits, offline/host boundary and teardown controller before provisioning or execution. No private documents or prompts.

## Proposed stages

| Stage | Operation | Admission / evidence |
|---|---|---|
| Fake contracts |Test-first packing/admission/identity/request/owner failure handling; mutate a boundary guard |Meaningful red/green, caught mutation, lint/format; all subprocess/control work in one meter |
| Freeze |Verify all artifacts, source/request/settings and corpus identities |No missing hashes/unknown generation branch, no unsupported shapes |
| Render |Owned Ollama renders synthetic complete inputs, separately for each approved branch |Exact bytes remain local; record hashes/identity summaries, no payload logs |
| Teardown |Stop/reap owned runtime/model and verify port release |No concurrent reference load or attach to unrelated process |
| Native reference |Start exact runner directly with retained process/birth identity and explicit local model/loopback ownership |CPU-only, single model/slot, no router/autoload/remote/media/tool/download path; verify context/build identity and reject unexpected children |
| Compare |Count identical effective strings using reference flags and standalone adapter |Exact IDs and counts required where specified by frozen parity matrix; compare actual effective policy, not just raw text |
| Teardown / generation cross-check |Reap reference, reverify identities, then use owned Ollama only for approved synthetic generation/embedding checks |No overlap; reject reload/settings/source drift; post-generation usage is supplementary evidence |
| Close |Verify all owned processes/ports stopped, preserve partial results and shared accounting |Mismatch/unknown/timeout stops without retry/adoption |

A directly started reference resolves test-process ownership; it does not grant access to Ollama's existing child. Browser never calls reference endpoints. No arbitrary port/log scanning. Exact future launch arguments, CPU/no-shift/no-truncate behavior, API authentication and request bounds must be reviewed against the verified artifacts; do not invent working commands here. General native server capabilities such as tools/tunnels/remote loading must remain disabled, not assumed absent.

## Acceptance matrix

Carry forward every case in the frozen [FP01–08/NP01–08 design](input-fit-tokenizer-parity-validation.md); this matrix summarizes, not replaces, it.

| Group | Cases | Required result |
|---|---|---|
| Chat text and rendering |ASCII, Unicode, whitespace, empty/explicit system, complete history, evidence/citations, assistant prefix, delimiter-like content |Same complete effective input and policy; exact reference/standalone IDs and counts |
| Special-token negatives |Insertion/parsing toggles, missing/duplicate BOS, model-specific EOS/boundary handling |Correct selected policy matches; deliberately wrong policy caught |
| Embeddings |Query/document prefixes, case/normalization, CLS/SEP, empty/unsupported input |Separate model-specific parity; no reuse of chat count |
| Capacity |Below/equal/above effective context with192output plus proven overhead |No unknown margin as zero; equality only with verified reservation/EOS proof |
| Packing |At most8candidates, complete-history then lowest-ranked evidence removal; mandatory overflow |No extra inference for packing; no silent evidence loss; honest unavailable/partial result |
| Lifetime/failures |Wrong executable/model/DLL/settings, restart/socket reuse, unavailable oracle, malformed response, cancel/timeout, source drift before publication |Fail closed; no stale admission, extra model/download or inference retry |
| Truncation/shift |Attempted overflow and changed effective context |Reject unproven transformation; preserve selected evidence and source identity |

Agreement on synthetic examples alone is not universal correctness. Adoption also needs branch/source-policy reasoning, identity enforcement and retained regression checks. Failure in a required case blocks adoption; do not silently restrict mandatory Stage1 requirements.

## Proposed envelope for a later exact package

For review only: at most60active minutes across preparation/tests/native/control/teardown/reporting;64total counted process starts;256local HTTP transactions including health/render/reference/generation/negative attempts; one heavy model workload at a time, maximum90seconds per answer attempt,8GiB owned aggregate and4GiB available RAM targets on the unchanged16GB CPU-only machine. Proposed local trial output16MiB, excluding pre-existing model binaries/weights; bounded logs/results/partial artifacts included. Synthetic corpus at most24chat and12embedding cases before explicit controls; executable schedule must prove it fits all ceilings and reserve protected teardown before approval. Do not reset counters between phases or omit negative controls.

These numbers are unapproved design proposals, not new product defaults or demonstrated capacity. If source checks cannot prove safe enforcement or the schedule does not fit, revise the package before seeking execution approval. Define actual resource sampling and strict disconnection/host boundaries at that point; no runtime privacy guarantee is claimed from a source-only review. Verified teardown is mandatory before reconnecting for any later disconnected trial.
