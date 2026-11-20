# T17-IF-HS — bounded Hub-only static continuation

## Status and purpose

**Proposed; execution and the five planning-document commit await approval.** The user approved committing the nine IF-SA results and preparing this proposal. Results are committed as `2ad9cb1`; [findings](../benchmarks/standalone-tokenizer-static-verification.md) retain the partial stop and reporting deviation.

Inspect only the existing Hub wheel that exceeded IF-SA's 128-entry cap, then conditionally review remaining public dependency/provenance questions. Propose **256 entries for this wheel only**. The old runtime/archive limits and stopped epochs remain unchanged. Do not repeat the already completed 1.6 GB Ollama archive/75-file comparison.

This package permits authored stdlib inspection aids, synthetic tests, one owned static worker and bounded public text research. It permits no candidate import/execution, installation, payload download, archive extraction to disk, model access/inference/API call, build, environment/PATH/lockfile modification, application implementation or G2 adoption.

## Fixed inputs and code reuse

| Input | Exact identity / permitted use |
| --- | --- |
| Existing Hub wheel | `data/t17/input-fit-tokenizer-static-01/huggingface_hub-2.4.0-py3-none-any.whl`; 857,021 bytes; SHA-256 `42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801`. Verify regular-file identity, size and hash before ZIP/member reads. No redownload or alternate payload. |
| Reviewed authored inspection module | `tests/evals/spikes/standalone_static_verification.py`; SHA-256 `691d86c9cc750a2f88b266230e0938936d92ce54c3b5f21684bd3a080fcd6d03`, committed in `2ad9cb1`. Read/reuse only its owned stdlib admission/hash primitives after identity verification. |
| Existing evidence | IF-SA epoch 03 input/preservation/result/verification/teardown/delivery/closeout/deviation records and earlier linked preservation records, as data. Tokenizers' verified metadata/findings may inform research; no Tokenizers payload reread. |
| Public source roots | Hub 2.4.0 publishing commit `178e1a1797858724c79fd9d12d79d0902d730497`; Tokenizers 0.23.3 publishing commit `301277072263fb3830eb66eec7e47adadf76f1dc`. These are research coordinates, not established reproducible build provenance. |

Only two new authored code files are allowed: `tests/evals/spikes/hub_static_review.py` and `tests/evals/spikes/test_hub_static_review.py`. Preserve the older inspector/test bytes and their Git history. Do not run the old test script: its fixture directory points into closed epoch 03.

The new aid may reuse `Failure`, `Limits`, `ReadBudget`, `open_regular`, `ChargedFile`, `central_admission`, `admitted_entries`, `digest_stream` and `hash_regular` from the exact owned module. Verify and bind the imported source bytes/identity; do not execute a mutable replacement after hashing. This is explicit permission to execute reviewed, locally authored stdlib helper code, **not** downloaded Hub/Tokenizers code. Never call the old `worker` or `durable_json`, change its `RUN`, or write into old roots. The new aid supplies its own Hub-only metadata/RECORD/notice reader, accounting and fresh-root receipts.

Missing/mismatched inputs or an unsafe path stop optional work. Do not repair, replace, fetch or search user/global installations.

## Ordered tasks

| ID | Objective and prerequisites | Acceptance / evidence | Status |
| --- | --- | --- | --- |
| HS1 | After exact package approval, bootstrap a fresh epoch | First invocation only creates/flushed accounting/approval/report reservations before optional reads; demonstrate measured normal/oversized output gate; freeze prior identities and exact allowed inputs. | Pending approval |
| HS2 | After HS1, implement the two new aids test-first | Expected RED, smallest passing implementation, integrity/admission mutation detected, final focused tests plus lint/format checks. Synthetic fixtures stay in the new root; all cases share package budgets. | Pending HS1 |
| HS3 | After HS2, perform one supervised static attempt | Hub exact identity, admitted ZIP structure, all RECORD hashes/sizes, metadata and bounded notice/native-name inventory; otherwise a content-free partial-stop receipt. Owned exit/wait/handle teardown verified. | Pending HS2 |
| HS4 | Only after a coherent HS3 result with no stop, review public metadata | Applicable dependency/source-release/native-license/advisory/offline gaps classified verified/unknown/blocked. Versions/artifacts remain proposals. Stop expansion on a necessary unresolved provenance conflict. | Pending HS3 |
| HS5 | After HS3 stop or HS4, close and hand off | Recheck frozen small identities; capture readable diff, links/scope/privacy/resource evidence and checkpoint. Give an installation/trial readiness decision without adoption. Findings/source commit is separate. | Pending HS3/HS4 |

Checkpoints: review synthetic controls before real payload reads; review the single worker result before research; close with evidence and a Git approval gate. No subagents or skill scripts. Reuse the relevant manually reviewed incremental/TDD/security/review/documentation workflows.

## ZIP, file and output boundaries

