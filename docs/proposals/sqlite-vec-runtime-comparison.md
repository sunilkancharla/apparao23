# T12 PartB — Proposed disconnected SQLite/vector comparison

**Status: approved for this exact package, its execution boundary and five planning documents' commit.** The user explicitly approved all three and requested durable checkpoints because the session token allowance was running low. Companion notices were previously accepted in `48cdf72`. No DLL has been staged or loaded, no package installed, and no new runtime allocation or executable handoff created. Resume at T12-B1 without asking for this unchanged approval again. T12/G2 and product lifecycle/scale acceptance remain open; later preparation/source/results commits retain separate gates. The requested-approval paragraph below is historical.

## Purpose and exact artifacts

Compare the baseline's Python exact cosine search over SQLite BLOBs (A) with sqlite-vec0.1.9 `vec0` cosine search (B), using identical scoped synthetic float32 vectors and recovery checks. This is an exploratory small-scale comparison, not full Stage1 volume/quality acceptance. All previous allocations remain closed.

Reuse only the cached [statically reviewed wheel and DLL](../benchmarks/sqlite-vec-artifact-review.md), with the [accepted notice exception](../decisions.md):

| Artifact | Exact identity |
|---|---|
| Wheel | `sqlite_vec-0.1.9-py3-none-win_amd64.whl`,292804bytes,SHA-256 `4a28dc12fa4b53d7b1dced22da2488fade444e96b5d16fd2d698cd670675cf32` |
| DLL member | `sqlite_vec/vec0.dll`,289280bytes,SHA-256 `fcf98662a7ad9dce394b96a88f91032047823831b951c76636787c312a6476e6` |
| MIT companion | 1068bytes,SHA-256 `6ce72bbe12d975bd5286e5ab0a064c069693300c47bccbc57bec18485f1621ea` |
| Apache companion | 10931bytes,SHA-256 `a38070a94d4afd9cd710e3ce67bd1de78097cfe1784c1f0109ac95d3c196bfdc` |
| Source identity | Upstream commit `e9f598abfa0c06b328d8fe5da9c3760cce74be10`; matching helper AST and static DLL findings retained |
| Interpreter/SQLite | Existing project Python3.14.6,64-bitWindows; SQLite3.50.4 observed in PartA. Verify actual executable/DLL identities and SQLite build before preparation; stop on drift |

Hash-check every cached artifact against its completed receipt. No substitution, download, new native redistributable, source build or repair of old ledgers/seals. Missing runtime requirements stop the package.

## Native staging approach for this evaluation

Propose staging **only the verified DLL and both notice texts** under `F:/document_assistant/.venv/.cache/sqlite-vec-review/part-b-01/`, keeping the unchanged wheel/receipt identities linked. This is a project-local native-asset trial, not a Python-distribution installation: no pip, uv sync/lock change, wrapper import, NumPy initialization, PATH/global/service or application default change. Existing Python packages remain untouched. A future runtime Python dependency requires its own evaluated uv/pyproject/lock review. This staging choice is part of the approval requested here.

Use the reviewed ZIP reader to locate/hash the DLL without executing archive code, then write only fixed named outputs beneath the checked new cache root. Refuse existing nonmatching assets, links/junctions, path escape or missing notices. Create no executable frontend/SQL startup hooks. Preserve the license omission and incomplete binary/source-build provenance; do not repackage the wheel or declare redistribution/security clearance.

During the later **disconnected worker only**, rehash the full approved DLL path, open a dedicated synthetic SQLite connection, enable extension loading immediately around that exact absolute path, then disable it in a `finally` path. Never import `sqlite_vec` or load via environment/PATH/discovered filenames. Verify native reported version and required SQL functions/module before measuring. No startup download/fallback, extra entrypoint, arbitrary user SQL or optional NumPy/file-based function call is permitted.

## Shared resource and execution allocation

