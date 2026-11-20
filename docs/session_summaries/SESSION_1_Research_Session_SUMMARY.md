# Session 1 — Research Session Summary

Updated: **20 November 2026**. Research scope: initial commit **bb68c40** through **2698240**, the T17/G2 closeout. This replaces the earlier account that stopped at 8d25bd7.

## 1. Session Overview

The goal was to decide how to build a private assistant that reads your documents and answers questions using evidence from those files. This is **Stage 1 — Local Prototype**.

Research covered requirements, setup, PDF/spreadsheet readers, scanned-text reading, local models, search storage and architecture. **T17 is now closed following G2 approval.** The research produced evaluation tools and evidence; it did not produce the complete document-chat application.

## 2. Task-wise Work and Files

Each task explains its goal, process and outcome, followed by all associated authored file types. Expand the lists for individual descriptions. Documents and evaluation files now appear together under one heading per parent task.

Files are assigned once by main purpose and the previous report/Git history. Shared root files originated in initial setup; their placement explains usage rather than claiming they originated during a later task. Later T17 files missing from the earlier report are included.

#### T01 — Resolve blocking Stage 1 decisions

**Summary:** Agree what the assistant should do before development.

**Process:** Requirements and working rules were established, then clarified through choices about formats, English OCR, charts, limits and deletion. Shared plans were maintained as these choices developed.

**Outcome:** Stage 1 uses PDF/XLSX/CSV, local processing and the unchanged Windows 11/16 GB/CPU-only target. The shared root files were created in initial setup and are grouped here by purpose.

<details>
<summary>Files associated with T01 (7)</summary>

**Shared root requirements/planning files**

- [AGENTS.md](../../AGENTS.md) — Created in initial setup; persistent working, privacy and approval rules.
- [PLAN.md](../../PLAN.md) — Created in initial setup; implementation order and later approved sequencing changes.
- [README.md](../../README.md) — Created in initial setup; verified capabilities, setup commands and current limitations.
- [SPEC.md](../../SPEC.md) — Created in initial setup; approved Stage 1 requirements, limits and acceptance criteria.
- [TODO.md](../../TODO.md) — Created in initial setup; task objectives, approvals, evidence and remaining work.

**Documents and review plans**

- [docs/decisions.md](../decisions.md) — Records decisions across tasks, including scope, retention, internal tokenization and G2 approval.
- [docs/proposals/chart-interpretation.md](../proposals/chart-interpretation.md) — Defines the chart/diagram feasibility scope; the trial was later deferred until after the first CSV flow.

</details>

#### T02 — Define representative fixtures and evaluation rubric

**Summary:** Prepare examples and scoring rules for fair tool comparisons.

**Process:** The work defined answerable, unsupported, ambiguous, table and multi-file questions, known answers, synthetic samples and negative cases. Later T02R/scope amendments adjusted the active evaluation set.

**Outcome:** Reusable evaluation definitions exist; writing questions and scoring rules does not mean an application has passed them.

<details>
<summary>Files associated with T02 (3)</summary>

**Documents and review plans**

- [docs/evaluation.md](../evaluation.md) — Defines sample questions, scoring rules and acceptance checks.

**Evaluation programs, tests, manifests and scripts**

- [tests/evals/manifest.json](../../tests/evals/manifest.json) — Lists evaluation samples, synthetic fixtures, negative cases and known gaps.
- [tests/evals/questions.json](../../tests/evals/questions.json) — Stores evaluation questions, scoring guidance and current format scope.

</details>

#### T03 — Review the actual host and dependency/provisioning proposals

**Summary:** Understand the computer and prepare a dedicated project environment.

**Process:** The host and packages were reviewed for compatibility, licences, resource needs and local operation. Baseline tools and later approved evaluation dependencies were installed in the project environment at the user's request.

**Outcome:** The local environment, pinned dependencies and setup notes exist. The detected computer has more RAM than the unchanged 16 GB target, so its results are not equivalent target proof. Root environment files originated in initial setup.

<details>
<summary>Files associated with T03 (7)</summary>

**Root environment/configuration files**

- [.gitignore](../../.gitignore) — Created in initial setup; excludes private data, environments, caches and generated files from Git.
- [.python-version](../../.python-version) — Created in initial setup; records the Python interpreter choice for the project.
- [pyproject.toml](../../pyproject.toml) — Created in initial setup; declares dependencies and development-tool settings.
- [uv.lock](../../uv.lock) — Created in initial setup; fixes dependency versions for reproducible project installations.

**Documents and review plans**

- [docs/benchmarks/environment.md](../benchmarks/environment.md) — Report on T03 Workstation Inventory.
- [docs/dependencies.md](../dependencies.md) — Collects dependency identities, licence/compatibility reviews and the component inventory, updated across tasks.
- [docs/provisioning.md](../provisioning.md) — Collects approved setup steps, actual commands and provisioning limitations, updated across tasks.

</details>

#### T04 — Evaluate SkillSpector and manual skill-review process

**Summary:** Consider a tool for inspecting third-party skills.

**Process:** The intended review process was considered. The user explicitly deferred SkillSpector, while relevant skills/scripts continued to be reviewed manually.

**Outcome:** SkillSpector was not installed or executed. Manual review is not a security guarantee.

<details>
<summary>Files associated with T04 (1)</summary>

**Documents and review plans**

- [docs/benchmarks/skillspector.md](../benchmarks/skillspector.md) — Report on SkillSpector decision.

</details>

#### T05 — Compare native PDF parsers

**Summary:** Find a practical way to read PDF text and source locations.

**Process:** Readers and licences were compared. Approved local samples examined extraction, tables, locations and failures. PyMuPDF licensing was discussed, and its practical comparison was explicitly deferred.

**Outcome:** Useful component evidence and layout limitations were recorded. No upload feature was built; final component selection occurred at G2.

<details>
<summary>Files associated with T05 (4)</summary>

**Documents and review plans**

- [docs/benchmarks/pdf-parsers.md](../benchmarks/pdf-parsers.md) — Report on Native PDF parser evaluation.

**Evaluation programs, tests, manifests and scripts**

- [tests/evals/spikes/pdf_trial.py](../../tests/evals/spikes/pdf_trial.py) — Compares PDF readers under bounded local evaluation conditions.
- [tests/evals/spikes/pdf_trial_fixtures.py](../../tests/evals/spikes/pdf_trial_fixtures.py) — Creates small authored PDF samples without changing originals.
- [tests/evals/spikes/test_pdf_trial.py](../../tests/evals/spikes/test_pdf_trial.py) — Tests PDF evaluation controls and parser checks.

</details>

#### T06 — Retired DOCX-format work

DOCX was excluded from Stage 1; TXT is also outside the approved scope. No files were created specifically for this retired task. Historical scope definitions remain with T01/T02.

#### T07 — Compare XLSX and CSV extraction baselines

**Summary:** Read spreadsheet/CSV contents with useful row, column and cell references.

**Process:** Authored samples and approved local files exercised quoted CSV records, sheets, stored values and missing formula caches. Workbook formulas, macros and external links were not executed.

**Outcome:** Reader candidates and limitations were documented. Missing formula results and coarse structure must be disclosed by the eventual application.

<details>
<summary>Files associated with T07 (4)</summary>

**Documents and review plans**

- [docs/benchmarks/tabular-text-parsers.md](../benchmarks/tabular-text-parsers.md) — Report on XLSX and CSV parser review and trial proposal.

**Evaluation programs, tests, manifests and scripts**

- [tests/evals/spikes/tabular_trial.py](../../tests/evals/spikes/tabular_trial.py) — Compares spreadsheet and CSV readers using bounded samples.
- [tests/evals/spikes/tabular_trial_fixtures.py](../../tests/evals/spikes/tabular_trial_fixtures.py) — Creates small spreadsheet and CSV samples for independent parser checks.
- [tests/evals/spikes/test_tabular_trial.py](../../tests/evals/spikes/test_tabular_trial.py) — Tests spreadsheet and CSV evaluation cases.

</details>

#### T07A — Compare legacy XLS parsers — later deferred

**Summary:** Investigate the older XLS format while it was still considered.

**Process:** Candidates, licences and evaluation controls were prepared. Compatibility/acquisition difficulties were recorded; the user later removed XLS from Stage 1.

**Outcome:** XLS is deferred outside Stage 1. These files are historical research, not an active XLS feature.

<details>
<summary>Files associated with T07A (3)</summary>

**Documents and review plans**

- [docs/benchmarks/xls-parsers.md](../benchmarks/xls-parsers.md) — Report on T07A — Legacy XLS parser review and proposed trial.

**Evaluation programs, tests, manifests and scripts**

- [tests/evals/spikes/test_xls_trial.py](../../tests/evals/spikes/test_xls_trial.py) — Tests the deferred legacy XLS evaluation controls.
- [tests/evals/spikes/xls_trial.py](../../tests/evals/spikes/xls_trial.py) — Contains legacy XLS evaluation controls, now deferred outside Stage 1.

</details>

#### T08 — Evaluate Microsoft MarkItDown

**Summary:** Decide whether MarkItDown would simplify document reading enough to justify its costs.

**Process:** Source, dependencies, offline behaviour and source-location preservation were reviewed. The user accepted non-adoption and deferral of the practical comparison.

**Outcome:** MarkItDown was not adopted; no measured quality or speed advantage is claimed.

<details>
<summary>Files associated with T08 (1)</summary>

**Documents and review plans**

- [docs/benchmarks/markitdown.md](../benchmarks/markitdown.md) — Report on MarkItDown source and dependency review.

</details>

#### T09 — Compare local OCR and scanned/mixed-PDF paths

**Summary:** Check how scanned pages could be converted to text locally.

