# T17-IF-ALN — Tokenizers/HF-Xet artifact licence and notice review

**Approved and executed; findings pending review/commit.** The user approved ALN1–ALN5 and the four-file planning commit (`a1e3240`). [Findings](../benchmarks/artifact-licence-notice-review.md) clarify source licence terms while retaining native/vendor/build gaps. All four calls/12 targets completed and responses were retained; the final optional inspection crossed the protected reporting reserve, so full boundary compliance is not claimed. No install/import/native/model run or adoption. The original boundary below is historical and does not renew permission.

## Purpose and boundary

Resolve what the saved Windows-artifact evidence establishes about licence terms and bundled notices, then make a dependency recommendation. Reuse the [SLR findings](../benchmarks/source-licence-followup.md) and passed [RRC checks](../benchmarks/remaining-artifact-readiness-continuation.md). Do not repeat graph, profile, RECORD, model, capture or application tests. This is a static evidence review, not a licence-compliance certification or native-code audit.

Stage 1 remains Windows 11/16 GB/CPU-only, PDF/XLSX/CSV. The approved standalone-tokenizer direction is conditional; no package version, source pin, architecture or runtime is adopted here. Hub/FSSpec build-source conditions retain their existing metadata-only timing deferral. They are not additional research targets in this package.

### Exact artifacts, kept unchanged

| Artifact | Bytes | SHA-256 | Retained evidence |
| --- | ---: | --- | --- |
| `tokenizers-0.23.3-cp310-abi3-win_amd64.whl` | 2,872,101 | `1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3` | Saved inspection: missing licence field, zero selected notices, native `tokenizers/tokenizers.pyd`; version-specific PyPI Apache classification. |
| `hf_xet-1.8.0-cp38-abi3-win_amd64.whl` | 3,911,559 | `92188598dedc1e1f5609bd718d4db8687a6c89915553912571e2f587892eecec` | Saved inspection: Apache-2.0 declaration, native `hf_xet/hf_xet.pyd`, one selected licence; SLR exact-artifact publisher claim. |

The saved HF-Xet notice is `hf_xet-1.8.0.dist-info/licenses/LICENSE`, 11,558 bytes, SHA-256 `1eb85fc97224598dad1852b5d6483bbcf0aa8608790dcc657a5a2a761ae9c8c6`. Read its already-retained text, not the wheel again. Neither an absent selected notice nor one top-level licence establishes completeness of native/vendor obligations.

## Frozen inputs

