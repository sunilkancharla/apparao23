# T31 — Checked citations, live source previews and CP11 review

Date: 2026-11-20 (Asia/Calcutta). The user approved the eight-document T30-N1 results commit and explicitly instructed proceeding to T31; committed as `aff116e`. T31-A/B/C used the existing implementation/TDD/API/security/review/documentation workflows and local dependencies. No model/OCR/sqlite-vec trial, installation, download, private-document read, schema migration or retention change occurred. Prior native allocations/receipts/seals are preserved and remain closed.

## Implemented behavior

`app/chat/citations.py` validates supplied-ID uniqueness, rejects duplicate/unknown citations and uncited answered claims, and maps quotation spans to actual normalized passages/cells. It checks Unicode code-point offsets, exact source text, real locations, parser/method/confidence and table role/type/formula metadata. Generated chunk labels are excluded from quotes. Missing values remain null, empty values remain empty strings, repeated headers/context stay marked, and coarse precision retains its limitation. Synthetic PDF/XLSX provenance tests exercise these value contracts; runtime ingestion/resolution remains CSV-only.

`Citations.preview(conversation, answer_id, citation_id)` first reads that conversation's saved completed answer and requires an actually cited supplied ID. It verifies current membership, original size/hash, current extraction/index/generation/chunk/text identities and the saved source/location metadata. Membership/version is checked again after asynchronous hashing. It loads the referenced normalized units and checks quoted spans before escaping all preview strings once. The complete compact UTF-8 JSON envelope must fit 65,536 bytes after escaping; no text/coordinate truncation is hidden. The preview returns provenance, checked `passages`, warnings and explicit current-source/escaped flags, with no new persistent quotation snapshot.

GET `/api/conversations/{conversation_id}/sources/{citation_id}?answer_id={answer_id}` exposes that operation. The answer UUID is required because evidence IDs are response-local, including T29's `ev_...` IDs; no global lookup or filename/path input is accepted. Extra/duplicate parameters, caller quotations/locations and content encodings are rejected. Unknown/foreign answers and unknown/uncited IDs return 404. Unavailable/changed/unsafe/unreadable sources return 410 `SOURCE_UNAVAILABLE`; inconsistent stored citation metadata returns 503 `CITATION_INVALID`; oversized output returns 503 `PREVIEW_LIMIT`. Existing Host/Origin/security-header/no-store behavior remains binding. There is no original-file download or browser rendering flow here.

Saved-answer HTTP GET now calls `Citations.read`: it preserves historical answer text and adds citation availability/code entries plus aggregate `source_availability`. Missing/corrupt/detached/incompatible sources are labelled unavailable and cannot provide a live preview. Busy/recovery-pending storage returns historical text with `not_revalidated` and `SOURCE_BUSY`, without clearing the current owner's slot. No-citation results use `not_applicable`. Low-level `Messages.get()` and POST/idempotent replay stay historical/unrevalidated, retaining T30's saved-exchange equality/history behavior.

This increment checks citation bindings and normalized quotation spans. It does **not** independently verify a model claim's meaning, quotations/location assertions inside free prose, calculations or general grounding. The model output schema accepts only claim text and IDs; model-provided structured source/quote/location fields remain disallowed. `MEANING_NOT_VERIFIED` is explicit; final support-signal wording/coverage remains T32.

## Verification

**35 new cases:** ten pure citation/span cases and 25 real-storage/in-process HTTP cases. The latter use actual CSV upload/extraction/index metadata, saved selections/exchanges and current original checks, with injected generation/embedding/native ranking seams. HTTP tests release the fixture store owner before the application opens it, use the app's owning thread for SQLite work, and reacquire fixture ownership for metered teardown. This exercises actual startup/reopen and preserves one-owner/thread constraints.

| Check | Actual result |
|---|---|
| T31-A red / green | Ten missing-module failures, 1.49 s; ten passed, 1.14 s |
| T31-B red / verified | Twelve missing-class setup errors, 2.87 s; combined 36 passed/one warning, 10.76 s |
| T31-C red | Ten failed/one passed, 7.31 s: absent source route/availability labels and busy historical reads |
| Security boundary red | Explicit permission/unsafe-path tests reproduced uncaught failures before the safe unavailable-source mapping |
| Focused final HTTP/security checks | Five passed, 20 deselected/one warning, 4.70 s |
| Cited-ID mutation | Returning all supplied evidence instead of only cited IDs failed the uncited-preview control; one failed, 1.55 s; source restored exactly |
| Full regression after restoration | **541 passed, 1 skipped, 1 warning in 89.44 s**; shared meter **18/64 starts**, **894,737/2,000,000 retained metered artifact/child-output bytes** |
| Scoped Ruff lint / format | Lint passed; **69 files already formatted** |

During development, one collection run found a duplicate test basename; the new integration file was renamed. Fixture failures exposed immutable-reference constraints, an incorrect `to_thread` stub, exclusive store ownership and SQLite thread affinity. The fixtures were corrected to use actual detachment order, the real callback signature and owned-thread database operations. No old assertion was weakened/deleted. The full restored-source regression is the final acceptance evidence.

