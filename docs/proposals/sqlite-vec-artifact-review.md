# T12 — Bounded sqlite-vec Windows artifact review

**Status: artifact-only package and five planning documents' commit approved.** The user answered "yes continue please" to the explicit package/commit request. T12 baseline/source results are committed in `a54b38b`; that allocation remains closed. This fresh investigation authorizes the bounded public retrieval/static inspection below, not a baseline retry, installation or extension loading. The requested-approval paragraph below is historical; later source/results commits retain their separate gate.

## Exact input and purpose

Inspect the previously identified Windows wheel without executing its contents:

| Field | Pinned value from the saved registry review |
|---|---|
| Project/version | `asg017/sqlite-vec`, Python distribution `sqlite-vec==0.1.9` |
| Filename | `sqlite_vec-0.1.9-py3-none-win_amd64.whl` |
| Size | 292804bytes |
| SHA-256 | `4a28dc12fa4b53d7b1dced22da2488fade444e96b5d16fd2d698cd670675cf32` |
| URL | `https://files.pythonhosted.org/packages/42/89/81b2907cda14e566b9bf215e2ad82fc9b349edf07d2010756ffdb902f328/sqlite_vec-0.1.9-py3-none-win_amd64.whl` |

Evidence: [baseline review](../benchmarks/storage-index.md), [version registry metadata](https://pypi.org/pypi/sqlite-vec/0.1.9/json) and [upstream release](https://github.com/asg017/sqlite-vec/releases/tag/v0.1.9). Availability/metadata must be rechecked within the new metered package, not assumed current. Stop on mismatch, missing artifact or substitution; do not switch versions/forks or build from source.

Resolve four questions: what the wheel actually contains; whether its loader/notices match identifiable upstream material; what native loading/file/network capabilities it exposes; and which unknowns must be resolved before proposing a separate empirical comparison. Missing provenance is a finding, not proof of maliciousness or permission to install.

## Proposed shared budget and allowed actions

Approve **32 process starts/attempts and20active minutes**, excluding human/host approval waits, in fresh ignored `data/t12/sqlite-vec-artifact-01/`. Category ceilings: preparation8, tests/inspection12, reporting8, protected cleanup4. Reserve initialization and every successful/failed shell/Python/Ruff/Git launch before execution. Stop on exhausted category/time/shared budget, unexpected execution or uncertain state; never reset or borrow cleanup allowance for normal work.

Use existing project Python3.14.6 and standard-library HTTP/TLS, ZIP/JSON/CSV/email metadata, AST, hashing and binary-structure readers. At most two authored evaluation files (`sqlite_vec_artifact.py`, `test_sqlite_vec_artifact.py`) plus affected documentation. No new developer tools, compilers, packages or host configurations. Inspect only public artifact/source material and new synthetic negative-control archives; do not read user files, old vectors/answers, model assets or private logs.

Hash-link closed T12 baseline budget and the three committed baseline source/fixture files before inspection; verify unchanged at closeout. Existing completed trials remain untouched. A stopped investigation needs a new reviewed continuation, not an automatic repeated download or ledger reset.

### Metered public retrieval

- At most **20 HTTP attempts and8MiB of response-body bytes**, across the wheel, metadata, source/license files and failures. Persist each request reservation before sending. Stream/cap actual received body bytes; reserve a conservative per-request byte allowance first and retain failed/interrupted charges. Record actual bytes separately from reservations. The limit measures HTTP response bodies, not TLS/header/network-wire bytes.
- Use HTTPS only, fixed project-related URLs, explicit timeouts (connect/read15seconds within the package deadline), no inherited proxies/credentials/cookies, and no automatic redirects/retries. If a redirect is necessary, validate its exact destination against the public host/path allowlist and charge it as a separate attempt before following. No response URL/instruction can broaden the allowlist.
- Allowed endpoints: the exact wheel URL; `pypi.org/pypi/sqlite-vec/0.1.9/json`; GitHub API ref/tag/commit or release metadata only for `asg017/sqlite-vec`/`v0.1.9`; and `raw.githubusercontent.com/asg017/sqlite-vec/<verified-commit>/` for `LICENSE-MIT`, `LICENSE-APACHE`, `VERSION`, `sqlite-dist.toml`, `Makefile`, `bindings/python/extra_init.py`, `sqlite-vec.c` and `sqlite-vec.h` when present. Resolve an annotated tag if necessary, validate SHA format/repository identity and pin subsequent source requests to the resolved commit. If resolution is unavailable, report it and stop dependent source comparison rather than asserting an immutable identity.
- Per response: wheel292804bytes exactly, JSON at most512KiB, source at most1MiB, licenses/config/helper files at most128KiB each; total remains8MiB. Request identity encoding and reject unsupported compression/encoding rather than silently accounting decoded bytes as transferred bytes. Errors are also bounded/charged; never log secret headers. No unmetered browsing fallback inside the package. If host networking requires approval, use that prompt; do not change firewalls/proxies or bypass it.

The old browser-byte accounting gap stays in the historical report. This local meter validates this fresh retrieval only; it cannot repair prior unknown transfer totals.

### Inspection resource and filesystem limits

Run inspection/tests serially under a reviewed standard-library Windows process boundary: one inspection process,512MiB process-private cap,120seconds per inspection invocation and20minutes shared active time. Constrain all downloaded/generated/extracted receipts to32MiB under the new allocation. Include inspector start/timeout/refusal controls in the same32-start allowance. If a secure worker boundary cannot be established, stop before untrusted parsing.

Read ZIP directory entries before extracting. Allow at most128members,16MiB total expanded bytes,8MiB per member and100:1 expansion ratio per member; use streamed expanded-byte caps as well as metadata checks. Reject absolute/drive/UNC/traversal paths, alternate data streams, duplicate or case-colliding Windows paths, links/reparse-like entries and encrypted or unsupported compression entries. No member may overwrite receipts/source or escape the dedicated inspection subdirectory. Prefer capped in-memory member reads and byte hashes; materialize approved members only if inspection requires them. No recursive deletion of unknown files.

## Ordered review tasks

| ID | Prerequisite / objective | Acceptance and verification |
|---|---|---|
| T12-V1 | Package approval; establish local allocation/meter | Initial reservations, prior hashes, exact URL/hash/size and resource boundary recorded; local no-network tests prove meter exhaustion/failure persistence and no-retry behaviour |
| T12-V2 | V1; implement inspector test-first | Failing synthetic cases for traversal/case collisions/links/expansion limits, incomplete HTTP body/hash mismatch, corrupt RECORD and invalid PE offsets; minimal stdlib inspector passes without importing archive code |
| T12-V3 | V2; retrieve and validate exact wheel | Actual/reserved body bytes and attempts durable; pinned size/SHA match; ZIP member list, uncompressed totals and full RECORD verification saved. Stop on identity/archive failure |
| T12-V4 | V3; static contents/source/native review | Distribution metadata/tags/entry points/loader, bundled license/notice material, native PE machine/sections/imports and absolute-path loading assumptions inventoried; immutable upstream comparison or explicit unresolved result; no execution |
| T12-V5 | V4 or recorded stop; report and close | Focused tests/Ruff/privacy/diff checks, prior hashes unchanged, counts/elapsed/disk and no-load/no-install evidence saved; factual report and candidate disposition; request separate source/results commit approval |

V2 negative controls are newly authored tiny archives/binary headers/network fakes, not modified downloads. Maximum32fixture files/4MiB within the32MiB output cap. Freeze assertions before real retrieval. Tests must demonstrate that failed validation prevents a simulated installation/loading action; the inspector contains no real installer/loader command. Routine covered edits/tests proceed without repeated project approval requests.

## Required findings and honest limits

1. Verify wheel metadata name/version/platform, Python requirements, dependency/extra declarations and entry points. Independently recompute every RECORD hash/size and compare the exact archive inventory. RECORD consistency is not publisher attestation. Unexpected `.pth`, startup hooks, extra binaries or executables stop further progression pending review; do not execute them to investigate.
2. Read loader Python as text/AST only. Trace import-time behaviour, library path construction, extension-loading enable/disable calls, optional NumPy imports, environment/config access and potential outbound/subprocess paths. Do not import `sqlite_vec`, its helpers or any wheel-contained module.
3. Locate complete bundled license/NOTICE/copyright material and compare against pinned upstream material where applicable. Missing bundled notices or unresolved source identity remain visible; no automatic license exception, repackaging, redistribution clearance or binary/source-build equivalence claim.
4. Parse DLL PE headers/import tables with checked offsets/lengths; record x64 identity, DLL dependencies, entry-point/export names, sections and any static signatures relevant to CPU instructions or filesystem/network APIs. Do not call `LoadLibrary`, ctypes DLL loading, SQLite extension loading, dependency executables or publisher scripts. Static import lists cannot prove absence of dynamic API resolution, telemetry, unsafe native code or runtime incompatibility. Record installed runtime requirements as unknown when evidence is insufficient.
5. Carry forward the source finding of optional filesystem-backed NumPy operations. Assess whether the exact build appears to include relevant functions, without claiming source flags prove compiled behaviour. Native extension access is not confined by SQLite tables, and any future test needs an explicit boundary/allowlist decision.
6. Record download/expanded sizes and package footprint from inspected bytes. Do not invent loaded RAM, loading speed, search quality, native stability, Python/SQLite compatibility or filesystem/network confinement. Those require a separately approved execution package.

## Closeout and subsequent gate

Write actual findings to `docs/benchmarks/sqlite-vec-artifact-review.md` with links/hashes, commands, notices/capabilities, unresolved items and budget receipt identity; update README/TODO/checkpoint and this proposal outcome. Keep wheel/source copies and generated receipts ignored. No empty report is created now.

Possible disposition: suitable to propose an exact-artifact empirical trial; blocked pending a specific provenance/license/runtime decision; or unavailable/rejected with reasons. None completes T12's paired comparison or approves runtime adoption. The existing10000-row timeout stays recorded; do not rerun or extend that baseline during this review. Product retention/limits and physical16GB acceptance remain unchanged.

**Requested approval:** this exact32-start/20-minute artifact-only package, including bounded public retrieval and static inspection, plus a separate explicit decision to commit these five planning documents. Installation, lockfile changes, importing/loading/running wheel contents, additional artifacts, performance trials and G2 adoption remain outside scope.
