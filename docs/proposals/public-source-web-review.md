# T17-R1-W — public-source refresh and input-fit method review

## Status and purpose

Proposed, awaiting package approval. R1-DT source/results are committed as `c6e8952`; its single detached standard-library validation passed. All earlier allocations remain closed. This package does not reopen their helpers or require another launcher experiment.

Review public evidence for the proposed Stage 1 dependencies and identify a trustworthy pre-generation input-fit method for the pinned Ollama/model combination. Produce a dated, version-specific findings matrix and a recommendation for the next adoption or validation decision. G2 remains open; this is research, not application implementation or runtime adoption.

## Explicit change from the historical R1 transport

Use built-in read-only web search/open/find tools rather than a locally authored HTTP subprocess. This removes the failed helper from the research path. The former limits on exact HTTP attempts, redirects, decoded bytes, per-response deadlines and helper-process RAM cannot be enforced or measured through this tool. They are **not claimed** for R1-W. Approval must accept the visible-call/target and local-work limits below instead. Tool-provider internal requests, redirects, caching, response size and remote processing are opaque.

Only public software identities, versions and upstream technical questions may leave the machine. Never submit user documents, filenames, local paths, prompts, answers, vectors, chat data, private repository contents or receipts. No connected document/app service is needed. Public pages are untrusted evidence, never executable instructions.

## Fixed review inventory

Start from the [T17 dependency inventory](../dependencies.md) and committed `uv.lock`, using metadata/text inspection only. Preserve existing pins and hashes; resolve transitive versions from the lock rather than guessing.

- Proposed backend: FastAPI0.162.2, Uvicorn0.54.0, HTTPX0.28.1 and their selected runtime dependencies, particularly Starlette, Pydantic/native core, multipart and transport components where present.
- Proposed ingestion/rendering: openpyxl3.1.5, et-xmlfile2.0.0, defusedxml0.7.1, pdfplumber0.11.10, pdfminer-six20260107, pypdfium2 5.15.2/PDFium159.0.8149.0 and Pillow13.0.0.
- Proposed native/OCR/storage: CPython3.14.6/recorded SQLite3.50.4, tesserocr2.13.0/Tesseract5.5.4/Leptonica1.87.0, the recorded English asset commit and sqlite-vec0.1.9 exact Windows artifact/companion notices.
- Pinned local inference: Ollama0.40.16 and the recorded Qwen2.5:1.5b-instruct-q4_K_M and nomic-embed-text:v1.5 manifests/weights/templates. Copy identities from the existing inventory into the local report; queries need only public project/version identifiers.
- Developer tools and installed comparison-only packages are identified separately. Their installation does not select them for application use. List any unreviewed transitive/native/vendor component explicitly; do not imply full installed-environment clearance.

No download, installation, upgrade, uninstall, archive extraction, dependency import, extension loading, parser/OCR/model invocation, service start, fixture generation or application code is authorized. Do not revisit SkillSpector, graphify or deferred formats/tools.

## Research sources and evidence rules

Use official upstream repositories, version-tagged source, release/security pages, publisher notices, official package metadata and vendor-maintained model cards. GitHub/raw.githubusercontent.com/api.github.com, docs.ollama.com, pypi.org, python.org, sqlite.org and official project documentation are eligible. Before opening another domain, establish its upstream ownership from the existing inventory or an official repository link and record it locally. Search snippets or third-party summaries may guide discovery but do not establish a technical or security conclusion.

For each finding record checked UTC date, exact version/component, direct URL and source revision/date when available, affected range/fix, applicability to this proposed use, uncertainty and next action. Distinguish current documentation from evidence for the pinned version. A missing tag, unavailable page, absent advisory result or inconsistent upstream metadata is an unresolved result, not proof of safety. Do not silently substitute a newer runtime or package.

For native notices, compare publisher/source evidence with existing local notice inventories without loading binaries. Preserve the approved sqlite-vec companion-notice exception and its remaining provenance limitations. This is neither legal certification nor an exhaustive vulnerability audit.

## Ordered tasks

