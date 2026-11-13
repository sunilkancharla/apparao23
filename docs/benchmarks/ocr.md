# T09 - Local English OCR source review

**Date:** 2026-11-13. **Status:** Read-only shortlist review complete; artifact selection, bounded trial and runtime adoption pending. The user authorized this review after accepting T08 non-adoption/empirical deferral. No OCR package/binary/model download, installation, import, execution, PDF rendering or fixture generation occurred.

**Follow-up:** This shortlist is committed in `1337560`. The user authorized preparing the [bounded proposal](../proposals/ocr-trial.md) and [exact artifact inventory](../proposals/ocr-trial-artifacts.json). Further public metadata review identified tesserocr 2.13.0's Python 3.14 Windows wheel, whose upstream release reports bundled Tesseract 5.5.4/Leptonica 1.87.0; this offers a project-local alternative to the standalone installer gap below. Sixteen proposed new wheels and three English assets total 140,501,680 declared bytes. No binaries/models were fetched or installed. The proposal requests artifact inspection only first; native OCR execution remains separately gated on inspection findings and an agreed boundary. Earlier recommendations below describe the initial shortlist, not an adopted engine.

## Recommendation

Keep **Tesseract and RapidOCR with ONNX Runtime CPU** as the comparison shortlist. Prefer a narrowly configured Tesseract subprocess as the initial engineering baseline if a reviewed, patched Windows binary can be provisioned entirely inside `.venv`. Its TSV output suits word/region provenance and the subprocess interface avoids a Python extension ABI dependency. This is an architectural proposal, not a measured performance preference or engine adoption.

Resolve Tesseract's Windows artifact gap before proposing installation. If no suitable prebuilt artifact is available, report that limitation and propose RapidOCR first; do not substitute an older binary, compile a toolchain, change Python or use a global installation implicitly. T09 still requires empirical OCR evidence; the optional-tool exception at T08 does not waive scanned/mixed-PDF support.

## Candidate review

| Candidate | Public evidence | Fit and unresolved work |
|---|---|---|
| Tesseract **5.5.4** | Upstream release published 2026-10-28; release API lists no attached binary assets and reports fixes for 17 security advisories. | Source version is identified, but an acceptable project-local Windows binary, its hashes, native DLLs and notices are not selected. |
| UB Mannheim Windows distribution | Official Tesseract documentation links this third-party distributor; its wiki currently lists **5.5.3.20260724**. | Earlier than 5.5.4. Do not assume security-fix equivalence or silently install it. Installer behavior and dependencies need review; no installer was run. |
| RapidOCR **3.10.0** | Python wrapper and tagged source available, with ONNX Runtime backend and output boxes/text/scores. | Viable second candidate for investigation; exact English model tuple, native/transitive graph and local compatibility remain unverified. |

