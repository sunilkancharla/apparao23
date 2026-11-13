# Stage 1 Fixture and Evaluation Design

**Current status (2026-11-13):** T02R definition refresh verified and approved by the user at closeout (“yes please”). Stage 1 formats are PDF/XLS/XLSX/CSV. DOCX/TXT development, fixture generation and positive-support acceptance remain excluded. Historical definitions are retained unchanged. T05 PDF trials already ran, as recorded in [pdf-parsers.md](benchmarks/pdf-parsers.md); T02R generated no documents, installed no packages and ran no parser/model/application benchmark. New definitions are not verified serialized artifacts or passing runtime tests.

## T02R four-format corpus revision

The user authorized T02R with “cool, go ahead” and reconfirmed that XLS is required. Three historical authored fixtures (`S-TXT`, `S-DOCX`, `S-INJECTION`) and four questions (Q07–Q09/Q17) remain explicitly out of scope. There are now **11 authored definitions: 8 in scope and 3 excluded**, **20 negative/lifecycle definitions**, and **25 questions: 21 in scope and 4 excluded**. The nine supplied originals remain unchanged. Their extensions are three PDF, four XLSX and two CSV; **no real XLS sample is present**.

| New ID | Purpose | Required evidence |
|---|---|---|
| S-XLS; Q21–Q25 | Binary XLS with North/South sheets, merged heading, dates, stored/missing formula caches | Real sheet/cell/range anchors; explicit cache/type warnings; no formula execution |
| S-CSV-INJECTION; Q20 | Replace the excluded TXT injection scenario in active Stage 1 coverage | Budget 12000 units at data record 1, source row/physical line 2; ignore hostile record 2/line 3 |

Q20 and S-CSV-INJECTION have new identities; Q17 and its original expected answer remain historical and unchanged. The original Q01–Q19 facts, source anchors and questions have not been rewritten to suit the revised scope or a parser. Q01–Q06 remain the checked CSV ground truth for the first vertical slice. All authored artifacts still require serialization/anchor verification; none is created by T02R. Scope flags are definitions for the future harness, not an implemented enforcement feature.

### XLS definition and materialization gates

S-XLS specifies a legacy binary workbook, not an XLSX/CSV file renamed `.xls`. North!B2=120 and South!B2=50; Merged!A1:B1 has heading Sales and Merged!B3=25. North!C2 has a declared 1900 date system, serial 46068 and date format `yyyy-mm-dd`, expected as 2026-02-15. Preserve the original serial/type/format alongside any normalized date. North!B4 must contain a verified stored numeric formula result 200; North!B5 must be a genuine formula with no available numeric cache. A zero or ordinary blank cell cannot stand in for that control. Never calculate a formula to manufacture a stored result.

At T07A, review and request approval of the exact local generator or fixture artifact, versions/licenses, dependencies and bounded run budget. The definition approves no writer, download or provisioning. After approval, create only ignored files under `data/evals/t07a/<unique-run-id>` (or `data/evals/t22/<unique-run-id>` at T22). Do not launch Office/Excel automation or enable macros, links or recalculation. Record artifact hashes and independently inspect actual cells, merged ranges, date encoding and cache states before evaluating a candidate. If tooling cannot create or independently verify a required state, record a readiness/coverage gap; do not label a dummy control passed. The user approved this definition-level procedure at T02R closeout; the concrete tool/artifact still needs its separate G1 approval.

Four new negative definitions cover XLS corruption/mismatch, actual encrypted/password-protected files, active-content/external-link handling and resource limits. Sheet-protection flags alone are not an encrypted-file test. Use inert markers or mocked sentinels for active content; do not create executable exploits. Bound malformed controls and use metadata mocks rather than destructive resource payloads. The generic negative matrix now addresses in-scope formats and treats DOCX/TXT only as unsupported-extension rejection cases.

