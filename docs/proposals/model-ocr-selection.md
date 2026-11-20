# Model and OCR selection recommendation

**Status: shortlist approved; not G2 runtime adoption.** The user answered "yes commit" to the explicit shortlist/commit request, accepting Qwen2.5, Nomic and Tesserocr as preferred candidates for subsequent design/evaluation and approving these five documents' commit. Prepared from saved project evidence after combined-07 user acceptance, committed in `69a01b4`. No new installation, download, execution, application default or dependency change is authorized. Final adoption remains T17/G2 after the existing prerequisites; shortlist approval does not waive them. The requested-decision paragraph below is historical.

## Recommended candidates

| Role | Recommended candidate | Evaluated alternative | Reason from saved evidence |
|---|---|---|---|
| Local chat | `qwen2.5:1.5b-instruct-q4_K_M` | `qwen3:1.7b-q4_K_M` | Both completed combined-07 and user review accepted the answers/citations; Qwen2.5 had lower recorded mean chat elapsed time in each condition |
| Embeddings | `nomic-embed-text:v1.5` | EmbeddingGemma 300m BF16 | T10 showed equal retrieval coverage on its small set, a smaller weight layer and lower observed native-job peak; Nomic also completed the combined trial |
| English OCR | Tesserocr 2.13.0, evaluated Tesseract5.5.4/Leptonica1.87.0 and pinned English asset | RapidOCR3.10.0 with the evaluated local ONNX assets | Both passed readable synthetic cases; Tesserocr had lower standalone worker time and sampled worker memory, and completed combined overlap checks |

These are candidate preferences for the remaining design work. Keep alternatives' historical evidence and installed evaluation assets; no uninstallations or automatic runtime fallback are proposed. Do not treat the two chat models as interchangeable defaults or load both at once.

## Evidence and precise identities

- [Combined-07](../benchmarks/combined-ocr-model-seventh-results.md):36completed answers, four controls and24positive OCR/chat overlaps; qualitative user acceptance, no independently graded numerical accuracy score. Qwen2.5 means baseline/Tesserocr/RapidOCR:8.757/7.907/8.535s; Qwen3:12.841/11.827/12.718s. Fixed order/cache/background conditions limit causal comparison. No measured quality advantage for Qwen2.5 is claimed.
- [Embedding comparison](../benchmarks/embeddings.md): both candidates mean recall@5=1.00 on32passages/12closely related query variants. Nomic's weight layer274,290,656bytes versus621,867,104bytes; run-wide native-job peak462.83MiB versus815.62MiB, with separate-session/workload caveats. These are not general document retrieval scores or isolated per-model memory measurements.
- [Standalone OCR](../benchmarks/manual-ocr-results.md): both engines24/24readable-case repetitions passed. Mean worker time1.02s/5.21s and maximum sampled worker private memory193.82/543.92MiB for Tesserocr/RapidOCR. Repeated synthetic text is narrow coverage, not24independent real documents. Both failed the90-degree rotation comparison; preserve that finding separately from the user's earlier visual impression.
- Use the exact three model manifest hashes in the [combined-07 proposal](combined-ocr-model-seventh-run.md), cached weights/sealed runtime, and the [authored OCR artifact inventory](ocr-trial-artifacts.json). The evaluated English `tessdata_fast` asset is at commit `65727574dfcd264acbb0c3e07860e4e9e9b22185`, SHA-256 `7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2`. No replacement tag/assets or startup download is approved.

Continue with the evaluated CPU-only/context2048/four-thread settings and exact prompts/prefixes as the baseline for future approved tests. Nomic remains768dimensions/truncate=false; use the documented query/document prefix contract. Future tuning or different artifacts requires its own review. These trial settings do not establish the final application's context/chunking/latency budgets.

## What this recommendation does not resolve

1. **Target memory:** combined-07 ran on19.911GiB physical RAM, with2.609GiB job peak and at least9.389GiB available. It did not include a complete app or maximum-size documents. The Windows11/16-GB/no-dedicated-GPU target remains binding; validation method and final resource/latency budgets need review before corresponding acceptance claims.
2. **OCR and visual coverage:** representative scanned/mixed PDFs, varied layouts, table/image provenance, confidence/regions, rotation handling and chart/diagram feasibility remain open. Do not label OCR text extraction as chart understanding or drop mandatory scanned-PDF support.
3. **Storage and lifecycle:** T12 must evaluate local vector storage, persistence/recovery, ranking, versioning, deduplication and deletion/reference consistency. Keep embedding identity/dimension/prefix/extraction versions associated with indexes; model-change rebuild semantics must be designed and approved.
4. **Grounding and product limits:** T16 must settle citations/quotes/abstention/support indicators and wider quality thresholds. Existing size/count limits, retention decisions and source ownership remain governed by SPEC; small benchmark success does not waive them.
5. **Runtime/privacy/dependency review:** the disconnected synthetic trial accepted no filesystem confinement. It does not establish the application's upload/parser isolation, offline/no-download behaviour, startup handling, or complete dependency/license/maintenance acceptance. Reconcile exact selected artifacts and native/model notices in the T17 component inventory; do not infer blanket license/security clearance from this shortlist.

## Next ordered design work

The next core task is **T12 storage/index evaluation**, followed by T16 grounding contracts and T17/G2 architecture/adoption review; chart feasibility/deferral and outstanding OCR/parser acceptance prerequisites retain their existing gates. Optional developer tools do not block this sequence; UI UX Pro Max still precedes frontend implementation.

After shortlist review, prepare T12's concrete alternatives and bounded trial proposal using the approved formats and cached Nomic candidate. A simple representation should be compared with a justified index alternative, not silently adopted. Agree representative scale, resource/quality budgets and unresolved retention inputs before any storage trial/code/dependency work. This document authorizes no native run or product implementation.

**Decision requested:** accept or amend these three preferred candidates for subsequent design/evaluation, while retaining T17/G2 final adoption and all listed acceptance gates. Separately approve committing this proposal and its PLAN/TODO/README/checkpoint updates. Approval is not permission to skip storage/grounding review or begin the CSV application slice.