- Hub-only entry limit **256**, including directories; depth 8; central-directory metadata 256 KiB; declared and actual aggregate expanded bytes 16 MiB. Reject ZIP64/multidisk layouts not admitted by the reviewed reader, traversal/drive/ADS paths, aliases/collisions, links/reparse/hardlinks, unsafe types, encrypted/unsupported members and inconsistent sizes/CRC/RECORD. Bound the central directory before allocating its entry list. A 257-entry synthetic case must refuse before member parsing.
- No whole-wheel buffering or extraction. Stream hash compressed/member bytes, counting both against the shared read cap; precharge requests including failed/short/probe reads. Retain repeated same-API path/handle identity checks. Static inventory does not prove loader resolution or native safety.
- Read only METADATA, RECORD and license/notice/copyright text after exact wheel identity and member admission; hash other members as inert bytes for RECORD checks. Text cap 256 KiB/file, 1 MiB aggregate; metadata/RECORD 256 KiB each. Mark over-cap/unreadable notices unreviewed rather than silently truncating. Display no arbitrary filenames, notice bodies or error paths in summaries.
- All owned artifacts, temporary fixtures/logs/receipts/partial writes and source-output accounting share the artifact ceiling. Use explicit numeric accumulation; do not rely on PowerShell hashtable property measurement.
- Before each command/tool invocation, precharge a bounded capture and summary allowance. Capture **all** stdout/stderr, including Git warnings and failures. Measure UTF-8 bytes before emission through one output gate. Oversized results stay local or are refused with a measured scalar summary; never equate a token limit with a byte limit. Native/host/provider envelopes outside that gate are recorded honestly.

Synthetic controls must include 191-entry admission under 256, 257-entry refusal, unchanged 128-entry runtime defaults, unsafe/alias/type/identity cases, missing/mismatched wheel, RECORD omission/duplicate/hash/size failures, malformed/CRC/expansion/read/notice bounds, import/launch refusal, fresh-root confinement and proof that no old worker/test/root is used. Reserve final checks before refinements. No test may weaken historical controls merely to pass.

## One worker and conditional public review

Use isolated stdlib Python and one directly owned inspection worker, **120 seconds plus 30 seconds teardown**. Retain its PID/birth/handle until exit/wait is verified. Capture bounded stdout/stderr; no candidate child/service, parallel worker or automatic rerun. This is a same-user static-read process, not filesystem/outbound confinement or a kernel memory limit.

Public research: at most **8 web calls / 24 targets**, at most four targets/call, short/medium responses, public primary-source/registry text only. Precharge every attempt; failures/cache misses count. No binary/model/wheel downloads, raw HTTP fallback, resolver or audit-command execution.

Start from verified wheel METADATA. At most **20 distinct applicable runtime distribution names**, including roots. Distinguish `httpx2` from installed HTTPX; include applicable `hf-xet` native requirements; exclude unselected extras and Python<3.11-only `tomli`. Identify exact candidate versions/Windows tags/hash/size when evidence permits; do not claim closure at a ceiling or silently select replacements.

Review Hub source `.dev0` versus packaged 2.4.0 release mapping, source/wheel/native notices, advisory/fix applicability, Windows/Python compatibility and offline/cache/telemetry controls. Absence of a listed advisory is not a safety guarantee. A required unresolved provenance link stops further expansion and returns the exact blocker; no custom-build or runtime fallback.

## Shared package limits and stop conditions

Fresh ignored root **`data/t17/hub-only-static-review-01/`**, created only after approval; refuse if present. No old allocation is reopened.

| Resource | Proposed ceiling |
| --- | --- |
| Shared prepaid units | 128: initialization 8; aids/tests 40; static worker 16; research 16; findings/closure 24; protected closure 24. Normal total 104; no refunds/resets. |
| Active elapsed time | 2,400 seconds, including bootstrap, debugging, checks and closeout; separately approved Git actions remain separate. |
| Streamed reads | **128 MiB total**, covering wheel hashing/decompression, inherited small-file verification and failure/probe reads. Precharge **8 MiB per suite invocation**, including RED/mutation/negative cases, from this same total; at most 48 MiB goes to the six suites. This replaces the unnecessary 8 GiB allowance for this new package only. |
| New artifacts | 8 MiB upper bound, including authored outputs, fixtures, logs and receipts; report the counting basis and conservative margins. |
| Focused suites / Ruff | At most **6 suite invocations and 6 Ruff invocations**, including RED/mutation/negative controls and final regression/lint/format checks. The extra lint/format allowance is proposed explicitly to support routine corrections and final verification. |
| Controlled reporting | 8 KiB/invocation, 64 KiB aggregate; retain 8 KiB for closure. Precharge bootstrap/Git/error allowance and measure before emission. |

Include all shells/wrappers/interpreters/test/control/worker/research/report/cleanup in the shared allocation. No worker counter isolated from its regression/control suite. Freeze AGENTS/SPEC/pyproject/lock, prior comparison/parity/trial designs, the old inspector/test, prior final records and transitive preservation links. Recheck small identities at closure; do not rehash runtime binaries, the large archive, tokenizer assets or model files.

Stop optional work on any cap/deadline, host denial, identity/provenance conflict, unsafe input, unexpected I/O/report failure or uncertain teardown. Protected capacity is only for cleanup/partial findings; no more tests/research. Preserve stopped records and never retry/reset/reseal them automatically. No native/offline capability or secure-erasure claim follows from static hashes.

## Deliverables and approval request

After execution approval: the two new aids; `docs/benchmarks/hub-only-static-review.md`; local preservation/inspection/research/teardown/accounting records; affected dependency/preflight/PLAN/TODO/README/checkpoint updates. Frozen historical findings/designs stay unchanged. Existing Stage 1 formats/OCR/privacy, 16 GB CPU-only target, provisional context/output settings and G2/stage gates remain unchanged.

Requested: approve **HS1–HS5 with these exact changes and limits**, plus a separate commit of this proposal and PLAN/TODO/README/checkpoint (five files). Routine covered edits/checks do not need repeated approval. Later source/findings commits, any provisioning/native trial/runtime adoption and stage transition retain their separate gates.