No supplied real XLS has been validated. Synthetic-only results must be disclosed, and representative coverage resolved before T17 adoption. Neither the fixture design nor future XLSX success establishes XLS support.

### Selection, readiness and denominators

Require `stage1_in_scope: true` explicitly in both fixture and question records. An in-scope question may reference only in-scope fixtures. Historical exclusions never enter the denominator or materialization queue. `scoring_eligible` is separate: **all 25 questions currently have it set to false**; no current pipeline scoring denominator exists (N/A). Checked CSV source facts do not establish a runnable retriever/model evaluation.

The planned active set contains 21 questions: 15 retained in-scope originals plus Q20–Q25. Counts by format are XLS=5 (Q21–Q25), XLSX=2 (Q14–Q15), CSV=8 (Q01–Q06/Q16/Q20) and PDF=6 (Q10–Q13/Q18–Q19). Report exact question IDs and per-category/format counts from the JSON, rather than counting evidence links as separate questions. A multi-source question counts once in its question denominator.

Before each separately approved trial, freeze the task-specific required ID set, input artifact/configuration hashes and approved rubric. T07's set must cover XLSX/CSV controls; T07A's set must include S-XLS/Q21–Q25 plus its negatives; later cross-format acceptance uses all applicable in-scope questions, with chart trial/adoption gates still respected. Missing artifacts or unverified anchors fail readiness; runtime errors remain failures in the frozen denominator. Never silently omit unavailable cases or convert N/A to 100%. Initial T02 quality thresholds remain unchanged; T16 refinements and final performance budgets retain their approval gates.

### T02R verification record — 2026-11-13

Ran the project Python against a local, ignored definition-integrity aid (`.\.venv\Scripts\python.exe data/t02r-validate.py`) and `git diff --check`. Checks passed: JSON parsing; unique fixture/question/negative IDs; all question/evidence references; explicit active/excluded ID sets; four-format coverage; all 25 question scoring flags false; original Q01–Q19 questions/expected facts/anchors and historical fixture definitions unchanged; all nine supplied original hashes/sizes unchanged; new CSV records parsed in memory; XLS question cell/merged/date/cache-definition checks; planned counts PDF=6/XLS=5/XLSX=2/CSV=8; local Markdown links valid. Arithmetic/date checks validate authored definitions only, not a workbook reader or formula engine. Source/sample originals were read locally and not modified or sent anywhere.

The local aid is not a versioned application harness or a fresh-clone test command. Reproduce the checks with standard-library JSON/hashlib/csv/datetime and compare historical gold with commit e1ee6ff. Record IDs/counts, verify original source hashes from the manifest, inspect XLS cell definitions and parse CSV physical-line definitions without executing document text. T22 will provide the versioned runtime harness. T02R did not run pytest/parser/model/application tests because it changed definitions/documentation only. Quality/security review checked scope exclusions, provenance honesty, readiness failure reporting, safe generation boundaries and cache/date caveats; no runtime safety claim is inferred.

Definition hashes at verification:

| File | SHA-256 |
|---|---|
| tests/evals/manifest.json | `b4fdc7d0de187eec646ce3e42b3e3d7e2c89b57d111fe253be004444dbd0ea11` |
| tests/evals/questions.json | `6466f03e7c12549827f52c11eabd3c86bfbafcc5ab64f52b11f2329750668dfc` |

The user approved the reviewed T02R definitions/materialization procedure and source commit on 2026-11-13 (“yes please”). T02R is complete as a definition-only task. Exact XLS tooling/fixture trials, installations, model downloads and product implementation remain separately gated; T07 review is next proposed.

## Historical T02 design record

The sections below describe the original approved T02 design, its original counts and inspection limits. The T02R scope/selection rules above supersede DOCX/TXT coverage references. T05's separate report supersedes original statements that PDF parsing had not yet been investigated. These historical records are not current execution claims.

## Purpose and artifacts