**Process:** OCR engines, English assets and Windows execution boundaries were reviewed. Startup, configuration and disconnection problems were investigated before the completed user-run disconnected manual-04 trial.

**Outcome:** The final schedule completed 60 comparisons and 20 controls. Readable samples passed; rotated text remained a weakness. The historical checkpoint is grouped here because it was first added during OCR work and is now disabled.

<details>
<summary>Files associated with T09 (32)</summary>

**Documents and review plans**

- [docs/benchmarks/appcontainer-preflight.md](../benchmarks/appcontainer-preflight.md) — Report on AppContainer preflight stopped at positive runtime startup.
- [docs/benchmarks/consolidated-isolation-validation.md](../benchmarks/consolidated-isolation-validation.md) — Report on Consolidated isolation validation: permission boundary stop.
- [docs/benchmarks/job-accounting-investigation.md](../benchmarks/job-accounting-investigation.md) — Report on Job accounting investigation results.
- [docs/benchmarks/launch-flag-comparison.md](../benchmarks/launch-flag-comparison.md) — Report on Launch flag comparison results.
- [docs/benchmarks/manual-ocr-first-stop.md](../benchmarks/manual-ocr-first-stop.md) — Report on First offline run: package-name comparison defect.
- [docs/benchmarks/manual-ocr-preparation.md](../benchmarks/manual-ocr-preparation.md) — Report on Manual disconnected OCR runner preparation.
- [docs/benchmarks/manual-ocr-results.md](../benchmarks/manual-ocr-results.md) — Report on Manual-04: completed offline synthetic OCR comparison.
- [docs/benchmarks/manual-ocr-second-stop.md](../benchmarks/manual-ocr-second-stop.md) — Report on Manual-02 OCR trial: stopped on reconnection.
- [docs/benchmarks/manual-ocr-third-stop.md](../benchmarks/manual-ocr-third-stop.md) — Report on Manual-03 stop: RapidOCR enum configuration.
- [docs/benchmarks/ocr.md](../benchmarks/ocr.md) — Report on Local English OCR source review.
- [docs/benchmarks/python-startup-diagnostic.md](../benchmarks/python-startup-diagnostic.md) — Report on Startup diagnostic: basic launches work; accounting stop.
- [docs/proposals/consolidated-isolation-validation.md](../proposals/consolidated-isolation-validation.md) — Plan for Authorized consolidated isolation validation.
- [docs/proposals/job-accounting-investigation.md](../proposals/job-accounting-investigation.md) — Plan for Proposed two-case Job accounting investigation.
- [docs/proposals/launch-flag-comparison.md](../proposals/launch-flag-comparison.md) — Plan for Proposed launch-flag comparison.
- [docs/proposals/manual-disconnected-ocr-trial.md](../proposals/manual-disconnected-ocr-trial.md) — Plan for Proposed manual disconnected synthetic OCR trial.
- [docs/proposals/manual-ocr-continuation.md](../proposals/manual-ocr-continuation.md) — Plan for Prepared fresh manual OCR continuation.
- [docs/proposals/manual-ocr-fourth-run.md](../proposals/manual-ocr-fourth-run.md) — Plan for Approved manual-04 offline OCR continuation.
- [docs/proposals/manual-ocr-handoff.md](../proposals/manual-ocr-handoff.md) — Plan for Manual offline OCR trial: manual-04 instructions.
- [docs/proposals/manual-ocr-third-run.md](../proposals/manual-ocr-third-run.md) — Plan for Approved fresh manual-03 OCR handoff.
- [docs/proposals/ocr-appcontainer-preflight.md](../proposals/ocr-appcontainer-preflight.md) — Plan for AppContainer feasibility and proposed preflight.
- [docs/proposals/ocr-trial-artifacts.json](../proposals/ocr-trial-artifacts.json) — Pins approved OCR trial files, versions and expected identities.
- [docs/proposals/ocr-trial.md](../proposals/ocr-trial.md) — Plan for Proposed bounded English OCR evaluation.
- [docs/proposals/python-startup-diagnostic.md](../proposals/python-startup-diagnostic.md) — Plan for Proposed bounded Python startup diagnostic.
- [docs/session-checkpoint.md](../session-checkpoint.md) — Historical progress log first added during OCR work; later disabled and preserved unchanged.

**Evaluation programs, tests, manifests and scripts**

- [tests/evals/spikes/appcontainer_preflight.py](../../tests/evals/spikes/appcontainer_preflight.py) — Checks whether Windows isolation can support the bounded OCR trial.
- [tests/evals/spikes/ocr_trial.py](../../tests/evals/spikes/ocr_trial.py) — Runs approved offline comparisons of local scanned-text readers.
- [tests/evals/spikes/ocr_trial_fixtures.py](../../tests/evals/spikes/ocr_trial_fixtures.py) — Creates synthetic PDF and image samples for OCR evaluation.
- [tests/evals/spikes/python_startup_diagnostic.py](../../tests/evals/spikes/python_startup_diagnostic.py) — Compares Python startup methods to investigate blocked launches.
- [tests/evals/spikes/run_manual_ocr.ps1](../../tests/evals/spikes/run_manual_ocr.ps1) — Starts the user-operated offline OCR trial and checks required confirmation.
- [tests/evals/spikes/test_appcontainer_preflight.py](../../tests/evals/spikes/test_appcontainer_preflight.py) — Tests Windows isolation preflight controls and refusal cases.
- [tests/evals/spikes/test_ocr_trial.py](../../tests/evals/spikes/test_ocr_trial.py) — Tests OCR trial preparation, limits and failure handling.
- [tests/evals/spikes/test_python_startup_diagnostic.py](../../tests/evals/spikes/test_python_startup_diagnostic.py) — Tests the fixed Python startup diagnostic cases.

</details>

#### T10 — Benchmark local Ollama embedding candidates

**Summary:** Compare models that turn passages and questions into representations for search.

**Process:** Pinned model files were acquired under approved limits. Fixed documents and queries compared retrieval quality, latency and resources, with download/process/cleanup evidence retained.

**Outcome:** Nomic became the preferred candidate for later selection. These samples do not establish universal quality, speed or target-machine feasibility.

<details>
<summary>Files associated with T10 (4)</summary>

**Documents and review plans**

- [docs/benchmarks/embeddings.md](../benchmarks/embeddings.md) — Report on Local embedding comparison and retained trial limitations.

**Evaluation programs, tests, manifests and scripts**

- [tests/evals/spikes/embedding_budget.py](../../tests/evals/spikes/embedding_budget.py) — Tracks shared allowances for embedding setup, tests and model calls.
- [tests/evals/spikes/embedding_trial.py](../../tests/evals/spikes/embedding_trial.py) — Compares local embedding models using fixed questions and reference vectors.
- [tests/evals/spikes/test_embedding_trial.py](../../tests/evals/spikes/test_embedding_trial.py) — Tests embedding trial limits and result validation.

</details>

#### T11A — Check chat feasibility early using fixed evidence

**Summary:** Check early whether small CPU-only models can answer using supplied passages.

**Process:** Two candidates used fixed questions and evidence. An interrupted request was retained as a failure; the approved continuation completed missing cases and the user reviewed the answers.

**Outcome:** All 96 planned result slots completed across 97 attempts. This was a component benchmark, not a working document-chat application.

<details>
<summary>Files associated with T11A (4)</summary>

**Documents and review plans**

- [docs/benchmarks/chat-models.md](../benchmarks/chat-models.md) — Report on T11A — Early CPU chat feasibility review and trial proposal.

**Evaluation programs, tests, manifests and scripts**

- [tests/evals/spikes/chat_cases.json](../../tests/evals/spikes/chat_cases.json) — Defines fixed questions and evidence for chat-model comparisons.
- [tests/evals/spikes/chat_trial.py](../../tests/evals/spikes/chat_trial.py) — Runs controlled local chat-model comparisons and records results.
- [tests/evals/spikes/test_chat_trial.py](../../tests/evals/spikes/test_chat_trial.py) — Tests chat trial limits, validation and error handling.

</details>

#### T11 — Benchmark local chat candidates with combined OCR/model trials

**Summary:** Check answering and OCR together under the agreed resource rules.

**Process:** Combined trials stopped on deadline, monitoring, storage and state-file issues. Corrections were checked and fresh allocations used for later runs. Combined-07 completed and the user accepted its local answer review.

**Outcome:** All 36 responses passed automated schema/citation-scope checks and were qualitatively accepted. This is sample-specific evidence, not an independent accuracy score or physical-16-GB guarantee.

<details>
<summary>Files associated with T11 (35)</summary>

**Documents and review plans**

