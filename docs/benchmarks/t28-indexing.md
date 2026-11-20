# T28 — Versioned local vector persistence and CP10 review

Date: 2026-11-20 (Asia/Calcutta). The user approved the 16-file T27 repair/S2 closeout and instructed proceeding; that commit is `73cb659`. T28 used the existing implementation/TDD/security/review/documentation workflows, existing project interpreter/dependencies and the explicit routine allocation in TODO. No skill script, download, installation, model, OCR or sqlite-vec DLL execution was needed. No historical trial was reopened.

## Implemented behavior

`LocalIndex(store).index(conversation, reference, key, session_factory=runtime.session)` is a trusted backend entry point for an existing complete CSV extraction. The runtime must own the same store and its heavy-work slot. No browser indexing route, startup model launch, query/ranking implementation or alternate vector backend is introduced. T29 consumes this durable index through the already selected sqlite-vec search path; this task stores canonical vectors and metadata in SQLite without loading the extension or creating its search structures yet.

Schema v5 adds canonical generations, ordered vectors, per-extraction bindings/chunks/omissions and scoped request intents. Exact v1/v2/v3/v4 migrations preserve previous metadata and retain exact-schema/version/journal checks. Vectors are pinned Nomic v1.5 document batches: all runtime/model/digest/dimension/normalization/space fields, ordered source IDs, text hashes, complete counts, finite nonzero normalized 768-component vectors must match before freezing exact little-endian float32 bytes. Each vector is 3,072 bytes; it is not renormalized after freezing.

Generation identity covers content SHA256, format, parser/extraction/normalization versions, chunk policy/version, embedding space and float32 storage version. Filenames, conversation/document/extraction IDs and membership are separate. For two identical CSV uploads with different names/conversations, tests observe **one generation/two vectors**, **two source bindings** and only **one embedding session**. Each binding keeps its own chunk IDs, filename, source/extraction/unit identity, anchors and warnings. A different conversation cannot read the other reference. Text equality is checked in ordinal order before reusing vectors; a mismatch rolls back the new binding without failing the shared complete generation.

Requests have durable processing/complete/failed states, including binding-only reuse failures. Completed-key replay returns the same receipt without another embedding session. Failed keys do not silently restart; an explicit new key creates a new attempt. Changed current identities do not reuse old generations or replay old keys; historical operation status reports `reindex_required`. Old generations remain retained and charged under the existing processed-data policy; no eviction, compaction or deletion policy is added.

## Atomicity, resource and status boundaries

The controller verifies originals before admission and immediately before publication. It streams stored source units through T26, submits at most eight chunks per embedding batch and uses existing growth/page/journal accounting before storing payloads. A short durable intent precedes a single publication transaction containing vectors, source bindings, chunks, omissions and completion. Commit follows verified runtime teardown and source revalidation. Failure, cancellation, quota refusal or uncertain native cleanup cannot publish a partial generation; uncertain cleanup also blocks admission.

The single write transaction intentionally spans embedding awaits and teardown, matching the existing serialized extraction/store approach. This keeps metadata/vector publication atomic with SQLite's rollback journal, at the cost of a longer write transaction and cache pressure. It assumes one event-loop/store owner and the existing owned runtime's session deadline; cross-thread writers, full-size/16-GB memory and large-corpus throughput are not validated. Canonical BLOB persistence avoids introducing a second database or a separate filesystem-promotion boundary. Native sqlite-vec query structures/search remain T29, not an unapproved Python similarity fallback.

Startup marks a rolled-back processing intent `INDEX_INTERRUPTED` without rerunning inference or deleting originals. Unexpected persisted vectors/bindings attached to an incomplete intent block admission for recovery review. Operation status now reflects committed indexing, including upload/extraction/batch and scoped index operation IDs. Complete source indexing reports `indexed`; retained omissions report `indexed_with_omissions`, `INDEX_OMISSIONS` and `ready: false`. All-omitted evidence fails explicitly. These are source-operation flags; application health remains unready. Metadata status is not a fresh integrity hash of every source; later retrieval must revalidate source eligibility/current evidence. Internal chunk reads are scoped, preserve typed provenance and return bounded pages of at most 100 items; returned text remains untrusted/unescaped backend data.

## Verification

**37 new cases**: 18 vector/profile unit cases and 19 stored-CSV integration cases. All embeddings are synthetic; SQLite, upload, extraction, chunking, transactions, status and restart paths are real. Three metered Python children deliberately exit after a durable intent, during the publication transaction and after publication. Reopen confirms respectively interrupted/no-vector, interrupted/no-vector and complete/vector states, with `integrity_check: ok`; no native model/DLL child is involved.

