# T07 — XLSX and CSV parser review and trial proposal

**Date:** 2026-11-13 (Asia/Calcutta). **Status:** User-approved T07 bounded trial finished; the user reviewed the results/gaps and approved committing the package; remaining acceptance coverage is open. Three packages installed in the dedicated `.venv`; no runtime adoption or application ingestion implemented. The retained filename is from the original plan; this report covers XLSX/CSV only, not TXT. The proposal below is retained as the approved pre-run scope, superseded by the actual results here.

## Actual trial results

The user explicitly approved T07 installation/local trial and the three process improvements. Added only openpyxl 3.1.5, et-xmlfile 2.0.0 and defusedxml 0.7.1 in `tabular-eval`; all earlier pins and pdf-eval packages were retained. Lock wheel sizes/hashes match the approved proposal. Offline frozen sync and offline lock checks passed after provisioning. No global packages, PATH, interpreter, model or application changes.

The three distributions' registered files occupy **992,236 bytes (~0.95 MiB)**, excluding unregistered bytecode/cache. Actual download wheel payload is the approved 294,573 bytes. Packaged notices were inspected and archived locally in ignored `data/evals/t07/license-notices.zip`: openpyxl MIT, et-xmlfile MIT plus its bundled Python-license notices, and defusedxml PSF v2. Preserve all notices at distribution; this is not a legal compatibility certification or a complete vulnerability audit.

**Forty original-sample workers succeeded without parser-error payloads:** four fresh processes per workbook/reader pair and per CSV. No OS-cache cold guarantee. Samples were frozen at five sheets, 200 rows and 64 columns, with shared archive hardening. All four real workbooks report sample truncation; the two CSVs were read completely (22 data records, 47 columns each). Each candidate's extracted payload was stable over its four repeats.

| Source | Candidate | Median seconds (min–max) | Peak private committed MiB |
|---|---|---:|---:|
| R01 | ZIP/XML | 0.859 (0.592–1.003) | 22.6 |
| R01 | openpyxl wrapper | 1.683 (1.418–1.699) | 33.6 |
| R02 | ZIP/XML | 0.259 (0.255–0.263) | 22.3 |
| R02 | openpyxl wrapper | 1.656 (1.066–1.763) | 32.8 |
| R06 | ZIP/XML | 0.448 (0.400–0.556) | 17.3 |
| R06 | openpyxl wrapper | 1.435 (1.026–1.662) | 28.3 |
| R07 | ZIP/XML | 0.274 (0.172–0.382) | 16.3 |
| R07 | openpyxl wrapper | 1.455 (1.015–2.723) | 27.1 |
| R08 | standard csv | 0.282 (0.261–0.327) | 11.2 |
| R09 | standard csv | 0.350 (0.301–0.446) | 11.3 |

Times include process/import/IPC and shared hardening. Peak memory comes from the T05 Windows Job Object process-commit measurement, not RSS, total system RAM or combined app/OCR/model pressure. Peak working set was not collected for T07. The openpyxl wrapper does a common XML preflight, paired formula/cache workbook loads, then reads bounded cached values while source formula and merge metadata come from direct XML. This measures that composite adapter, not standalone openpyxl throughput or fully independent metadata implementations. A future runtime should justify/remove redundant loads and remeasure after changing the design.

Sampled cell values agree between readers: R01=7,528, R02=7,128, R06=400, R07=600, totaling **15,656 per repetition / 62,624 comparisons across repeats**. Sheet names, cell keys and merged references also agree. Shared metadata/hardening and comparison agreement are not independent ground truth or whole-workbook correctness. Controlled S-XLSX facts/merges/missing cache plus an additional date/dimension control have explicit authored expectations.

CSV numeric evidence matches Q01–Q04 and Q05's alternative evidence: original stored values, arithmetic inputs and physical-line anchors were checked locally. Q05 clarification and Q06 causal abstention require later model evaluation; this parser spike cannot pass those behaviors. S-CSV preserves the embedded newline and physical span 3–4; S-CSV-INJECTION preserves budget 12000 at line 2 while treating the hostile note as data. No document instructions executed.

### Checks and limits

