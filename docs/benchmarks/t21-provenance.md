# T21 — Normalized provenance contracts

Date: 2026-11-20. The user explicitly requested T21 after T20 commit `99dc36e`. Scope: pure typed extraction/provenance values and synthetic tests using existing Pydantic. No dependency/lock/SPEC/AGENTS change, parser/OCR/model execution, network operation, generated document, application-data write, storage migration, new public API or T22 work.

## Implementation and review

`app/ingestion/models.py` separates document/extraction identity from normalized source units and their anchors. Supplied stable IDs/hash/versions and plain filenames round-trip without regeneration. Frozen nested models/tuple collections reject extra fields. Per-unit parser/version, native/OCR labels, warnings and optional engine-scaled confidence allow mixed PDFs without collapsing provenance. A missing confidence value stays unknown, not zero or certainty.

PDF page/region, XLSX sheet/range/merged-origin and CSV record/physical-line/positional-column anchors use the conventions documented in [contracts](../contracts.md#t21--implemented-normalized-provenance-contract). Non-exact precision requires a limitation and unavailable precision cannot assert coordinates. Exact PDF table/image precision requires a region; coarse page-only representation remains available. XLSX bounds describe the format, not a newly chosen product budget. No OCR confidence thresholds were selected.

Structured tables retain sparse grid positions, roles, per-cell anchors, nullable stored text/type and inert formulas. Missing formula caches require a warning. Missing structure has an explicit limitation. Text mappings preserve raw-unit identity and normalized/source spans; unmapped text or unknown source offsets requires a stated limitation. Offsets are Unicode code points, zero-based/end-exclusive, distinct from UTF-8 transport/chunk byte budgets. No formula or embedded instruction is executed.

Correctness/security review checked metadata requirements, discriminated format anchors, relationships, missing information, numeric types (including rejected Boolean indices), stable round-trip values and source separation. Validation does not infer coordinates, reconstruct originals, fill merged cells, normalize confidence or establish chart meaning. Raw extraction IDs/source offsets still require verification by later adapters. Pydantic error values may contain source text and must be sanitized at future API/log boundaries; these models expose no HTTP/logging path themselves.

## Test evidence

Test-first initial run failed because `app.ingestion` did not exist. After implementation, 29 initial cases passed. Additional negative cases found that missing formula-cache values did not require a warning; the corresponding test first failed, then passed after the validator was added. Invalid XLSX-range tests explicitly use XLSX parent documents so unrelated format-mismatch rejection cannot mask range defects.

Fifty new test cases cover PDF/XLSX/CSV passage/table round-trips, Unicode offsets, duplicate CSV headers, multiline physical spans, mixed native/OCR and raw confidence, PDF image regions, merged origins, missing caches, unknown structure/mappings, missing metadata, extra fields, invalid hashes/ranges/indices, duplicate IDs/cells, out-of-grid cells, format conflicts and finite confidence.

Final commands:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp=data/t21-final --tb=short
.\.venv\Scripts\ruff.exe check app tests/test_project_setup.py tests/unit tests/integration
.\.venv\Scripts\ruff.exe format --check app tests/test_project_setup.py tests/unit tests/integration
```

Observed **107 passed, 1 skipped, 1 warning in 4.70 seconds**. Ruff lint passed; all fourteen Python files formatted. The existing Windows symlink-permission skip and Starlette HTTPX test-client deprecation warning remain unchanged; no test was disabled or warning suppressed. New provenance tests are pure model operations. The regression suite retains T19's Python launcher checks and T20's process-exit SQLite recovery check; no native/model trial is run or prior trial budget reused.

Review mutation inverted the exact-PDF-page requirement. The empty-page rejection test failed as expected because it accepted an exact anchor without a page. Original source bytes were restored and verified exactly. Correct-source full-suite results apply to the restored bytes; no mutation is retained.

## Limits and closeout

Structural validity cannot prove source fidelity, quote accuracy, actual table interpretation or semantic support. All examples are authored synthetic values, not parsed-file benchmarks or real source-location verification. IDs remain supplied opaque labels; these models neither allocate server ownership nor establish reference eligibility. Content/raw extraction persistence, parser resource bounds, original-byte hashing, normalization production, chunking and citation resolution remain later work. No T22 fixture harness or parser implementation is implied.

Eight scoped files are intended: two ingestion source files, the provenance test, README, PLAN, TODO, contracts and this report. Consistency/UTF-8/local-link/whitespace checks accompany closeout; protected project/dependency/evaluation/checkpoint files remain unchanged. The user explicitly approved the reviewed eight-file T21 closeout and commit on 2026-11-20. T22 has not started.
