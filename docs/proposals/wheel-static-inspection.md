# T17-IF-WI — bounded wheel acquisition and static inspection

## Status and purpose

**Proposed; WI1–WI5 execution and the four planning-document commit await approval.** Seven GC/rule changes are committed as `90a01de`. The user authorized this proposal's preparation, not its probe, helper implementation or downloads.

Inspect exact artifacts as inert bytes to resolve [MR](../benchmarks/hub-metadata-dependency-review.md)/[GC](../benchmarks/hub-dependency-gap-closure.md) requirements, notice and native-inventory gaps. This is evaluation tooling, not application implementation, installation or runtime adoption. Build-source mapping remains an explicit adoption item under the unchanged metadata-only timing deferral.

## Fixed acquisition allowlist

Eight new wheels only; no version substitution. First-six sizes are existing registry declarations, not downloaded verification. Last-two sizes are rounded. Fresh release metadata must provide a positive exact integer byte count within the cap before any binary request; six known sizes must also match. Missing/ambiguous/mismatched/yanked entries stop acquisition, never a guessed URL.

| Filename | Existing size evidence | Wheel body cap | Fixed expected SHA-256 |
| --- | --- | --- | --- |
| httpx2-2.16.2-py3-none-any.whl | 97893 exact | 256KiB | `f05c13aade4c45dbf1c9060647a1058f0acad62398fad96e741269edb33d46f5` |
| httpcore2-2.16.2-py3-none-any.whl | 85551 exact | 256KiB | `16051ae2a42f776007543f32de9349a317b23d2cbb4e1456b4bac0e88b87419a` |
| anyio-4.16.0-py3-none-any.whl | 134521 exact | 256KiB | `c66ae634e0b8228396b801741beb3294326d4b6102f7bba4041c0dfb58c29026` |
| click-8.5.1-py3-none-any.whl | 126163 exact | 256KiB | `8bb5376d2006950386f8c6427613334a2acadc5f559cb80e638d00b4df957e37` |
| filelock-4.2.10-py3-none-any.whl | 218040 exact | 256KiB | `9479aaeb4db20b5a53e3da28493edd24720b66b8a0b84030aa56ccdf243d6857` |
| truststore-0.10.5-py3-none-any.whl | 19017 exact | 256KiB | `9aaaedaefaf06d8b206278cf8b5012bc897f485a874503501e12d776df78951c` |
| hf_xet-1.8.0-cp38-abi3-win_amd64.whl | 3.9MB rounded; exact bytes pending | 8MiB | `92188598dedc1e1f5609bd718d4db8687a6c89915553912571e2f587892eecec` |
| fsspec-2026.9.0-py3-none-any.whl | 221.7kB rounded; exact bytes pending | 1MiB | `8dd6e646e99ea382bd85f97a45e6b526a442d79423a7dc673f1e2756d05fcb5f` |

FSSpec's missing Trusted Publishing/provenance metadata is an explicit limitation. Approval here accepts publisher-listed checksum identity for **non-executing acquisition/inspection only**, not independently verified origin, licence clearance or adoption. Rounded sizes are not exact bytes; caps are proposed resource limits.

Two existing cached roots may be read without reacquisition:

- `data/t17/input-fit-tokenizer-static-01/huggingface_hub-2.4.0-py3-none-any.whl`: 857,021 bytes/SHA `42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801`.
- `data/t17/input-fit-tokenizer-static-01/tokenizers-0.23.3-cp310-abi3-win_amd64.whl`: 2,872,101 bytes/SHA `1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3`.

Verify regular-file identity/size/SHA before ZIP access. Reuse cached roots' prior full RECORD evidence; do not rehash every member again. Do not read the large Ollama archive/runtime, model weights, global installations or user documents.

## Ordered tasks

| ID | Objective / prerequisites | Acceptance / evidence | Status |
| --- | --- | --- | --- |
| WI1 | After approval, bootstrap, review design/trust boundary and probe native metadata access early | Accounting before optional reads; freeze inputs/controls; one owned fixed metadata request succeeds or stops before substantial helper work. | Pending approval |
| WI2 | After successful WI1, implement two aids test-first | Expected RED, minimal implementation, abuse/regression cases, caught integrity mutation, final lint/format and code/security review. No candidate imports or real network in suites. | Pending WI1 |
| WI3 | After WI2 passes, one acquisition attempt | Exact admitted registry entries/URLs, at most eight once-only wheel acquisitions, streamed SHA/size checks and verified exit/teardown; no inspection on failure. | Pending WI2 |
| WI4 | After coherent WI3, one static inspection attempt | Bounded new-wheel RECORD/metadata/notice/native results, cached-root text comparison and verified teardown; no candidate code loading. | Pending WI3 |
| WI5 | At completion/stop/cutoff, close | Concise readiness/gaps/resource/process evidence; frozen/history/scope/touched-link/whitespace/readable-diff checks; validated non-null summary; task/report updates and separate commit request. | Pending completion / stop |