- Test-first collection failed because the T07 adapter did not exist. After implementation/refactoring, the then-full available suite passed **9 tests in 20.90 seconds**, including the existing T05 process/network tests. The subsequently added focused duplicate-member guard test passed; removing its guard caused the expected failure, and restoring the adapter byte-for-byte restored the pass. This is nine full-suite tests plus one later focused test, not a claim that a single ten-test suite was run. Duplicate-name warnings are intentional authored controls.
- Checked controlled native cells, missing caches, merged ranges, a declared date serial, misleading worksheet dimensions, inert external hyperlink metadata, corrupt input, traversal, duplicate members, forbidden entities/DTD, member count, CSV quoted/multiline fields, hostile data, invalid UTF-8/quoting/headers and oversized fields. Actual hardened XML backend assertions passed inside openpyxl workers. Library warning messages are discarded with worker stderr; no zero-warning claim is made.
- **79 T07 worker invocations**, including initial/final T07 tests, 40 benchmark runs and three focused guard/mutation checks. Each uses the inspected 2 GiB/60-second job bound and remaining 15-minute T07 budget. The full suite also launched **13 existing T05 regression workers outside that counter: 92 child invocations overall**. This is a budget-accounting gap: the 80-worker cap was not enforced across the combined test session. No additional workers were run after this was identified. A future combined run needs one shared cap, including regressions, before execution; do not describe this session as wholly within 80. Ruff lint/format and diff checks passed; offline sync/lock passed. Raw comparison output is 7,433,091 bytes, within the 256 MiB allowance. Originals matched their recorded hashes before/after.
- Genuine encrypted-workbook rejection, real VBA/embedded-object controls, full 100 MB workbook scalability, broad date/format/shared-formula variants, chart/image semantics and arbitrary encodings were **not** established. Do not replace these gaps with corrupt ZIP success. T08/T17 and final security/acceptance must resolve relevant coverage before adoption. The minimal ZIP/XML reader only covers the tested subset; it is not a general replacement workbook engine.
- Offline sync and the passing inherited socket-denial test corroborate local behavior in this host sandbox; there was no packet capture or final disconnected application test. No corpus/prompt content was sent remotely. Privacy/security review found no reason to change the approved boundary, but does not certify arbitrary documents safe.

Recorded raw results: `data/evals/t07/originals-01/results.json`, SHA-256 `5fa94a2510243f9dcefc9f8a7b095f44d0852de2c7313a6b307dc5565c379323`; local summary and original source/code hashes are retained alongside it. Adapter/fixture hashes still match the benchmark after the temporary mutation was restored. Authored documents, private raw output, notices archive and review aids remain ignored.

Verified commands used project-local Python/uv/Ruff. The full-suite command was `python -m pytest -q --basetemp=data/pytest-tabular-full01 --tb=short`; the later focused check selected `tests/evals/spikes/test_tabular_trial.py::test_duplicate_archive_rejected`. Benchmark command: `python tests/evals/spikes/tabular_trial.py --benchmark data/evals/t07/originals-01`. These used `.venv/Scripts/` executables. The persistent `data/evals/t07/budget.json` intentionally prevents unapproved repeated runs; a fresh bounded run/budget record and unused output/basetemp must be arranged before reproduction, not silently deleted/reset. The spike is Windows/sandbox-specific, not a portable default application test harness.

**Recommendation:** Carry openpyxl plus bounded XML provenance checks and standard-library CSV forward as candidates for T08/T17. The direct XML subset was faster/lighter here but would need substantial additional format/security validation as a production parser. Neither path is adopted. Review the disclosed coverage gaps before closeout/adoption. Per the approved process improvement, next propose T10 embedding and T11A fixed-evidence chat feasibility before the remaining parser/tool work; XLS remains required at T07A. The user approved committing these reviewed results and process changes; remaining acceptance coverage and future package/G2 gates are unchanged.

## Approved pre-run proposal (historical)

## Scope and acceptance

The user authorized T07 after T02R was committed as `28ec7ad`. Compare XLSX extraction with explicit sheets/cell ranges, merged-header context, stored formula values and missing-cache warnings. CSV must preserve logical records, columns and original physical-line spans, including quoted multiline fields. Reject malformed/unsupported inputs, do not execute formulas/macros or fetch links, and measure time, memory, footprint and local/offline operation. XLS is required but remains its separate T07A evaluation; DOCX/TXT are excluded from development and positive-support evaluation.