| Boundary | Proposed limit |
|---|---|
| Total starts/attempts | 96 shared, including all shells/tools/Git/tests/controls/controller/workers/native descendants/report/cleanup |
| Categories | Preparation24; fake tests16; native workers32; reporting16; protected cleanup8 |
| Time | 30active connected preparation minutes; one45-minute disconnected epoch including controls/loading/measurements/cleanup; human/host approval waits excluded |
| Worker deadline | 120seconds per owned worker, no retry or extension; shared epoch also enforced |
| Memory | 2GiB aggregate controller+worker job; controller-private512MiB sampled; at least4GiB free physical RAM |
| Concurrency | One controller and at most one worker; no native descendants permitted beyond the counted root worker |
| Monitoring | 100-ms work-aware target;300-ms hard completed-reading/collection/full-iteration gap. Software checks are not kernel real-time guarantees |
| Added storage | 512MiB run outputs/database/journals/fixtures; staged DLL+notices capped at1MiB separately, all paths accounted |
| Downloads / API calls | Zero; no Ollama, OCR, cloud grader or model inference |

The larger process allowance covers both adapters' real termination/reopen controls, performance workers and refusal sentinels; it is not an increase to the closed PartA budget. At most24native worker starts are planned, with up to8additional accounted slots reserved for setup/unknown-descendant detection, not retries. Category ceilings cannot be borrowed; cleanup reserve cannot fund normal work. An unexpected descendant still stops even if unused slots remain.

Initialize fresh ignored `data/t12/sqlite-vec-runtime-01/` only after approval. Reserve initial inspection/initialization commands before launch, then count successful and failed commands and native processes durably. Link the closed PartA and artifact-review budgets, baseline's three authored source/fixture files and the artifact inspector's two source files (seven prior records). Include exact cached wheel/DLL/notices and interpreter in the fresh source/artifact seal. Recheck linked identities before handoff and after results; no old file/state mutation.

## Frozen comparison and controls

Use fresh synthetic fixture directories in the new allocation. Reuse `t12-synthetic-v1` generator/seed12001+scale,768float32 little-endian normalized components,12queries,top5,first+three repeated passes,1e-6distance tolerance and stable source/chunk IDs. **This package measures32and1000rows only.** Their vector/query hashes must equal the corresponding saved PartA identities; inspect only those synthetic identities, not old vectors/user content. The10000-row timeout stays unmodified; no10000-row run, smaller replacement labelled as10k, baseline optimization or silent deadline extension.

Run A and B in separate serialized workers for each size, with A then B as a frozen order. Explicitly report cache/order bias; neither first pass is controlled cold cache. New A measurements belong to this new approved experiment; they are not a retry/reset of the old allocation. Measure identical stage boundaries: fixture creation excluded from query timing; scoped eligibility/readiness/decoding/ranking included as applicable. Separately report insert, native-load, query, delete, rebuild, reopen/integrity time, all query samples, database/journal bytes and aggregate/per-worker memory where actually observed. Do not fabricate a causal speedup or apply a product latency threshold that has not been agreed.

B must maintain stable chunk-ID/integer-rowid mapping and transactional consistency of metadata, references and `vec0` rows. Declare cosine metric explicitly. Filter against authorized eligible IDs **inside candidate selection**, not by dropping unrelated results after global topK. Compare both adapters against an independent exhaustive reference on the same frozen float32 values. Include closer excluded rows, missing originals, invalid vectors, model/prefix/extraction mismatch, duplicate ownership, ties at the cutoff and fewer-than-five/empty scopes. If exact filtering or deterministic boundary-tie handling cannot be established for this pinned extension, stop/record incompatibility rather than changing metrics or silently replacing B with a different algorithm.

Preparation may inspect the already cached pinned source to design the SQL; unsupported query/API behaviour is a trial finding. The attempted public fetch of the pinned upstream tests during proposal preparation was unavailable; no inference of compatibility is made from it. No extra public retrieval is authorized in this no-download package.

### Security and interruption checks