WI1 is a fixed read-only connectivity spike; WI2 is test-first helper implementation. The package includes routine covered edits/tests/reviews, not an architecture/runtime selection. Significant scope or guard changes need a new decision.

## Probe and acquisition boundary

Use existing `F:/Python/Python314/python.exe -I -S -B` and stdlib only; no interpreter/package installation. One directly owned metadata probe requests only `https://pypi.org/pypi/httpx2/2.16.2/json`, at most1MiB, timeout30seconds plus15seconds teardown. Author/review its inline source after bootstrap and retain source/hash/result as evaluation evidence. If native access, TLS, ownership or JSON checks fail, stop before WI2. Reuse a successful response; no repeated probe.

Host permission prompts are separate from package approval. Request the required native-network boundary before the first started request. A denial stops work; no proxy/firewall/global configuration change, insecure TLS or alternate transport. Earlier native-network restrictions are not presumed fixed.

Acquire metadata through version-specific `https://pypi.org/pypi/<distribution>/<version>/json`. Select exactly one wheel with expected filename/SHA/non-yanked status and admitted exact size. Freeze the resulting manifest before payload requests. File URLs must come from those admitted entries. [Official release JSON API](https://docs.pypi.org/api/json/).

Allow only HTTPS443 `pypi.org` metadata and `files.pythonhosted.org` listed payloads; reject userinfo/query/fragment and redirects. Validate all IPv4/IPv6 DNS results as public, reject mixed/private/reserved results, and bind connections to a validated address with origin Host/SNI and normal certificate verification. One connection attempt; no address fallback/retry. No ambient proxy credentials, cookies or authentication. Send public package identifiers only, never private content/paths/secrets.

Maximum16 HTTP transactions: eight metadata requests including the reused probe, plus eight wheel requests. Failures count, no range resume/redirect request. Require200; reject unexpected content encoding. Bound metadata1MiB/response and headers64KiB. Count HTTP status/header/body reads; DNS/TLS/kernel overhead is not claimed inside that counter. Validate duplicate JSON keys, shapes/lengths and exact admitted fields.

Stream to exclusive owned `.part` files and hash while writing. Verify exact admitted size and fixed SHA before marking usable. Retain invalid/partial bytes as unusable within disk limits. No extraction, installer, package manager, setup script, entry point, macro or candidate import; no automatically fetched newly discovered dependency.

## Authored aids and ZIP inspection

Only two new versioned code files: `tests/evals/spikes/wheel_static_inspection.py` and `tests/evals/spikes/test_wheel_static_inspection.py`. Fixtures/requests/logs/artifacts stay in the fresh ignored root. Never run old tests/workers/writers into closed roots.

Explicitly permit reuse only of `Failure`, `Limits`, `ReadBudget`, `open_regular`, `ChargedFile`, `central_admission`, `admitted_entries`, `digest_stream`, `hash_regular` from reviewed owned `standalone_static_verification.py`,21,836bytes/SHA `691d86c9cc750a2f88b266230e0938936d92ce54c3b5f21684bd3a080fcd6d03`. Review/freeze before use; execute the same verified owned bytes, not a mutable replacement. No old entry points/root/default changes or model-specific downloader reuse. Downloaded code is never compiled/imported.

Before ZipFile entry-list allocation, admit bounded central-directory/counts and reject traversal/drive/ADS/aliases, links/reparse/hardlinks, overlapping/inconsistent layouts, encryption and unsupported compression/ZIP64/multidisk cases. Stored/deflated only. New wheels512entries each; cached Hub256/Tokenizers128 retain existing limits. Aggregate4096entries, central directory256KiB/wheel,64MiB expanded/wheel and128MiB expanded/batch. Stream CRC/hash/size verification. A limit refusal is not proof of a defective artifact.

New wheels: verify required RECORD entries/hashes/sizes, normalized name/version, WHEEL tags and declaration differences. Handle the RECORD self-entry and legacy signature-sidecar exceptions explicitly; inventory deprecated signatures without claiming verification. For core metadata>=2.4, check declared License-File locations. [Official wheel format](https://packaging.python.org/en/latest/specifications/binary-distribution-format/).

Bound METADATA/RECORD256KiB each, other metadata64KiB/file, notices256KiB/file/4MiB total; strict decoding, explicit missing/over-cap results. Inventory native suffixes and hooks/scripts without executing. Inventory/licence declarations do not establish bundled-native compliance, ABI safety or complete security.

Cached source-as-data reads, if present, are limited to `huggingface_hub/constants.py`, `tokenizers/__init__.py`, `tokenizers/__init__.pyi`, `tokenizers/tokenizers.pyi`,128KiB/file/512KiB total. Compare offline/local-asset declarations as intent only; do not follow embedded URLs or claim actual offline behavior. Missing members stay unavailable; no outside source search.

## Supervision, controls and shared limits

Fresh ignored root **`data/t17/wheel-static-inspection-01/`**; refuse if present. Bootstrap alone precedes optional skills/source/history reads. Parent is sole global-meter writer and prepays non-refundable suite/probe/worker leases; child local counters/receipts stay within them. No racing/reset/adapter-only accounting.

Bind tested owned helper bytes before worker action; never re-open changed source unchecked after hashing. Retain PID/birth/kernel handles. Verify kill-on-close Windows Job/startup gating before payload work; stop on lost ownership/uncertain teardown. Probe uses direct ownership/timeout/wait evidence. This is not filesystem/kernel-egress confinement. No worker descendants, GUI/service/port. Acquisition worker once:180s+30s teardown; inspector once:120s+30s teardown, sequential. Monitor total owned private memory against512MiB; state sampling/kernel coverage, not a physical16GB benchmark.

Synthetic tests use mocked transport only: golden manifests, altered bytes/size/name/version, duplicate metadata/RECORD, malformed CRC/paths/admission, 513-entry early refusal, read/expansion caps, public/private/mixed DNS, TLS/redirect/credential refusal, partial transfers, root confinement and inert import/launch/hook traps. Catch an in-memory integrity-guard mutation. No real negative-control network or frozen-source mutation.

| Resource | Proposed ceiling / allocation |
| --- | --- |
| Work | 128 prepaid units: bootstrap/probe 16; aids/tests 48; acquisition 16; inspection 16; findings/checks 16; protected closure 16. Normal allocation 112, no refunds/resets; all wrappers/failures/controls share it. |
| Time | 2,400 seconds total. Start probe by 360 seconds, acquisition by 1,200 seconds, inspector by 1,440 seconds. Stop optional work at 1,800 seconds; 600 seconds reserved for closure, interim findings before cutoff. |
| Processes | 64 owned starts including controllers, probe, test/negative/regression interpreters, Ruff, workers and read-only Git; one probe, one acquisition worker, one inspector. Separately approved commits remain separate. |
| Checks | At most 8 suite and 8 Ruff invocations including RED/mutation/negative/final checks. Reserve final validation before refinements. |
| HTTP bytes | 24 MiB status/header/body total; 16 transactions, per-response caps above. |
| Streamed reads | 512 MiB total including HTTP/disk/ZIP/member/hash/source/fixture/closure; 16 MiB ledger preallocation and 16 MiB per suite, within this cap. |
| Retained artifacts | 48 MiB total including all wheels/partials, metadata, fixtures, notice copies, logs/receipts and authored outputs; no disk extraction. |
| Ledger/report | 64 immutable records/64 validations, 4 KiB each; 8 KiB/report invocation, 128 KiB aggregate with 16 KiB closure reserve/prepaid failure margin. Capture both streams; non-null summary. |

At most two trustworthy orchestration corrections within the same limits; retain failures, no candidate refetch. Stop optional work on phase/cap/host denial, unsafe input, identity mismatch, actual output violation, lost accounting/capture or uncertain ownership. A started transport failure stops the attempt; no reset/bypass. If short on time, save truthful minimal findings/unfinished checks before polishing.

## Deliverables and approval

After approval: two aids, `docs/benchmarks/wheel-static-inspection.md`, affected dependency/preflight and PLAN/TODO/README updates, ignored probe/manifests/artifacts/control/teardown/accounting records. Keep statuses concise/in place; **no session-checkpoint files**. No pyproject/lock/PATH/global install, model/Ollama call, product implementation or stage transition.

Request **WI1–WI5 approval**, including native probe, eight checksum-bound acquisitions with rounded-size/FSSpec trust limitations, static reads and all budgets above; separately approve this proposal plus PLAN/TODO/README commit (**four files**). One approval covers covered routine steps, not later results commits, installation/import/native parity, adoption or G2.

Preparation consulted four official format/API targets for RECORD/signature/licence-file and release-JSON rules. No WI root/helper/fixture/probe/acquisition exists. Local planning/documentation/security workflows informed this proposal; no skill scripts/subagents.