Coverage includes genuine PDF/XLSX/CSV anchors in pure values; multiline records, duplicate/coarse header context and missing cells; altered quotes/locations/units/offsets/parser; unknown/duplicate/uncited IDs; foreign answers/conversations; stale index, changed/corrupt/missing originals and removed membership during hashing; caller path/quote fields, query duplication and escaping; post-escape response bounds; safe filesystem refusals; historical reads during busy/recovery state. The existing skip is Windows symlink permission and the warning is Starlette/HTTPX deprecation. Existing retrieval/generation/persistence/error tests also remain green.

The CSV source trace is the authored `Name,Units / North,42 / South,50`. The cited North chunk's data passages resolve to **North** and **42**, data record **1**, physical line **2**, columns **1 (Name)** and **2 (Units)**. Header parts separately disclose coarse physical-line context. A second authored multiline case retains physical lines 2–3; a missing column stays null/coarse. These are normalized decoded cell offsets, not fabricated raw-file byte positions. No sample is a private user document.

Actual routine commands, with logs under ignored `data/t31-01/`:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest -q -rP -p no:cacheprovider
.\.venv\Scripts\python.exe -m ruff check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration tests/evals/spikes/t27_runtime_smoke.py tests/evals/spikes/t29_native_search.py tests/evals/spikes/t30_model_smoke.py
.\.venv\Scripts\python.exe -m ruff format --check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration tests/evals/spikes/t27_runtime_smoke.py tests/evals/spikes/t29_native_search.py tests/evals/spikes/t30_model_smoke.py
```

Mutation-restored `app/chat/citations.py` SHA256: `7d7f9e90a88d05f50ccdd582c686554d3b27ae9b082e3d4c2be12ffc9675f78b`. Routine allocation: 64 total starts and 2,000,000 combined metered artifact/child-output/log/review bytes, with the existing 120-second per-run shared harness. The ledger is `data/t31-01/budget.json`; no native trial allocation was opened/reused.

**Accounting correction:** Windows `python -m ruff` launches a Ruff subprocess. Five commands consumed ten starts; earlier quality phase charges understated those children. Closeout corrects that phase to ten and allocates two unused starts to it. Final conservative charges are red 6, green 14, regression 22, quality 10 and mutation 2 = **54/64**, with no refund/reset/extra execution. Initial 52-start prepayment became 54 under the unchanged aggregate ceiling. Future quality admission must count wrapper and child before launch; this run's retroactive quality correction is a procedural limitation, not claimed pre-launch descendant enforcement. The final full suite observed 18 within its 22 reserved starts; combined reported metered bytes across all routine attempts are 1,494,326 before logs/review overhead, with final totals retained in the ledger.

## Review and limits

Review traced answer/conversation/cited-ID scope, current source/generation matching, exact normalized quotes/coordinates, no arbitrary path access, safe filesystem errors, escaping after source validation, complete response bounds, no-store headers, ownership/thread constraints, busy/recovery historical reads and unchanged retention. No required code finding remains after the safe filesystem mapping. The caught/restored mutation demonstrates that the cited-only boundary is exercised. The accounting correction above is retained explicitly.

Live checks may hash up to five originals sequentially and parse referenced normalized units. The cooperative 90-second operation timeout does not hard-confine file threads or SQLite, prevent hostile same-account edits between checks, or establish full-scale latency/memory. A current availability observation is not a guarantee of future access. No semantic quality, exact model-input fit, GPU residency/physical-16-GB acceptance, combined real Nomic/sqlite-vec/Qwen retrieval or new disconnected-runtime claim follows from mocks. Browser selection/chat/preview flows, later-format runtime ingestion, final evidence signals and lifecycle cleanup remain later tasks. No stage transition/readiness change is made.

## CP11 review and next decision

| Boundary | Evidence / remaining limit |
|---|---|
| Selected evidence and source scope | T29 routine scope/mutation tests and [T29-N1](t29-native-search.md) selected DLL bridge; vectors in N1 are authored, not model relevance evidence |
| Grounded answer/abstention and durable context | T30 routine failure/history/revision/restart tests and [T30-N1](t30-model-smoke.md) actual Qwen generation/persistence bridge with fixture retrieval; broad refusal/semantic accuracy unverified |
| Real citation and current preview | T31 actual CSV storage/source trace, cited-only scope control, exact normalized quote/anchor checks and escaped bounded HTTP preview; plain model claim meaning remains unverified |
| Historical source failure | Missing/changed/detached/unsafe sources block live preview while preserving labelled historical text; no fresh quotation snapshot or retention promise |
| Injection/error handling | Mechanical input/scope/schema/escape/no-retry boundaries pass routine tests; this is not proof of model prompt-injection resistance |

Closeout checks resolve all 593 local file-link targets across the six affected documents, preserve all 18 S1/S2/T29-N1/T30-N1 receipt hashes and the unchanged T30 source-seal file, and check whitespace plus the complete readable diff. The source seal records its historical version; it was not regenerated for T31. The Git index remains empty pending source-commit approval.

The user subsequently **accepted CP11, approved the reviewed 12-file source/results commit and explicitly instructed proceeding to T32**, 2026-11-20. Use the approved citation-validity/coverage/abstention/warning semantics and no numerical correctness probability. T32's new source commit retains a separate gate. No additional native smoke is needed for this mechanical T31 gate; any future native/model package remains separately gated. No SPEC, checkpoint/session-summary or unrelated user content was edited. Readable reviewed diff including all four new authored files: `data/reviews/t31-citations.diff`; the approval record is the subsequent closeout update.
