# T17-R1-W — bounded public-source review

## Outcome and scope

Checked **2026-11-16 UTC** under the approved [R1-W package](../proposals/public-source-web-review.md), proposal committed `780bad2`. The read-only review reached its prepaid research block after **12 visible web calls /48 requested targets**. Findings are useful but coverage is partial. No component is newly adopted, upgraded, installed or executed; G2 remains open.

The specific Starlette, pdfminer and Pillow advisories examined list patched versions at or below the recorded pins. This is a version-range comparison, not proof that the installed payload contains every fix or that the whole environment is safe. Complete transitive/native notice and advisory coverage remains unresolved. For input fit, the pinned Ollama source provides promising rendering and truncation controls but no verified application-facing exact count-only contract. Recommend a separate design of matching-template/tokenizer preflight before any native trial or implementation.

No private documents, prompts, answers, vectors, local filenames/paths or receipts entered web requests. Only public software/version identifiers and upstream questions were researched. No source code from a page was executed. Sources below were read through built-in tools; their internal HTTP requests/redirects, bytes and remote resource use are opaque.

## Local inventory and artifact identity

Text inspection of `uv.lock` confirms the following relevant transitive pins: Starlette1.10.0, Pydantic2.14.3, pydantic-core2.50.4, anyio4.16.0, h11 0.16.0, httpcore1.0.9, cryptography50.0.2, cffi2.1.1, charset-normalizer3.5.2, certifi2026.10.23 and idna3.20. No `python-multipart` distribution is recorded. This absence is a future upload-interface dependency decision, not permission to add it. Existing 52-installed/53-lock reconciliation is historical metadata evidence; no new imports or full payload integrity audit were performed.

