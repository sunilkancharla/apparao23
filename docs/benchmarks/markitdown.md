# T08 - MarkItDown source and dependency review

**Date:** 2026-11-13. **Status:** Closed with user-approved non-adoption and empirical-trial deferral on 2026-11-13 ("okay, proceed"). Stage 1 scope is PDF/XLSX/CSV. No MarkItDown installation, import, conversion, fixture generation or model call was performed. This report is source evidence, not a benchmark.

## Recommendation for review

Do not adopt MarkItDown as the Stage 1 ingestion backbone. Prefer the existing format-specific candidates for subsequent architecture review: standard-library CSV, openpyxl with independently retained workbook metadata, and the T05 PDF candidates plus separately evaluated local OCR. Those candidates are not automatically adopted by this recommendation.

MarkItDown's Markdown is useful for readable text, but the public result contract supplies Markdown and an optional title rather than our structured source-location records. Reconstructing citations afterward would require a second provenance pipeline. This is a project-fit inference from the [result contract](https://raw.githubusercontent.com/microsoft/markitdown/v0.1.9/packages/markitdown/src/markitdown/_base_converter.py), not a measured extraction-quality verdict.

The user accepted this recommendation and explicitly approved committing the review and proceeding to the T09 read-only OCR review. The empirical T08 comparison is deferred by that decision; source review is not a benchmark. No execution package, runtime parser adoption or OCR installation is authorized.

## Identity, license and maintenance