- [docs/benchmarks/combined-monitor-300ms.md](../benchmarks/combined-monitor-300ms.md) — Report on Combined monitor: 300-ms policy implementation.
- [docs/benchmarks/combined-monitor-cadence-repair.md](../benchmarks/combined-monitor-cadence-repair.md) — Report on Fake-only monitor cadence repair.
- [docs/benchmarks/combined-ocr-model-fifth-preparation.md](../benchmarks/combined-ocr-model-fifth-preparation.md) — Report on Combined-05 static preparation.
- [docs/benchmarks/combined-ocr-model-fifth-stop.md](../benchmarks/combined-ocr-model-fifth-stop.md) — Report on Combined-05 stop: local atomic state replacement denied.
- [docs/benchmarks/combined-ocr-model-first-stop.md](../benchmarks/combined-ocr-model-first-stop.md) — Report on Combined-01 stop: reused OCR deadline field mismatch.
- [docs/benchmarks/combined-ocr-model-fourth-preparation.md](../benchmarks/combined-ocr-model-fourth-preparation.md) — Report on Combined-04 static preparation.
- [docs/benchmarks/combined-ocr-model-fourth-stop.md](../benchmarks/combined-ocr-model-fourth-stop.md) — Report on Combined-04 stop: sampling interval exceeded.
- [docs/benchmarks/combined-ocr-model-preparation.md](../benchmarks/combined-ocr-model-preparation.md) — Report on T11 combined OCR/model runner preparation.
- [docs/benchmarks/combined-ocr-model-second-stop.md](../benchmarks/combined-ocr-model-second-stop.md) — Report on Combined-02 stop: missing-file error during first sentinel.
- [docs/benchmarks/combined-ocr-model-seventh-preparation.md](../benchmarks/combined-ocr-model-seventh-preparation.md) — Report on Combined-07 static preparation.
- [docs/benchmarks/combined-ocr-model-seventh-results.md](../benchmarks/combined-ocr-model-seventh-results.md) — Report on Combined-07 completed — local semantic review accepted.
- [docs/benchmarks/combined-ocr-model-sixth-preparation.md](../benchmarks/combined-ocr-model-sixth-preparation.md) — Report on Combined-06 static preparation.
- [docs/benchmarks/combined-ocr-model-sixth-stop.md](../benchmarks/combined-ocr-model-sixth-stop.md) — Report on Combined-06 partial results and completed-reading gap stop.
- [docs/benchmarks/combined-ocr-model-third-stop.md](../benchmarks/combined-ocr-model-third-stop.md) — Report on Combined-03 stop: resource boundary during corpus embeddings.
- [docs/benchmarks/combined-resource-diagnostic.md](../benchmarks/combined-resource-diagnostic.md) — Report on Combined resource diagnostics repair.
- [docs/benchmarks/combined-state-coordination-repair.md](../benchmarks/combined-state-coordination-repair.md) — Report on Synthetic state coordination repair.
- [docs/benchmarks/combined-state-write-investigation.md](../benchmarks/combined-state-write-investigation.md) — Report on Synthetic state-file investigation.
- [docs/benchmarks/combined-storage-diagnostic.md](../benchmarks/combined-storage-diagnostic.md) — Report on Approved fake-worker storage diagnostic.
- [docs/benchmarks/combined-storage-repair.md](../benchmarks/combined-storage-repair.md) — Report on Approved fake-only live storage repair.
- [docs/proposals/combined-monitor-300ms.md](../proposals/combined-monitor-300ms.md) — Plan for Proposed 300-ms combined-trial monitoring ceiling.
- [docs/proposals/combined-monitor-cadence-repair.md](../proposals/combined-monitor-cadence-repair.md) — Plan for Proposed monitor cadence and timing repair.
- [docs/proposals/combined-ocr-model-continuation.md](../proposals/combined-ocr-model-continuation.md) — Plan for Approved combined-02 deadline repair and fresh offline continuation.
- [docs/proposals/combined-ocr-model-fifth-run.md](../proposals/combined-ocr-model-fifth-run.md) — Plan for Proposed combined-05 offline evaluation.
- [docs/proposals/combined-ocr-model-fourth-run.md](../proposals/combined-ocr-model-fourth-run.md) — Plan for Proposed combined-04 offline evaluation.
- [docs/proposals/combined-ocr-model-handoff.md](../proposals/combined-ocr-model-handoff.md) — Plan for Approved combined OCR/model trial: local offline instructions.
- [docs/proposals/combined-ocr-model-seventh-run.md](../proposals/combined-ocr-model-seventh-run.md) — Plan for Proposed combined-07 offline evaluation.
- [docs/proposals/combined-ocr-model-sixth-run.md](../proposals/combined-ocr-model-sixth-run.md) — Plan for Proposed combined-06 offline evaluation.
- [docs/proposals/combined-ocr-model-third-run.md](../proposals/combined-ocr-model-third-run.md) — Plan for Approved combined-03 offline continuation.
- [docs/proposals/combined-ocr-model-trial.md](../proposals/combined-ocr-model-trial.md) — Plan for T11 proposal: bounded combined OCR/model pressure evaluation.
- [docs/proposals/combined-state-coordination-repair.md](../proposals/combined-state-coordination-repair.md) — Plan for Proposed minimal state reader/writer repair.
- [docs/proposals/combined-state-write-investigation.md](../proposals/combined-state-write-investigation.md) — Plan for Proposed bounded state-file investigation.
- [docs/proposals/model-ocr-selection.md](../proposals/model-ocr-selection.md) — Plan for Model and OCR selection recommendation.

**Evaluation programs, tests, manifests and scripts**

- [tests/evals/spikes/combined_native.py](../../tests/evals/spikes/combined_native.py) — Supervises offline OCR and model workloads, resource limits and cleanup.
- [tests/evals/spikes/combined_trial.py](../../tests/evals/spikes/combined_trial.py) — Prepares combined trials and shares accounting and safety controls.
- [tests/evals/spikes/test_combined_trial.py](../../tests/evals/spikes/test_combined_trial.py) — Tests combined OCR/model accounting, monitoring and safety controls.

</details>

#### T12 — Compare local vector storage and consistency strategies

**Summary:** Choose local search storage with document scoping and recoverability.

**Process:** A SQLite baseline and the exact sqlite-vec artifact were reviewed. Synthetic/offline runs checked search, filtering and interruption/recovery. Startup and MATCH authorization problems were corrected before the remaining comparison completed.

**Outcome:** Results supported the later SQLite/sqlite-vec choice. They did not implement saved chats, library deletion or application storage services.

<details>
<summary>Files associated with T12 (30)</summary>

**Documents and review plans**

- [docs/benchmarks/sqlite-vec-artifact-review.md](../benchmarks/sqlite-vec-artifact-review.md) — Report on sqlite-vec0.1.9 Windows artifact — static review complete, adoption blocked.
- [docs/benchmarks/sqlite-vec-match-preparation.md](../benchmarks/sqlite-vec-match-preparation.md) — Report on MATCH correction and static preparation.
- [docs/benchmarks/sqlite-vec-match-results.md](../benchmarks/sqlite-vec-match-results.md) — Report on completed disconnected storage comparison.
- [docs/benchmarks/sqlite-vec-runtime-followup-results.md](../benchmarks/sqlite-vec-runtime-followup-results.md) — Report on native trial partial results, MATCH permission refusal.
- [docs/benchmarks/sqlite-vec-runtime-preparation.md](../benchmarks/sqlite-vec-runtime-preparation.md) — Report on T12 PartB — static preparation and process checkpoint.
- [docs/benchmarks/sqlite-vec-runtime-startup-correction.md](../benchmarks/sqlite-vec-runtime-startup-correction.md) — Report on startup correction and static readiness.
- [docs/benchmarks/sqlite-vec-runtime-startup-stop.md](../benchmarks/sqlite-vec-runtime-startup-stop.md) — Report on T12 PartB — startup stopped before native execution.
- [docs/benchmarks/storage-index.md](../benchmarks/storage-index.md) — Report on T12 PartA — SQLite baseline, partial scale coverage.
- [docs/proposals/sqlite-vec-artifact-review.md](../proposals/sqlite-vec-artifact-review.md) — Plan for Bounded sqlite-vec Windows artifact review.
- [docs/proposals/sqlite-vec-match-correction.md](../proposals/sqlite-vec-match-correction.md) — Plan for MATCH permission correction and remaining comparison.
- [docs/proposals/sqlite-vec-match-handoff.md](../proposals/sqlite-vec-match-handoff.md) — Plan for runtime-03 offline instructions.
- [docs/proposals/sqlite-vec-runtime-comparison.md](../proposals/sqlite-vec-runtime-comparison.md) — Plan for T12 PartB — Proposed disconnected SQLite/vector comparison.
- [docs/proposals/sqlite-vec-runtime-followup-handoff.md](../proposals/sqlite-vec-runtime-followup-handoff.md) — Plan for replacement offline trial instructions.
- [docs/proposals/sqlite-vec-runtime-handoff.md](../proposals/sqlite-vec-runtime-handoff.md) — Plan for T12 PartB — approved standalone disconnected instructions.
- [docs/proposals/sqlite-vec-runtime-startup-correction.md](../proposals/sqlite-vec-runtime-startup-correction.md) — Plan for Proposed startup correction and fresh comparison.
- [docs/proposals/storage-index-evaluation.md](../proposals/storage-index-evaluation.md) — Plan for Proposed local storage and search evaluation.

**Evaluation programs, tests, manifests and scripts**