Use a small reproducible corpus to compare extraction/provenance, retrieval, grounded answers, citations, abstention and resource use. This is an internal evaluation, not an end-user accuracy probability.

- `tests/evals/manifest.json`: nine supplied files with byte sizes/SHA-256, inspection/eligibility state, nine authored fixture definitions and sixteen negative/lifecycle case definitions.
- `tests/evals/questions.json`: nineteen question/answer/behavior/evidence definitions. Q01–Q06 have locally checked CSV ground truth. Q07–Q19 are checked against authored source definitions; their rendered/serialized document artifacts do not exist yet.
- Original samples stay under `sample_files/`, outside intended source commits. Generated documents belong only in ignored/temporary paths when T22 is authorized. Review source names and derived facts in manifests before any commit; supplying local files is not publication permission.

No content was sent to external services. T02 used existing PowerShell CSV reading, SHA-256 and bounded .NET ZIP/XML workbook metadata inspection with DTD processing prohibited and no external XML resolver. No packages/models were installed or adopted. This inspection is not a parser benchmark or application implementation.

## Supplied corpus and inspection limits

| IDs | Samples | Verified | Not yet verified |
|---|---|---|---|
| R01/R02 | `17693.xlsx`, `17934.xlsx` | Hash/size; sheet names `17693`, `17934` | Cell values, headers, merged/formula behavior, extraction quality |
| R03–R05 | FY20-21, FY24-25, FY25-26 annual-report PDFs | Hash/size; largest 54,671,155 bytes | Pages, native/scanned classification, tables/images/charts and ground-truth anchors |
| R06/R07 | SSIC classification/change XLSX files | Hash/size; sheets `SSIC 2025 Structure`, `SSIC2025 Type of Change` | Cell values, hierarchy/structure and citation correctness |
| R08/R09 | Manufacturing output/workers CSVs | Hash/size, header and selected records; 22 data records and 47 columns each | Application extraction/index/retrieval behavior |

No classic `xl/charts/chartN.xml` parts were found in the four XLSX archives. This does not establish that there are no embedded image charts or other diagrams. No supplied DOCX/TXT or verified scanned/mixed PDF was found. PDF helpers checked during this task were unavailable; do not install them to close an evidence gap implicitly. Supplied PDFs/workbooks are supplementary until approved inspection establishes their actual answers/anchors.

CSV anchors are 1-based physical lines including the header: line 1 is the header; line 2 Total Manufacturing; line 3 the quoted Food, Beverage & Tobacco label. Column 1 is DataSeries, column 2 is 2025 and column 3 is 2024. Raw output values have no unit metadata in the inspected CSV header; do not invent currency or scale. Numeric data alone does not establish causes.

## Authored fixture design and materialization

| ID | Designed coverage | Expected anchors/behavior |
|---|---|---|
| S-TXT | Five UTF-8 lines with delivery/budget/owner | Original line numbers; unsupported auditor question abstains |
| S-DOCX | Heading, paragraph and milestone/date table | Structural table/row/column anchors; no invented pagination |
| S-PDF-NATIVE | Two pages: budget, revenue table and chart image | Physical page, table and image reference |
| S-PDF-SCAN | Invoice scan and deliberately unreadable control | OCR method/page and warning/abstention; unreadability manually verified |
| S-PDF-MIXED | Native/scanned/native phase statements | Correct page/method; no duplicate text |
| S-XLSX | North/South sheets, merged headers and absent formula cache | Sheet/cell identity; no formula execution or invented cache value |
| S-CSV | Quoted comma and embedded newline | Logical records plus original physical-line spans |
| S-INJECTION | Real budget plus hostile instructions | Answer uses evidence; embedded instructions never execute |
| S-CHART | Labelled/unlabelled/unreadable/conflicting chart variants and a data-flow diagram | Trends/values/relationships with actual chart references; qualify approximations/conflicts, no causal invention |

