# T17-IF-EA — explicit marker profiles and conditional dependency comparison

**Proposed; EA1–EA6 execution and the four-file planning commit await approval.** MG results were committed as `a0578ce`. The user approved that commit and preparation of this environment-adapter review. Preparation read local source as text; no factory override, import, trial root or new parser run occurred.

## Source review and alternatives

[MG findings](../benchmarks/marker-environment-guard-review.md) establish that default Windows platform discovery requested a denied subprocess. Keep that restriction. Packaging 26.3's `Marker.evaluate` first calls its module's public `default_environment` function, then merges the supplied dictionary; passing a dictionary alone therefore does not avoid discovery.

Read-only inspection also found that missing marker fields are translated to the public `UndefinedEnvironmentName` exception. Evaluation visits compound-expression components rather than guaranteeing short-circuit behavior. Missing facts must consequently remain conservative **unknowns**, even when another component might imply an inactive edge.

| Approach | Benefit / cost |
| --- | --- |
| Temporarily replace the public environment factory in an isolated review child | Small, version-pinned change; retains public marker evaluation and strict audit restrictions. This is an explicit in-memory library override, **not a documented dependency-injection extension or an approved product integration**. Requires tests for restoration, missing facts, profile separation and no discovery. Recommended for this bounded review only. |
| Write a separate marker evaluator | Avoids the override, but duplicates grammar/comparison/extras behavior and adds substantial correctness/maintenance risk. No implementation proposed. |
| Allow the Windows helper subprocess | Preserves discovery, but widens execution and descendant-management boundaries. Not proposed; keep subprocess denial. |

The proposed package validates the adapter first. **Only if those checks and the original ten controls pass**, continue into a local dependency/lock comparison using already retained metadata. This conditional step is new proposed scope for approval; it avoids another task-start gate after passing tests. Licence/native/source-provenance research, installation and adoption remain separate.

## Exact tool, inputs and boundary

Use existing `F:/Python/Python314/python.exe -I -S -B` (record its actual version), standard library, and existing project-local **packaging 26.3** as a review tool. Its recorded licence is Apache-2.0 OR BSD-2-Clause. No installer, new dependency, interpreter change, global site-packages, model or cloud service.

Verify these immutable inputs before reuse. MG paths below are relative to `data/t17/marker-environment-guard-01/`:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| MG `guard-before.txt` — original strict policy | 422 | `c58b576024f5efaa341fb324295d8aa98c81ad3b45be735e5db58611fe758490` |
| MG `capture.py` | 4,482 | `15849ddbd03c992da78baee314b48731c036d7ab5563e1719e61892f64b590d3` |
| MG `tool-verified.json` | 3,354 | `ceac44262e5538db67fac59f1bc63bfcc40c59186ddcf5884ba46e30bbb68531` |
| MG `tool-metadata-freeze.json` | 419 | `f74181e8de5730bbacfa87eeffb6e444c9976a3f2bdacf6e1929a103ce3d9333` |
| MG `summary.json` | 3,523 | `9feb4885bba1b9d89fb7ca0b87c11953dc3c0f4183376aef4775974c4211bddd` |
| `data/t17/reconciliation-capture-correction-01/parser_controls.py` — authored fixture source | 3,072 | `41261c05e5f876c72a24b1a0818650e58a562209e46359b8fc3858b526fcbc53` |
| `data/t17/wheel-artifact-review-02/inspect-result.json` | 127,374 | `2b03271be8c491c648ba2d5e31d9fe86cf112d9180bad06788b4e03afdf73141` |
| `docs/benchmarks/marker-environment-guard-review.md` | 7,932 | `9c420e756af4aaef4654a4d2436c5e9433e22cfeb9b933220b3ffa594ff47fe1` |
| `.venv/Lib/site-packages/packaging/markers.py` | 20,554 | `6cbe860d35d98d2b599e7f0ec73feab124e015711b30be9045e678c92940d9cc` |

Revalidate all 20 installed packaging source identities and both installed metadata identities from the saved inventory. Read current `pyproject.toml`/`uv.lock` as data. Do not execute old top-level dispatch or reopen wheels, archives, native payloads or model files. Do not inventory global installations or user documents. The retained evidence fixes the same eight acquired candidates plus Hub 2.4.0/Tokenizers 0.23.3; it does not authorize selecting or changing them.

