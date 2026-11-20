# T26 — Deterministic source-preserving chunks

Date: 2026-11-20 (Asia/Calcutta). The user explicitly instructed starting T26 after T25 commit `ebbe77b` and accepted CP09. Implementation followed sequential prose (A), structured table/CSV (B), and boundary/integration/review (C) increments. The repository implementation, TDD, security, quality and documentation skill instructions were read and applied manually; no referenced skill script was executed or installed. The user explicitly approved the reviewed T26 closeout and ten-file Git commit on 2026-11-20. T27 is unstarted and CP10 remains open through T28.

## Implemented behavior

`app/retrieval/chunking.py` exposes the pure iterator `iter_chunks(extraction, units=None)`. Input is the existing immutable `NormalizedExtraction`, optionally with a separate ordered stream of validated source units for T25's stored envelope. It yields `Chunk` and `ChunkOmission` models from `app/retrieval/models.py`. No API route, database schema change, persisted chunk/index store, automatic processing trigger or readiness transition is added. Integration tests load the existing stored envelope and ordered units explicitly.

The implementation uses the already approved **provisional** T16 baseline, without selecting final model context or claiming token fit:

| Policy | Implemented behavior |
|---|---|
| Prose target | Greedily pack complete punctuation/paragraph spans toward 600 UTF-8 bytes including the generated format/location/method label |
| Maximum | 800 UTF-8 bytes of evidence text including labels; structured provenance serialization has a separate, uncapped size here |
| Prose overlap | Repeat trailing complete spans totaling at most 120 UTF-8 bytes, provided the next complete span still fits; zero if none fits |
| Structured overlap | Repeat headers and declared row keys with their own source spans and a `repeated` marker; never arbitrary character overlap |
| Large/empty units | Explicit omissions for empty prose, oversized unsplittable spans/rows, tables without usable structure, and images needing interpretation |

Boundary detection is a deterministic conservative punctuation/blank-paragraph rule, not a linguistic sentence model. A long sentence/value without a usable boundary is omitted rather than split into partial words, numbers or values. Following text starts a new fragment; it never bridges the omitted interval into a continuous quotation. Units/pages are not merged into an invented continuous source. Split prose carries `SOURCE_UNIT_SPLIT`; shared overlap is marked separately from fresh text.

Table chunks retain whole cell values and explicit grid roles. Each generic table row includes all supplied headers and its row keys. If a wide row cannot fit, splitting is attempted only with explicitly declared row keys: each complete data cell repeats every header and key. The entire row is omitted if any required fragment cannot fit; no partial row is published. Successful fragments carry `TABLE_ROW_SPLIT`. All repeated context retains its original unit/cell anchors, not invented adjacency.

T25 CSV columns are reunited by logical record and complete physical-line span, in original positional-column order. One chunk holds the complete record and its headers if it fits. CSV has no declared semantic row key, so an oversized record is omitted as a whole. No first-column/key/unit inference is introduced. Duplicate/missing headers, empty strings, missing cells, quoted newlines and inert formula-like text remain distinguishable. Source extraction is never modified or discarded by the transform.

## Identity and provenance

Each chunk carries the document ID, original content SHA256, filename/format, extraction ID/version, normalization version, `source-boundaries-1` chunking version, text SHA256 and deterministic chunk ID. The ID hashes content/extraction/chunking identity, text hash and full source-part metadata using sorted JSON. Display filename/document-view changes alone do not change shared-content chunk identity. Source/version/parser/anchor/text changes represented in that identity do. Equal bytes with independently created T25 extraction IDs are not newly deduplicated by T26; future indexing remains T28.

Parts use zero-based, end-exclusive Unicode code-point offsets in chunk text and the original normalized unit text or decoded cell text. They retain unit IDs, actual locations/precision/limitations, method, parser/version, raw OCR confidence or unknown, warnings and available original text mappings. Existing mappings stay in the original unit coordinate system. Cell mappings explicitly disclose missing raw-file byte offsets, with row/column/role, stored type and inert formula metadata. Missing cached values have no source text span and display a generated missing-value marker; they are not computed or converted to zero. Generated labels are not source quotation spans.

Contract-fixture walkthrough, using authored `Industry,2024,2025` headers and `North,352361,350764` values:

```text
[csv records 1-1 lines 2-2; exact; native]
column 1 header: Industry
column 1 data: North
column 2 header: 2024
column 2 data: 352361
column 3 header: 2025
column 3 data: 350764
```

Observed evidence text: **178 UTF-8 bytes**, including the trailing newline. Text SHA256: `9613a757000168e0cc02f8ab1fc16430edd5a1a0ce2cb94431d9e36393e8aef3`. This walkthrough uses synthetic contract identities, not a private document or a model answer.