The [component inventory](../dependencies.md#t17-a1--static-reconciliation-and-proposed-runtime-set) remains authoritative. Frozen model identities carried forward, not newly fetched or loaded:

| Component | Recorded immutable identity |
|---|---|
| Ollama0.40.16 executable | SHA256 `4ccefcbfecc50fb6526471adabbc20869dd614e29e351120b15083cb174b0b8a` |
| Qwen2.5:1.5b-instruct-q4_K_M | Manifest `65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b`; weight `183715c435899236895da3869489cc30ac241476b4971a20285b1a462818a5b4` |
| nomic-embed-text:v1.5 | Manifest `0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f`; weight `970aa74c0a90ef7482477cf803618e776e173c007bf957f635f1015bfcfef0e6` |

Public Ollama source was read at tag `v0.40.16`, not `main`. This review did not independently bind every binary/vendor file to a full source commit or reproducible build. Discovery results from `main` were not used to assert pinned behavior.

## Advisory findings

All rows were checked2026-11-16UTC. Dates are upstream publication dates. “Outside range” applies only to that advisory's recorded range. Proposed user-facing routes do not yet exist, so reachability statements describe the planned surface, not a tested application.

| Component / source | Published; affected / patched | Applicability and next action |
|---|---|---|
| Starlette: [GHSA-82w8-qh3p-5jfq](https://github.com/Kludex/starlette/security/advisories/GHSA-82w8-qh3p-5jfq) |2026-06-12; >=0.4.1,<1.3.1 /1.3.1 |Recorded1.10.0 is outside range. URL-encoded form limits were bypassed; future upload/body limits must still be enforced and tested independently. |
| Starlette: [GHSA-wqp7-x3pw-xc5r](https://github.com/Kludex/starlette/security/advisories/GHSA-wqp7-x3pw-xc5r) |2026-05-23; <1.1.0 /1.1.0 |Recorded1.10.0 is outside range. The Windows StaticFiles/UNC credential-leak path is directly relevant to the target OS; future path checks must reject unsafe forms before filesystem resolution. No SMB probe performed. |
| pdfminer.six: [GHSA-wf5f-4jwr-ppcp](https://github.com/pdfminer/pdfminer.six/security/advisories/GHSA-wf5f-4jwr-ppcp) |2025-11-07; <20251230 / >=20251230 |Recorded20260107 is outside range. Crafted PDF/CMap loading could reach unsafe deserialization. No exploit or parser was run. |
| pdfminer.six: [GHSA-f83h-ghpp-7wcc](https://github.com/pdfminer/pdfminer.six/security/advisories/GHSA-f83h-ghpp-7wcc) |2025-11-07; <20251230 / >=20251230 |Recorded20260107 is outside range. Distinct local CMap deserialization issue; its narrative discusses an incomplete older patch. Use the published fixed range without inferring that an earlier partial fix suffices. |
| Pillow: [GHSA-78g4-xqwv-q3g8](https://github.com/python-pillow/Pillow/security/advisories/GHSA-78g4-xqwv-q3g8) |2026-10-17;11.1.0–12.3.0 /13.0.0 |Recorded13.0.0 is the listed fixed version. Bundled OpenJPEG matters independently of host OS updates. The advisory header's fixed range and older descriptive narrative must not be conflated with verification of our exact wheel. |
| Pillow: [GHSA-wqgw-9xfh-qf2g](https://github.com/python-pillow/Pillow/security/advisories/GHSA-wqgw-9xfh-qf2g) |2026-11-02; <=12.3.0 /13.0.0 |Recorded13.0.0 is listed fixed. TIFF/EXIF allocations can precede pixel decoding; keep bounded workers and explicit format handling. No reproducer executed. |

The [Starlette index](https://github.com/Kludex/starlette/security/advisories) additionally lists host/path/method, Range and older multipart issues; those detailed ranges were not all opened. The former encode repository redirects to Kludex on the same GitHub domain. The [FastAPI index](https://github.com/fastapi/fastapi/security/advisories) lists a historical CSRF advisory; its full affected range was not reviewed. The [Pillow index](https://github.com/python-pillow/Pillow/security/advisories) lists further image-processing issues not individually triaged. An [Ollama advisory index](https://github.com/ollama/ollama/security/advisories) with no published entries does not establish absence of vulnerabilities, including in its bundled runner or Go dependencies.

## Native notices and provenance

| Component | Public evidence compared with existing inventory | Remaining gap |
|---|---|---|
| pypdfium2 5.15.2 / recorded PDFium159.0.8149.0 |[Publisher package page](https://pypi.org/project/pypdfium2/5.15.2/) describes Apache2.0/BSD3 wrapper terms and separately shipped PDFium/vendor notices. Existing T05 report records47 packaged notice files retained locally and flags[] without an optional V8/XFA request. |Version-specific LICENSE/tree URLs attempted returned404/cache miss. No fresh file-by-file binary/vendor notice reconciliation or native advisory audit; the package page alone does not prove the exact build's full contents. |
| tesserocr2.13.0 / recorded Tesseract5.5.4, Leptonica1.87.0 |[Publisher package page](https://pypi.org/project/tesserocr/2.13.0/) identifies MIT wrapper terms and bundled Tesseract/Leptonica/runtime dependencies in prebuilt wheels, with language assets separate. Existing artifact inventory retains the exact Windows wheel/English asset identity. |Attempted tagged LICENSE/tree pages were unavailable. Wrapper MIT metadata is insufficient for all bundled codecs/libraries/notices; no fresh native advisory/notice completeness claim. |
| sqlite-vec0.1.9 |Tagged [MIT](https://raw.githubusercontent.com/asg017/sqlite-vec/v0.1.9/LICENSE-MIT) and [Apache2.0](https://raw.githubusercontent.com/asg017/sqlite-vec/v0.1.9/LICENSE-APACHE) texts are available; [tagged tree](https://github.com/asg017/sqlite-vec/tree/v0.1.9) contains both. Existing [artifact review](sqlite-vec-artifact-review.md) resolved commit `e9f598abfa0c06b328d8fe5da9c3760cce74be10` and companion hashes. |No new response-byte hash comparison, binary/source attestation or reproducibility proof. The approved companion-notice exception remains exact-artifact-specific; missing bundled notices remain disclosed. |
| Ollama0.40.16 |Tagged [wrapper license](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/LICENSE) is MIT. |Not a complete notice inventory of bundled llama.cpp/native dependencies/model assets. No model-card/template license refresh or Windows artifact-to-source attestation completed. |

Prior sqlite-vec companion identities remain MIT1068bytes/SHA256 `6ce72bbe12d975bd5286e5ab0a064c069693300c47bccbc57bec18485f1621ea`, Apache10931bytes/SHA256 `a38070a94d4afd9cd710e3ce67bd1de78097cfe1784c1f0109ac95d3c196bfdc`. No license payload was downloaded or repackaged. This review does not change the approved exception or certify redistribution rights.

## Pinned input-fit evidence and recommendation

The following is a source review, not a runtime demonstration. Findings derived from a source file are grouped to preserve their context.

1. **Message selection/rendering:** tagged [server/prompt.go](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/server/prompt.go), `chatPrompt` and `renderPrompt`, selects renderer versus template and can remove older messages when truncation is enabled. It retains system/latest messages; that retention rule is not a proof that the final prompt fits. Its text-token comparison uses context size, without a visible reservation of our192 output tokens in this function. This supports explicit admission accounting rather than trusting defaults.
2. **Public routing and safeguards:** tagged [server/routes.go](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/server/routes.go), `GenerateRoutes`, `ChatHandler`, debug branches and `EmbedHandler`, has no exposed `/api/tokenize` route in the inspected registration. Chat forwards `truncate`/`shift`; `_debug_render_only` returns rendered text. That is useful for template comparison, not an exact count. Embedding `truncate=false` checks token/context limits and refuses overflow rather than using its truncation retry. This source also routes cloud/management operations, so localhost alone is not the entire privacy policy. Exact selected local model references, endpoint allowlisting and verified no-cloud behavior remain required. These findings do not establish that debug rendering avoids model loading or other native work.
3. **Request versus count contract:** tagged [api/types.go](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/api/types.go) defines `Truncate`, `Shift`, `_debug_render_only`, `NumCtx` and `NumPredict`. `DebugInfo` exposes rendered text/image count; ordinary response metrics include evaluated token counts. There is no exact token count in that debug structure. Post-generation metrics cannot serve as pre-generation admission proof.
4. **Internal tokenizer:** tagged [llm/llama_server.go](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/llm/llama_server.go), `tokenize`/`Tokenize`, calls an internal owned runner's `/tokenize` on its own loopback port. `Tokenize` passes false for added special tokens, while the completion pre-processing path can request true. The file also selects native chat-template versus rendered completion behavior. Therefore counting arbitrary raw text with an unrelated tokenizer, or ignoring BOS/template behavior, is unsafe. This internal interface is not an adopted stable application API. Its runner and exact special-token/template parity would need independent ownership, identity and compatibility validation.

Current [chat documentation](https://docs.ollama.com/api/chat) describes response token metrics; it does not establish an exact count-only interface for our pinned binary. Current [embedding documentation](https://docs.ollama.com/api/embed) states that `truncate=false` refuses overlong input. These moving pages corroborate intent but are not substitutes for pinned behavior and local tests. The tagged [runtime interface](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/llm/server.go) exposes tokenizer/template/context operations internally; requested context can be clamped to model training context.

| Option | Assessment |
|---|---|
| Public count-only API with no new component |Not established by the inspected registration/types/docs. Do not invent an endpoint or treat zero output tokens as a documented count-only operation. |
| Exact rendered prompt plus matching pinned tokenizer |Preferred design to investigate. Determine the actual cached Qwen template/native path, special-token policy and effective context. Compare the full system/history/question/evidence request, then require input tokens +192 output reserve + any justified measured overhead <= effective context. A tokenizer artifact, direct internal runner access or runtime modification would require its own review/approval. |
| Disable truncation/context shifting and rely on errors |Useful additional safeguards to test, but they do not return an exact pre-generation count or prove output headroom. Cannot alone satisfy the unchanged gate. |
| Byte caps, trailing marker or returned token counts |Retain byte caps as resource bounds only. None independently proves exact fit; no safe byte/token conversion was established. |

The3000-byte serialized input,2000-byte evidence,800-byte chunks/top5,2048context/192output settings stay provisional. No new defaults are adopted. Nomic's recorded768 dimensions and `search_query:`/`search_document:` prefixes remain binding; the final prefixed input must be checked with its own tokenizer/context, not the chat model's. The model card/prefix asset was not refreshed publicly in this allocation.

**Unresolved:** the actual cached Qwen renderer/template and exact special-token stream were not executed or compared; tokenizer parity and output reservation are unverified. The next recommended work is a bounded static integration design for this preflight, paired with the missing runtime/native inventory items. Only after reviewing that design should a synthetic local validation package be proposed. No use of private inputs, internal port discovery, new tokenizer dependency or native execution is authorized by this recommendation.

## Coverage not completed

No current advisory clearance is claimed for Uvicorn0.54.0, HTTPX0.28.1/httpcore1.0.9/h11 0.16.0, Pydantic2.14.3/core2.50.4, anyio4.16.0, cryptography50.0.2/cffi2.1.1, openpyxl3.1.5/et-xmlfile2.0.0/defusedxml0.7.1, pdfplumber0.11.10, CPython3.14.6/SQLite3.50.4, Tesseract/Leptonica, PDFium, sqlite-vec or bundled runtime/vendor libraries. Likewise, certifi/idna/charset-normalizer/typing and other selected transitive notice coverage is incomplete. Named indexes are not exhaustive cross-registry audits. Installed comparison-only RapidOCR/ONNX/OpenCV, pypdf and related groups, and developer tools, remain separate from proposed runtime selections; no fresh security clearance or removal was performed for them.

Some attempted pages were unavailable (pypdfium2/tesserocr tagged paths, GitHub contents API, an alternate runner filename and GitHub llm tree). These count toward the budget. No transport fallback, new helper or hidden retry package was used. Only already eligible GitHub/raw/PyPI/Ollama-doc domains were opened; third-party search hits were discovery noise, not technical evidence.

## Verification, accounting and handoff

The fresh record `data/t17/public-review-web-01/meter.json` prepaid64units: initialization8, research24, report4, review8, close4 and protected16. The clock was persisted before optional inspection;16 source/spec/lock/closed-meter preservation hashes were captured. The explicitly approved proposal Git closeout `780bad2` finished before this research epoch and is a separate Git action, not charged to an old trial or represented as a research subprocess. No trial workers were launched.

Research used12 `functions.exec` wrappers plus12 web-tool invocations:24research units and48targets, including failed requests/finds/duplicates. The visible32-call/64-target caps were not the limiting boundary; the prepaid24-unit research block was. No further research is permitted in this closed allocation. Full reservations are retained without refund; final elapsed/output/preservation/check values are saved locally at closeout. Tool-provider infrastructure is not measured as local process starts.

Local review verified318 link targets and all16 preservation hashes. Conservative full-file output accounting was510,920bytes at that check, including entire affected authored files rather than just additions, with327.718seconds elapsed. Final whitespace/diff and closeout values are retained locally. Two protected units cover this final reporting clarification; two more cover the closeout tool/shell/Git verification overhead beyond its four normal units. All64reservations remain prepaid, with no refund or further research.

No new application tests or vulnerability scanner were run, and no historical suite was rerun. Results, affected freshness notes and PLAN/TODO/README/checkpoint await separate commit approval. SPEC/AGENTS/lock/dependency pins and historical sources/ledgers remain unchanged. G2, native trust, model-input fit, representative format/scale/resource acceptance and application implementation remain open.
