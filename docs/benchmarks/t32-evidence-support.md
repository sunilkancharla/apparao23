# T32 — Observable evidence-support signals

Date: 2026-11-20 (Asia/Calcutta). The user accepted CP11, approved the reviewed T31 source/results commit and explicitly instructed T32; committed as `fd830e5`. Ordered T32-A/B/C used existing implementation/TDD/API/security/review/documentation workflows, local dependencies and a fresh routine allocation. No model/OCR/sqlite-vec trial, installation, download, private-document read, schema migration or retention change occurred. Prior native and routine allocations remain preserved/closed.

## Behavior and semantics

`app/chat/evidence.py` projects trusted saved-answer and current citation observations into an ephemeral `evidence_support` response. Fixed labels explain observable states; `semantic_support` is always `not_independently_verified`. Coverage counts declared text blocks and blocks with supplied/checked/no citations; a block needs all its citation IDs checked to count as checked. These are not independently identified atomic facts, relevance scores or semantic citation coverage. No correctness probability, model-self-assessed grade, accuracy/score field or benchmark target is exposed.

| Observation | Display state / handling |
|---|---|
| Source/request failure or unavailable selected source | `unavailable`; retain other detected issues and historical text |
| Unknown/duplicate/out-of-manifest ID or invalid quote/location | `citation_problem`; never resolve it by a different source or silent retry |
| Unknown/truncated input fit, invalid/incomplete output, pending completion or unrevalidated current citations | `incomplete`; separate successful subchecks remain visible |
| Successful explicit pre-generation no-evidence abstention, no supplied/cited evidence | `no_evidence`; model completion/fit and coverage are N/A, not a failed unattempted generation |
| Clarification/refusal without declared cited factual blocks | `clarification` / `abstained`; coverage N/A, with no factual-answer badge |
| Declared factual blocks lacking citations | `citations_missing`; report structural counts, not assumed factual support |
| All declared citations/quotes resolve and applicable checks complete | `citations_resolved`: **Citations checked; meaning not independently verified** |

The table follows display precedence from top to bottom. Every detected issue/warning remains available independently. Partial answers may have resolved citations plus `PARTIAL_ANSWER`; this is not complete-answer acceptance. Model-declared block counts can miss hidden assertions or attach irrelevant sources. A valid citation on “The budget doubled” does not establish that the source supports doubling; the T16-E03 unit case preserves that distinction.

**Current runtime fit remains unverified.** Ordinary HTTP callers never set the classifier's trusted `input_fit_verified` argument; that seam is for authored truth-table predicates/future validated backend use. Existing `INPUT_FIT_UNVERIFIED`/`TOKEN_FIT_UNVERIFIED` observations also override a positive predicate. Actual generated answers therefore display `incomplete` support while GET can separately report `locations_and_quotes:checked`. The durable exchange's `state:complete` means it was saved, not that input fit or semantic support was verified. No new tokenizer method, token count, context limit or runtime adoption is claimed.

Answer POST/replay and saved-answer GET add the object without changing persisted questions/claims/citation manifests. POST uses historical/publication metadata and does not add a live hash/preview pass. GET reuses T31's existing current-source resolver; its success observations now carry warning codes, actual methods/precision and whether OCR confidence was available. These are ephemeral flags, not new quote snapshots or recognition thresholds. Source/OCR/coarse/omission/partial/conflict/missing-cache warnings survive any primary state; unknown source-warning text becomes a generic fixed message, never reflected source/model text or a path. Legacy records use only retained observations and do not acquire invented historical facts.

`ChatService` now preserves `SOURCES_UNAVAILABLE` when every selected source is blocked; that branch previously returned only the generic `NO_EVIDENCE` warning. Its persisted answer remains an explicit insufficiency response without a model call. The indicator gives the source limitation precedence, rather than displaying a successful empty-evidence signal. No retry, scope broadening, inference, new route or request setting is introduced. Caller-provided fit/confidence fields remain forbidden by the existing request schema.

## Verification

**38 new cases:** 30 pure indicator cases and eight real-storage/in-process HTTP cases. Existing upload/extraction/index/storage, selected-source checks and model/ranking seams are reused. Routine models/native kernels remain injected. The OCR bridge case substitutes observed metadata from a checked synthetic preview; it is not actual OCR or later-format ingestion evidence.

