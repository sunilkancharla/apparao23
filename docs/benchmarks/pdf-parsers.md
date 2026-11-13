# T05 - Native PDF parser evaluation

**Date:** 2026-11-13. **Status:** T05 complete with user-approved PyMuPDF empirical-comparison deferral. No runtime parser selected. PyMuPDF was reviewed from metadata but not installed or benchmarked.

## Authorization and scope

After the exact trial proposal and licensing explanation, the user said "ok sir, carry on". Proceeded with the recommended free, permissively licensed candidates: pypdf and pdfplumber. The original ten-package proposal included PyMuPDF 1.28.2; the actual trial excludes it and installs nine packages. This narrows provisioning rather than authorizing a paid license. The original PLAN/TODO/SPEC mention a PyMuPDF benchmark. Replying “ok, next step please” to the explicit closeout/deferral/commit question, the user accepted deferring that empirical comparison and authorized the T05 commit. This records an explicit evaluation exception; no PyMuPDF trial or runtime adoption is claimed.

Target remains Windows 11, 16 GB RAM, CPU only. The actual host/interpreter are documented in environment.md. Parsers ran sequentially without models/GPU inference. Tests/benchmarks are evaluation aids, not application implementation or an upload-security boundary. T06 has not started.

## Dependencies actually installed

All installations use the existing project `.venv`, Python 3.14.6 and uv 0.13.8. The optional `pdf-eval` group has these exact pins; all baseline package versions remain unchanged. Source builds were forbidden, compatible wheels used and uv.lock records registry hashes. No global packages/PATH/services were changed.

| Package | Version | Purpose | Publisher license metadata |
|---|---|---|---|
| pypdf | 7.0.1 | Pure-Python native-text/page baseline | BSD-3-Clause |
| pdfplumber | 0.11.10 | Text geometry and tables | MIT |
| pdfminer-six | 20260107 | pdfplumber text/layout engine | MIT |
| pillow | 13.0.0 | Image support/render inspection | MIT-CMU |
| pypdfium2 | 5.15.2 | PDFium rendering, required by pdfplumber | BSD-3-Clause / Apache-2.0 / dependency notices |
| charset-normalizer | 3.5.2 | Text encoding support | MIT |
| cryptography | 50.0.2 | pdfminer cryptographic primitives | Apache-2.0 OR BSD-3-Clause |
| cffi | 2.1.1 | Native interface for cryptography | MIT-0 |
| pycparser | 3.12 | cffi dependency | BSD-3-Clause |