- [tests/evals/spikes/sqlite-vec-match.json](../../tests/evals/spikes/sqlite-vec-match.json) — Sets corrected storage-trial sizes, queries and recovery checks.
- [tests/evals/spikes/sqlite-vec-runtime-followup.json](../../tests/evals/spikes/sqlite-vec-runtime-followup.json) — Sets follow-up storage cases and candidate restrictions.
- [tests/evals/spikes/sqlite-vec-runtime.json](../../tests/evals/spikes/sqlite-vec-runtime.json) — Sets initial offline vector-storage trial cases and settings.
- [tests/evals/spikes/sqlite_vec_artifact.py](../../tests/evals/spikes/sqlite_vec_artifact.py) — Inspects the vector-extension package without installing or loading it.
- [tests/evals/spikes/sqlite_vec_match_trial.py](../../tests/evals/spikes/sqlite_vec_match_trial.py) — Runs corrected offline storage comparisons after the MATCH permission repair.
- [tests/evals/spikes/sqlite_vec_runtime.py](../../tests/evals/spikes/sqlite_vec_runtime.py) — Prepares and controls the initial offline SQLite and vector-extension comparison.
- [tests/evals/spikes/sqlite_vec_runtime_followup.py](../../tests/evals/spikes/sqlite_vec_runtime_followup.py) — Controls follow-up offline storage checks, including recovery behavior.
- [tests/evals/spikes/storage-fixtures.json](../../tests/evals/spikes/storage-fixtures.json) — Defines reproducible synthetic vectors, dataset sizes and query settings.
- [tests/evals/spikes/storage_trial.py](../../tests/evals/spikes/storage_trial.py) — Measures a synthetic SQLite storage baseline without creating app storage features.
- [tests/evals/spikes/test_sqlite_vec_artifact.py](../../tests/evals/spikes/test_sqlite_vec_artifact.py) — Tests inert vector-package inspection and unsafe-artifact rejection.
- [tests/evals/spikes/test_sqlite_vec_match_trial.py](../../tests/evals/spikes/test_sqlite_vec_match_trial.py) — Tests corrected storage permissions and recovery controls.
- [tests/evals/spikes/test_sqlite_vec_runtime.py](../../tests/evals/spikes/test_sqlite_vec_runtime.py) — Tests initial offline storage trial boundaries.
- [tests/evals/spikes/test_sqlite_vec_runtime_followup.py](../../tests/evals/spikes/test_sqlite_vec_runtime_followup.py) — Tests follow-up storage trial and recovery boundaries.
- [tests/evals/spikes/test_storage_trial.py](../../tests/evals/spikes/test_storage_trial.py) — Tests SQLite baseline and consistency controls.

</details>

#### T13 — Identify and evaluate the intended RTK project

Not executed in this research session. Review is scheduled after the first slice or before proposed use. No files were created specifically for T13.

#### T14 — Identify and evaluate the intended ponytail project

Not executed in this research session. Exact project identity and a justified trial are needed before use. No files were created specifically for T14.

#### T15 — Evaluate UI UX Pro Max before frontend adoption

Pending before frontend implementation. Design 1/Design 2 are supplied references, not generated application features. No files were created specifically for T15.

#### T16 — Specify retrieval, citations and evidence-support contracts

**Summary:** Define how to find evidence, answer cautiously and show sources.

**Process:** The design covered selected-document retrieval, evidence/history limits, citations, unsupported questions, saved chats, deletion/recovery and disk accounting. The user settled the recorded storage/retention choices.

**Outcome:** The contracts and indicator wording were agreed. Citation validity is not a factual-correctness percentage; small-context settings remain provisional.

<details>
<summary>Files associated with T16 (2)</summary>

**Documents and review plans**

- [docs/proposals/t16-grounding-contracts.md](../proposals/t16-grounding-contracts.md) — Plan for evidence, citations and support-indicator design package.
- [docs/retrieval-design.md](../retrieval-design.md) — Describes finding relevant passages and answering with citations.

</details>

#### T16A — Evaluate data charts and diagrams — explicitly deferred

The user deferred this feasibility trial until after the first usable CSV flow/T34. The earlier chart-scope proposal is listed under T01, where clarification began. No separate trial results or runtime chart-understanding claim exist.

#### T17 — Present architecture and component-adoption decision pack

**Summary:** Combine earlier research into a concrete architecture decision before implementation.

**Process:** Component choices, ownership, local access, storage, limits and recovery were combined. Work then expanded into tokenizer/package-source investigations and Windows reporting/accounting repairs. Some checks found real problems, but repeated controls and reports became a loop that delayed the actual standalone/Ollama comparison.

**Outcome:** The user accepted omitting remaining investigations, selected Ollama's internal tokenizer and approved G2. T17 closed in 2698240 on 20 November 2026. Standalone tokenization was never installed or compared end to end. Remaining selected-runtime trust, exact input-fit/output-boundary and physical-16-GB checks are unverified limitations, not passes.

Final component checks included model/runtime identity work, 21 metadata/simulated-input tests and eleven matching packaged-reference token counts. A later review verified the seventeen-package standalone graph and recorded hashes, but did not resolve every build/notice question or execute the standalone comparison. The final choice was the existing Ollama-internal path. No further standalone installation or comparison is pending under T17.

<details>
<summary>Files associated with T17 (151)</summary>

**Documents and review plans**

