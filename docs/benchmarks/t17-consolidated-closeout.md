# T17 consolidated closeout — 2026-11-19

## Outcome

The user authorized the remaining T17 work and scoped commits in one package without intermediate project approvals. The earlier six RPT results were committed as **34ca104**. [This package](../proposals/t17-consolidated-closeout.md) completed the independent safe evaluation work and presents an updated architecture decision pack.

**T17 remains open; unconditional G2 approval is not supported yet.** No requirement, hardware target, risk exception or architecture approval was silently substituted. This report distinguishes completed work from the three remaining blockers.

| Requested block | Completed now | Still outstanding |
| --- | --- | --- |
| Component decisions | Exact existing candidates retained; 52 installed distributions match all 52 locked dependency versions; all 75 cached Ollama files rehashed; both full model hashes verified; actual loopback/key and CPU-requested reference operation tested | Complete selected native/vendor notices, applicable advisory coverage and standalone dependency/provisioning closure |
| Model-input handling | Twenty-one fake/data tests; FP01–FP08 contract coverage; exact model/vocabulary inspection; eight chat and three embedding reference count comparisons passed | Full standalone Tokenizers versus selected Ollama parity, special-marker safety, context/equality/EOS reservation and lifetime/publication controls |
| Component/target evidence | Fresh CSV/XLSX/native-and-scanned PDF/OCR checks passed; prior model/OCR evidence reconciled; new jobs remained bounded and were closed | Physical 16 GB acceptance or an explicitly approved proxy; wider representative/scale and rotation checks before relevant acceptance |
| Final architecture | ADR/readiness, dependency inventory, resource/input contracts and implementation handoff updated | Final user G2 decision after applicable blockers are resolved or explicitly decided; T18 was not started |

## New evidence

### Model files and tokenizer metadata

The complete 986,048,512-byte chat weight and 274,290,656-byte embedding weight matched their recorded SHA-256 values. The bounded decoder reads GGUF metadata without executing native/model code; hashing streams tensor bytes as opaque chunks. The input reader rejects malformed headers, duplicate keys, excessive strings/arrays, truncation, byte-budget exhaustion and hash drift.

- **Qwen:** all 151,665 known publisher vocabulary/added-token IDs match the GGUF representation; merge rules match exactly. The GGUF contains 271 additional entries tagged type 5. This does not prove their runtime reachability or full algorithm parity.
- **Nomic:** literal vocabulary comparison initially differed for 29,523 entries. Keeping bracketed special tokens, removing the continuation prefix from continuation pieces, and adding a word-boundary marker to other pieces yields **zero mismatches across all 30,522 IDs**. This is an observed representation mapping, not proof of normalization/segmentation parity.
- **Context:** both running reference properties report one 2,048-token slot. Nomic's GGUF also declares 2,048, whereas earlier auxiliary settings declared 8,192. The latter must not be treated as verified effective capacity. No product limit was changed.
- The runner's default n_predict is -1. All new chat requests explicitly set max_tokens=1. These trials do not validate the provisional 192-token production reservation or justify an unlimited default.

### Actual packaged-reference checks

The verified packaged llama-server was directly owned, using explicit local model paths, --device none, --n-gpu-layers 0, a 2,048 context, one slot, no context shift and no web UI. Kernel listener ownership was checked before requests; wrong API keys were rejected with HTTP 401 for both model phases. Requests used loopback, no proxy/redirect and cached assets only.

| Check | Observed result |
| --- | --- |
| Eight chat render → tokenize → one-token completion cases | All eight reference counts equal runtime prompt-token usage |
| Three Nomic query/document/Unicode cases | All three counts match runtime embedding usage; each vector has 768 finite values |
| Overlong input inspection | 4,096 chat tokens / 4,098 embedding tokens; local budget calculation rejects them; no oversized inference was submitted |
| Shared native fit API attempts | 42, including health and negative-key requests |
| Native fit jobs | Four cumulative native processes observed; both owned roots reaped and jobs closed; no monitor errors |

This is **direct packaged-reference** evidence. It is not a completed standalone Tokenizers comparison, selected Ollama preprocessing test, full-answer benchmark or physical-disconnection test. Marker-string count agreement does not prove protection against marker injection. Native equality/overflow/truncation boundary behaviour was not fully exercised. All NP01–NP08 groups therefore remain not fully passed; none was silently removed.

### Parser/OCR and resources

Three fresh authored fixture files verified quoted multiline CSV records and a sum, XLSX sheet values and an unavailable formula cache without execution, native PDF text, an image-only page in a mixed PDF, PDFium rendering and local English OCR against the known numeric/text gold. Observed OCR confidence was 95. No user sample documents, macros, external links or cloud evaluators were used.