Sources: [Tesseract release metadata](https://api.github.com/repos/tesseract-ocr/tesseract/releases/latest), [Tesseract installation guidance](https://tesseract-ocr.github.io/tessdoc/Installation.html), [UB Mannheim distributor](https://github.com/UB-Mannheim/tesseract/wiki), [RapidOCR output contract](https://raw.githubusercontent.com/RapidAI/RapidOCR/v3.10.0/python/rapidocr/utils/output.py). Release/distributor pages are mutable observations as of this review; freeze exact artifacts before approval.

### Tesseract assets and provenance

The engine is Apache-2.0; bundled Leptonica/image libraries and runtime DLLs need separate notices/security review. Engine and language data are separate installations. Use explicit executable and tessdata paths, never a PATH-discovered global engine. [Installation documentation](https://tesseract-ocr.github.io/tessdoc/Installation.html)

Propose **English `eng.traineddata` from tessdata_fast**, LSTM mode, as the first candidate. Fast integer models support Tesseract 4/5 LSTM. Freeze a repository commit, asset hash, exact size and license before download; none is pinned here. `tessdata_best` English is an alternative if the trial demonstrates a quality need. Orientation data is a separate optional asset, not an automatic language-pack download. [Fast-model repository](https://github.com/tesseract-ocr/tessdata_fast), [data variants](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html)

TSV includes text, hierarchy, bounding boxes and confidence. Preserve raw confidence, distinguish non-word sentinel values and map rendered-image coordinates back to the original PDF page. Per-image OCR page numbering cannot substitute for original PDF page identity. Confidence is not answer correctness or calibrated support. Proposed LSTM/English/page-segmentation/thread settings need trial approval and measurements before adoption. [Command-line/TSV documentation](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html)

A standard-library subprocess adapter could avoid adding pytesseract/tesserocr. No wrapper is selected: pytesseract does not itself supply the engine, and an in-process binding would add ABI/native-library review. Invoke an exact argument list with shell disabled, an owned working directory, validated local paths and bounded outputs/time/descendants. Some distributor builds support URL input; a subprocess alone is not a network boundary.

### RapidOCR assets, dependencies and CPU behavior

Registry candidate: `rapidocr-3.10.0-py3-none-any.whl`, approximately **27.3 MB**, SHA-256 `2fc34e26cd0f48514804a94f8832283039c7334076bff60768b1fed9ad068050`, released 2026-10-08. Requires Python `>=3.8,<4`, but classifiers stop at 3.13; the version range alone does not validate this project's Python 3.14.6. The wheel was not downloaded or inspected. [Registry release](https://pypi.org/project/rapidocr/3.10.0/)

The wrapper declares OpenCV-headless, NumPy, pyclipper, Shapely, PyYAML, Pillow, six, tqdm, OmegaConf, requests and colorlog. ONNX Runtime needs an explicit backend selection in the trial graph; GPU, Paddle/PyTorch and other backend packages are unnecessary for the proposed comparison. Native libraries and all transitive versions/licenses must be inventoried before provisioning. [Pinned requirements](https://raw.githubusercontent.com/RapidAI/RapidOCR/v3.10.0/python/requirements.txt)

A standard CPython 3.14 Windows x64 CPU-runtime wheel exists: `onnxruntime-1.31.1-cp314-cp314-win_amd64.whl`, approximately **15.3 MB**, SHA-256 `0a3998e18cb667ef54287556bd62291a788ed235723dd90c83b2294b24e71d81`. This is compatibility evidence for one artifact, not a resolved or approved graph. Other native wheels and required Windows runtime DLLs remain unchecked. Total footprint/RAM is unmeasured; do not add the displayed rounded sizes and treat the sum as a download budget. [ONNX Runtime registry](https://pypi.org/project/onnxruntime/1.31.1/)

RapidOCR code is Apache-2.0. Its model notice distinguishes upstream PaddleOCR weights from wrapper ownership and limits coverage to specified artifacts; inspect each selected model/dictionary and bundled font separately. [Pinned package metadata](https://raw.githubusercontent.com/RapidAI/RapidOCR/v3.10.0/python/pyproject.toml), [model notices](https://raw.githubusercontent.com/RapidAI/RapidOCR/v3.10.0/python/MODEL_LICENSES.md)

Default configuration selects Chinese model families and leaves paths unset. Do not initialize defaults for the English-only trial. Select/review English recognition and compatible detection/orientation assets, explicitly set local model/dictionary paths, cap threads and use CPU-only providers. The source exposes GPU controls, but actual providers must be observed during a run. [Pinned configuration](https://raw.githubusercontent.com/RapidAI/RapidOCR/v3.10.0/python/rapidocr/config.yaml)

The ONNX session source invokes model download logic when explicit model paths are absent. Preprovision approved assets and fail on missing/hash-mismatched files before initialization; verify no fallback download. Explicit local paths reduce this path's download behavior but do not prove all dependency traffic is absent. [ONNX initialization](https://raw.githubusercontent.com/RapidAI/RapidOCR/v3.10.0/python/rapidocr/inference_engine/onnxruntime/main.py)

## Proposed PDF/OCR comparison contract

This is a review proposal, not implemented behavior or an approved benchmark configuration:

1. Reuse the evaluated pypdfium2 **5.15.2** renderer candidate and existing PDF parsers; no new renderer by default. Render one page at a time. Freeze DPI, rotation/crop transforms, pixel limit and time/memory limits before the trial. Rendering a 100-MB PDF can expand far beyond 100 MB.
2. Preserve native text and original page/region/image anchors. Determine OCR need per page/region using checked text/image evidence; test native-only, image-only and mixed pages. Do not silently duplicate native text with an OCR copy or classify unreadable gibberish as good text based only on character count.
3. Store engine/version, asset digest, extraction method, original page ID, pixel-to-PDF transform, region boxes, warnings and available raw confidence. Keep originals separate. OCR words alone do not establish table cell relationships; preserve a page/region preview and qualify ambiguous table readings.
4. Use S-PDF-SCAN and S-PDF-MIXED definitions plus safe authored native/table/low-quality controls. Verify serialized scans and manual answers/locations locally before scoring; their definitions are not ready-to-run artifacts. No need to expose user PDF text in reports. English only; standalone image uploads are not added to Stage 1.
5. Compare character/word errors with declared normalization, exact invoice/table numbers, location correctness, native/OCR distinction, unreadable-page warnings, duplicate text and unsupported-answer behavior. OCR scores and later answer-grounding scores remain separate. Agree numerical quality/latency/memory thresholds before an acceptance run.
6. Exercise missing/wrong language/model assets, empty/rotated/unreadable pages, corrupt/protected inputs, timeouts and oversized renders. Keep all controls inside a fresh shared budget. No embedded code, external links or document instructions execute.
7. Measure renderer plus OCR cold/warm time and peak private memory/working set, system available RAM and disk footprint. T09 explores OCR alone; T11 must still measure combined Ollama/OCR/application pressure against the 16-GB CPU-only target. Actual machine capacity does not revise that target.

## Provisioning and security gates

No exact execution package is ready. Before installation/trial approval, publish exact artifact URLs/hashes/bytes, full dependency/native notices, English asset identities, permitted local fixture generation, shared process/download/time/storage/output/memory budgets, subprocess/descendant accounting and stop conditions. Tools and caches belong in `.venv`; ignored fixtures/results belong under `data/`. No global/PATH/service/Windows-feature changes or source builds are implied.

The earlier T07A native-network readiness failure is retained. Removing XLS or rejecting MarkItDown did not establish native denial for renderers/OCR. Define and obtain approval of a suitable execution boundary before document trials; no automatic retry, firewall modification or Python-only socket patch can substitute for that evidence. Do not reset old meters. Public documentation research used no document content.

## Current evidence and open decisions

- Source/metadata comparison completed; no OCR or rendering measurements, downloads, imports or smoke tests. No offline-runtime guarantee, quality score, engine adoption or Stage 1 OCR capability is claimed.
- Unresolved: patched project-local Tesseract Windows artifact; exact RapidOCR English models/backend graph; trial isolation; representative verified scan controls; bounded settings/budgets and quality thresholds. None is silently decided here.
- Recommendation: review exact artifacts next, then present one executable bounded trial package. T09 remains in progress; T11 combined-pressure checks and G2 runtime adoption remain blocked on actual required OCR evidence.
- Documentation/local-link/whitespace checks apply to this report. Python dependency files and existing sample/evaluation definitions remain unchanged.
