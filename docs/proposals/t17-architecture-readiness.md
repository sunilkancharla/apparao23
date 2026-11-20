# T17 — architecture readiness and design/adoption package

## Current outcome and authority

**T17-A1–A6 static package authorized and prepared:** after readiness commit `e9d107e`, the user said "I approve and proceed further". The concrete [proposed ADR](../ADR/0001-stage1-architecture.md), [C01–C08 contracts](../contracts.md), [reconciled inventory](../dependencies.md#t17-a1--static-reconciliation-and-proposed-runtime-set) and [provisioning/validation handoff](../provisioning.md#t17-static-pack--provisioning-and-validation-handoff) are now written. Additional accounting/original-cap/resource/tombstone choices were explicitly approved and synchronized into SPEC/decisions. G2 remains open with exact freshness/input-fit/native-trust/resource/representative-validation gaps; no implementation or runtime adoption occurred. The next recommended [R1public review](../provisioning.md#proposed-follow-up-r1--public-source-refresh-and-input-fit-method-review) is concrete but unapproved and unexecuted. Earlier proposed-package wording below is historical.

T16 static review is committed as `cdbb975`. The user authorized proceeding to the next step and explicitly chose **"Defer chart trial until after first CSV flow"**. The pre-G2 chart gate is therefore satisfied by that narrow deferral; T16A remains tracked after T34, before any claim of chart interpretation. PDF/XLSX/CSV, scanned-PDF OCR, local processing and the Windows11/16GB/CPU-only target remain unchanged. This is not deferral of required OCR or of all remaining acceptance checks.

This readiness assessment and concrete static design package are prepared for review. **G2 is not ready for unconditional approval.** Preferred candidates and T16 policies exist, but final component contracts, input-fit validation, resource/latency acceptance and several recovery/accounting details remain unresolved. No runtime installation, loading, model/parser/OCR/API execution, new trial allocation or application implementation occurs here.

## Existing component inventory — candidates, not new selections

| Role | Existing reviewed candidate / evidence | Remaining T17 action |
|---|---|---|
| Environment / backend | Existing project-local `.venv`, uv0.13.8, Python3.14.6; FastAPI0.162.2/Uvicorn0.54.0/HTTPX0.28.1 pinned in pyproject/lock | Reconcile exact installed versus evaluation-only inventory; no reinstall/global changes or assertion of current advisory clearance |
| Browser UI | Minimal local HTML/CSS/JavaScript already approved; Design1 landing and Design2 chat/citations inspiration | Define safe browser/API contract; UI UX Pro Max separate review before T33; no framework/CDN adoption |
| CSV | Standard-library CSV with record/column/physical-line provenance, per [tabular evaluation](../benchmarks/tabular-text-parsers.md) | Define encoding, duplicate headers, multiline/long records, validation and parser-error behavior |
| XLSX | openpyxl3.1.5 with reviewed XML support; same tabular report | Adopt only after exact cache/merged-cell/date/external-link and resource contracts; never calculate formulas/macros |
| PDF | Reviewed pypdf7.0.1 and pdfplumber0.11.10/pdfminer-six20260107; PDFium rendering candidate per [PDF evaluation](../benchmarks/pdf-parsers.md) | Select exact text/table/render path and failure policy, reconcile transitive native notices and representative scan detection; PyMuPDF/MarkItDown exceptions remain recorded |
| OCR | Preferred Tesserocr2.13.0/Tesseract5.5.4/Leptonica1.87.0 with pinned English asset | Use the exact [model/OCR shortlist](model-ocr-selection.md) identities; readable synthetic results are not representative scanned/mixed-PDF acceptance; rotation limitation remains |
| Local chat / embeddings | Preferred Qwen2.5:1.5b-instruct-q4_K_M and Nomic-embed-text:v1.5; exact manifests/assets linked by shortlist | Resolve digests/prefixes/dimensions/context/CPU controls and startup checks, no tag-only adoption or silent downloads; validate input-fit before use |
| Metadata / search | SQLite3.50.4 in evaluated interpreter; exact sqlite-vec0.1.9 Windows artifact preferred | Carry [T12-D](../benchmarks/sqlite-vec-match-results.md) hashes/notices/query/scope limitations; no new index optimization, larger-scale guarantee or native confinement claim |

Entries describe recorded project evidence, not a fresh security/maintenance audit or a complete application dependency bill. Preserve exact cache/seal identities; T17 must reconcile runtime versus evaluation dependencies and refresh necessary public advisory/license evidence before adoption under an explicit research boundary. Do not import parsers/extensions to populate a documentation table.

## Proposed architecture to make concrete in the design pack

Locally served browser → loopback FastAPI validation/configuration → selected-reference document/chat services → versioned extraction/chunk/index storage → scoped retrieval and supplied-evidence manifest → local Ollama generation → citation/completion checks → saved answer and honest support indicator. SQLite owns reference/history/processing/cleanup metadata; originals remain separate from normalized outputs and derived indexes. File paths and evidence IDs are server-controlled. Background processing must have an adopted resource/concurrency boundary; the trial harness is not a production worker subsystem.

The pack must show a small diagram, trust boundaries and failure paths, not merely a proposed directory tree. It must distinguish usable implementation from evaluation aids. No schema, module or endpoint is created just to illustrate this document.

## Settled decisions — carry forward without asking again

- PDF/XLSX/CSV; English OCR; library versus attachment ownership; local-only models/storage and browser assets; loopback binding.
- Decimal100MB/file,10document references/upload/conversation,1GB unique library originals;5GB processed and1GB temporary disk caps, clear stop when full. Reference identity is distinct from deduplicated bytes.
- Delete conversation messages, quotations and exclusive data; preserve shared/library content; block referenced-library deletion. Keep saved answers when a source is unavailable, labelled and excluded from new answers.
- Approved R02 indicator design and R08 durable deletion/pending cleanup direction; R01 only a provisional validation baseline, not final defaults or permission for an inference trial.
- T16A deferred until after T34. Q18/Q19 and chart fixture definitions stay active but deferred/unready; do not mutate their gold facts, score them as passed or claim visual support. A CSV-first evaluation may use its explicitly frozen subset, not silently relabel full-stage coverage complete.

## Remaining readiness decisions and evidence

| ID | Needed before the dependent adoption/implementation | Alternatives / consequence to present |
|---|---|---|
| A01 | Exact selected runtime artifacts, notices, dependency/transitive inventory and current relevant advisory review | Reuse pinned reviewed artifacts with documented limitations, or propose a separately reviewed change; no "latest" substitution |
| A02 | Quota classification and atomic reservations: originals versus normalized/index/preview/history/journal/temp files, concurrent writes and duplicate requests | Explicit managed accounting with clear reservation/recovery rules; no automatic eviction or unapproved reclassification to evade caps |
| A03 | Aggregate saved-conversation-original storage policy | Separate total cap chosen by user, or explicitly uncapped aggregate with free-space safeguards. The1GB library cap does not silently cover all attachment originals |
| A04 | Exact logical deletion, cleanup/refcount/ownership and answer-publication transaction/coordination, restart state and bounded retries | Implement the approved durable-intent/pending design; spell out exclusive/shared paths, race prevention and failures before selecting schema |
| A05 | Model-input fit and scope-safe history/evidence packing | Byte guards alone are insufficient; select a trustworthy local token/template-fit or verified equivalent method and truncation handling. Additional dependencies/native trials require a new bounded package |
| A06 | Final application concurrency, deadlines, memory/headroom, disk-expansion and latency budgets | Benchmark observations inform choices but are not approved product thresholds. Keep CPU-only16GB target and disclose larger actual-host RAM; no unapproved physical-target waiver |
| A07 | Representative quality and scale readiness | Plan source/anchor, scanned/mixed/rotation/table, multi-file and restart checks with existing gold and preserved exclusions; distinguish validated contracts from later product acceptance |
| A08 | App trust boundaries and local/offline operation | Define upload/parser/preview/model-output protections and missing-asset refusal; native trial jobs/SQL authorizer do not prove application filesystem confinement |

Classify each row as established evidence, a user decision, a static design task or a separately budgeted validation gap. A draft ADR does not close an evidence gap. If new measurement is required, present exact artifacts/fixtures/resources/stop conditions and obtain that package approval before executing it; do not reuse a closed meter or reopen native trials.

## Proposed bounded T17-A static package

Primary outputs: `docs/ADR/0001-stage1-architecture.md` (proposed until G2), `docs/contracts.md`, focused updates to `docs/dependencies.md` and `docs/provisioning.md`. Supporting PLAN/TODO/README/decision/checkpoint updates preserve the approved decisions. Existing ADR directory is absent; create it only when writing the actual proposed ADR, not as an empty placeholder.

No application/evaluation executable code, dependency/lock/environment change, new fixture, native/model/parser/OCR/server/API run or installation/download is included. Static execution budget: **zero runtime trials and zero outbound requests**; only authored-source/report reads, normal document edits and local link/diff/JSON/hash checks. Do not read original documents/raw answer/vector databases into connected tools. A necessary public advisory/license refresh is an explicit follow-up research gate if it cannot be satisfied from current recorded evidence; do not label it complete here.

| Task / status | Objective and prerequisite | Acceptance / verification |
|---|---|---|
| T17-A1 / proposed | Reconcile evidence/artifacts and decision ownership; exact package approval | Candidate-to-hash/notice/report inventory and A01–A08 matrix; distinguish preferred/evaluated/adopted and identify freshness gaps |
| T17-A2 / proposed | Specify data/network/API/storage contracts; A1 | Version/reference/ownership/quota/delete/publish/startup boundaries and explicit A02–A04 choices; manual shared-content, quota-full, crash and scope-race walkthrough; no invented policies |
| T17-A3 / proposed | Specify resource/context/privacy readiness; A1–A2 | A05–A08 alternatives, exact required user decisions and any separately scoped validation/research proposals; do not claim byte counts prove token fit or a trial job confines the app |
| T17-A4 / proposed | Assemble proposed architecture ADR; A1–A3 | Concrete diagram, selected-versus-candidate inventory, constraints, alternatives and acceptance matrix; every unresolved gate visible; at most three primary files per increment |
| T17-A5 / proposed | Independent static quality/security review; A4 | Trace contracts against approved SPEC/T16, local links/IDs/diff checks; no blanket schema/component approval or hidden acceptance waiver |
| T17-A6 / proposed | Present G2 readiness/remaining gaps and checkpoint; A5 | User receives a concrete pack and decisions; record G2 only after explicit approval and prerequisite satisfaction, otherwise report specific blockers; separate commit and T18 authorization |

One approval covers the necessary static tasks, checks and corrections; no per-edit permission is needed. User choices, new execution/research, runtime adoption, Git commits and stage transitions retain their gates. Optional developer tools do not block the pack; SkillSpector is deferred, RTK/ponytail stay after the slice or before use, and UI UX Pro Max remains before frontend implementation.

## Requested next decision

Approve the exact T17-A1–A6 static package and, separately, committing these readiness/status changes. The chart-timing decision is already approved and must not be asked again. Do not approve application coding or unconditional G2 from this readiness report; the actual architecture/contracts and outstanding decisions must first be made reviewable.