These are small component checks, not 100 MB/ten-file or full application acceptance. Existing [manual OCR](manual-ocr-results.md) rotation/layout limitations and [36-answer combined evaluation](combined-ocr-model-seventh-results.md) remain visible. Their old ledgers were not reused or reset.

The machine reports **21,379,649,536 physical bytes (about 19.91 GiB)**. New sampled native-job peaks were approximately 832.4 MiB for chat, 58.7 MiB for embeddings and 301.0 MiB for representative parsing/OCR. These are job commit observations, not total RAM/RSS or full upload-to-answer latency. Native jobs used the existing 6 GiB kernel job limit and available-memory checks; no physical-16-GB equivalence or whole-application memory guarantee follows.

New jobs were closed and their roots reaped. Native activity observed only loopback peers; this is not independently enforced egress prevention, physical disconnection, filesystem confinement or private-document application acceptance.

## Component and security decision

Retain the existing proposed stack: FastAPI/Uvicorn/HTTPX, minimal local HTML/CSS/JavaScript, SQLite/sqlite-vec, standard-library CSV, openpyxl/defusedxml, pdfplumber/pdfminer with PDFium, Tesserocr English OCR, Qwen2.5 1.5B and Nomic v1.5. Exact versions/artifact authorities remain in the [inventory](../dependencies.md). No dependency/environment/lock change or installation occurred. Evaluation alternatives do not become automatic runtime fallbacks.

Keep standalone Tokenizers 0.23.3 and its complete seventeen-distribution candidate graph **on hold for adoption/provisioning** until its outstanding notice/ABI/artifact and end-to-end parity checks close. No --no-deps, metadata editing, stub imports or silent graph reduction was used. The reference executable was an evaluation tool, not an adopted additional application service.

Current primary-source checks confirmed that the two reviewed pdfminer advisories list versions before 20251230 as affected; the selected 20260107 pin is outside those stated ranges. [Crafted-PDF advisory](https://github.com/pdfminer/pdfminer.six/security/advisories/GHSA-wf5f-4jwr-ppcp), [CMap advisory](https://github.com/pdfminer/pdfminer.six/security/advisories/GHSA-f83h-ghpp-7wcc).

Two reachable Starlette advisories list fixes at 1.3.0 and 1.1.0; the installed/locked 1.10.0 is outside those stated affected ranges. [First advisory](https://github.com/encode/starlette/security/advisories/GHSA-jp82-jpqv-5vv3), [second advisory](https://github.com/encode/starlette/security/advisories/GHSA-x746-7m8f-x49c).

Searches/unavailable pages do not establish complete freshness or absence of vulnerabilities. Four other requested Starlette pages did not yield affected-version ranges in the retained response. Native/vendor build/notice and full selected-runtime advisory coverage remain open; local file agreement is not independent publisher attestation.

## Remaining G2 blockers and disposition

| ID | Exact remaining requirement | Disposition |
| --- | --- | --- |
| B01 | Full selected-Ollama/standalone exact IDs, rendering, special-token interpretation, embedding policy, verified 192-output/termination/equality handling and drift/cancellation/publication matrix | Not fully validated. Native-reference successes and fake contract passes are supporting evidence only; no unconditional counter adoption. |
| B02 | Unchanged Windows 11/16 GB CPU-only acceptance | This computer has more RAM. A physical target or explicitly approved bounded proxy is needed; no proxy/hardware waiver was inferred. Full application checks correctly follow G2. |
| B03 | Exact standalone provisioning and selected native/vendor/advisory trust closure | Complete seventeen-node and selected-runtime evidence or explicit narrow decisions are still required. No blanket licence/security exception was inferred. |

The final architecture is **Proposed, with these named blockers**, not approved. This is the requested G2 presentation; no intermediate project approval was requested. The report does not claim all four technical blocks or T17 are fully finished. No finite static review or larger-host trial can supply the unavailable physical target or the unexecuted standalone/Ollama matrix.

## Verification and delivery

New tests: ten bounded-metadata/hash tests and eleven FP contract tests passed after expected REDs. An identity-guard mutation was caught without modifying the real source. A final during-count drift regression also failed first; the evaluator now pins identity across the oracle call, and all 21 final tests passed. Ruff formatting passed; three import-order findings were corrected and lint passed. Tests remain evaluation-only, with no application endpoint or startup command.

Detailed observations, raw synthetic outputs, receipts, public responses and the shared ledger stay ignored under data/t17/consolidated-closeout-01/. Historical inputs, AGENTS, SPEC, pyproject/lock, user files and old checkpoints remain unchanged. The final summary records actual closeout checks, conservatively charged starts, research targets and resource limitations. The reviewed scoped commit includes authored reports/evaluation source only, never models, fixtures, environments or databases.
