# T17-IF-MR — Hub 2.4.0 metadata and dependency readiness

## Status and approved timing decision

**Proposed; MR1–MR4 execution and the five planning-document commit await approval.** The user approved the seven AR findings/status files, the narrow timing deferral and preparation of this proposal. Results and the approval record are committed as `0d4003e`.

[The approved decision](../benchmarks/stable-tokenizer-alternatives.md) permits metadata/notices/advisory/dependency review of the unchanged Hub 2.4.0 candidate before exact build-source mapping is resolved. Registry-displayed publisher identity is publication evidence. Carry the unresolved mapping into the later adoption decision; do not infer actual wheel behavior from unbound source, substitute a source pin, install/execute a candidate or approve G2. No SPEC requirement or persistent rule is waived.

Purpose: establish what the candidate actually declares, which exact dependency/artifact proposals fit this project, what conflicts or licensing/security/native gaps remain, and whether a later provisioning proposal can be concrete. Completing this review does not adopt Hub, Tokenizers or the architecture.

## Fixed baseline

| Input | Identity / permitted use |
| --- | --- |
| Hub wheel evidence | `huggingface_hub-2.4.0-py3-none-any.whl`; 857,021 bytes; SHA-256 `42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801`. Read reviewed HS metadata/receipts; no payload reread or download. |
| Tokenizers wheel evidence | `tokenizers-0.23.3-cp310-abi3-win_amd64.whl`; 2,872,101 bytes; SHA-256 `1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3`. Existing metadata declares Hub `>=0.16.4,<3.0`. No payload reread/import. |
| Source roles | Publishing `178e1a1797858724c79fd9d12d79d0902d730497`; prior release `3739729b86489e4ae28b5a62e622be320b141493`. Neither is relabelled verified build source. No independent signature verification or reproducible-build claim. |
| Project compatibility | `pyproject.toml` declares Python>=3.11. Existing Windows AMD64 evaluation packages have Python3.14 markers; this is not proof of support across every Python>=3.11 version. Read project/lock metadata only. Windows11/16GB/CPU-only target is unchanged. |
| Existing constraints | Preserve all current pins, including HTTPX0.28.1 and declared transitive constraints. `httpx2` is a distinct distribution; existing HTTPX does not satisfy that name. Existing evaluation-group packages are not automatically adopted as application runtime dependencies. |
| Frozen records | AGENTS/SPEC/pyproject/lock; input-fit/parity designs; HS/SC/AR reports/proposals/aids and closed preservation/approval/closure records. Small authored evidence and saved public text only. |

Hub's reviewed direct requirements are click>=8.4.2,<9; filelock>=3.10; fsspec>=2023.5; hf-xet>=1.6,<2 with an applicable AMD64 marker; httpx2>=2,<3; packaging>=20.9; pyyaml>=5.1; tqdm>=4.42.1; typing-extensions>=4.1. Python<3.11-only tomli and unselected extras stay excluded. Verify against the existing reviewed metadata, not memory or candidate code.

## Ordered tasks

| ID | Objective / prerequisites | Acceptance / evidence | Status |
| --- | --- | --- | --- |
| MR1 | After exact approval, bootstrap and verify inputs/controls | Durable initial accounting/failure reservation before optional reads; immutable/reporting/Unicode/response controls pass; freeze exact small baseline identities and confirm approved timing scope. | Pending approval |
| MR2 | After MR1, build a proposed applicable dependency graph | Roots and direct edges verified; marker/extras decisions explicit; exact candidate versions identified from stable/non-yanked primary metadata; compare all applicable proposed edges with project/lock constraints. Record conflicts/unknowns without overriding pins. | Pending MR1 |
| MR3 | After MR2 or a partial graph, review readiness evidence | Per-candidate licence/notices, Windows/Python tags, native implications, published artifact hash/size, material advisory applicability and documented offline/telemetry intentions classified verified/declared/unknown/blocked. No runtime or full-security assurance. | Pending MR2 / partial graph |
| MR4 | After MR3 or earlier stop, recommend and close | Compact graph/artifact/conflict/readiness matrix with exact next decision, frozen/history/link/scope/whitespace/readable-diff/resource checks, statically validated final command and checkpoint. Separate results commit and later provisioning/adoption gates. | Pending MR3 / stop |

Checkpoints: prove controls before research; resolve or expose constraint conflicts before describing a provisioning package; review actual artifact identities and unknowns before any later installation request. An incomplete graph is a partial result, never adoption readiness.

## Candidate and research boundaries

Public primary-source/registry text through the web tool only: **12 calls / 36 targets**, at most four targets/call, short/medium responses. Opens/clicks/finds/searches and failures count. Source roots are official package registries, package-maintainer repositories/docs and primary security advisories. Never include user documents/chat content in queries.