## Proposed adapter contract

- Restore the **original strict audit policy**, including denial of every `socket.*` event, hostname queries, subprocesses, native-library loading and unreviewed imports. MG's hostname exception is not carried into this package. Install the guard before tool imports/evaluation that might discover the environment. Admit only the reviewed packaging package and standard library; no broad site-packages path.
- Inside a bounded `try/finally` context, save `packaging.markers.default_environment`, replace that public factory with a reviewed function returning a **fresh dictionary**, then restore the original function even on failure. Do not change installed files, private helpers/marker trees, private caches or platform functions. Do not prewarm discovery before installing the guard.
- Construct observed interpreter facts from `sys.implementation`, `sys.version_info`, `sys.platform` and `os.name`. Validate the actual CPython/final-version assumptions; unexpected values stop rather than inventing a format. Record the exact supported fields and their origin. The already approved hypothetical Windows CPython 3.11.0 case is a separate profile with clearly labelled version assumptions, not executed Python 3.11 or a deployment decision.
- Leave unobserved `platform_machine`, `platform_release`, `platform_system` and `platform_version` absent. Never fabricate OS release, machine identity or hardware values. Known CPython implementation naming can be derived explicitly from the verified implementation identity. Preserve public metadata-context/extras behavior.
- Handle only the library's expected missing-environment exception as an **unknown marker** with its field identified. Do not turn missing facts into false/inactive or compatible results, and do not swallow unrelated errors. Compound expressions may conservatively remain unknown. Keep profiles and per-call dictionaries independent.
- Tests and real controls must use the same factory/adapter source. Demonstrate no original-factory call while active, restoration after success/error, no original-profile mutation, correct active/inactive/unknown outcomes and preserved denied audit decisions. Do not claim this override is supported beyond the pinned review or adopt it in the application.

## Ordered tasks and acceptance

| ID | Objective / prerequisite | Acceptance / evidence | Status |
| --- | --- | --- | --- |
| EA1 | After approval, bootstrap/freeze and inspect exact source/commands | Fixed inputs/tool identities and strict guard checked; unchanged copied capture aid, allowed functions and profile contract reviewed; no old dispatch or discovered platform values. | Pending approval |
| EA2 | Execute meaningful RED before adapter implementation | The unchanged public-evaluation path still reaches prohibited default discovery despite an explicit dictionary; retained expected failure. Write adapter/graph behavior tests before corrected implementation. | Pending EA1 |
| EA3 | Implement review-only adapter and run GREEN | Fresh-profile/restoration/error/missing-field/extras/compound-marker tests, original strict policy checks and graph status/global-cap fixture tests pass. No real networking/helper execution or installed-file patch. | Pending EA2 |
| EA4 | One original ten-control attempt under the adapter, after EA3 | Same reviewed fixture semantics; complete admitted stdout/stderr/exit/teardown. No discovery exception or platform-cache workaround. A complete failure ends the attempt and blocks EA5. | Pending EA3 |
| EA5 | Conditional local graph/lock comparison only after EA4 passes | Two labelled partial profiles, active/inactive/unknown edges and conflicts/missing metadata explicit; 20-node global union; no resolver or pin change. Retain the full bounded result plus concise findings. | Pending EA4 |
| EA6 | At completion/stop, readiness and closeout | Resource/ownership/deviation evidence and blocker matrix; source/config/prior-root preservation, scope/links/whitespace/readable diff/empty index/non-null receipt. Separate results-commit/adoption gates. | Pending completion/stop |

Use the already reviewed incremental, test-first, security, quality-review and documentation workflows. Keep scripts/fixtures ignored. RED must run before the corrective implementation is authored; no recreation of the historical CC authoring-order deviation.

## Conditional graph rules

Start with the ten fixed artifact identities in the retained inspection result; no optional root extras. Propagate only extras required by a known active edge. An edge is active if an evaluated context establishes it, inactive only if every applicable context is false, and otherwise unknown. Preserve inactive/unknown requirements and reasons. Missing platform fields can leave the graph partial.

