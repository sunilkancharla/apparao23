# Manual-03 stop: RapidOCR enum configuration

Recorded 2026-11-14 (Asia/Calcutta) from the user's traceback, sanitized summary and installed source. No raw OCR text/images were inspected.

Offline resolution checked the existing 52 installed packages. Fixture generation/review succeeded. All 30 Tesserocr comparison workers completed; the first RapidOCR worker (`rapidocr-M01-0`) exited 1 during configuration, before inference. No negative controls ran. The controller stopped with verified teardown and no active owned children; preserve its 79/160 ledger and original seal. No full quality result or runtime adoption follows.

The traceback identifies `TypeError: The value of Det.ocr_version must be Enum Type.` Static inspection of RapidOCR 3.10.0's installed `utils/parse_parameters.py`, `utils/typings.py`, package exports and configuration confirms that OCR version/model/engine overrides require Enum instances. Our adapter incorrectly passed strings for OCR version/model and language. Language values also need their respective enum classes for downstream consumers.

Repair: inject the enum namespace into the configuration builder. The offline adapter supplies RapidOCR's actual types; routine tests supply standard-library fake enum classes. Det/Rec now use OCRVersion.PPOCRV4, ModelType.MOBILE, English language enums and explicit EngineType.ONNXRUNTIME. CPU/thread restrictions, exact cached paths, classifier/download refusals, fixture schedule and resource guards remain unchanged. No dependency/settings-value/model change or native rerun.

The strengthened contract first failed, then all 15 tests passed in 0.118 s using the stdlib-only Job-bounded bootstrap. Ruff initially flagged import ordering; corrected, then passed. These are fake configuration checks, not validation of RapidOCR initialization, model compatibility or inference. Separate local repair evidence is in `data/t09-manual-ocr/enum-repair-01/`; it is not merged into or charged as a restarted stopped native trial. Conservative 16 shell/test/lint/closeout starts are recorded separately, with zero native OCR roots/downloads. No new combined trial allocation is implied.

Do not rerun manual-03 or change its ledger/seal. A fresh bounded continuation and seal require explicit user approval; source changes invalidate previous handoffs. The partial Tesserocr quality results remain unreviewed. Further backend compatibility failures remain possible until an approved offline run actually validates them.