- At most **20 distinct applicable runtime distribution names**, including Hub and Tokenizers. Reuse already reviewed direct metadata and saved public responses. Identify one exact proposed version per distribution satisfying the relevant constraints where possible; one bounded alternative may be compared for a documented conflict. Candidate identification is not runtime selection/adoption.
- Prefer retaining a compatible existing pin. Do not choose latest solely by recency or silently upgrade/downgrade, remove a constraint, narrow supported Python or add an extra. A conflict requires an explicit options/impact entry and later user decision. No resolver, lock generation or install command.
- For each proposed candidate, record distribution/version, metadata/source URL, direct edges/markers, licence declaration and notice availability, Python/platform tags and relevant native dependencies. If officially exposed, record exact Windows or universal wheel filename, SHA-256 and size as **publisher metadata**, not independently downloaded verification. No new archive/wheel/sdist/model acquisition or extraction.
- Separate source-declared offline/cache/telemetry settings from verified artifact behavior. Native bundled notices, actual load/ABI compatibility, total RAM/disk use, offline operation and parity remain later checks. Documented wheel size is not a RAM benchmark or installed-footprint measurement.
- Assess material published advisory/fixed-range applicability to exact proposed versions when primary evidence is available. No index search, absent result or declared licence establishes complete security/licensing clearance. Mark transitive/bundled-native coverage incomplete when necessary.
- Do not repeat the failed HS/SC URLs listed in closed source-target records, switch HTTP transports or attempt repository cloning. Build/source reconciliation is explicitly outside this package. Source text may inform a declared intention, never a claim of matching wheel implementation.

No candidate imports/execution, package scripts, shell HTTP fallback, audit/resolver commands, build, environment/PATH/lock change, payload acquisition, model/Ollama API call, worker or application implementation. Inline stdlib/PowerShell accounting and metadata/documentation handling only; no skill scripts or subagents.

## Accounting, limits and stops

Fresh ignored root **`data/t17/hub-metadata-dependency-review-01/`**; refuse if present. Earlier allocations remain closed and unchanged. The first execution invocation only creates the fresh root and durably flushes exclusive-create initial accounting/approval/reporting/failure reservations; no optional skill/source/history read precedes bootstrap.

Reuse the proved immutable record chain: literal contiguous names, exclusive-create/Flush(true), strict schema/epoch/fixed ceilings, parent-byte SHA and nondecreasing counters, terminal refusal. No File.Replace/mutable pointer/overwrite/gap filling or invalid-tail skipping. At most **32 ledger records and32 validations,4KiB/record**. Keep immutable failure evidence and no refunds/resets. Hash linkage is workflow integrity evidence, not tamper-proof storage against the local user.

Verify runtime-compatible UTF-8 counting, normal/boundary/Unicode/string/object/oversized handling before source calls. Admit public text only within **256KiB per response** and the shared artifact cap; retain it before measured metadata/explicit excerpts. Do not assume TextEncoder/Buffer/Node globals. Prepay controller/source/handling/error allowances before invocations; capture both stdout/stderr. Statically parse the exact final PowerShell command, retain its identity and run that same text without AST execution or policy bypass.

| Resource | Proposed ceiling / allocation |
| --- | --- |
| Work | **64 prepaid units**: bootstrap/controls8; research28; decision/docs8; verification4; protected closure16. Normal48; all wrappers/controls/failures/research/report/cleanup share it. |
| Active time | **1,200 seconds**, including research, corrections, documentation/checks/closeout. Separately approved Git actions remain separate. |
| Local reads | **16MiB total**:4MiB conservative ledger validation plus12MiB precharged small-file/public-evidence/documentation reads, including repeat hashes/diffs/authoring reads. No runtime/archive/wheel/tokenizer/model payload reads. |
| Artifacts | **4MiB total upper bound**, including public text, all ledgers/receipts/partial writes, captures/diffs and authored output/status edits. Per-response256KiB is within this total; state the conservative accounting basis. |
| Reporting | **8KiB/invocation /64KiB aggregate**, retaining **8KiB for closure** and prepaid failure margin. Prefer at most3KiB per research-call reservation; safely withhold larger text. Provider response envelopes are not claimed locally byte- or kernel-bounded. |
| Research | **12 calls /36 targets /20 names**, as above; failures count. These larger research/read/artifact allowances support a broader dependency graph than AR, not more candidate execution. |
| Trials | **Zero** suites/Ruff/inspection workers/candidate imports/model/API/native trials. Only described inline controls, static parsing and documentation checks. |

At most two corrections to authored orchestration are covered if accounting/capture/output boundaries remain trustworthy; retain failed attempts within the same budget and do not refetch a failed target. Expected source-access failures and safely withheld text are recorded results.

Stop optional research at any cap/deadline/record limit, host denial, unsafe input, identity conflict, actual output-bound failure, loss of trustworthy accounting/capture or uncertain exposure/process ownership. A graph ceiling, missing artifact identity, licence conflict or incompatible requirement yields a partial/blocked readiness entry; do not broaden scope or represent it as cleared. Protected capacity is only for findings/cleanup/closure. Verify any unexpected owned-process teardown; never reopen/reset a stopped epoch.

## Deliverables and approval

After execution approval: `docs/benchmarks/hub-metadata-dependency-review.md`, affected dependencies/preflight and PLAN/TODO/README/checkpoint, plus ignored graph/artifact/source/control/preservation/accounting/closure receipts. Preserve existing report text and entry baselines, distinguishing authorized result edits from frozen files. No new executable aid, ADR adoption, SPEC/AGENTS edit or dependency/lock change.

MR4 must give one concrete recommendation: ready to **prepare** an exact later provisioning/inspection proposal, needs a specified dependency/constraint decision, or incomplete/blocked with precise remaining evidence. Exact installation/native/parity execution and runtime adoption remain separate packages/decisions. Carry build-source mapping explicitly into adoption; this review does not resolve or permanently waive it.

Request approval for **MR1–MR4 under these exact limits**, plus a separate commit of this proposal and PLAN/TODO/README/checkpoint (**five files**). Stage1 PDF/XLSX/CSV, OCR/privacy,16GB CPU-only target and G2/stage-transition gates remain unchanged.