| Check | Actual result |
|---|---|
| T32-A red / green | 23 missing-module failures, 0.54 s; 23 passed, 0.44 s |
| T32-B red / green | Seven HTTP failures before integration, 4.77 s; 30 combined cases passed/one warning, 4.11 s |
| Warning-precedence red | Five hard-warning failures/two controls passed, 0.51 s: reported failure warnings incorrectly allowed a resolved label |
| Focused final checks | **38 passed**, one warning, 4.20 s after hard-warning handling |
| Failure/no-evidence mutation | Allowed unavailable evidence to receive the successful no-evidence label; blocked-selected-source HTTP control failed, 1.37 s; exact source restored |
| Full regression after restoration | **579 passed, 1 skipped, 1 warning in 63.41 s**; shared meter **18/64 starts**, **913,767/2,000,000 retained metered artifact/child-output bytes** |
| Scoped Ruff lint / format | Lint passed; **72 files already formatted** |

Cases cover all approved observable outcomes, declared-block denominators, mixed citation availability, partial answers, duplicate/foreign IDs, missing completion records, malformed/failed operation categories, safe no-inference abstention, hidden-claim/semantic counterexamples, unknown fit, later historical-source disappearance, query/response scope, model/caller grade spoofing, no saved badge and independent extraction warnings. The existing skip is Windows symlink permission; the warning is Starlette/HTTPX deprecation. No old test/assertion was weakened or deleted.

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest -q -rP -p no:cacheprovider
.\.venv\Scripts\python.exe -m ruff check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration tests/evals/spikes/t27_runtime_smoke.py tests/evals/spikes/t29_native_search.py tests/evals/spikes/t30_model_smoke.py
.\.venv\Scripts\python.exe -m ruff format --check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration tests/evals/spikes/t27_runtime_smoke.py tests/evals/spikes/t29_native_search.py tests/evals/spikes/t30_model_smoke.py
```

Mutation-restored `app/chat/evidence.py` SHA256: `ae24ffd76f87d1ef0cd804f07ae7549622e5fa03eae6bfdacfe1bc9c194d7d03`. The ignored ledger/log root is `data/t32-01/`. Prepaid starts: red 6, green 10, full regression 22, quality 8, mutation 2 = **48/64**. Conservative charges are red 6, green 6, regression 22, quality 6 and mutation 2 = **42/64**; no refunds/reset. Each of the three Windows Ruff commands was charged for both wrapper and native child before launch. Full regression observed 18 within its 22 reserved starts. The 120-second per-run shared harness and 2,000,000 combined retained metered artifact/log/review-byte ceiling apply; final totals are retained in the ledger. No consumed native trial allocation was reopened/resealed.

## Review, limits and next step

Review traced fixed messages/no source-text reflection, current versus historical observations, ID/quote/source/failure precedence, N/A stage applicability, declared-block denominators, independent warnings, no model/caller grading authority, scoped HTTP integration, no extra inference/hash pass solely for the indicator and unchanged storage/retention. Five missed hard-warning cases were corrected before final regression; no required code finding remains. The mutation confirms the source-failure/no-evidence boundary is exercised.

Input fit, semantic claim/quote/calculation correctness, broad model refusal/injection behavior, full-scale latency/memory and combined real Nomic/sqlite-vec/Qwen quality remain unverified. Recognition confidence availability is not answer correctness; no threshold or calibrated claim is introduced. T31's cooperative hashing/SQLite/same-account limits remain. The indicator is an observable check summary, not Stage 1 acceptance or browser readiness. Existing internal human-quality targets/denominators are unchanged and unclaimed.

Closeout checks resolve all 598 local file-link targets across the seven affected documents, preserve all 18 S1/S2/T29-N1/T30-N1 receipt hashes and the historical T30 source-seal file, and verify whitespace plus the complete readable diff. T31's routine allocation remains closed with its prior counters. No source seal was regenerated. The Git index remains empty pending commit approval.

T32 implementation/routine verification is complete and committed as `c3c6e61`: the 13 reviewed source/report files plus three explicitly approved policy/decision records. The user skipped T15/UI UX Pro Max review/use, added initial CSV validation T34A after T34/before format expansion, and reserved T33 for a new session. The original proposed T15 source review is withdrawn; no tool research/trial/install occurred. T34A's exact future native package remains gated, and T48 remains the final all-format baseline. The explicitly requested [Session 4 summary](../session_summaries/SESSION_4_AI_Session_SUMMARY.md) is a one-file exception to the default no-summary rule. These approved documentation amendments update SPEC/AGENTS/decisions only for that workflow/schedule; no application code, dependency, model, resource/quality threshold, format scope or stage transition changes. Prior native receipts/seals and routine ledgers remain preserved. Readable reviewed implementation diff: `data/reviews/t32-evidence-support.diff`; approved decision closeout: `data/reviews/t32-approved-closeout.diff`. Summary/status edits are documentation only and do not rerun application tests or consumed native packages.