- [docs/ADR/0001-stage1-architecture.md](../ADR/0001-stage1-architecture.md) — Records the architecture accepted at G2, selected components and unverified limitations.
- [docs/benchmarks/artifact-licence-notice-review.md](../benchmarks/artifact-licence-notice-review.md) — Records review findings: licence terms clarified; native notice/build gaps remain.
- [docs/benchmarks/evaluation-parent-accounting-correction.md](../benchmarks/evaluation-parent-accounting-correction.md) — Records review findings: parent accounting correction.
- [docs/benchmarks/hub-dependency-gap-closure.md](../benchmarks/hub-dependency-gap-closure.md) — Records review findings: identifiers improved; static-inspection proposal next.
- [docs/benchmarks/hub-metadata-dependency-review.md](../benchmarks/hub-metadata-dependency-review.md) — Records review findings: partial readiness; installation not ready.
- [docs/benchmarks/hub-only-static-review.md](../benchmarks/hub-only-static-review.md) — Records review findings: Hub wheel verified; source provenance remains unresolved.
- [docs/benchmarks/hub-source-coordinate-review.md](../benchmarks/hub-source-coordinate-review.md) — Records review findings: epoch 03 publisher origin confirmed; build-source link unresolved.
- [docs/benchmarks/input-fit-adapter-source-review.md](../benchmarks/input-fit-adapter-source-review.md) — Report on counting-adapter primary-source review.
- [docs/benchmarks/input-fit-inspection-results.md](../benchmarks/input-fit-inspection-results.md) — Report on bounded inspection stopped at open-handle identity check.
- [docs/benchmarks/input-fit-oracle-dependency-review.md](../benchmarks/input-fit-oracle-dependency-review.md) — Report on stopped before research.
- [docs/benchmarks/input-fit-oracle-review-continuation.md](../benchmarks/input-fit-oracle-review-continuation.md) — Report on counting reference needs an integration decision.
- [docs/benchmarks/input-fit-remaining-assets.md](../benchmarks/input-fit-remaining-assets.md) — Report on remaining tokenizer data assets acquired.
- [docs/benchmarks/input-fit-static-review.md](../benchmarks/input-fit-static-review.md) — Report on partial static artifact review.
- [docs/benchmarks/input-fit-tokenizer-manifest-review.md](../benchmarks/input-fit-tokenizer-manifest-review.md) — Report on tokenizer manifest review.
- [docs/benchmarks/input-fit-tokenizer-static-review.md](../benchmarks/input-fit-tokenizer-static-review.md) — Report on partial static artifact review and persistence stop.
- [docs/benchmarks/local-file-trial-readiness.md](../benchmarks/local-file-trial-readiness.md) — Records review findings: local-file core confirmed; readiness blocked.
- [docs/benchmarks/marker-environment-adapter-followup.md](../benchmarks/marker-environment-adapter-followup.md) — Records review findings: field correction and partial dependency comparison passed.
- [docs/benchmarks/marker-environment-adapter-review.md](../benchmarks/marker-environment-adapter-review.md) — Records review findings: adapter suite caught missing-field normalization bug.
- [docs/benchmarks/marker-environment-guard-review.md](../benchmarks/marker-environment-guard-review.md) — Records review findings: policy checks passed; platform subprocess remains blocked.
- [docs/benchmarks/metadata-identity-correction-results.md](../benchmarks/metadata-identity-correction-results.md) — Report on corrected metadata inspection completed.
- [docs/benchmarks/public-source-accounting-results.md](../benchmarks/public-source-accounting-results.md) — Report on fake-only accounting and verdict controls.
- [docs/benchmarks/public-source-detached-results.md](../benchmarks/public-source-detached-results.md) — Report on single detached stdlib validation passed.
- [docs/benchmarks/public-source-launcher-results.md](../benchmarks/public-source-launcher-results.md) — Report on instrumented probe stopped after resume.
- [docs/benchmarks/public-source-owned-identity-results.md](../benchmarks/public-source-owned-identity-results.md) — Report on additional owned image captured; count discrepancy remains.
- [docs/benchmarks/public-source-process-options.md](../benchmarks/public-source-process-options.md) — Report on console-host evidence and process-accounting options.
- [docs/benchmarks/public-source-repair-results.md](../benchmarks/public-source-repair-results.md) — Report on S startup/cleanup repair — stopped, no research.
- [docs/benchmarks/public-source-review-stop.md](../benchmarks/public-source-review-stop.md) — Report on research helper startup stop.
- [docs/benchmarks/public-source-static-diagnosis.md](../benchmarks/public-source-static-diagnosis.md) — Report on static launcher and accounting review.
- [docs/benchmarks/public-source-web-review.md](../benchmarks/public-source-web-review.md) — Report on bounded public-source review.
- [docs/benchmarks/receipt-persistence-investigation.md](../benchmarks/receipt-persistence-investigation.md) — Report on synthetic receipt-persistence investigation.
- [docs/benchmarks/reconciliation-capture-correction.md](../benchmarks/reconciliation-capture-correction.md) — Records review findings: capture verified; parser guard conflict diagnosed.
- [docs/benchmarks/remaining-artifact-readiness-continuation.md](../benchmarks/remaining-artifact-readiness-continuation.md) — Records review findings: local checks passed; public-source review stopped.
- [docs/benchmarks/remaining-artifact-readiness-review.md](../benchmarks/remaining-artifact-readiness-review.md) — Records review findings: stopped during bookkeeping bootstrap.
- [docs/benchmarks/source-licence-followup.md](../benchmarks/source-licence-followup.md) — Records review findings: response capture verified; source/licence decisions remain.
- [docs/benchmarks/stable-tokenizer-alternatives.md](../benchmarks/stable-tokenizer-alternatives.md) — Records review findings: retain the current release; decide the evidence gate.
- [docs/benchmarks/standalone-tokenizer-static-verification.md](../benchmarks/standalone-tokenizer-static-verification.md) — Records review findings: partial static identity verification.
- [docs/benchmarks/standalone-tokenizer-validation-design.md](../benchmarks/standalone-tokenizer-validation-design.md) — Report on standalone reference design findings.
- [docs/benchmarks/t17-consolidated-closeout.md](../benchmarks/t17-consolidated-closeout.md) — Records review findings: T17 consolidated closeout — 2026-11-19.
- [docs/benchmarks/t17-standalone-validation-closeout.md](../benchmarks/t17-standalone-validation-closeout.md) — Records review findings: exact dependency review and tokenizer validation status.
- [docs/benchmarks/tokenizer-bounded-frame-continuation.md](../benchmarks/tokenizer-bounded-frame-continuation.md) — Records review findings: preflight capture stop.
- [docs/benchmarks/tokenizer-cached-wheel-source-review.md](../benchmarks/tokenizer-cached-wheel-source-review.md) — Records review findings: cached Python source findings and accounting stop.
- [docs/benchmarks/tokenizer-closeout-report-fix.md](../benchmarks/tokenizer-closeout-report-fix.md) — Records review findings: closeout reporting correction.
- [docs/benchmarks/tokenizer-preflight-frame-continuation.md](../benchmarks/tokenizer-preflight-frame-continuation.md) — Records review findings: retained-source findings and readiness.
- [docs/benchmarks/tokenizer-prelaunch-gap-closure.md](../benchmarks/tokenizer-prelaunch-gap-closure.md) — Records review findings: default-expression review and prelaunch checklist.
- [docs/benchmarks/tokenizer-retained-source-review.md](../benchmarks/tokenizer-retained-source-review.md) — Records review findings: retained evidence verification and excerpt stop.
- [docs/benchmarks/tokenizer-source-metadata-continuation.md](../benchmarks/tokenizer-source-metadata-continuation.md) — Records review findings: findings.
- [docs/benchmarks/tokenizer-source-metadata-review.md](../benchmarks/tokenizer-source-metadata-review.md) — Records review findings: early stop before source or manifest access.
- [docs/benchmarks/wheel-artifact-review-reporting-correction.md](../benchmarks/wheel-artifact-review-reporting-correction.md) — Records review findings: acquisition and inert inspection completed.
- [docs/benchmarks/wheel-artifact-review.md](../benchmarks/wheel-artifact-review.md) — Records review findings: source display truncated before implementation.
- [docs/benchmarks/wheel-evidence-reconciliation.md](../benchmarks/wheel-evidence-reconciliation.md) — Records review findings: reconciliation stopped during parser controls.
- [docs/benchmarks/wheel-metadata-probe-retry.md](../benchmarks/wheel-metadata-probe-retry.md) — Records review findings: native metadata probe passed.
- [docs/benchmarks/wheel-static-inspection-continuation.md](../benchmarks/wheel-static-inspection-continuation.md) — Records review findings: reporting controls passed; probe deadline stopped execution.
- [docs/benchmarks/wheel-static-inspection.md](../benchmarks/wheel-static-inspection.md) — Records review findings: stopped before the metadata probe.
- [docs/benchmarks/windows-file-identity-results.md](../benchmarks/windows-file-identity-results.md) — Report on controls passed; host refused saved controller.
- [docs/benchmarks/windows-identity-direct-results.md](../benchmarks/windows-identity-direct-results.md) — Report on synthetic comparison completed; cross-API timestamp difference observed.
- [docs/contracts.md](../contracts.md) — Defines accepted request, storage, privacy, recovery and answer-publication boundaries.
- [docs/proposals/artifact-licence-notice-review.md](../proposals/artifact-licence-notice-review.md) — Defines the historical review plan: Tokenizers/HF-Xet artifact licence and notice review.
- [docs/proposals/controlled-local-file-tokenizer-trial.md](../proposals/controlled-local-file-tokenizer-trial.md) — Defines the historical review plan: controlled local-file tokenizer trial proposal.
- [docs/proposals/evaluation-parent-accounting-correction.md](../proposals/evaluation-parent-accounting-correction.md) — Defines the historical review plan: shared parent accounting correction.
- [docs/proposals/hub-dependency-gap-closure.md](../proposals/hub-dependency-gap-closure.md) — Defines the historical review plan: focused metadata gap closure.
- [docs/proposals/hub-metadata-dependency-review.md](../proposals/hub-metadata-dependency-review.md) — Defines the historical review plan: Hub 2.4.0 metadata and dependency readiness.
- [docs/proposals/hub-only-static-review.md](../proposals/hub-only-static-review.md) — Defines the historical review plan: bounded Hub-only static continuation.
- [docs/proposals/hub-source-coordinate-continuation.md](../proposals/hub-source-coordinate-continuation.md) — Defines the historical review plan: source-coordinate continuation with immutable accounting.
- [docs/proposals/hub-source-coordinate-review.md](../proposals/hub-source-coordinate-review.md) — Defines the historical review plan: Hub source-coordinate reconciliation.
- [docs/proposals/hub-source-reporting-continuation.md](../proposals/hub-source-reporting-continuation.md) — Defines the historical review plan: runtime-compatible reporting continuation.
- [docs/proposals/input-fit-adapter-comparison.md](../proposals/input-fit-adapter-comparison.md) — Plan for counting-adapter comparison and proposed validation contract.
- [docs/proposals/input-fit-adapter-review.md](../proposals/input-fit-adapter-review.md) — Plan for bounded counting-adapter source review and design comparison.
- [docs/proposals/input-fit-counting-integration-comparison.md](../proposals/input-fit-counting-integration-comparison.md) — Plan for standalone counting and runtime integration comparison.
- [docs/proposals/input-fit-inspection-correction.md](../proposals/input-fit-inspection-correction.md) — Plan for bounded metadata inspection correction.
- [docs/proposals/input-fit-oracle-dependency-review.md](../proposals/input-fit-oracle-dependency-review.md) — Plan for counting-oracle feasibility before dependency closure.
- [docs/proposals/input-fit-oracle-review-continuation.md](../proposals/input-fit-oracle-review-continuation.md) — Plan for summary-only oracle review continuation.
- [docs/proposals/input-fit-preflight-design.md](../proposals/input-fit-preflight-design.md) — Plan for exact input-fit preflight design.
- [docs/proposals/input-fit-remaining-assets-continuation.md](../proposals/input-fit-remaining-assets-continuation.md) — Plan for diagnostic-enabled remaining-asset continuation.
- [docs/proposals/input-fit-tokenizer-manifest-review.md](../proposals/input-fit-tokenizer-manifest-review.md) — Plan for tokenizer acquisition manifest and parity-validation design.
- [docs/proposals/input-fit-tokenizer-parity-validation.md](../proposals/input-fit-tokenizer-parity-validation.md) — Plan for exact tokenizer parity validation requirements.
- [docs/proposals/input-fit-tokenizer-static-reconciliation.md](../proposals/input-fit-tokenizer-static-reconciliation.md) — Plan for bounded static tokenizer artifact reconciliation.
- [docs/proposals/local-file-tokenizer-comparison.md](../proposals/local-file-tokenizer-comparison.md) — Defines the historical review plan: local-file tokenizer comparison.
- [docs/proposals/marker-environment-adapter-review.md](../proposals/marker-environment-adapter-review.md) — Defines the historical review plan: explicit marker profiles and conditional dependency comparison.
- [docs/proposals/marker-environment-guard-review.md](../proposals/marker-environment-guard-review.md) — Defines the historical review plan: narrow marker-environment guard correction.
- [docs/proposals/metadata-identity-correction.md](../proposals/metadata-identity-correction.md) — Plan for targeted identity correction and one metadata-only attempt.
- [docs/proposals/public-source-launcher-validation.md](../proposals/public-source-launcher-validation.md) — Plan for proposed instrumented launcher validation.
- [docs/proposals/public-source-owned-identity.md](../proposals/public-source-owned-identity.md) — Plan for proposed effective-limit and owned-image investigation.
- [docs/proposals/public-source-web-review.md](../proposals/public-source-web-review.md) — Plan for public-source refresh and input-fit method review.
- [docs/proposals/receipt-persistence-investigation.md](../proposals/receipt-persistence-investigation.md) — Plan for synthetic receipt-persistence investigation.
- [docs/proposals/reconciliation-capture-correction.md](../proposals/reconciliation-capture-correction.md) — Defines the historical review plan: complete subprocess capture before parser review.
- [docs/proposals/remaining-artifact-readiness-continuation.md](../proposals/remaining-artifact-readiness-continuation.md) — Defines the historical review plan: correct bookkeeping, then finish the retained-artifact review.
- [docs/proposals/remaining-artifact-readiness-review.md](../proposals/remaining-artifact-readiness-review.md) — Defines the historical review plan: remaining platform, Python, licence and provenance evidence.
- [docs/proposals/source-licence-followup.md](../proposals/source-licence-followup.md) — Defines the historical review plan: response retention and remaining source/licence evidence.
- [docs/proposals/stable-tokenizer-alternatives-review.md](../proposals/stable-tokenizer-alternatives-review.md) — Defines the historical review plan: stable Hub options and evidence requirements.
- [docs/proposals/standalone-tokenizer-parity-trial-design.md](../proposals/standalone-tokenizer-parity-trial-design.md) — Plan for Standalone tokenizer parity — staged trial design, not execution approval.
- [docs/proposals/standalone-tokenizer-static-verification.md](../proposals/standalone-tokenizer-static-verification.md) — Defines the historical static runtime/tokenizer review; later findings are recorded in its benchmark report.
- [docs/proposals/standalone-tokenizer-validation-design.md](../proposals/standalone-tokenizer-validation-design.md) — Plan for standalone tokenizer validation design.
- [docs/proposals/t17-architecture-readiness.md](../proposals/t17-architecture-readiness.md) — Plan for architecture readiness and design/adoption package.
- [docs/proposals/t17-consolidated-closeout.md](../proposals/t17-consolidated-closeout.md) — Defines the historical review plan: T17 consolidated closeout — 2026-11-19.
- [docs/proposals/t17-standalone-validation-closeout.md](../proposals/t17-standalone-validation-closeout.md) — Defines the historical review plan: standalone dependency and input-fit closeout.
- [docs/proposals/tokenizer-bounded-frame-continuation.md](../proposals/tokenizer-bounded-frame-continuation.md) — Defines the historical review plan: finish retained-source review with bounded excerpts.
- [docs/proposals/tokenizer-cached-wheel-source-review.md](../proposals/tokenizer-cached-wheel-source-review.md) — Defines the historical review plan: cached Tokenizers Python-source review.
- [docs/proposals/tokenizer-closeout-reporting-fix.md](../proposals/tokenizer-closeout-reporting-fix.md) — Defines the historical review plan: bounded closeout-reporting correction.
- [docs/proposals/tokenizer-preflight-frame-continuation.md](../proposals/tokenizer-preflight-frame-continuation.md) — Defines the historical review plan: bounded preflight and retained-source review.
- [docs/proposals/tokenizer-prelaunch-gap-closure.md](../proposals/tokenizer-prelaunch-gap-closure.md) — Defines the historical review plan: targeted prelaunch-gap closure.
- [docs/proposals/tokenizer-retained-source-review.md](../proposals/tokenizer-retained-source-review.md) — Defines the historical review plan: review retained tokenizer/source evidence.
- [docs/proposals/tokenizer-source-metadata-continuation.md](../proposals/tokenizer-source-metadata-continuation.md) — Defines the historical review plan: small-page source and metadata continuation.
- [docs/proposals/tokenizer-source-metadata-request.md](../proposals/tokenizer-source-metadata-request.md) — Defines the historical review plan: bounded pinned-source and manifest request.
- [docs/proposals/wheel-artifact-review-reporting-correction.md](../proposals/wheel-artifact-review-reporting-correction.md) — Defines the historical review plan: host-reporting correction to artifact review.
- [docs/proposals/wheel-artifact-review.md](../proposals/wheel-artifact-review.md) — Defines the historical review plan: bounded acquisition and inert wheel inspection.
- [docs/proposals/wheel-evidence-reconciliation.md](../proposals/wheel-evidence-reconciliation.md) — Defines the historical review plan: dependency, licence and provenance reconciliation.
- [docs/proposals/wheel-metadata-probe-retry.md](../proposals/wheel-metadata-probe-retry.md) — Defines the historical review plan: one metadata probe using the existing controls.
- [docs/proposals/wheel-static-inspection-continuation.md](../proposals/wheel-static-inspection-continuation.md) — Defines the historical review plan: continuation with bounded reporting.
- [docs/proposals/wheel-static-inspection.md](../proposals/wheel-static-inspection.md) — Defines the historical review plan: bounded wheel acquisition and static inspection.
- [docs/proposals/windows-file-identity-investigation.md](../proposals/windows-file-identity-investigation.md) — Plan for synthetic Windows file-identity investigation.
- [docs/proposals/windows-identity-direct-controller.md](../proposals/windows-identity-direct-controller.md) — Plan for host preflight and one direct-controller synthetic trial.

