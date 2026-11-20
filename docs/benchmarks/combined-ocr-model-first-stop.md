# Combined-01 stop: reused OCR deadline field mismatch

Recorded 2026-11-14 (Asia/Calcutta), from sanitized local summary/meter and source review. No raw OCR, prompts, evidence or model answers were inspected.

The owned runtime started and five metadata API attempts completed before the first Tesserocr deadline sentinel stopped with KeyError. Summary phase: `sentinel-tesserocr-deadline`. No control completed and no scored chat response was recorded. Owned server/processes were reaped, port released, active owned children zero and teardown verified.

Source/meter review identifies the integration mismatch: combined Ledger.start writes numeric `execution_deadline`, but the reused OCR OwnedRunner.run polling loop directly reads ISO-format `execution_deadline_utc`. The combined adapter rebound process accounting without supplying that deadline representation. This guard fails before the sentinel can finish. This is a runner integration defect, not an established model/OCR engine or Windows failure; the fake contracts missed the reused runner's complete meter schema.

Preserve combined-01 at 75/160 process reservations, five API attempts, two explicit native roots, seven additional observed descendants, nine observed native starts. Do not reset its ledger, rerun its command or reseal its started epoch. Existing prior ledgers remain historical. No completed combined resource or quality evidence is established.

Required repair: expose both deadline representations from the same single 75-minute instant, and add a regression that exercises the reused OCR deadline reader against a started combined ledger, including expiry agreement. Improve sanitized diagnostics to retain a missing-key identifier without printing raw content. No deadline extension, guard bypass, new dependency, engine change or automatic native retry.

A fresh bounded continuation must explicitly cover repair verification and offline execution, with linked prior counters and a fresh handoff. No new allocation, source/results commit or runtime adoption is inferred from this stop report.

**Subsequent approval:** The user explicitly approved the documented repair/regression and a fresh same-limit160-start continuation. [Combined-02](../proposals/combined-ocr-model-continuation.md) preserves this stopped ledger and does not merge its partial startup into a completed comparison. New source/results commit remains gated.