T02R's exact definitions and selection/readiness rules are in [evaluation.md](../evaluation.md). Inputs proposed here: four supplied XLSX files, two supplied CSV files, S-XLSX, S-CSV, S-CSV-INJECTION and bounded negative controls. No XLS file is created by T07. No library/runtime adoption is inferred from a trial.

## Candidate comparison

| Option | Purpose and benefits | Costs and limitations | Proposed treatment |
|---|---|---|---|
| openpyxl 3.1.5 | Mature XLSX reader with cell identities, types, styles and formula/cache modes | Requires et-xmlfile; XML hardening is an explicit concern; lazy mode may omit metadata needed for merged/header provenance; actual Python 3.14 behavior untested | Trial with defusedxml, read-only mode and bounded supplementary metadata inspection |
| Python zipfile plus defusedxml XML reading | A bounded comparison baseline exposing worksheet XML, merges and formula/cache presence directly; no second workbook library | Must correctly resolve relationships/shared strings/styles/date systems; significant custom parser work if expanded; a small fixture reader is not a production-ready replacement | Trial only on the declared subset, warn/reject unsupported constructs rather than guessing |
| Python 3.14.6 standard-library csv | No extra package; strings, quoted fields and physical-line tracking suitable for the supplied CSVs | Encoding/dialect/header ambiguities need policy; field/row/output bounds are not supplied automatically | Required CSV baseline; preserve raw values and explicit trial encoding/dialect settings |
| python-calamine 0.9.1 | Alternative Rust-backed workbook reader; registry lists a CPython 3.14 Windows x64 wheel | Native binary/dependency/license review and exact provenance/cache behavior need separate investigation; Python dependency list alone does not disclose embedded Rust components | Metadata reviewed only; consider in T07A shortlist, not this installation proposal |
| pandas, Office/Excel automation | Dataframe or application-based alternatives | Broader dependency/process footprint or application execution; unnecessary for this bounded provenance comparison | Not proposed; no installation/automation |