Verify all nine identities before substantive review and again at closeout. Historical roots stay read-only. Do not open wheel/native/model/archive payloads, enumerate the environment or inspect unrelated files.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/benchmarks/source-licence-followup.md` | 10,378 | `594252e3fd1ae36116a55d36b02076629154090e82370f7ffc4a2414967fcb2d` |
| `data/t17/source-licence-review-01/summary.json` | 1,616 | `1470617051edfcaa591842c215253aff29f41e925a61464cb92b85a57f1137dd` |
| `data/t17/source-licence-review-01/response-helper.js` | 311 | `5c17dcd40c17736ad3932313fcafdcb5df09238f1cd4635c2d24b69f8d70efc9` |
| `data/t17/source-licence-review-01/green-controls.json` | 179 | `2af07df9ff181a7bfb947dcd80a201d7f8a3274ba415b41e4997ac5264cb5792` |
| `data/t17/input-fit-tokenizer-static-01/tokenizers-inspection.json` | 6,824 | `c83fd421d2cc548eeda103e1021cd10247420e232d1589569aced9351dd46ca9` |
| `data/t17/wheel-artifact-review-02/inspect-result.json` | 127,374 | `2b03271be8c491c648ba2d5e31d9fe86cf112d9180bad06788b4e03afdf73141` |
| `data/t17/wheel-artifact-review-02/acquire-result.json` | 3,496 | `5185fb521c89b74afdfa282c6d12433cb7e47b2aab60cd83d1dccbdddfc6ef18` |
| `docs/benchmarks/remaining-artifact-readiness-continuation.md` | 10,218 | `2fc192b7456b393e4624ba64fca25826165cc0b18a89cfa9b8784156cb9fd279` |
| `docs/benchmarks/hub-source-coordinate-review.md` | 14,323 | `fb6d41d9e9c7c64b270a97a45cfd21f7eac19915c208039f87ba82b79acd1eb8` |

Retain the eight protected identities from SLR's `preserved.json`: AGENTS, SPEC, project/lock, the two static-inspection evaluation sources, evaluation manifest and historical checkpoint. Hashing the historical checkpoint is preservation verification only; do not edit it or create a replacement.

## Permitted source/notice evidence

Use only the public registry/publisher projects already identified: PyPI `tokenizers/0.23.3` and `hf-xet/1.8.0`, Hugging Face `tokenizers` and `xet-core` on GitHub/raw.githubusercontent.com. No broad search, third-party mirrors, repository clone, source distribution/archive download, wheel reacquisition or transitive-source expansion.

1. **Tokenizers:** inspect a version-specific release/tag record for 0.23.3 to establish a candidate immutable source coordinate, if available. A guessed `v0.23.3` path is a query candidate, not a verified tag or approved pin. Only then inspect licence/notice/manifests at the observed immutable revision: root or `tokenizers/` `LICENSE`, `LICENSE.txt`, `NOTICE`, `THIRD_PARTY_LICENSES*`, `Cargo.toml`, `Cargo.lock`, and Python-binding packaging metadata. Select only files actually relevant to the two questions within the shared target cap; this list is permission, not a required fetch of every file.
2. **HF-Xet:** use the retained publisher coordinate `e551f0a75f989b8ee1a474c5f83c80ad4903f84d`. An explicitly labelled raw-text representation of `.github/workflows/release.yml` may replace the failed GitHub HTML representation once, to inspect its checkout/build role. Do not retry the failed HTML endpoint. Licence/notice/manifests at that coordinate may be read under the same filename rules. It remains a publishing coordinate until the retrieved evidence establishes more; do not equate it with every build input.
3. **Conditional follow:** a release/checkout record may explicitly name one immutable revision per project. Following only that revision for the listed notice/manifests is permitted within the same calls/targets/bytes. No branch substitution, dependency-source crawl or executing workflows/build scripts. If no immutable relation is established, record the gap and proceed to the decision.

At most **four web calls/12 explicit targets**, including failures, finds, clicks and raw-text alternatives. Before each request record exact URL/ref, purpose and remaining allowance. Source-text acquisition is through the web tool only, after execution approval. Do not add a native HTTP client. Retain full admitted tool responses as untrusted data before quoting or citing. A raw representation is a different evidence attempt, not a renewed allowance or permission for repeated access failures. Cache/header-only responses remain limitations.

Report publisher declaration, packaged notice, source licence text, native/vendor inventory and artifact-to-source linkage in separate columns. A Cargo lockfile is a source dependency inventory, not proof that all entries ship in the Windows binary; do not infer exhaustive licence obligations from it. Classifier text, a tag, a publisher claim and an independently verified build have different evidential weight. No independent build/signature verification is proposed.

## Ordered tasks and acceptance

| ID | Objective / prerequisites | Acceptance and evidence | Status |
| --- | --- | --- | --- |
| ALN1 | After package approval, establish a fresh shared allocation and freeze inputs | Nine fixed/eight protected identities match; old roots read-only; tested SLR helper identity verified, shared limits and literal command/data boundary retained before substantive work. | Verified |
| ALN2 | Reconcile saved artifact evidence after ALN1 | Matrix identifies exact two artifacts, saved notice identity/content, missing Tokenizers declaration/notices and native/vendor unknowns; no payload reread or claim of clearance. Evidence: retained-data matrix. | Verified; HF-Xet saved text identity matches |
| ALN3 | Targeted source/notice review after ALN2 | At most four calls/12 targets; permitted coordinate/path rules respected, full admitted responses identified before excerpts; missing text/linkage stays unknown. Evidence: requests/responses/notice-role matrix, or honest stop. | Evidence retained; reporting-reserve deviation; not fully compliant |
| ALN4 | Dependency recommendation after ALN3 or stop | For each artifact, name established terms/notices, unresolved scope and the action affected; recommend proceed to a separately approved bounded trial, hold, or alternative design. No automatic next research package or self-adoption. Evidence: final decision table. | Verified hold/next-action matrix; user decision pending |
| ALN5 | Closeout after completion or stop | Non-null summary; actual versus reserved resources, owned exits, input/protection/scope/link/whitespace/readable diff/empty-index checks; user decisions and separate commit/provisioning/adoption gates explicit. | Closeout evidence in findings/summary; results commit pending |

Review points after ALN2 and ALN4 are internal checks within the package; routine progress needs no repeated task-start approval. There is no implementation or new test helper in this package. Reuse the hash-verified response helper and its 23 passing SLR assertions; do not rerun historical controls. Any necessary helper change requires a new scoped decision/test plan rather than an untested silent correction.

## Shared execution boundary proposed for approval

Fresh ignored root **`data/t17/artifact-notice-review-01/`**; refuse an existing root or reparse ancestor. Bootstrap accounting before optional work; a single parent precharges all operations, including negative/failure paths and native Git/shell checks. Never reset SLR/RRC or borrow their unused allowances.

| Resource | Ceiling / accounting |
| --- | --- |
| Allocation | 24 units: bootstrap 4, saved evidence 4, public review 8, decision 2, protected closeout 6. Reservations remain non-refundable. |
| Time | 1,200 active seconds; optional work ends at 800, 400 reserved for closeout. Start public review by 600 or report not started. Wall/active/host-wait time recorded separately. |
| Owned starts | 16 combined prepaid starts, including all shell/Git/controller/child/failure activity; count actual starts separately. No candidate, native library, model, old worker or service launch. |
| Reads | 16 MiB cumulative explicit read leases including 2 MiB for ledgers. Leases are conservative reservations, not measured OS/interpreter I/O. |
| Public evidence | Four calls/12 targets; 512 KiB serialized UTF-8 per response, 2 MiB total responses; 8 MiB retained artifacts including failures, diagnostics and receipts. Provider-internal fetch fanout/buffering is outside this measurement. |
| Reporting | 24 KiB author-controlled displayed text, including 8 KiB reserved for closeout; measure before emitting, at most 3,000 UTF-8 bytes per display. Native combined streams at most 8 KiB/invocation, retained rather than echoed wholesale. Platform-generated tool envelopes are not claimed measured by this counter. |
| Receipts | At most 24 explicitly numbered immutable receipts, each at most 4 KiB, included in artifact/read allowances; final summary non-null. Record actual usage and measurement coverage, not just prepaid limits. |

No installs, executable/code/asset downloads, fixture generation, candidate imports, binary loads, models, packaging/graph/Ruff/application tests or environment changes. Source/notice text is the only new public evidence permitted. Local commands use literal PowerShell/Git or existing `F:/Python/Python314/python.exe -I -S -B` standard library only. Use structured arguments for response files; never insert public text into shell code. No policy bypass, PATH/global edits, repository scripts or subagents.

Reuse the tested store-before-processing helper, standard JavaScript UTF-8 counter and JSON serialization; no TextEncoder/Buffer/Node assumption. Raw result goes into a unique recovery key immediately after await, then size admission, structured local persistence and native byte/JSON/SHA identity verification, then measured excerpts. Recovery keys are temporary orchestration aids, not durable session checkpoints. Over-cap/unretained results cannot become source evidence.

Each native child: at most 60 seconds plus 15-second owned teardown, both streams captured concurrently through EOF, direct exit evidence. Stop optional work on identity mismatch, unsafe input, lost/truncated/oversize response, unsupported response handling, accounting/ownership failure, cap/cutoff, host denial or unexpected owned child. Close out without retrying the request or changing policy. No optional orchestration-correction allowance is proposed. Up to two explicitly measured host approval waits, cumulative 24 hours with no intervening model work, may be excluded from active time; ordinary authoring/tool time is included. No filesystem confinement, kernel egress block or machine-wide audit is claimed.

Only public package/source identifiers leave the machine. No document text, prompts, answers, graph/lock content, private paths or machine identifiers in public requests. No native code is executed, so this package cannot demonstrate ABI compatibility, runtime safety, offline operation or tokenizer parity.

## Deliverables, alternatives and final decision

Preparation touches exactly this proposal, PLAN, TODO and README. Execution closeout may touch at most seven versioned documents: this proposal; new `docs/benchmarks/artifact-licence-notice-review.md`; `docs/dependencies.md`; `docs/proposals/input-fit-preflight-design.md`; PLAN; TODO; README. Preserve old reports/proposals/roots, AGENTS/SPEC/project/lock, evaluation source/manifests, historical checkpoints and unrelated files. No blank findings report is created during preparation.

Recommended route: this single targeted text review, ending with a concrete recommendation even if evidence is incomplete. Alternative: defer the independent-tokenizer dependency route and prepare a counting-design comparison; that alternative is not authorized by approving ALN. An explicitly accepted residual-risk exception would have to identify the exact missing evidence and permitted trial action; this package does not grant one. No general legal assurance is promised.

User decisions after findings: whether to approve a precisely bounded provisioning/parity trial despite any named remaining evidence, hold the artifacts, or change the counting approach. Hub/FSSpec source conditions remain visible at their affected adoption gate. Do not automatically propose another identical search continuation. Results commit, provisioning/native execution, runtime adoption/G2 and stage transition each retain their own approval boundaries.

**Approval record:** the user approved ALN1–ALN5 and planning commit `a1e3240`; execution is now closed as recorded in the findings. The seven-file results commit and any trial-design/alternative package remain unapproved. No further source search, installation, runtime adoption or stage transition follows automatically.