At most **20 distinct (normalized distribution name, exact version) nodes in the union across both profiles**, including roots. Do not reset the cap per environment. For additional names use a unique retained lock version; multiple/no lock versions are unknown/missing, not permission to choose a version. Read matching project-local installed METADATA only, at most 256 KiB/file, verifying Name/Version and freezing its hash. If matching metadata is unavailable, preserve unknown transitive closure. Direct URLs are unresolved inputs, not fetch authorization.

Compare incoming specifiers, fixed candidates, current lock versions and relevant declared project/group constraints. Report satisfied, conflicting, missing and unknown separately. Do not drop existing roots, replace package names, override pins, call a resolver or infer runtime/ABI/security compatibility. Requirements not retained in the evidence remain unknown. Graph fixtures must cover these statuses, missing-field propagation, extras and the shared cross-profile node cap before the real comparison.

## Shared execution limits

Fresh ignored root **`data/t17/marker-environment-adapter-01/`**; refuse an existing root/reparse ancestor. Bootstrap before optional reads. Older roots remain read-only. The parent alone owns shared accounting and prepays non-refundable leases for all shell/controller/child, test/negative/regression, graph and Git-check starts. A counter for only one child is insufficient.

| Resource | Ceiling |
| --- | --- |
| Work | 64 prepaid units: bootstrap/source 8; adapter/GREEN 16; original controls 8; graph 16; protected closure 16. |
| Time | 1,800 active seconds; optional cutoff 1,200, closure reserve 600. |
| Processes/checks | 32 owned starts total; four ordered check invocations: RED, GREEN fixture suite, original ten controls, conditional real graph comparison. Zero Ruff, web or model runs; no extra capture-suite rerun. |
| Children | Exact allowlisted interpreter commands without a shell; at most 60 seconds plus 15 seconds teardown. Hold direct handles/PIDs through exit; no fixture/parser child may spawn descendants. |
| Reads/disk | 64 MiB explicit streamed-read leases including 8 MiB ledger allowance; 16 MiB retained artifacts. No claim of total OS/interpreter I/O accounting. |
| Reports/ledger | 64 KiB aggregate reporting with 16 KiB closure reserve; 8 KiB combined raw host/child streams per invocation, 3,000 UTF-8 displayed bytes; at most 48 immutable records/validations, 4 KiB each. Authored graph JSON at most 2 MiB; it is not console output. |

The capture aid must retain its verified bytes; historical capture tests are reused, not reported as new runs. Save admitted diagnostics before display; withhold planned oversized displays. Both stream EOFs and child exit are necessary for complete capture. No filesystem confinement, Job, kernel egress or memory guarantee is added or claimed.

Expected RED, handled policy denials and intentionally unknown marker fields are planned controls. Unexpected GREEN failure, unsafe input/tool identity, cap/cutoff, host denial, actual output loss/truncation or uncertain ownership stops optional work. A complete original-control failure blocks the graph; a bounded partial graph is reported honestly. No automatic reruns, private-cache patch, wider exception, installation or accounting reset. One trustworthy orchestration correction is allowed within these limits.

If permission prompts are necessary, allow at most two measured submission-to-entry/decision-observation waits totalling 24 hours, with no intervening model work. Exclude no ordinary work and report wall/active/host time separately. Routine covered steps do not require repeated project approval.

## Deliverables and approval

After approval: ignored source/tests/profiles/capture/graph/accounting receipts; `docs/benchmarks/marker-environment-adapter-review.md`; affected updates to this proposal, dependencies, input-fit preflight, PLAN, TODO and README (**seven versioned closeout documents maximum**). Preserve AGENTS, SPEC, pyproject/lock, existing versioned tests/manifests, historical checkpoints and unrelated user files. No runtime candidate install/import, public research, licence/native adoption or product implementation.

Passing adapter/marker checks and a local graph only supports the next dependency/licence/provenance decision. It does not approve the override for runtime use, select packages, close G2 or advance Stage 1. Explicit unknowns/conflicts remain blockers for later user review.

Request approval for **EA1–EA6**, explicitly including the isolated public-factory override, original strict guard, labelled partial profiles and conditional local graph comparison. Separately approve the **four-file planning commit**: this proposal, PLAN.md, TODO.md and README.md. Preparation alone does not authorize execution or that commit.