Sources: [pypdf](https://pypi.org/project/pypdf/7.0.1/), [pdfplumber](https://pypi.org/project/pdfplumber/0.11.10/), [pdfminer metadata](https://pypi.org/pypi/pdfminer.six/20260107/json), [Pillow metadata](https://pypi.org/pypi/Pillow/13.0.0/json), [PDFium binding metadata](https://pypi.org/pypi/pypdfium2/5.15.2/json), [charset-normalizer](https://pypi.org/pypi/charset-normalizer/3.5.2/json), [cryptography](https://pypi.org/pypi/cryptography/50.0.2/json), [cffi](https://pypi.org/pypi/cffi/2.1.1/json), [pycparser](https://pypi.org/pypi/pycparser/3.12/json).

Nine proposed wheel sizes total 22,824,060 bytes (~21.8 MiB compressed). Installed distribution files total 45,965,332 bytes (~43.8 MiB, excluding untracked bytecode/cache). Environment/bootstrap/cache snapshot after installation: 258,602,159 bytes; this is disk usage, not RAM. Earlier baseline snapshot was 157,216,478 bytes, with different cache contents, so the difference is not a precise package-only footprint. Installed metadata/file paths confirmed project-local isolation and disabled user-site inheritance. Copies of all 47 packaged license/notice files are retained locally in `data/pdf-t05/license-notices.zip`; PDFium notices include build variants that are not all used by this wheel. Its version metadata reports PDFium 159.0.8149.0, flags []. No optional V8/XFA build was requested. Review complete notices again before redistribution/adoption.

PyMuPDF alternatives: [1.28.2](https://pypi.org/project/PyMuPDF/1.28.2/) has a ~19.8 MB Windows wheel and no mandatory Python dependencies; it remains an older, AGPL/commercial candidate only. [2.1 metadata](https://pypi.org/pypi/PyMuPDF/2.1/json) adds ONNX Runtime, NumPy and layout/LLM dependencies. Neither version was installed here. A smaller pypdf-only installation cannot provide this trial's table/region interface; pdfminer alone would avoid Pillow/PDFium but would omit pdfplumber's table algorithm.

Security source spot-checks: [pypdf 7.0.1 release](https://github.com/py-pdf/pypdf/releases/tag/7.0.1) contains security fixes; the [dictionary-loop advisory](https://github.com/py-pdf/pypdf/security/advisories/GHSA-mfr5-77xh-9j7h) lists versions below 6.21.4 as affected. The [pdfminer crafted-input advisory](https://github.com/pdfminer/pdfminer.six/security/advisories/GHSA-wf5f-4jwr-ppcp) lists versions below 20251230 as affected; the trial pin is later. [pdfplumber release notes](https://github.com/jsvine/pdfplumber/releases/tag/v0.11.10) explain its dependency updates. These checks are not a complete nine-package/native-code advisory audit or a vulnerability-free guarantee. Refresh advisory reachability and versions before T17 adoption. No upstream exploit payload was executed.

## Fixtures, boundaries and method

Three original PDFs retained their manifest hashes: FY20-21 (5,512,015 bytes, PDF 1.6), FY24-25 (28,339,007, PDF 1.6), FY25-26 (54,671,155, PDF 1.4). Both candidates reported 37, 52 and 31 physical PDF pages respectively. FY25-26 uses some two-page spreads: physical PDF page 3 includes printed pages 4/5. Citations must distinguish these numbers.

Only physical pages 1-3 of each real report were extracted. No suitable ruled table appeared there; real-report table coverage is a known gap. No unbounded search/full-report extraction was performed. Independent local PDFium renders were visually inspected for one native page per original and the controlled table page. Two factual strings per original were frozen in ignored `data/pdf-t05/gold.json` before scoring. These six spot checks establish limited exact-fact/page correctness, not a full transcription or semantic accuracy score.

The authored fixture is a separate five-page micro-PDF, not completion of T22: native budget text; ruled 3x2 table plus raster image; empty content; raster-only content; two text columns. Its uncompressed content streams, exact drawing coordinates and local render provide ground truth independent of either extraction result. The raster control is a simple image, not a realistic scanned invoice or OCR-quality test. AES-protected, malformed, truncated and wrong-extension controls were also generated locally. Original reports were never rewritten.

Windows Job Objects enforce a 2 GiB per-process and whole-job commit ceiling, kill-on-close, and at most two active processes (venv launcher plus actual interpreter). Workers block on stdin until assigned to the job; no parsing occurs before assignment. Each worker has a 60-second wall-clock timeout. A deliberate 3 GiB allocation is refused and a stalled child is terminated in tests. The batch has a 180-second candidate budget checked between runs, so it is not a separate preemptive 180-second job timer. Each worker returns at most 8 MiB JSON, with text limited to 256 KiB/page; batch result serialization is capped at 256 MiB before writing. The parser worker writes no extraction files; bytecode writes are disabled. The trial did not approach the proposed 1 GiB additional disk ceiling; ignored data occupied 2,162,694 bytes at measurement.

All document runs used the default restricted tool sandbox, never an escalated/network-enabled parsing command. An actual child socket to 1.1.1.1:443 fails with Windows error 10013; a test asserts that specific denial. Native PDFium render checks ran in the same restricted environment and job limits. This supports bounded local operation under this host's sandbox; it is not packet-capture proof of zero attempted native-library connections, an application firewall implementation, or the final disconnected-runtime gate. No document text was sent in web queries or provisioning requests.

Libraries' warning messages may contain source text: the worker counts warnings without logging their contents, and records only known exception class names. Unexpected errors fail the worker rather than being disguised as corrupt input. Generated documents, raw extraction, images, gold facts, license archives and failed/intermediate results remain under ignored `data/`; they must not be committed.

## Results

The final benchmark uses only the selected parser's imports per worker. Earlier runs importing both stacks inflated overhead; retained locally but excluded from this table. Four fresh-process runs per candidate/report (one initial plus three repeats), identical three-page sets: 24 successful runs. OS cache was not flushed; first run is not guaranteed cold. Host load was not controlled. Elapsed time includes interpreter/import/startup/IPC; open/page-enumeration and extraction are separately recorded locally. Memory values are per-worker peaks, not total system/application/Ollama memory.

| Candidate | Report | Median seconds (min-max) | Peak private MiB | Peak working set MiB |
|---|---|---:|---:|---:|
| pypdf | FY20-21 | 1.052 (0.961-1.283) | 31.4 | 41.7 |
| pypdf | FY24-25 | 1.200 (1.104-1.372) | 56.1 | 65.9 |
| pypdf | FY25-26 | 1.787 (1.461-2.067) | 84.0 | 93.9 |
| pdfplumber | FY20-21 | 1.356 (0.960-1.619) | 27.8 | 35.9 |
| pdfplumber | FY24-25 | 1.969 (1.587-2.196) | 30.6 | 38.3 |
| pdfplumber | FY25-26 | 2.972 (2.512-3.297) | 40.4 | 48.0 |

All six visually checked fact/page expectations passed in each candidate's four runs (48/48 individual string checks across both candidates). This is a tiny spot-check sample, not a benchmark of all report content. All controlled fixture assertions passed, including exact pdfplumber table values and region [50, 92, 250, 182] and image region [300, 92, 360, 152], using top-left PDF-point coordinates. pypdf recovered the same table text but this baseline exposes no cell associations/regions. Both rejected the four protected/invalid controls; pdfplumber wraps underlying errors, so password detection inspects the wrapped cause.

Observed limitations:

- pypdf uses content-stream order; pdfplumber's spatial order interleaves rows from two columns in the simple fixture. Neither default establishes robust reading order for complex layouts. Real decorative/rotated text also differs.
- pypdf's simple direct-image `Do` inspection misses a nested form image on FY24-25 page 3; pdfplumber reports its image region. Neither path proves all inline/form/vector cases are covered.
- FY20-21 page 1 has an image and no native text. FY25-26 page 1 has only a native page-number character plus an image. Therefore `has_text` is insufficient to decide OCR coverage. Blank/image controls are distinguished, but production scan/mixed detection remains T09/T36.
- pypdf emitted 3/0/1 library warnings per report run respectively; pdfplumber emitted zero. Source-bearing warning text was not retained in reports. Native extraction contains decoding artifacts; facts passing does not imply faithful punctuation/fonts or complete image text.
- No real ruled-table pages, realistic OCR, visual chart semantics, full-report resource behavior, malicious corpus, parser fallback policy or combined model/app memory were validated.

## Reproduction, review and recommendation

Evaluation aids: `tests/evals/spikes/pdf_trial.py`, `pdf_trial_fixtures.py`, `test_pdf_trial.py`. The main benchmark requires the ignored originals and locally established gold file; their absence fails instead of fabricating expectations. Gold SHA256: `3c433850d85d6819cde1ac172c89034371f8d6a1749daee3089905283c84aff3`. Final benchmark script SHA256: `60e359c693d6574bd24c42805645d95b54f798dcd5858f7e24eeed2d8c6d120f`.

Verified commands from the project root:

```powershell
.\.venv\Scripts\uv.exe sync --frozen --group pdf-eval --no-build --offline
.\.venv\Scripts\uv.exe lock --check --offline
.\.venv\Scripts\python.exe -m pytest -q --basetemp=data/pytest-pdf-t05-07 --tb=short
.\.venv\Scripts\ruff.exe check tests/evals/spikes
.\.venv\Scripts\ruff.exe format --check tests/evals/spikes
.\.venv\Scripts\python.exe tests/evals/spikes/pdf_trial.py --benchmark data/pdf-t05-final
```

Use a fresh, unused basetemp/output path for reruns: pytest can remove an existing basetemp; the benchmark deliberately refuses existing output directories. Socket-denial assertions require the documented sandbox; do not run parsing escalated to make that check pass. Offline sync depends on the already provisioned project cache. Final raw results: `data/pdf-t05-final/results.json` (80,851 bytes), with source/script/gold hashes and per-run values.

Test-first evidence: initial collection failed because trial helpers did not exist; later tests reproduced wrapped-error handling and raw-output boundary cases before correction. Final full available suite: **5 passed in 15.84 seconds**. Ruff lint/format and `git diff --check` passed. Early pytest attempts failed due to inaccessible system temp; later runs use workspace-owned data. Job active-process allowance was corrected for the Windows venv launcher; no limits were disabled. Five-axis review checked adapter/citation limitations, simple trial-only architecture, exception privacy, process boundaries and measured overhead. No blocking issue remains in the authorized subset; the explicitly listed coverage and PyMuPDF requirements remain open for review.

Recommendation: carry pdfplumber forward as the strongest tested permissive candidate for table/region provenance, with pypdf as a useful text/control baseline. A single pdfplumber path is simpler than shipping two parsers; whether a pypdf fallback earns its complexity is not demonstrated. Neither is adopted. Compare MarkItDown at T08 and OCR/rendering at T09, cover real table/layout gaps before T17, and explicitly decide whether to defer the PyMuPDF empirical comparison required by the current artifacts. No paid license is proposed.

Closeout: the user accepted the results, deferred the unrun PyMuPDF comparison and approved the T05 commit on 2026-11-13. The earlier references to open review describe the pre-closeout position. G1 later-trial provisioning and G2 architecture/runtime adoption at T17 remain gated. No app feature or model download was performed.