**Evaluation programs, tests, manifests and scripts**

- [tests/evals/spikes/evaluation_parent_accounting.py](../../tests/evals/spikes/evaluation_parent_accounting.py) — Shares process/output allowances across evaluation helpers and child checks.
- [tests/evals/spikes/hub_static_review.py](../../tests/evals/spikes/hub_static_review.py) — Inspects the cached Hub package and dependencies without importing it.
- [tests/evals/spikes/input_fit_metadata.py](../../tests/evals/spikes/input_fit_metadata.py) — Reads selected model metadata without loading models or using the network.
- [tests/evals/spikes/input_fit_metadata_corrected.py](../../tests/evals/spikes/input_fit_metadata_corrected.py) — Reads model metadata with corrected Windows file-identity checks.
- [tests/evals/spikes/public_source_accounting.py](../../tests/evals/spikes/public_source_accounting.py) — Checks research accounting rules using simulated observations.
- [tests/evals/spikes/public_source_detached.py](../../tests/evals/spikes/public_source_detached.py) — Checks ownership and resource limits for a detached research worker.
- [tests/evals/spikes/public_source_identity.py](../../tests/evals/spikes/public_source_identity.py) — Records owned process identities and effective Windows job limits.
- [tests/evals/spikes/public_source_launcher.py](../../tests/evals/spikes/public_source_launcher.py) — Investigates starting and stopping a controlled research worker.
- [tests/evals/spikes/public_source_repair.py](../../tests/evals/spikes/public_source_repair.py) — Investigates research-worker startup and cleanup without network access.
- [tests/evals/spikes/public_source_review.py](../../tests/evals/spikes/public_source_review.py) — Controls bounded public-source research without loading candidate software.
- [tests/evals/spikes/receipt_persistence_review.py](../../tests/evals/spikes/receipt_persistence_review.py) — Investigates receipt-writing failures using synthetic files and controlled locking.
- [tests/evals/spikes/remaining_asset_review.py](../../tests/evals/spikes/remaining_asset_review.py) — Acquires only remaining approved tokenizer files with strict limits and diagnostics.
- [tests/evals/spikes/standalone_static_verification.py](../../tests/evals/spikes/standalone_static_verification.py) — Checks retained runtime and tokenizer records without starting a model.
- [tests/evals/spikes/t17_fit_contract.py](../../tests/evals/spikes/t17_fit_contract.py) — Simulates packing, budget refusal, identity changes and cancellation; not application admission code.
- [tests/evals/spikes/t17_model_metadata.py](../../tests/evals/spikes/t17_model_metadata.py) — Reads bounded model metadata and verifies complete hashes without running a model.
- [tests/evals/spikes/test_evaluation_parent_accounting.py](../../tests/evals/spikes/test_evaluation_parent_accounting.py) — Tests shared accounting and refusal at evaluation limits.
- [tests/evals/spikes/test_hub_static_review.py](../../tests/evals/spikes/test_hub_static_review.py) — Tests Hub inspection and malformed-package rejection.
- [tests/evals/spikes/test_input_fit_metadata.py](../../tests/evals/spikes/test_input_fit_metadata.py) — Tests the original metadata reader and its safety boundaries.
- [tests/evals/spikes/test_input_fit_metadata_corrected.py](../../tests/evals/spikes/test_input_fit_metadata_corrected.py) — Tests corrected file-identity and timestamp checks.
- [tests/evals/spikes/test_public_source_accounting.py](../../tests/evals/spikes/test_public_source_accounting.py) — Tests shared research accounting and simulated verdicts.
- [tests/evals/spikes/test_public_source_detached.py](../../tests/evals/spikes/test_public_source_detached.py) — Tests detached-worker ownership and resource controls.
- [tests/evals/spikes/test_public_source_identity.py](../../tests/evals/spikes/test_public_source_identity.py) — Tests owned-process identity checks and rejection cases.
- [tests/evals/spikes/test_public_source_launcher.py](../../tests/evals/spikes/test_public_source_launcher.py) — Tests research-worker launch controls and cleanup.
- [tests/evals/spikes/test_public_source_repair.py](../../tests/evals/spikes/test_public_source_repair.py) — Tests startup and cleanup repairs without external research.
- [tests/evals/spikes/test_public_source_review.py](../../tests/evals/spikes/test_public_source_review.py) — Tests public-source research safeguards and limits.
- [tests/evals/spikes/test_receipt_persistence_review.py](../../tests/evals/spikes/test_receipt_persistence_review.py) — Tests receipt-writing failures, journals and handle cleanup.
- [tests/evals/spikes/test_remaining_asset_review.py](../../tests/evals/spikes/test_remaining_asset_review.py) — Tests remaining-file identity, redirects, download and reporting limits.
- [tests/evals/spikes/test_standalone_static_verification.py](../../tests/evals/spikes/test_standalone_static_verification.py) — Tests static runtime and tokenizer verification controls.
- [tests/evals/spikes/test_t17_fit_contract.py](../../tests/evals/spikes/test_t17_fit_contract.py) — Tests simulated token-budget, packing, source-identity and cancellation rules.
- [tests/evals/spikes/test_t17_model_metadata.py](../../tests/evals/spikes/test_t17_model_metadata.py) — Tests metadata limits, malformed model files and changed hashes.
- [tests/evals/spikes/test_tokenizer_static_review.py](../../tests/evals/spikes/test_tokenizer_static_review.py) — Tests tokenizer package integrity and download boundaries.
- [tests/evals/spikes/test_tokenizer_wheel_source_review.py](../../tests/evals/spikes/test_tokenizer_wheel_source_review.py) — Tests bounded reading of cached tokenizer Python source.
- [tests/evals/spikes/test_wheel_static_inspection.py](../../tests/evals/spikes/test_wheel_static_inspection.py) — Tests package records, unsafe archive rejection and inspection boundaries.
- [tests/evals/spikes/test_windows_file_identity.py](../../tests/evals/spikes/test_windows_file_identity.py) — Tests synthetic Windows file-identity investigation controls.
- [tests/evals/spikes/test_windows_file_identity_followup.py](../../tests/evals/spikes/test_windows_file_identity_followup.py) — Tests direct-controller identity investigation controls.
- [tests/evals/spikes/tokenizer_static_review.py](../../tests/evals/spikes/tokenizer_static_review.py) — Checks approved tokenizer downloads, package contents and file identities without importing them.
- [tests/evals/spikes/tokenizer_wheel_source_review.py](../../tests/evals/spikes/tokenizer_wheel_source_review.py) — Reads selected cached tokenizer Python files as data to investigate loading.
- [tests/evals/spikes/wheel_static_inspection.py](../../tests/evals/spikes/wheel_static_inspection.py) — Acquires/checks approved package archives without installing or importing them.
- [tests/evals/spikes/windows_file_identity.py](../../tests/evals/spikes/windows_file_identity.py) — Investigates Windows file timestamps and identities using a synthetic file.
- [tests/evals/spikes/windows_file_identity_followup.py](../../tests/evals/spikes/windows_file_identity_followup.py) — Runs the approved synthetic identity comparison through a fresh direct controller.