| Chunk code-point span | Verbatim value | Actual data anchor |
|---|---|---|
| `[84,89)` | North | Record 1, physical line 2, original column 1 / Industry |
| `[127,133)` | 352361 | Record 1, physical line 2, original column 2 / 2024 |
| `[171,177)` | 350764 | Record 1, physical line 2, original column 3 / 2025 |

Header parts retain their own physical-line-1 anchors with coarse header precision and no fabricated positive data-record number. The stored-extraction integration uses a quoted multiline `North,` + newline + `works` cell: all three data values map to logical record 1 / physical lines 2–3, while headers stay on line 1. It verifies the original bytes remain unchanged and the extraction receipt stays `awaiting_index`, `indexed: false`.

## Verification and review

Tests were introduced before the new behavior: initial collection failed because `app.retrieval` did not exist; then four prose cases passed. Four table/CSV cases failed against the prose-only implementation and passed after table support. Additional controls cover exact 800 versus 801 bytes using multibyte characters, complete overlap/zero overlap, full source-span coverage, an oversized middle sentence, preserved mappings, declared-key fragments, rejected partial rows, missing formula caches, coarse images/tables, streamed format/order/column errors, source-version identity and malformed serialized chunks.

There are **32 new cases**: 31 unit cases and one integration case using actual upload/extraction/SQLite normalized storage. Two test files initially shared a basename under pytest's default import mode; renaming the integration file resolved collection without changing test configuration. A focused Ruff finding was corrected before the final checks.

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest tests/unit/test_chunking.py tests/integration/test_stored_chunking.py -q -rP -p no:cacheprovider
.\.venv\Scripts\python.exe -m pytest -q -rP -p no:cacheprovider
.\.venv\Scripts\ruff.exe check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration
.\.venv\Scripts\ruff.exe format --check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration
git diff --check
```

Focused result: **32 passed in 0.88 seconds**. Final full result: **273 passed, 1 skipped, 1 warning in 42.66 seconds**. The skip remains the Windows symlink-permission case; the warning remains Starlette's HTTPX test-client deprecation. Ruff lint passed and **34 files** passed formatting. Final shared suite meter: **13/64 starts; 263,388/2,000,000 retained factory-artifact/child-output bytes**, within the existing 120-second admission/child boundary. The new integration adds no child processes; all prior control/regression children share the existing suite meter. This is not a meter for every temporary database byte or a renewed historical/native trial allocation.

Review temporarily inverted the prose maximum-byte predicate. Both exact-boundary controls failed as expected. The original implementation was restored; its before/after Git object hash matched `de73aef63a951bc3c4a99e712ba352ee49dd9fe2`. The mutation is absent from the delivered change. Correctness/security review traced source offsets, complete-value publication, repeated context, identity/version dependencies, original preservation and untrusted text handling. No outstanding required finding remains in this task's implemented scope.

The transform has no file/network/subprocess/database writes and executes no document instructions or formulas. Its text and labels remain untrusted data. HTML encoding, document/reference eligibility and current-source availability checks remain obligations of future consumers; an opaque chunk ID or filename is not authorization. Input iterators must contain complete, validated, ordered extraction units; this helper is not an upload validator or a scope-filtering API. No dependency, model/OCR run, download, private sample access or source data transport occurred.

## Reviewable files and limits

| Change | Files |
|---|---|
| Pure chunk transform and immutable provenance values | `app/retrieval/__init__.py`, `app/retrieval/chunking.py`, `app/retrieval/models.py` |
| Boundary/structure controls and stored-CSV trace | `tests/unit/test_chunking.py`, `tests/integration/test_stored_chunking.py` |
| Current behavior, task evidence and serialized-field contract | README, PLAN, TODO, `docs/contracts.md`, this report |

The 800-byte guard applies to evidence text, not metadata RAM/disk usage. Processing streams source groups but may hold a whole CSV record or one structured table and its row fragments; full-size memory/latency and physical-16-GB validation remain unperformed. Long headers and required labels can make otherwise short values unsuitable. Numeric CSV rows without declared keys are not split into isolated lookup values. These omissions limit retrieval coverage and must be surfaced by later indexing/answer consumers; they do not reduce approved original upload/storage limits or permit answers from omitted evidence.

No inference quality, embedding/index persistence, retrieval scope enforcement, complete prompt fit, live citation resolution, frontend flow, semantic chart understanding, general deletion or disconnected-runtime acceptance is claimed. Future model input must independently enforce its full evidence/context budgets. CP10 stays open through T28; no stage transition is authorized. `/status` and `/compact` are not exposed in this host and were not run. No session checkpoint or session summary was created/updated.

Readable complete diff, including authored untracked files: `data/reviews/t26.diff`. Generated review/test artifacts stay ignored. The approved commit includes only the ten reviewed source/test/documentation files; unrelated user files, runtime data and generated artifacts are excluded. Only closeout documentation changed after the final passing suite and byte-for-byte mutation restoration.
