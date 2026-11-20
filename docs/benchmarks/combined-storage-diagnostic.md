# Approved fake-worker storage diagnostic

**Date:** 2026-11-14 (Asia/Calcutta). **Authorization:** User approved at most24 starts/10active minutes, fake workers only, no OCR/model imports/inference, downloads or installation. This diagnostic does not authorize another native run, runtime storage-policy change or Git commit.

## Reproduction and evidence

Two deterministic threaded fake-worker transitions reproduced FileNotFoundError through the actual combined Supervisor.storage and unchanged bounded_tree_bytes implementation:

1. The scanner enumerates an authored `meter.json.tmp`; a coordinated fake writer atomically replaces it with `meter.json` before lstat.
2. The scanner enumerates an authored temporary file; a coordinated fake worker deletes it before lstat.

Both transitions use real local tiny temporary files and standard-library threads, with bounded event waits and joined threads. Neither launches a native OCR/model worker. These reproduce the failure class and identify a real live-scan hazard; they do not establish which path caused the historical combined-02 stop, because that report omitted it. Never convert this controlled result into a claim that the old filename is known.

The new diagnostic/privacy regressions first failed. After implementation, **21 stdlib/fake tests passed in1.511s**. Ruff initially flagged loop closures in the new test; explicit parameter binding corrected them, then lint passed. Existing accounting/deadline/residency/ownership tests remain passing. Negative storage controls still reject an over-limit synthetic stat, permission denial and a reparse-marked entry. No real large file, link, private document, executable fixture or inference engine was used.

## Reporting changes only

Storage inspection now tags OSError with the inspected area (`run`, `raw`, `answers`) and rethrows it unchanged. The strict counter/helper, caps, reparse checks and refusal behavior are unchanged. No disappearing entry is ignored and no guard has been relaxed.

Controller and observer failures now retain sanitized filesystem metadata: error class/codes, inspected area, approved filename category and the last project-owned source module/function/line. No arbitrary filename, path or exception message enters the sanitized record. Exact filename/filename2 are saved only in ignored `filesystem-error-local.json`; do not read that private receipt into tools or paste it into chat. A failure writing the receipt is reported without replacing the original exception. Observer stop messages no longer embed raw OSError filenames.

## Budget, preservation and recommendation

Evidence is under ignored `data/t11/storage-diagnostic-01/` (budget, red/green checks, Ruff output). Conservative reservations total20/24 including final review/documentation, leaving four cleanup slots. All work completed inside the10-minute boundary; no model/OCR roots, API requests, downloads or installation. The started combined-02 ledger remains51/160/fiveAPI calls with its original hash; prior native ledgers/seals are not reset or resealed. Existing source edits and these diagnostics remain uncommitted pending approval.

**Next recommendation, not adopted:** design a separate live-run storage counter that handles entries already removed after enumeration while keeping quota limits, required-directory checks, permission failures and reparse refusals. Keep the existing strict helper for static/isolation uses. Compare that with serializing app-owned writes/scans: locking alone cannot coordinate native temporary-file removal. A live counter observes storage at polling points and must not be described as a kernel disk quota. Prove both race cases and all negative controls with fake workers before preparing any new native package. This policy/implementation decision and the next native allocation remain unapproved; do not give an offline run command now.

**Subsequent decision:** The user approved the fake-only [live storage repair](combined-storage-repair.md) and committing the reviewed changes. Its positive/negative checks supersede the diagnostic-only policy recommendation; this does not authorize a new native run. Historical diagnostic observations above remain unchanged.