- Official project: `microsoft/markitdown`; reviewed release **v0.1.9**, GitHub release short commit `21d9c1d`, released 2026-10-21. The release notes include Windows CI and dependency/security-related maintenance. These are upstream claims, not local compatibility tests. [Releases](https://github.com/microsoft/markitdown/releases/tag/v0.1.9)
- License: **MIT**, including permission for commercial use with the required copyright/license notice. Dependency and bundled-asset licenses require their own review. [Pinned license](https://raw.githubusercontent.com/microsoft/markitdown/v0.1.9/LICENSE)
- Registry artifact: `markitdown-0.1.9-py3-none-any.whl`, **90,071 bytes**, SHA-256 `52f59c48bea9cf887224c56247f648d68beb7aa7af5a12d414748210c83c20ea`. Python requirement `>=3.10,<3.15` includes the project's observed Python 3.14.6. Artifact bytes were not downloaded or independently hashed; registry identity does not prove correspondence with tagged source. [Version metadata](https://pypi.org/pypi/markitdown/0.1.9/json)

## Dependencies and Windows/CPU implications

The pinned package declares beautifulsoup4, requests, certifi, markdownify, Magika, charset-normalizer and defusedxml. The PDF extra adds pdfminer.six/pdfplumber; XLSX adds pandas/openpyxl. The existing pinned PDF packages meet its declared PDF minimums, but no resolver or compatibility test ran. Avoid `[all]`: it adds excluded formats and remote-service integrations. A future proposal would restrict extras to PDF/XLSX and retain all existing pins. [Pinned dependency declarations](https://raw.githubusercontent.com/microsoft/markitdown/v0.1.9/packages/markitdown/pyproject.toml)

Magika is a separate content classifier, not an Ollama replacement. Its 0.6.1 documentation describes platform-specific Rust CLI binaries and a fallback Python distribution. This is an example within MarkItDown's allowed range, not a selected pin; do not infer its Python inference backend from the bundled CLI. Exact Magika, inference assets/native libraries and pandas/transitive Windows wheels still need resolution and license/asset inspection before any installation. [Magika 0.6.1 metadata](https://pypi.org/pypi/magika/0.6.1/json)

Total download/installed size, RAM and latency are **unmeasured**. The 90-KB top-level wheel is not the dependency footprint. No claim of suitability for the 16-GB CPU-only target follows from its Python version range. Compared with the existing baseline, classification and dataframe dependencies add review and provisioning work.

## Format comparison from pinned source

| Format | Observed implementation | Consequence for this project |
|---|---|---|
| PDF | Uses pdfplumber for word/form extraction, with pdfminer fallbacks; reads the input into memory and combines text into Markdown. | No structured page/region mapping in the returned contract. Fallbacks and table heuristics require explicit warnings and independent evaluation. |
| XLSX | Reads all sheets through pandas/openpyxl, emits sheet headings and converts dataframe HTML to Markdown without dataframe indexes. A repair path rewrites archive entries in memory. | Sheet headings survive, but original cell coordinates, merged ranges, formula/cache distinctions and source types need separate retention. Bound archive expansion and dataframe size before conversion. |
| CSV | Uses csv.reader, materializes rows, trims selected blank rows, pads widths, escapes pipes and collapses cell newlines. | Markdown rows cannot substitute for original record/physical-line spans. Preserve raw values and source spans in an independent representation. |

Sources: [PDF converter](https://raw.githubusercontent.com/microsoft/markitdown/v0.1.9/packages/markitdown/src/markitdown/converters/_pdf_converter.py), [XLSX converter](https://raw.githubusercontent.com/microsoft/markitdown/v0.1.9/packages/markitdown/src/markitdown/converters/_xlsx_converter.py), [CSV converter](https://raw.githubusercontent.com/microsoft/markitdown/v0.1.9/packages/markitdown/src/markitdown/converters/_csv_converter.py). These are source observations; no sample conversion or performance comparison was run.

The reviewed base PDF converter does not establish scanned/mixed-PDF OCR. OCR confidence, method and page provenance remain T09 requirements. Charts/diagrams are not understood merely by producing Markdown. The image converter can send image content to a configured LLM client; that path must remain disabled for this review and is not an approved chart solution. [Image converter](https://raw.githubusercontent.com/microsoft/markitdown/v0.1.9/packages/markitdown/src/markitdown/converters/_image_converter.py)

## Permissions, outbound behavior and security

Upstream explicitly states that conversion runs with the process's I/O privileges and recommends narrow local/stream APIs. It is not a sandbox. [Security guidance](https://github.com/microsoft/markitdown/blob/v0.1.9/README.md#security-considerations)

The constructor creates a requests session and Magika instance; built-in registration covers remote/broad-format converters, while plugins load when enabled. Configured Azure endpoints register remote converters. A constrained future trial must use only allowlisted local streams/converters, disable plugins and cloud/LLM endpoints, avoid the permissive general `convert()` entry point, and reject excluded formats before dispatch. Disabling built-ins alone does not skip constructor classification setup. None of these settings proves OS-enforced network denial. [Pinned dispatcher](https://raw.githubusercontent.com/microsoft/markitdown/v0.1.9/packages/markitdown/src/markitdown/_markitdown.py)

The inspected advisory page showed no published repository advisories. This is not a clean bill of health for the package or its unselected dependency graph. [Maintainer advisories](https://github.com/microsoft/markitdown/security/advisories)

The T07A native-network preflight remains failed readiness evidence even though XLS is now deferred. Do not reuse/reset that ledger, retry its control or claim that removing XLS resolves isolation for another package. No firewall/policy/Windows feature changes are proposed here.

## If an empirical trial is requested

Prepare a separate bounded proposal before execution:

1. Resolve exact new distributions/artifacts/hashes without changing baseline pins; inventory all licenses, native assets, Python 3.14 Windows wheels and offline initialization. Review resolver-induced changes before installation.
2. Freeze identical safe local PDF/XLSX/CSV fixtures and independently checked anchors, including native/scanned/mixed PDF readiness, multiline/blank-row CSV and workbook formula/cache/merged-cell cases. Exclude XLS/DOCX/TXT. Do not treat missing artifacts as passing coverage.
3. Define a fresh shared process/download/time/output/memory budget including controls, regressions and teardown. Verify the agreed native network and resource boundaries before document trials; stop if unavailable. Never inherit old consumed allocations.
4. Use test-first adapters to compare values, structure, missing-cache warnings and exact citation locations against T05/T07; collect actual footprint, time and memory. Keep document text/results local. OCR integration remains separately gated at T09.
5. Present measured benefit and limitations for adoption review. No optional converter is a runtime dependency until separately approved.

## Verification and limits

Reviewed pinned public source/metadata and existing T05/T07 reports; no user content was sent externally. Documentation/link and whitespace checks apply to this change. No parser, model, application, offline-runtime or security-control tests ran, and no speed/quality scores exist for MarkItDown. `pyproject.toml` and `uv.lock` are unchanged. T08 closes with the explicit evaluation exception above; empirical quality/performance remains unmeasured.
