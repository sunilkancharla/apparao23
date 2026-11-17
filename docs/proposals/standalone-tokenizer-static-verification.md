# T17-IF-SA — existing runtime artifacts and standalone dependency review

## Status and scope

Proposed; execution and five-document proposal commit await approval. [SV findings](../benchmarks/standalone-tokenizer-validation-design.md) and the [conditional trial design](standalone-tokenizer-parity-trial-design.md) are committed as `8d25bd7`. User approved preparing this package. Standalone direction C is approved conditionally; no software/runtime adoption follows.

Perform static verification only: compare the already cached Ollama archive with its project installation, identify the exact native runner/DLL/license inventory, and review outstanding standalone dependency/native/source-release gaps. No candidate executable, DLL, tokenizer or downloaded code is loaded or executed. No native API/model call, installation, extraction to disk, build, payload acquisition, environment/PATH change or dependency/lockfile modification.

## Exact permitted inputs

| Input | Identity / permitted access |
|---|---|
| Cached archive |`.venv/.cache/ollama/ollama-windows-amd64-0.40.16.zip`,1,618,244,995bytes, SHA256`50fcf5ad54277f2fa5d173ebfc93bcb017adbc0c9ef2314daabc96ca9e6aa64e`, copied from existing provisioning definition; verify before member reads |
| Installed runtime |Read-only `.venv/tools/ollama/0.40.16/` only; existing ollama.exe SHA256`4ccefcbfecc50fb6526471adabbc20869dd614e29e351120b15083cb174b0b8a`; compare every selected regular file with same archive member |
| Earlier provisioning evidence |Read sanitized `data/t10/run-01/installation.json`, `archive-inspection.json`, `native-notices.json` and authored embeddings/provisioning definitions as data/design references; do not execute old helpers or inspect raw logs/state |
| Standalone wheels |Only IF-N's two already verified Tokenizers0.23.3 and Hub2.4.0 wheel payloads identified in its manifest/receipts, after recorded exact hash/size checks; read ZIP metadata, METADATA/RECORD and bounded license/notice texts, never import/extract/install |
| Existing tokenizer/model metadata |Preservation hashes and committed findings only; no new payload parsing, weights/GGUF read, tokenizer instantiation or model-store inspection |

Absent or mismatched archive/installation/wheel identity stops optional work; no redownload, repair, deletion or alternate installation location. Do not enumerate user/global Ollama installations. The installed path and ZIP expectation come from earlier authored provisioning records, not a new discovery claim.

## Ordered tasks and acceptance

| ID | Objective / prerequisite | Acceptance / verification | Status |
|---|---|---|---|
| IF-SA1 |After approval, bootstrap/freeze inputs |UTC clock/full accounting/research/report reservations before inspection/output; immutable old identities plus fixed input paths; absent fresh root |Pending approval |
| IF-SA2 |After SA1, test-first static inspector |Meaningful red/green and caught admission/integrity mutation; archive/path/type/read/report boundaries, no candidate execution; final lint/format |Pending SA1 |
| IF-SA3 |After SA2, one owned static worker |Exact archive/member/installed comparisons, runner/DLL/notices manifest or honest partial stop; owned exit/reap verified, no extraction/import/launch |Pending SA2 |
| IF-SA4 |Only after coherent SA3 result, public dependency/provenance review |Applicable graph, native notice/advisory/source-release/offline gaps explicitly verified/unknown/blocked, exact candidate artifact metadata distinguished from approval |Pending SA3 |
| IF-SA5 |After SA3 stop or SA4, close |Findings/preservation/link/diff/limits/checkpoint; installation/trial readiness verdict and next decision, separate findings commit |Pending SA3/SA4 |

Possible new authored files only: `tests/evals/spikes/standalone_static_verification.py` and `test_standalone_static_verification.py`. Use verified local incremental/test-driven/security/review/documentation workflows; no skill scripts/subagents. Old aids are read-only design references, not imported or run. Application code remains gated.

## Static inspection and trust boundaries

Use isolated stdlib Python for the authored inspector. Reject archive traversal/absolute/drive/ADS paths, duplicate or case-colliding destinations, symlinks/reparse/hardlink surprises and out-of-root paths before member comparison. Bound metadata/count/depth, stream hashing and decompression; never trust declared size alone. Check regular-file identity/size before/open/after with the reviewed Windows same-API timestamp policy; do not reintroduce the known cross-API ctime equality error. Record named failure fields, not arbitrary error messages or private paths. Do not load PE/DLL code or execute archive scripts. Static DLL names do not prove which libraries a later loader will resolve.

At most128archive entries and128installed regular files, depth8; at most3GiB declared/actual aggregate expanded archive bytes,256KiB central-directory metadata, and **8GiB cumulative streamed payload bytes** across archive hashing, decompression and installed-file hashing, including overflow probes/failed reads. No whole-file memory buffering. Bounded text notices256KiB/file/1MiBaggregate; record remaining licenses as unreviewed rather than truncating silently. No output member extraction/copies. Input binaries/ZIP pre-exist and do not count as newly written artifacts; every receipt/partial/journal does.