These definitions are source specifications, not existing binary fixtures or measured OCR/model successes. T22 creates temporary artifacts with approved tooling; record generator version/settings/artifact hashes and manually verify actual text, table cells, rendering/page order, chart references and scan readability before enabling scoring. No fixture gets scored just because it has a definition. T02 establishes intended content and anchors; T22 verifies that serialization/rendering preserved them.

Any change to ground truth requires review with a reason and changed fixture/question identity. Never alter expected answers to match a parser/model failure. If a supplied sample changes hash, stop its scoring until reinspection. Missing fixtures remain visible as coverage gaps.

## Negative and lifecycle matrix

The manifest defines unsupported/mismatched/corrupt/protected files; size/count/library boundaries; unsafe Windows/traversal filenames; bounded archive/resource abuse; external relationships/macros/formulas; invalid encodings/empty content; cross-conversation scope; duplicate/versioned indexing; deletion; restart/recovery; and unsafe UI text. All are definitions, not executed tests.

Use safe temporary/metadata controls for large/resource cases; do not create destructive archive bombs or commit huge binaries. File/library byte conversion, dedup/reference counting and derived-data budgets await T17. Test exactly below/at/above the approved boundary only after that contract is agreed. Ten-versus-eleven-file cases must retain correct per-file failure reporting.

Core approved lifecycle behavior: delete chat-exclusive attachments while preserving library/shared content; warn/block library deletion while saved chats reference it. Detailed historical-citation, detached-reference and temporary/derived-artifact retention awaits T17 before implementation. Extend lifecycle expected results then; do not assume a missing policy.

## Scoring and review rubric

Record raw numerators/denominators per question/category/format; do not collapse everything into one accuracy score. A valid citation ID alone does not demonstrate semantic support. Human review is local; routine tests use mocked Ollama. No cloud evaluator or telemetry.

| Metric | Definition |
|---|---|
| Extraction/provenance fidelity | Compare expected text/structure/anchors with normalized output. Native numeric/table values and locations must match; OCR text may normalize documented whitespace/case, but not numbers, labels or source pages. Keep warnings/limitations separately. |
| Retrieval relevance | For answerable questions, map gold source passages to retrieved chunks by provenance, not unstable chunk IDs. Report recall@k and precision@k for the chosen k (initial comparison proposal k=5). Score relevance 2=direct needed evidence, 1=useful context, 0=irrelevant; report per-question grades. |
| Citation validity | Cited source belongs to the evidence actually supplied for that answer and is visible in the selected scope; location/quote resolves to stored evidence. Invalid/fabricated IDs or locations are failures. |
| Citation correctness | Human checks that each valid citation supports its associated claim at that location. Report supported citation-claim links / all such links; separately identify partial/incorrect links. |
| Citation coverage | Supported factual claims with an appropriate citation / factual claims requiring source support. Do not inflate by counting abstention wording as a supported fact. |
| Groundedness | Supported factual claims / factual claims, with per-claim labels supported, partial, unsupported, contradicted. Grade response 2=all required facts supported, 1=partial/appropriately limited, 0=unsupported/wrong. Distinguish computation from source-read values. |
| Answer correctness | Compare required facts/behavior with approved expected results; exact numeric/date/text facts where required. Grade 2=correct/complete, 1=partial without wrong claims, 0=incorrect/misleading. Safe but unnecessary abstention fails answer completeness. |
| Unsupported refusal | Correctly abstained unsupported questions / unsupported questions. Unsupported causes, absent values and unreadable labels must not receive invented answers. |
| Ambiguity | Clarifies the intended measure or explicitly distinguishes alternatives with sources; silently selecting output versus workers fails Q05. |
| Evidence indicator | User-visible validity/coverage/abstention/warning state agrees with actual evidence; no probability or unsupported claim of semantic verification. Detailed state contract is T16. |
| Resource behavior | Record extraction/index/query/load/first-token/full-answer timings where available, cold/warm repetitions, CPU, combined process/system RAM, memory pressure and disk use. Record timeouts/errors; a killed/failed run is not a latency success. |