</details>

## 3. File Coverage and Shared Ownership

The catalogue contains **288 committed research files**: **9 root files**, **198 files under docs/** and **81 files under tests/evals/**. Each appears once under its primary task. This includes Markdown, Python programs/tests, JSON definitions, the PowerShell handoff, configuration, the lockfile and root ignore/interpreter files.

AGENTS, SPEC, PLAN, TODO, README, the decision register and dependency/provisioning notes were updated by many tasks. This grouping does not imply exclusive ownership. Narrower T17 investigation codes are grouped under their parent task.

Private samples, model downloads, installed environments, caches, databases and generated trial outputs are excluded. Supplied agents/skills/references/design images are inputs, not claimed as files created by these tasks. The historical checkpoint is listed for completeness; its updates were disabled and this edit leaves it unchanged.

The separate T18 setup test/pending changes and this summary itself are outside the committed T01–T17 research-file count.

## 4. Git Commits


The reviewed history contains **183 commits**, from **bb68c40** to **2698240**. Each is listed with its actual short explanation. A research, planning or test-tool commit does not itself represent a finished application feature.

<details>
<summary>All 183 research-session commits, oldest first</summary>

| Commit | What changed |
| --- | --- |
| `bb68c40` | Initialize Stage 1 setup, planning, and evaluation definitions |
| `eaad7f1` | Defer SkillSpector and record manual review fallback |
| `d8d12e7` | Evaluate permissive PDF parsers with bounded local trials |
| `e1ee6ff` | Restrict Stage 1 formats to PDF XLS XLSX and CSV |
| `28ec7ad` | Align evaluation definitions with four-format Stage 1 scope |
| `e8ec471` | Evaluate XLSX and CSV parsers and streamline approved work packages |
| `55d68f6` | Complete bounded T10 embedding comparison and resource accounting |
| `0872c22` | Record bounded T11A chat benchmarks and pending semantic review |
| `130e979` | Record user acceptance of local T11A answer review |
| `e3c598d` | Document approved T07A XLS parser evaluation package |
| `535339f` | Record T07A native network preflight stop and control tests |
| `6724ac1` | Defer legacy XLS and limit Stage 1 to PDF XLSX CSV |
| `1621862` | Record MarkItDown review and approved trial deferral |
| `1337560` | Document local English OCR shortlist and trial prerequisites |
| `bf3b82e` | Approve bounded OCR artifact preparation proposal |
| `7c50144` | Record bounded OCR artifact preparation stop |
| `6491666` | Record FlatBuffers license provenance and approved continuation |
| `44a8be8` | Record verified OCR artifacts and preparation results |
| `5374496` | Document OCR execution boundary alternatives and recommendation |
| `e6ecd5a` | Approve bounded AppContainer isolation preflight proposal |
| `9bdfef0` | Record stopped AppContainer preflight and evaluation helpers |
| `1658cdc` | Approve bounded Python startup diagnostic proposal |
| `c52151a` | Record startup contrasts and native accounting stop |
| `ab1a04d` | Preserve startup diagnostic evidence before accounting stop |
| `db50257` | Approve bounded Job accounting investigation |
| `a1f511c` | Record Job accounting snapshots and preserved safety stop |
| `2475ef8` | Approve bounded launch flag comparison |
| `ed11d68` | Record no-window flag association and preserved accounting stop |
| `ed4cb3a` | Record consolidated isolation validation and permission stop |
| `76db076` | Approve manual disconnected synthetic OCR trial package |
| `c7709cd` | Prepare sealed manual offline synthetic OCR runner |
| `6120666` | Normalize distribution aliases before offline OCR pin checks |
| `0766743` | Prepare approved fresh offline OCR continuation and checkpoint |
| `0797fe5` | Fix RapidOCR enum configuration and prepare approved offline continuation |
| `94f3e46` | Record completed offline OCR comparison and rotated-case review limitation |
| `53b9de1` | Prepare approved bounded combined OCR and model offline evaluation |
| `e55a2b7` | Repair shared OCR deadlines and live storage accounting with sanitized diagnostics |
| `d9a2792` | Prepare approved combined-03 offline evaluation after live storage repair |
| `28844cb` | Preserve failing combined resource measurements and record third trial stop |
| `473d24a` | Approve bounded combined-04 evaluation package and task sequence |
| `7ca4ee3` | Prepare approved combined-04 offline trial with resource diagnostics |
| `74fb75a` | Record combined-04 sampling-gap stop and verified teardown |
| `fd3361b` | Approve bounded fake-only monitor cadence repair |
| `0b345d5` | Repair monitor cadence and enforce measured timing intervals |
| `79a2dea` | Approve bounded combined-05 evaluation after monitor repair |
| `888f184` | Prepare approved combined-05 trial with repaired monitor |
| `dbe607a` | Record combined-05 atomic replacement denial and verified teardown |
| `4a2261e` | Approve bounded synthetic state-file investigation |
| `612378a` | Record synthetic state-write investigation and safe operation diagnostics |
| `2a65871` | Approve bounded state reader-writer coordination repair |
| `92f3b67` | Coordinate owned state readers and writers and skip unchanged counters |
| `a7732ab` | Approve bounded combined-06 evaluation with committed safety repairs |
| `eeda648` | Record combined-06 preparation, partial overlap results and timing stop |
| `7586f68` | Approve bounded 300ms monitor policy implementation |
| `c47dfda` | Apply approved 300ms combined monitoring ceiling |
| `1dddbcb` | Approve combined-07 offline evaluation package |
| `1428cfd` | Prepare combined-07 trial and clarify package approval workflow |
| `b225d57` | Record completed combined-07 trial and pending answer review |
| `69a01b4` | Record user acceptance of combined-07 answers and citations |
| `48f0333` | Record approved model and OCR shortlist for design review |
| `976455c` | Approve bounded T12 storage baseline evaluation |
| `a54b38b` | Record T12 SQLite baseline and partial scale results |
| `dcb70be` | Approve exact sqlite-vec Windows artifact review |
| `3092aeb` | Record static sqlite-vec artifact inspection and notice blocker |
| `48cdf72` | Record accepted exact-wheel companion notice exception |
| `9478fea` | Approve T12 runtime comparison and save resume checkpoint |
| `d5e8c68` | Prepare approved T12 disconnected sqlite-vec comparison |
| `8353db0` | Record T12 runtime startup timing failure and checkpoint |
| `aef0b25` | Approve bounded T12 startup correction and replacement trial |
| `960fa7c` | Fix T12 startup accounting and prepare approved offline comparison |
| `4146d7c` | Record partial T12 native results and MATCH authorization refusal |
| `5a82a70` | Approve focused T12 MATCH permission correction package |
| `e4db995` | Fix MATCH authorization and prepare bounded remaining storage trial |
| `18be917` | Record completed T12 storage comparison and verified teardown |
| `cc08343` | Record preferred storage candidate and propose T16 design package |
| `486fd1b` | Draft T16 grounding contracts and record approved storage policies |
| `cdbb975` | Complete T16 static review and record approved design directions |
| `e9d107e` | Prepare T17 architecture readiness and record chart trial deferral |
| `dbd9137` | Prepare T17 architecture contracts and record approved operating policies |
| `986305d` | Record public research startup failure and bounded repair proposal |
| `832bb06` | Preserve partial no-network repair and execution-accounting findings |
| `3f7591a` | Review launcher accounting and propose fake-only admission controls |
| `bcdb9c4` | Validate fake-only accounting admission and control verdicts |
| `c023f37` | Plan bounded instrumented Windows launcher validation |
| `91d6433` | Record instrumented launcher stop and verified owned cleanup |
| `7fae685` | Plan one-worker owned identity and effective-limit investigation |
| `4847f1b` | Record owned conhost identity and effective job-limit evidence |
| `3dddbc8` | Review console-host accounting options and propose detached validation |
| `c6e8952` | Validate single detached stdlib worker and preserve bounded results |
| `780bad2` | Plan bounded public-source web review and input-fit investigation |
| `197eb6e` | Record bounded dependency source review and input-fit gaps |
| `145278f` | Define input-fit admission contract and bounded static artifact review |
| `f1b62d4` | Preserve partial model metadata inspection and verified shell stop |
| `dee832a` | Plan bounded metadata inspection correction with owned timeout |
| `9a72136` | Preserve bounded metadata identity refusal and verified child exit |
| `16d6f97` | Plan synthetic Windows file identity investigation |
| `c94d6da` | Record synthetic identity controls and pre-execution policy block |
| `a084243` | Plan host preflight and direct synthetic identity controller |
| `6f1e007` | Record successful synthetic Windows timestamp comparison |
| `c4dff2d` | Plan targeted metadata identity correction and bounded read |
| `bc6f677` | Verify pinned model metadata with corrected identity checks |
| `0a3a709` | Plan bounded counting adapter source review and comparison |
| `6a06493` | Record counting adapter source findings and conditional comparison |
| `6b67433` | Plan bounded tokenizer manifest and parity design review |
| `2275acc` | Record partial tokenizer manifest and parity validation requirements |
| `b8ebed3` | Plan bounded static tokenizer artifact reconciliation |
| `1770d69` | Record bounded tokenizer artifact inspection and persistence stop |
| `3b43968` | Plan synthetic receipt persistence investigation |
| `a13e8b2` | Record synthetic persistence diagnostics and controlled locking results |
| `2533f27` | Plan diagnostic continuation for remaining tokenizer data assets |
| `2fa113c` | Record remaining tokenizer asset identities and bounded diagnostics |
| `be1690a` | Plan oracle-first runtime counting feasibility review |
| `fd9cf38` | Record oracle review reporting stop and preserved checkpoint |
| `fa670fa` | Plan precharged summary-only oracle review continuation |
| `17e0e70` | Record counting interface review and integration decision |
| `aae897e` | Compare counting integrations and record standalone direction approval |
| `68a878c` | Plan standalone tokenizer validation against bundled runtime |
| `8d25bd7` | Record standalone tokenizer reference feasibility and staged validation design |
| `fca4bb9` | Record approved static verification package and execution stop |
| `9462a08` | Document static verification stop and bounded continuation |
| `740dc3a` | Record second reporting stop and measured-output continuation |
| `2ad9cb1` | Verify installed runtime identities and record Hub entry-limit stop |
| `9834ce4` | Plan bounded Hub-only static review and dependency continuation |
| `12416e1` | Verify Hub wheel records and record unresolved source provenance |
| `0868f05` | Plan bounded Hub publisher and source-coordinate reconciliation |
| `c404b61` | Record source-review accounting stop and protected closeout |
| `fd5f61b` | Plan immutable-accounting source-coordinate continuation |
| `7d60633` | Record immutable-accounting success and source-response reporting stop |
| `aa61658` | Plan runtime-compatible source-review reporting continuation |
| `ec34c59` | Record exact-wheel publisher evidence and unresolved build-source gate |
| `e1a1571` | Plan bounded stable Hub options and evidence-gate review |
| `0d4003e` | Record stable comparison and approved metadata-review timing deferral |
| `ed7ec1b` | Plan bounded Hub metadata and dependency readiness review |
| `e25690b` | Record partial dependency graph and remaining readiness gaps |
| `0768aea` | Plan focused dependency gaps with reserved closeout time |
| `90a01de` | Record dependency gap evidence and disable session checkpoint files |
| `424962f` | Plan bounded wheel acquisition and static inspection |
| `5ec1002` | Record wheel inspection stop before metadata probe |
| `2aa9ea7` | Plan wheel inspection continuation with bounded reporting |
| `0882bc0` | Record reporting controls and missed probe start deadline |
| `103a6f1` | Plan metadata-only probe with explicit host-wait accounting |
| `7c4e172` | Record successful native metadata probe and verified teardown |
| `b466a78` | Plan guarded wheel acquisition and static inspection |
| `1d30457` | Record source-display stop before artifact implementation |
| `42a2aea` | Plan artifact review with tested host-display bounds |
| `8bf88b3` | Add guarded inert wheel review aids and verified artifact findings |
| `f3dad02` | Plan bounded dependency licence and provenance reconciliation |
| `2b8f4ce` | Record reconciliation stop and incomplete diagnostic capture |
| `86bdaa9` | Plan complete-stream capture correction before parser retry |
| `d36bd49` | Verify complete capture and diagnose hostname audit blocker |
| `299498d` | Plan narrow hostname audit exception and marker controls |
| `a0578ce` | Record marker policy checks and blocked Windows version helper |
| `a09d8cc` | Plan explicit marker profiles and conditional dependency comparison |
| `629fc82` | Record adapter field failures and bounded correction follow-up |
| `da860aa` | Verify adapter correction and partial dependency comparison |
| `da952e1` | Plan bounded remaining artifact readiness review |
| `e5d037c` | Record bounded readiness review bootstrap stop |
| `234e07d` | Plan tested bookkeeping and remaining artifact review continuation |
| `cc0905f` | Record passing artifact checks and bounded public-source stop |
| `a382e7e` | Plan focused response retention and source licence review |
| `832191c` | Record retained source responses and remaining licence decisions |
| `a1e3240` | Plan targeted Tokenizers and HF-Xet licence notice review |
| `fc0d8f5` | Record artifact licence evidence and remaining native notice gaps |
| `cbfedf3` | Compare local-file tokenizer loading and declared dependencies |
| `8e846c1` | Plan bounded local-file tokenizer trial readiness checks |
| `073025c` | Record local-file source evidence and blocked trial readiness |
| `4a8275a` | Plan cached wheel Python source and CPU reference review |
| `5d28c59` | Record cached Python source findings and validate parent accounting |
| `b4e880f` | Plan retained tokenizer source and CPU contract review |
| `acfc5f3` | Record retained source verification and excerpt capture stop |
| `96022c9` | Record bounded-frame preflight capture stop |
| `55ecaf3` | Plan preflight-bounded retained tokenizer source review |
| `4cc2d24` | Record bounded tokenizer source review and prelaunch gaps |
| `1f94a74` | Plan targeted tokenizer prelaunch-gap closure |
| `679194b` | Record targeted tokenizer prelaunch checklist and source gaps |
| `625a347` | Record tokenizer source-metadata prebootstrap stop and preserved evidence |
| `68e012c` | Plan small-page tokenizer source and metadata continuation |
| `8c07563` | Record SMC findings and plan bounded closeout reporting correction |
| `34ca104` | Record validated closeout reporting correction and T17 evidence |
| `2f77c79` | Consolidate T17 component validation and explicit G2 blockers |
| `86885e2` | Record user selection of standalone tokenizer direction |
| `8529155` | Record exact standalone dependency checks and remaining T17 blockers |
| `2698240` | Close T17 with G2 approval and select Ollama internal tokenization |
</details>

## 5. Important Decisions

- Keep Windows 11, 16 GB RAM and CPU-only as the target; larger-machine results are not target proof.
- Support PDF/XLSX/CSV. XLS is deferred; DOCX/TXT are excluded from Stage 1.
- Keep processing, models, prompts, answers and storage local. Install project dependencies in the dedicated environment.
- Deliver CSV upload → evidence → answer → citation → saved chat first. Chart interpretation follows that first flow.
- Preserve source locations, shared library documents and missing-evidence warnings. Chat deletion removes exclusive data while preserving shared/library content.
- Describe observed support and limitations without presenting citation checks as a correctness percentage.
- Use Ollama's internal tokenizer. The earlier standalone route is historical and no longer selected for installation.
- Accept G2 with the omitted investigations explicitly unverified. Normal implementation tests, privacy requirements and final Stage 1 acceptance remain required.

## 6. Testing and What the Evidence Means

The session included parser comparisons, local model/storage benchmarks, simulated failure controls and user-operated disconnected OCR/model trials. The final OCR schedule completed **60 comparisons and 20 controls**. Combined-07 completed **36 answers**; citation-scope checks passed and the user qualitatively accepted the local answers. T11A completed all 96 planned chat slots across 97 attempts.

T17 added **21 metadata/simulated-input tests** and **eleven packaged-reference count matches**: eight chat cases and three embedding cases. These were separate checks, not a full standalone/Ollama proof or a complete application regression suite. Later package checks verified static identities and compatibility declarations without installing the standalone tokenizer.

Problems included Windows launch/accounting restrictions, script-policy blocks, OCR configuration errors, timing stops, state-file replacement failures, timestamp differences and reporting errors. Reports preserve fixes, partial results, unproven causes and execution/reporting deviations. Small synthetic successes do not prove broad document quality, a working app or physical-16-GB performance.

Some controls protected the trial process rather than product behaviour. During T17, repeated control/review repairs became disproportionate and delayed the compatibility question. That loop was stopped by user decisions. The omitted selected-runtime trust, exact input-fit/output-boundary and target-machine checks remain **unverified**, not passed.

No application, model, OCR or historical evaluation trial was rerun to rewrite this report. This edit is checked for coverage, grouping, links, formatting and preservation of unrelated work.

## 7. Current Status

**Research:** T01–T17 evaluations and accepted deferrals supplied the architecture decision. **T17/G2 is closed in 2698240**, with the recorded limitations. The design selects a local browser/Python app, SQLite/sqlite-vec, the evaluated PDF/XLSX/CSV/OCR paths and local Ollama with internal tokenization.

**Working evidence/tools:** the dedicated environment, evaluation runners, definitions, actual local component trials and retained results. These are development assets; the complete user-facing assistant is not built yet.

**After the research boundary:** T18 foundations have since passed the offline lock check, four setup smoke tests and Ruff checks. Those source/configuration changes remain uncommitted; they are subsequent implementation foundations, outside this research-file count.

**Still ahead:** the working CSV-to-saved-chat flow, PDF/OCR/XLSX integration, application-level reliability/privacy/citation checks and Stage 1 acceptance. UI UX Pro Max remains pending before frontend implementation; SkillSpector remains deferred. This summary edit makes no Git commit.

## 8. Next Step

Finish the pending T18 source/configuration commit decision. The next implementation task is **T19**, after its applicable package approval, followed by the CSV-first sequence. Reuse completed research and normal test-first development. Omitted T17 investigations and closed historical trials are not an automatic retry queue.