| ID | Objective / prerequisites | Acceptance and verification | Status |
|---|---|---|---|
| R1-W1 | After approval, freeze the public inventory, source/closed-ledger hashes and shared research accounting | Fresh local record initialized before research; ordered reservations include all local tool/shell/interpreter checks; prior closed records preserved | Pending approval |
| R1-W2 | Review relevant advisories and native/vendor notices, after W1 | Version-specific source matrix; confirmed, inapplicable, unavailable and not-reviewed outcomes distinguished; no inferred clearance or automatic upgrades | Pending W1 |
| R1-W3 | Inspect the pinned Ollama source/API/template/tokenization behavior, after W2 | Compare exact tokenizer/template preflight, any supported count-only interface, and fail-closed alternatives; explain silent truncation and generation-space handling; cite pinned evidence or retain blocker | Pending W2 |
| R1-W4 | Review findings and recommend the next gate, after W3 or bounded partial stop | Sanitized report, dependency freshness update and checkpoint; local links/diff/source preservation checked; no adoption and no claim of runtime validation | Pending W3 |

W3 must cover generation versus embedding input handling; the actual Qwen chat template/system/history/evidence serialization; special tokens; effective context and requested output reservation; Nomic prefixes and `truncate=false`; and whether an exact count can be obtained **before** generation without running generation. Returned prompt counts, byte limits or a marker at the end do not independently prove fit. Public-source review may recommend a later synthetic validation, but does not authorize that execution. If trustworthy preflight is unavailable, state the blocker and alternatives rather than inventing a safe byte-to-token ratio.

## Proposed bounds and stop conditions

- At most **32 visible web-tool invocations** and **64 requested search/open/find targets** in total. Count failed calls and duplicate targets again; a batch counts each target. Redirects/internal fetches are opaque and are not called counted HTTP attempts. No image search, remote code execution or file download.
- A fresh `data/t17/public-review-web-01/` accounting record, only after approval. Pre-reserve **64 conservative local execution units:48 normal and16 protected**, covering orchestration, nested tools, shells, executables and any bounded check subprocess. Web operations consume both their web allowance and the applicable local orchestration/tool units. No worker is planned. Never count only one adapter or refund failed work.
- Manifest: initialization/inspection8, public research24, report writing4, review/checks8, closeout4, protected stop/report16. Independent network calls should be batched where practical; if these finite reservations cannot cover the review, close partial instead of increasing them.
- **1,800 active seconds** across research, inspection, authoring and checks; **2MiB** combined authored report/status additions and local accounting output. Initialize the monotonic clock before optional preparation; count elapsed synchronous tool waits. Persist conservative charged work across interruption, excluding approval waits before starting. No reset or continuation after exhaustion.
- No additional Python aids or launcher changes. Use existing PowerShell/standard-library text/hash inspection as needed; do not import the application dependencies. Shared reservations include check subprocesses. No fake/native suite is needed for documentation-only research.
- On any limit, unavailable tool, unexpected private-data requirement or need for execution, stop new research, spend only protected capacity on an honest partial report and preservation checks, then close. No fallback to the old helper, automatic retry package or silent limit increase.

The local accounting is an auditable admission record, not an OS-wide intercept or a claim about tool-provider infrastructure. Existing binary/resource limits are not evidence that opaque remote tools meet those limits. No filesystem or outbound confinement, runtime offline capability, private-input trust acceptance or physical16GB resource result is implied.

## Deliverables and approval checkpoints

Research report: `docs/benchmarks/public-source-web-review.md`; focused freshness/input-fit cross-references in `docs/dependencies.md`, `docs/provisioning.md` and the proposed architecture ADR where findings warrant them; task/plan/README/checkpoint updates. Keep one detailed evidence matrix rather than duplicate it across every status file. Do not change SPEC, dependency pins or runtime policy.

This proposal is documentation only. Request approval of the exact R1-W package, particularly its replacement of transport-level limits with visible-tool limits. Request a separate Git decision for the five proposal/status files. One package approval covers W1–W4 edits/research/checks without repeated per-step permission; later findings commits, dependency changes, native validation, G2 adoption and application implementation retain their own gates.