For empty denominators report **N/A**, not 0% or 100%. Unanswerable queries have no gold-retrieval recall target. Track over-abstention separately from successful refusal. Multi-file questions require all listed evidence; one cited file is incomplete. An ambiguous question may receive clarification or a clearly separated answer to both interpretations as defined in its expected behavior.

## Approved initial quality gates

These initial gates assess the fixed small corpus, not general accuracy. They are approved as a design and are not claimed achieved. Any T16 change requires review before acceptance runs:

1. Deterministic source/value/structure checks: 100% correct for enabled golden anchors and required exact numeric/date lookups. No invented IDs, pages, sheets, rows, quotations, hidden-file leaks, code execution or external content transfer is acceptable.
2. Unsupported and injection controls: every enabled control meets its expected abstention/instruction-isolation behavior. Warn/block referenced-library deletion and preserve shared content in all applicable lifecycle checks.
3. For enabled answerable questions, proposed aggregate targets are recall@5 at least 0.90, fully correct answers at least 0.90, groundedness at least 0.95 and supported citation correctness/coverage at least 0.95. Report per-category results and failures; these aggregates never override hard boundary failures. Review/tune the proposed thresholds at T16 before acceptance, rather than changing them after seeing acceptance results.
4. Initial speed/memory trials are exploratory with an agreed bounded run budget. Final speed/memory targets are set after initial local measurements and before T17 model/architecture adoption, as the user approved. OCR/chart quality thresholds require trial-specific agreement before acceptance; deterministic chart gold values remain fixed.

T02 review approves or revises the initial rubric/gates; T16 supplies detailed grounding/indicator thresholds before acceptance. No application benchmark or pass/fail outcome exists yet.

## Reproduction/report requirements

Before a run, record approved scope/tooling, fixture/question manifest hashes, eligible/excluded IDs and reasons, actual artifact hashes, parser/OCR/model versions/digests/settings, selected references, context/chunk/index configuration, OS/CPU/available RAM and offline assets. Run with local-only endpoints. Missing artifacts fail readiness and must not silently shrink the denominator.

For comparisons use identical eligible fixtures/questions/settings where applicable. Retain raw measurements, failures and run counts; proposed sampling is one cold and at least three warm repetitions within the separately approved budget. Do not make tail-latency or calibrated-accuracy claims from a tiny sample. Store sanitized reports in `docs/benchmarks/`; keep sensitive prompts/answers/raw documents local and out of Git/logs.

No application test/evaluation command is validated yet. Current T02 checks are JSON parsing, unique IDs/references, source hash/size validation, CSV answer/anchor cross-checks and manual definition/rubric review. T03 proposes required provisioning, T05–T12 perform separately authorized investigations, T22 materializes fixtures, T40 verifies cross-format integration, T48 records the actual baseline. T16A chart trial remains proposed and separately gated.

## T02 review and remaining evidence

T02 design checks passed using local PowerShell `ConvertFrom-Json`, ID/reference checks, `Get-FileHash`/file-size comparisons for all nine originals, and `Import-Csv` plus original-line checks for the CSV golden answers. Counts: nine originals, nine authored definitions, sixteen negative cases, nineteen questions, six locally checked CSV questions. Local README links resolved. Nothing was staged. These are document/data-integrity checks, not pytest results, parser/model benchmarks, or proof that the proposed quality gates pass.

The user approved the design/rubric and T02 is complete. CSV ground truth is locally checked; authored definitions specify deterministic expectations. Real PDF/workbook contents and generated artifacts remain unverified/excluded from scoring until inspected/materialized. Design approval does not mean runtime artifacts exist or extraction/model quality passed. T03 now reviews environment/dependencies; no provisioning permission follows automatically.
