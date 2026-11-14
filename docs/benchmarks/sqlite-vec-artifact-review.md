# sqlite-vec0.1.9 Windows artifact — static review complete, adoption blocked

## Subsequent notice decision

After commit `3092aeb`, the user accepted the exact-wheel companion-notice proposal with "i do accept". [Decision record](../decisions.md) limits this to the unchanged reviewed wheel and the pinned upstream MIT/Apache texts identified below, preserved together for any later approved local evaluation. The missing-bundled-notices finding remains; no wheel was modified, installed or loaded. Binary provenance/runtime unknowns and empirical/G2 gates remain open. Earlier notice-decision/commit-pending statements below describe the pre-acceptance state. Acceptance-document commit approval is pending.

## Outcome and authority

The user approved the [artifact-only package](../proposals/sqlite-vec-artifact-review.md); its five planning documents were committed in `dcb70be`. The exact wheel was retrieved and inspected under the reviewed standard-library Windows process boundary. **No package was installed/imported, no DLL/SQLite extension was loaded, and no model/OCR/baseline trial was run.** Only new inspector/test source and documentation changed; global/project dependencies and prior trials remained untouched.

Disposition: **blocked pending a notice/provenance decision and a separately approved runtime test**. The wheel contains no full license/NOTICE/COPYING files. Upstream notices now have pinned identities, but their retrieval is not an automatic exception or redistribution approval. Static review found no reason to substitute another version/fork; it also provides no runtime-safety guarantee.

## Artifact, archive and metadata

| Identity | Verified result |
|---|---|
| Wheel | `sqlite_vec-0.1.9-py3-none-win_amd64.whl` |
| Download | 292804bytes |
| SHA-256 | `4a28dc12fa4b53d7b1dced22da2488fade444e96b5d16fd2d698cd670675cf32` |
| ZIP inventory | 6files,291964expanded bytes; capped in-memory reads, no extraction |
| DLL | `sqlite_vec/vec0.dll`,289280bytes |
| DLL SHA-256 | `fcf98662a7ad9dce394b96a88f91032047823831b951c76636787c312a6476e6` |
| Wheel loader | `sqlite_vec/__init__.py`,1905bytes,SHA-256 `fe41981daa9515dd5d07a0376223da47bf758b6f2bb907cd3578c21ad4680a89` |

Every RECORD member hash/size and complete member coverage checked successfully. Remaining entries are METADATA,WHEEL,top_level.txt and RECORD. No executable startup hooks/entry-point file, extra DLL or bundled notice was found. Metadata name/version and `py3-none-win_amd64` tag matched; no `Requires-Python` or mandatory `Requires-Dist` was declared. The registry still contains placeholder author/homepage/description material. RECORD and registry consistency establish selected bytes, not publisher attestation or a reproducible build.

## Immutable source and notices

The approved GitHub ref resolved directly to commit **`e9f598abfa0c06b328d8fe5da9c3760cce74be10`**. Seven allowed source files were retrieved from that commit, not a moving branch/tag. Local byte/hash receipts include:

| Source | Bytes | SHA-256 |
|---|---:|---|
| LICENSE-MIT | 1068 | `6ce72bbe12d975bd5286e5ab0a064c069693300c47bccbc57bec18485f1621ea` |
| LICENSE-APACHE | 10931 | `a38070a94d4afd9cd710e3ce67bd1de78097cfe1784c1f0109ac95d3c196bfdc` |
| bindings/python/extra_init.py | 1404 | `12038b99f015816f51364c6febc14749cab33553ab0d15583c657e08356f911e` |
| sqlite-vec.c | 320026 | `ba081a47fa02eadc3cf6b16c314b695b84081269349aac722b4efa338fe8fd85` |

The helper portion of the wheel loader and upstream `extra_init.py` produced equal Python ASTs after excluding the wheel's generated loading prefix; neither was executed. This supports source identity for those Python helpers only. The generated prefix was reviewed as text: it builds a package-relative `vec0` path and exposes `load(conn)` calling `conn.load_extension(...)`. It does not enable/disable SQLite extension loading for the caller. Importing the wrapper would attempt an optional `numpy.typing` import, which can itself initialize the already installed NumPy; this review did not import either module. Float serialization uses Python's native-endian `struct.pack`, so later tests must compare the frozen little-endian float32 baseline on this Windows target explicitly.