- Before loading, missing/wrong DLL and missing companion texts must refuse with no load attempt. Use local synthetic failures/fakes for wrong identity; never load a modified or unapproved binary. Test that loading is disabled on both success and exception paths. Observe actual native version/module availability only after offline attestation.
- No arbitrary SQL/document strings enter SQL execution. Parameterize data and fix schema/statement identifiers. Propose a connection authorizer that denies `ATTACH`/`DETACH`, SQL `load_extension` and the optional filesystem/static-pointer functions identified in the pinned source, while allowing required fixed vector queries. Agree the explicit allowed SQL/function surface in reviewed preparation before sealing; stop if it blocks required safe operations instead of widening it silently.
- For each adapter, run the four PartA real termination boundaries (before/after commit, original file before metadata commit, metadata commit before staging cleanup), followed by separate counted reopen workers. Require exact reference/chunk/vector counts, SQLite integrity/foreign-key checks, expected scope and pending/ready/orphan reporting. Record extension virtual-table transaction limitations rather than claiming atomicity from base tables alone.
- Preserve approved chat-exclusive deletion/shared-library preservation and referenced-library blocking. Original bytes can be shared without sharing ownership/scope. Fixture-only deletion/reconciliation must resolve allowlisted roots and ownership before mutation, leave unknown files untouched, and retain opaque historical records until product retention decisions exist. No secure-erasure/power-loss guarantee.
- Deadline/memory sentinel workers and fresh-run/old-ID/no-ID refusal tests share the same allocation. Normal workers launch suspended, receive the job boundary before resume, and are killed/reaped only through owned handles. No old baseline/helper CLI is run; reusable trusted helpers may be imported with paths bound only to the new synthetic allocation, without editing those old source files.

## Disconnected native boundary

The DLL is native code with the user's Windows account filesystem access: **this package has no filesystem confinement**. Use only new authored synthetic data. The user must physically disconnect Wi-Fi/Ethernet/tethering/every external link and attest OFFLINE before any DLL load. Remain disconnected until verified zero owned workers, controller teardown and an explicit safe-to-reconnect message. Kernel job/resource checks and SQL restrictions do not replace this boundary or prove complete native containment.

Connected preparation may stage/hash the cached DLL/notices, generate synthetic definitions, run fake tests, inspect SQLite build settings without loading the DLL, parse PowerShell syntax and seal the standalone runner. It may not load/import the extension or run baseline performance workers. No runnable command is issued until actual independent readiness passes. Source/config/asset drift, reconnect/egress, unexpected file/SQL/native behaviour, wrong identity/version/scope, resource/accounting/budget failure or uncertain cleanup stops without retry/reset/reseal. Do not change firewall/permissions/Windows scheduling or reopen the earlier AppContainer chain.

## Ordered work and evidence

| ID | Prerequisite / task | Acceptance and verification |
|---|---|---|
| T12-B1 | Exact approval; fresh shared allocation and contract | Seven prior hashes, exact artifacts, fixture identities, SQL/function allowlist and resource/measurement boundaries recorded; counted initial commands |
| T12-B2 | B1; evaluation adapters/controller test-first | Red/green scoped ranking/reference/ties/version/transaction/refusal and no-download fake tests; no connected native loading; at most three new authored evaluation files |
| T12-B3 | B2; stage and independently seal readiness | DLL/notices under new project-venv cache root, all hashes match; frozen selected sizes/query hashes, interpreter/source/SQL settings and PowerShell syntax verified; actual counters/time and no-load evidence reported before handoff |
| T12-B4 | B3; user-operated disconnected controls/comparison | OFFLINE attestation before load, native identity/security checks, both adapters' four crash/reopen cases and fixed32/1000measurements under shared ceilings or truthful partial stop |
| T12-B5 | Execution starts; verified owned teardown | No remaining worker/descendant; handles closed, final marker and safe reconnect message; uncertain cleanup means remain offline; no retry |
| T12-B6 | Verified teardown/reconnection; findings and next decision | Report ranking/integrity/privacy/performance/footprint, loading/artifact limitations, complete counters/hash preservation and missing coverage; request separate source/results commit; do not infer adoption |

Source scope is at most three new evaluation files: `sqlite_vec_runtime.py`, `test_sqlite_vec_runtime.py` and a frozen schedule/SQL manifest. Import existing reviewed standard-library helpers where suitable; preserve all older source/fixture identities. Update PLAN/TODO/README/checkpoint, this proposal and factual readiness/results reports/handoff as actual evidence becomes available. No product schema or frontend changes.

T12 remains incomplete for larger scales and any unresolved integrity/privacy gates even if this initial paired subset succeeds. Product retention/derived-storage limits, representative capacity/latency budgets, physical16GB end-to-end validation and T17/G2 final adoption remain explicit decisions.

**Requested approval:** this exact96-start,30-minute preparation/45-minute disconnected package; fixed32/1000synthetic workloads; cached DLL-only staging under project `.venv` with accepted companion notices; and manual disconnected native execution without filesystem confinement. Separately approve committing these five planning documents. This does not authorize Python package installation, downloads, optional NumPy/filesystem functions, old10k reruns, product coding, further limit changes or adoption.