Upstream identifies openpyxl as an Office Open XML library, not a legacy XLS reader. Its current registry release is 3.1.5, dated 2024-06-28, with Python >=3.8 and MIT metadata. The [upstream changelog](https://openpyxl.pages.heptapod.net/openpyxl/changes.html) includes named-style performance fixes; the age of a release is neither proof of abandonment nor evidence that current interpreter compatibility/security is verified. [Version-specific registry](https://pypi.org/project/openpyxl/3.1.5/).

The [optimized-mode documentation](https://openpyxl.pages.heptapod.net/openpyxl/optimized.html) describes lazy reading, explicit closing and incorrect worksheet dimensions. Measure real process memory rather than treating streaming as a memory guarantee. The [reader API](https://openpyxl.pages.heptapod.net/openpyxl/api/openpyxl.reader.excel.html) distinguishes formulas from last stored values using `data_only`; it does not calculate a missing value. Propose paired bounded reads with `data_only=False/True`, `keep_links=False`, `keep_vba=False`; retain source formula/cache observations and warnings. Verify merged/header and date metadata separately instead of inventing values from empty lazy cells.

The [Python 3.14 CSV documentation](https://docs.python.org/3.14/library/csv.html) explains newline handling and string-valued reading. Open with `newline=''`, use an explicit trial dialect and strict parsing, retain reader physical-line spans and logical record IDs. Do not silently coerce identifiers or units, overwrite duplicate column names, execute formula-like strings or treat dialect sniffing as reliable validation. Test UTF-8/UTF-8 BOM and explicit invalid/unsupported-encoding errors; this is a trial policy, not final product encoding approval.

The [python-calamine registry](https://pypi.org/project/python-calamine/) and [upstream repository](https://github.com/dimastbk/python-calamine) identify the Rust bindings and empty-area behavior; default offset trimming is a provenance concern to verify if trialed later. Public metadata returned version 0.9.1, Python >=3.11, no declared Python runtime dependencies and a 788,399-byte standard CPython 3.14 Windows x64 wheel. Its legacy `license` field was empty in that query; review the SPDX field and actual upstream/native notices before any proposal. No licensing conclusion or installation is inferred.

## Exact G1 provisioning proposal — three packages only

All three are absent from the dedicated project environment as checked with `importlib.metadata`. Install only in `F:/document_assistant/.venv` using its uv and local cache. Preserve all existing baseline/pdf-eval pins. No global/PATH/interpreter changes, native builds, models, Office, lxml, pandas or calamine installation.

| Pin | Purpose / alternatives | License metadata | Compatibility, maintenance and impact |
|---|---|---|---|
| openpyxl==3.1.5 | XLSX candidate; alternative bounded ZIP/XML baseline | MIT | Universal Python wheel, requires Python >=3.8 and et-xmlfile; Windows classified. Published 2024-06-28; Python 3.14 smoke still needed. Installed size/RAM unknown. |
| et-xmlfile==2.0.0 | Required openpyxl dependency, not independently selected runtime functionality | MIT | Universal wheel, Python >=3.8, no declared dependencies; registry release 2024-10-25. Actual notices/import/size checked after installation. |
| defusedxml==0.7.1 | Harden openpyxl and direct XML parsing against entity-related attacks; alternatives are a separately reviewed XML backend or rejecting XML parsing | PSF license (PSFL registry metadata) | Universal wheel, no declared dependencies; older 2021 release, Python 3.14 operation still needs verification. XML protection does not bound ZIP decompression, rows or output. |

Sources: versioned [openpyxl metadata](https://pypi.org/pypi/openpyxl/3.1.5/json), [et-xmlfile metadata](https://pypi.org/pypi/et-xmlfile/2.0.0/json), [defusedxml metadata](https://pypi.org/pypi/defusedxml/0.7.1/json). These are free open-source licenses; no paid license is proposed. Preserve packaged notices; inspect them before adoption. No complete vulnerability-free finding is claimed.

Registry wheel identities, read 2026-11-13:

| Filename | Download bytes | SHA-256 |
|---|---:|---|
| openpyxl-3.1.5-py2.py3-none-any.whl | 250910 | `5282c12b107bffeef825f4617dc029afaf41d0ea60823bbb665ef3079dc79de2` |
| et_xmlfile-2.0.0-py3-none-any.whl | 18059 | `7a91720bc756843502c3b7504c77b8fe44217c85c537d85037f0f536151b2caa` |
| defusedxml-0.7.1-py2.py3-none-any.whl | 25604 | `a352e7e428770286cc899e2542b6cdaedb2b4953ff269a210103ec58f6198a61` |

Total wheel payload: **294,573 bytes (~288 KiB)**, excluding registry/TLS/cache overhead. Proposed provisioning cap: 10 MiB network payload allowance and 100 MiB additional project environment/cache space; actual installed footprint must be measured. Stop if resolution adds packages, changes existing pins, needs source builds or exceeds the approved budget; return the concrete change for review. Universal-wheel tags and Python lower bounds are metadata evidence, not a tested compatibility claim.

After approval only: add an isolated `tabular-eval` dependency group with these three exact pins, resolve with `uv lock --no-build`, inspect the complete diff, then run:

```powershell
.\.venv\Scripts\uv.exe sync --frozen --group pdf-eval --group tabular-eval --no-build
```

The pdf-eval group is retained so uv does not remove the earlier trial packages. These are proposed commands, not commands executed in this review. Verify wheel hashes, actual XML backend, packaged licenses, imports and unchanged baseline pins before parsing originals. Freeze/sync and repeat with `--offline` after caching. No startup installation/downloads and no runtime adoption.

## Security and trust review

The [upstream security warning](https://openpyxl.pages.heptapod.net/openpyxl/) recommends defusedxml because default openpyxl XML handling does not guard against certain expansion attacks. Its published [XML backend selection](https://openpyxl.pages.heptapod.net/openpyxl/_modules/openpyxl/xml.html) and [functions](https://openpyxl.pages.heptapod.net/openpyxl/_modules/openpyxl/xml/functions.html) support explicit environment selection and hardened parsing. Proposed worker settings: `OPENPYXL_LXML=False`, `OPENPYXL_DEFUSEDXML=True`; assert actual backend flags/functions after import and fail closed if hardening is absent. Package presence alone is insufficient. Reject DTD/entity-bearing XML and test a tiny inert declaration; never generate a real XML/ZIP bomb.

Upstream security notes and changelog were reviewed; public advisory searches did not establish a complete current audit. Recheck applicable upstream advisories and the resolved graph before inputs, preserve any unresolved findings, and do not equate no search hit with safety. Neither defusedxml nor a worksheet row cap prevents all archive/style/shared-string/resource abuse. ZIP member paths/duplicates, actual decompressed sizes, relationship targets and output need explicit checks. Keep worker time/memory bounds and fail safely if valid documents exceed this exploratory budget. Treat originals, extracted values, warnings and filenames as untrusted; never log private contents or raw exception strings externally.

No network access is needed by the proposed extraction algorithms after provisioning, but offline behavior is not yet tested. Run parsing in the existing restricted environment, with the T05 Windows Job Object time/memory boundary reused after inspection. A denied external socket is only evidence about this host sandbox, not an application firewall or proof that no component attempted traffic. Do not elevate parsing to bypass a boundary. Inspect external relationships as local metadata; never follow UNC, file or HTTP targets. Do not execute shell commands, macros or formula-like CSV cells.

## Proposed bounded local trial

1. Write meaningful failing checks for golden S-XLSX/S-CSV/S-CSV-INJECTION anchors and error/security controls before the evaluation adapters. Use at most three T07 evaluation files; reuse the inspected T05 process limiter. This is spike code only, not application ingestion.
2. Generate small authored XLSX with standard-library ZIP/XML definitions, and CSV with the standard library, only under a fresh ignored `data/evals/t07/<unique-run-id>`. Independently inspect XML/CSV ground truth before either candidate reads it. Preserve missing-cache state explicitly; never launch Office or calculate formulas. Retain artifact/definition hashes and exclude DOCX/TXT. Generated originals/raw results remain outside Git.
3. Compare openpyxl with the bounded ZIP/defusedxml baseline on identical S-XLSX and supplied workbook subsets. Sample at most five sheets, 200 rows/sheet and 64 columns; report truncation and unsupported constructs. Actual ZIP work is separately bounded: at most 2,000 members, 32 MiB decompressed/member and 64 MiB total, with streamed byte counts checked. These are proposed trial safety/sample limits, not new product limits or evidence of full-workbook handling.
4. Read both supplied CSVs completely within that budget and compare known Q01–Q06 values/anchors locally; exercise S-CSV multiline and S-CSV-INJECTION record/column checks. Test invalid encoding/quoting, duplicate/empty headers and field bounds (1 MiB/field trial cap), without selecting unreviewed final product policies.
5. Verify merged-heading anchors, formula/value/cache distinctions, date/type warnings, empty/misleading dimensions, corrupt/mislabeled/protected containers, inert external-link/macro markers, traversal/duplicate ZIP entries and XML/resource controls. Genuine encrypted workbook coverage may be unavailable without separate assets: explicitly report it, never present a fake corrupt ZIP as an encrypted-file test.
6. Four fresh workers per original/candidate combination (first launch plus three repeats; no OS-cache cold guarantee): 32 XLSX runs (four originals, two readers), eight CSV runs (two originals, one reader). Allow at most 80 worker invocations overall including controls, sequential only, 60 seconds (or the shorter remaining global budget) and 2 GiB committed memory per job, 15 minutes global wall time, 8 MiB worker output, 256 MiB total ignored artifacts/raw results. Stop on a limit, retain failures/coverage gaps and ask before expanding; no models run concurrently.
7. Record installed footprint, import-inclusive elapsed time, peak job committed memory/working set where available, extraction fidelity, real source anchors, warnings and all failures. Check original hashes before/after, offline frozen sync/lock, and local output/network observations. Do not treat round-trip success or valid coordinates alone as semantic support.

Exact trial subset IDs/settings are frozen in the eventual run record before execution. Evidence is extraction/control behavior only: no retrieval, chat, model quality, chart reasoning, full 100 MB workbook scalability or combined 16 GB application feasibility claim. Remaining gaps feed T08/T07A/T17. Ask for reviewed adoption at G2 after later evidence, not here.

## Review outcome and remaining gates

Recommend this three-package XLSX/CSV trial with the ZIP/XML and standard-library CSV baselines. Metadata review found no reason to add pandas/lxml/Office or a second native reader for T07. It did not establish that any candidate meets the acceptance criteria. Exact installation/local fixture generation/spike execution and the stated budgets need user G1 approval. No `pyproject.toml`/`uv.lock` change or commit occurred. T07 trial evidence, task closeout and Git approval follow afterward; T07A XLS remains separate and required.