Upstream VERSION/build/config and MIT/Apache files were saved, but no binary/source reproducibility, Authenticode trust, bundled transitive-notice completeness or maintenance/security clearance is established. Missing notices must remain a specific decision. Proposed next policy for review: preserve the exact unchanged wheel together with the pinned upstream license texts as companion files for a bounded local evaluation, with the omission recorded. **That exception is not approved by this report.** Do not repackage the wheel, change its hash or infer unrestricted redistribution.

## Native/static trust boundary

The bounded PE parser identified an AMD64 PE32+ DLL and file-backed sections/import/export tables. Export names: `sqlite3_vec_init`, `sqlite3_vec_numpy_init`, `sqlite3_vec_static_blobs_init`. The normal import table names only `KERNEL32.dll`; recorded imports include `CreateFileW`, `ReadFile`, `WriteFile`, `LoadLibraryExW`, `GetProcAddress` and environment/process functions. These are capabilities/import dependencies, not proof that a specific operation runs during import or inference. Dynamic loading and resolution mean the table does not establish all runtime dependencies or absent network access.

The optional NumPy/file-access surface remains relevant to a future test. No loaded memory, search speed, CPU-instruction compatibility, actual SQLite/Python loading behaviour, native stability or enforced filesystem/network confinement was measured. The wheel has no Python ABI-specific tag, but that is not proof that this host's SQLite extension support or runtime linkage is compatible. Do not load it merely to fill those gaps without a new approved package.

## Tests, accounting and limits

The first test run failed on the missing inspector. Initial implementation passed9synthetic tests, then expanded RECORD/PE/byte-meter controls brought the suite to11passes in0.051s. Ruff lint/format passed after replacing a regex alias. A final test-module import placement adjustment allows ordinary test discovery; **11tests then passed in0.071s**. Ruff was not repeated after that import-only adjustment. Tests cover traversal/Windows aliases/case collisions, links/expansion limits, independently wrong RECORD identity, truncated/oversized/hash-mismatched body, failed request/byte reservations, corrupt PE offsets, valid minimal x64/wrong-machine headers and destination allowlisting. A failed RECORD check prevented simulated progression. No real installer or wheel loader exists in the inspector's execution path.

The inspector and tests configured a512MiB/single-process Windows Job before untrusted archive/AST/PE parsing, with a120-second self-termination watchdog. The successful invocation did not exercise the real timeout kill or prove comprehensive parser fuzz resistance. Source inspections are bounded static checks, not a native security audit. There were no automatic redirects/retries or browser fallback. The connected fetch command used host-approved execution permissions; that is not permission to load artifact code.

Local HTTP meter: **10/20attempts,641244actual response-body bytes,3176398reserved bytes out of8388608**. Each request reserved its cap plus one overflow-detection byte before sending, and persisted actual read-byte counts by chunk. These are consumed response-body bytes reported by the HTTP reader, not TLS/header/wire traffic. Unlike the earlier browser review, this fresh request/body accounting is local and durable; it does not retroactively resolve that older gap. Registry JSON, the exact wheel, ref resolution and seven source files account for all ten requests. Missing or mismatched identities would have stopped without a retry.

Ignored receipts are under `data/t12/sqlite-vec-artifact-01/`: budget,started marker,wheel,source copies and summary/inventory/loader/PE findings. The allocation closed at **28/32reservations,488.918active seconds and649331output bytes** before the final budget rewrite; prior hashes, result links and whitespace checks passed. Categories: preparation8,inspection12,reporting8,cleanup0. The summary's earlier646787-byte observation preceded its own final rewrite; neither size is a loaded-memory measurement. Keep all downloaded/generated material out of Git. No other baseline/old trial state changed.

## Next decision

Review the narrowly described companion-notice exception and remaining binary provenance/runtime unknowns. If accepted, prepare an exact-artifact, project-local empirical comparison package with loading/security controls, the same frozen baseline/reference, versioned dependencies and fresh shared limits. The10000-row baseline timeout remains historical; no rerun or higher timeout is approved. T12's paired comparison and product retention/scale/latency decisions, physical16GB validation and T17/G2 adoption are still open. Source/results commit approval is pending.
