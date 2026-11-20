# T22 — Reproducible local fixture harness

Date: 2026-11-20. The user authorized T22 by instructing continuation after T21 commit `daf10c5`. The user also approved a blank image-only scan page. Following clarification, it is an **empty-page** control: expected absence of text/evidence, not a test of visible illegible text. The original illegibility/blur trial remains unverified; no new unreadability threshold is selected. Chart interpretation trials remain deferred until after the first CSV flow/T34.

## Implementation

`tests/fixtures/factories.py` selects six active authored definitions: S-CSV, S-CSV-INJECTION, S-XLSX, S-PDF-NATIVE, S-PDF-SCAN and S-PDF-MIXED. It does not open source_samples originals, materialize excluded formats or enable scoring. Source manifest/questions remain unchanged. Local ground-truth receipts retain definition expectations, SHA256/byte identities and explicit empty-page limitations. The unchanged manifest's original unreadable-page expectation is not claimed as passed.

Fixtures use existing pinned packages: standard-library CSV/ZIP/JSON, openpyxl3.1.5, pypdf7.0.1, Pillow13.0.0 and PDFium through pypdfium2 5.15.2 for visual checks. Workbook core timestamps/ZIP timestamps/order are canonicalized; PDF authoring uses fixed content/resources without time-dependent metadata. Formula strings remain inert and cached values absent. The PDF helper uses the pinned writer's private object-registration helper solely inside test support; package upgrades need fixture regression review. No additional authoring/runtime dependency is installed.

Factories require an explicit shared budget and an ignored project output root, reject traversal/reparse ancestry, and use exclusive creates without overwriting prior artifacts. Writes are charged before persistence; failed writes keep conservative charges. A root may retain partial synthetic output if a later write fails; cleanup is not falsely reported. Generated artifacts and receipts remain under ignored data or generated-fixture roots. Routine pytest defaults to a fresh ignored project-local test root. No existing/private root is recursively removed by this harness.

The in-memory HTTPX MockTransport implements synthetic Ollama tags, embedding/chat and missing-model responses. Other hosts/ports are refused, proxy use is disabled, and no sockets or model process are used. These fixture responses do not establish real model API interoperability or grounding quality.

## Shared execution boundary

`tests/conftest.py` provides one autouse meter to all routine tests. `tests/fixtures/budget.py` accounts for the pytest controller, every admitted subprocess start, generated artifacts/ground-truth/rendered PNG bytes and captured stdout/stderr across existing launcher/storage regressions and new controls. Limits are 64 starts, 2,000,000 retained bytes and a 120-second admission/owned-child deadline, per routine invocation. These are harness limits, not adopted product budgets or renewed native/model trial allocations.

Popen is wrapped for the entire session. Pipe readers charge chunks before retaining them; overflow kills the owned child and propagates an error. Child timers and bounded waits respect the shared deadline. Start/output exhaustion remains sticky across categories; failed starts are not refunded. The wrapper admits only the exact current project interpreter and the exact read-only Windows shell command `ver`, used indirectly by platform detection. Arbitrary shell commands/native executables are refused. No parser/model process is launched; future native process trees must use a separately approved descendant-accounted runner. This wrapper does not confine malicious Python descendants or provide a hard watchdog for pure controller code. Only actual supported children in this routine suite are claimed covered.

## Verification

Tests were written first; initial collection failed because the fixture modules did not exist. The first ten cases passed after implementation. Additional checks added output-overflow child stopping, invalid allocations, traversal refusal and PDF rendering. The first rendering run correctly refused an unaccounted indirect Windows version query from platform detection. Source inspection identified exact `ver`; narrowly admitting/charging that probe resolved the failure. No general shell permission was added.

Final commands:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest -q -rP -p no:cacheprovider --basetemp=data/t22-final-04 --tb=short
.\.venv\Scripts\ruff.exe check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration
.\.venv\Scripts\ruff.exe format --check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration
```

Observed **123 passed, 1 skipped, 1 warning in 7.48 seconds**; Ruff passed, all nineteen checked files formatted. The skip is the existing Windows symlink-creation restriction; the retained warning is Starlette's HTTPX integration deprecation. No test was weakened/disabled and no warning suppressed. Six shared starts were charged: controller, two launcher regressions, storage crash child, capture child and Windows version probe. Retained artifact/output total: **262,980 bytes**. Isolated fake-meter exhaustion tests do not launch native/model children or reset this live session allocation.

Sixteen new tests verify manifest selection without private originals, repeated identical bytes/hashes/ground truth, quoted/multiline/injection CSV content, workbook sheets/formula/missing-cache/merge preservation, native/scanned/mixed PDF structure, exclusive writes, traversal refusal, shared category/exhaustion behavior, deterministic deadlines/output limits, captured-child accounting, mock Ollama routing, overflow stopping and all seven PDF page renders. No private document was used; scores remain false.

The PDF skill marker was read/reviewed and run using the installed VS Code executable's headless Node runtime (v24.22.1); no Node installation/global PATH modification. Initial PowerShell invocations did not reliably wait/report GUI-subsystem exit status and emitted crash-handler diagnostics. A waited hidden subprocess with host permission verified marker exit0 before PDF generation. Its own 264-byte diagnostic log was moved into ignored data. No external operation or visible GUI was requested. This setup marker is outside the routine suite's child meter and is not described as a native/model trial.

All seven PDF pages were rendered with existing PDFium because Poppler was unavailable. A local contact sheet was visually inspected: phase A/B/C text and page order, native budget, table/bar reference, invoice image text and blank page were legible/consistent and unclipped. The small contact-sheet QA artifact is outside the suite receipt and stays ignored; the individual rendered page PNGs are included in its shared byte meter. No OCR was run, so recognition fidelity, confidence, unreadable-text handling and answer abstention are not scored.

Review mutation changed start-limit refusal from >= to >. The shared-category exhaustion test failed as expected; original source bytes were restored exactly. The correct-source full-suite evidence applies to those restored bytes. Review also checked output containment, immutable source definitions, no-overwrite semantics, inherited logging/proxy behavior and private-source separation.

## Closeout and limits

The fixture harness enables representative tests, not implemented application ingestion or evaluated document/model quality. Protected/encrypted/full-scale formats, real illegible-text behavior, parser scale/rotation quality, native/model descendant accounting and scored citations remain later gates. Prior native/OCR/model trial roots and budgets are unchanged. This task does not begin T23, alter SPEC/AGENTS/dependencies or change manifest scoring. The user separately approved the reviewed ten-file T22 closeout and commit on 2026-11-20.

Ten authored files are intended: tests/__init__.py, tests/conftest.py, three tests/fixtures modules, tests/unit/test_eval_fixtures.py, README, PLAN, TODO and this report. Generated PDFs/XLSX/CSVs/PNGs/receipts/debug logs are excluded. The user explicitly approved the reviewed ten-file T22 closeout and commit on 2026-11-20. T23 has not started.