Tests use small authored synthetic ZIP/installed-tree bytes only: malformed/path/case/duplicate/member-size/CRC/hash/type/identity mutations, missing inputs, interrupted/over-cap reads, filename/notice output sanitization and no candidate import/launch. Include negative/control/mutation work in the same budget. Up to **six focused suite invocations/four Ruff invocations**, reserve final checks before refinements. A synthetic executable-looking file is inert test data, never launched.

One supervised authored stdlib worker, maximum600seconds plus30seconds teardown, retained PID/birth/Process handle and captured bounded stdout/stderr. No child candidate/service or parallel workers. Same-user static-read boundary, no filesystem/outbound confinement or kernel RAM-cap claim. Verify process exit/reap even on partial failure; no automatic rerun/retry or old-root reuse.

## Conditional dependency and provenance review

At most **eight web calls/twenty-four targets**, maxfour/call, short/medium, public primary-source/registry text metadata only. Precharge before every call; failed/cache-miss requests count. No binary/wheel/archive/model download, registry resolver/audit execution or raw HTTP fallback. Root versions remain Tokenizers0.23.3/publishing commit`301277072263fb3830eb66eec7e47adadf76f1dc` and Hub2.4.0/publishing commit`178e1a1797858724c79fd9d12d79d0902d730497`; Ollama v0.40.16 and native b12177/fullcommit plus compatibility overlays unchanged.

Start from actual verified wheel METADATA. Maximum20distinct applicable runtime distribution names including roots; excluded extras/Python<3.11-only tomli stay excluded. Include applicable hf-xet/native and distinguish httpx2 from installed HTTPX. Identify exact versions/artifact tags/hash/size where public evidence permits; unresolved candidates stay unselected. Do not claim graph closure at the ceiling. Review source/wheel licensing and missing native notices, known advisory/fix applicability, Windows/Python compatibility, offline/cache/telemetry controls, and Hub source.dev0 versus wheel2.4.0 release mapping. No absence-of-advisory security guarantee or automatic substitutions/upgrades.

Keep local archive identity, member equality, publisher attestation, source-to-release provenance and runtime compatibility separate. Stop expansion on a necessary unresolved/mismatched provenance link; return the exact blocker and next decision. No installed binary launch to obtain version/help; no custom-build fallback. A partial static inventory can be useful evidence without permission to install or run it.

## Shared accounting and stop boundary

Fresh ignored `data/t17/standalone-static-verification-01/`, refuse if present. **128prepaid units:104normal/24protected**: initialization8, inspector/tests40, static worker16, public review16, design/report/closeout24, protected24. Include shells/wrappers/interpreters/worker/test/negative/mutation/Ruff/HTTP/report/cleanup in these shared ceilings, no refunds/resets. Separately approved Git actions outside epoch. **2,400active seconds/8MiB newly written artifacts**, with separate read/HTTP/report caps above. Do not copy2GBinputs into the new root.

First invocation exclusively creates/flushed accounting/reporting records before optional inspection/output. DateTimeOffset UTC, explicit scalars/ReadAllText, simple literal quoting. **8KiB/invocation64KiBaggregate controlled stdout with8KiBclosure reserve**, measured/precharged including newline, bootstrap/Git/error allowance recorded. Capture native command warnings/stderr and emit summaries; save readable diffs locally instead of nested-quote display commands. Web/provider envelopes are opaque, separately bounded by call/target/settings; record unexpected output/deviations honestly.

Preserve AGENTS/SPEC/pyproject/lock; frozen IF-L comparison/parity/integration comparison, IF-N/O/P aid/test pairs and findings, IF-Q/QC/SV findings and staged trial design, every linked old final meter/closeout/preservation/research record, IF-N pending/stopped meter and IF-P combined manifest. Reverify direct identities at closure, retain transitive links without rerunning older tests/trials. New fixed input hashes checked once at entry, streamed comparison hashes retained; do not silently exceed read budget by rehashing large inputs during closeout.

Stop optional work at cap/deadline, host denial, unexpected I/O/report failure, unsafe path/archive, identity/provenance conflict or uncertain teardown. Protected capacity only for partial closeout/teardown, no more research/tests. No reset/retry/reseal of any closed run. Preserve partial artifacts/content-free diagnostics. No secure-erasure, native safety or offline/runtime capability claim from static hashes.

## Deliverables and approval

After approval: the two reviewed aids, `docs/benchmarks/standalone-tokenizer-static-verification.md`, local static/research/preservation/teardown/accounting manifests, and affected dependencies/preflight/PLAN/TODO/README/checkpoint. Trial design and frozen prior reports stay unchanged; new readiness notes go in current findings. No installation/trial/adoption or G2/app/stage approval. Same16GB CPU-only/formats/OCR/privacy/provisional context/output/R01/chart deferral.

Requested: approve IF-SA1–SA5 including this exact read-only artifact inspection, bounded test-first aid and public metadata review, and separately commit this proposal plus PLAN/TODO/README/checkpoint (five files). Routine package steps need no repeated approval. Later source/findings commits, provisioning/native trial/runtime adoption retain explicit gates.

## Approval update

The user explicitly approved IF-SA1–SA5 and the five planning-document commit. Execution encountered a bootstrap/reporting-order stop before artifact inspection, tests or research; closure evidence is recorded separately. Earlier pending-approval wording describes the proposal state.