| Check | Actual result |
|---|---|
| Initial schema/vector red | Two collection errors for missing module/schema constant, 1.14 s |
| First schema/vector green | 16 passed, 1.43 s |
| Orchestration red | Missing index module, 1.07 s |
| Intermediate implementation checks | Import-source error corrected; then four failures exposed the missing `units` envelope field. A later test incorrectly treated a header anchor as a data record; corrected to assert the coarse header and exact first data record separately |
| Status red | 1 failed/1 passed, 1.70 s; original status stayed unindexed before integration |
| First complete integration/recovery check | 16 passed, 11.45 s; shared meter 4 starts, including three exit-control children |
| Historical version-status red | 1 failed, 1.77 s; stale operation advertised indexed before correction |
| Final focused non-child checks | 34 passed/3 deselected, 8.03 s |
| Space-identity mutation | Replacing the batch's space check with the selected constant made the mismatched-space test fail; original file restored exactly before final regression |
| Final full suite | **424 passed, 1 skipped, 1 warning, 72.89 s**; shared meter **16/64 starts, 470,244/2,000,000 retained metered bytes** |
| Established application/test Ruff scope | Passed lint; **51 files already formatted** |

Tests additionally cover changed content, wrong model/runtime/space/dimensions, missing/reordered/mismatched vectors, nonfinite/zero/bool/unnormalized vectors, source tampering, mid-batch failure, quota rollback, explicit retry, duplicate reuse, provenance/scope, partial/all omissions, busy refusal and uncertain-cleanup admission blocking. The existing skip is Windows symlink permission; the existing warning is Starlette/HTTPX deprecation. Mutation-restored `app/storage/index_state.py` SHA256: `a90b584c22242520c133226c3fcc69bf40c1d3e00b9947cfedd988531f6f5364`.

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest -q -rP -p no:cacheprovider
.\.venv\Scripts\python.exe -m ruff check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration tests/evals/spikes/t27_runtime_smoke.py
.\.venv\Scripts\python.exe -m ruff format --check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration tests/evals/spikes/t27_runtime_smoke.py
```

A broader initial `ruff check .`/`ruff format --check .` failed on historical evaluation scripts outside that established scope; formatting reported 24 legacy files. Those files were left untouched. The scoped commands above passed and include every changed/new Python file. No passing whole-repository Ruff claim is made. A transient typing import was replaced with `contextlib.AbstractAsyncContextManager`; no dependency was added.

The task ledger is `data/t28-01/budget.json`: 44 starts prepaid under the 64-start ceiling, with red 4/4, green 5/6, regression 21/24 conservative admissions, mutation 2/2 and quality/review 8/8 charges. The final regression observed 16 starts against its reserved 17; that unused reservation is not refunded. Observed total starts are 39, conservative phase charges 40. Combined reported test-meter artifact/child-output charges are **837,666 bytes**; the final ledger also charges actual retained logs/review diff, a ledger reserve and a conservative reserve for broad Ruff diagnostics under the 2,000,000-byte ceiling. Routine allocation is closed without reset; no native allocation is consumed.

## CP10 and handoff

CP10's technical review covers T26 deterministic provenance/chunk omissions, T27 pinned embedding/native ownership/error handling and T28 versioned content reuse/atomic restart integrity. T26's 600/800/120 byte policy remains provisional. The actual [T27 S2 smoke](t27-runtime-smoke-02.md) supplies bounded native embedding/cleanup evidence; T28's new persistence integration uses mocked embeddings and does not claim a new combined native indexing run. S1/S2 receipts and seals stay unchanged; their seals describe historical sources and are not resealed to include T28 changes.

Manual review traced scope joins, per-source versus canonical identity, parameterized SQL, complete-batch validation, intent/publication rollback, lease transfer, post-teardown commit, retained quota charges, safe status/errors and migration exactness. No required implementation finding remains in this bounded task. The reviewed change adds no API route, installation, runtime adoption, deletion policy or stage transition. General lifecycle, saved-chat/citation resolution, exact input-fit, scale/resource acceptance and grounded-answer quality remain later work.

T28 is implemented and verified. The user subsequently **accepted CP10, approved the 13-file T28 source/results commit and explicitly instructed proceeding to T29**, 2026-11-20. The next source commit and any new native trial retain separate gates; no stage transition is implied. Readable reviewed diff, including all five new authored files: `data/reviews/t28-indexing.diff`. No historical checkpoint/summary or unrelated user file was edited or staged.
