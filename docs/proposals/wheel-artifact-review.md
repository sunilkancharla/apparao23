# T17-IF-AS — bounded acquisition and inert wheel inspection

## Status and purpose

**Proposed; AS1–AS5 execution and the four-file planning commit await approval.** The user approved committing PR results and preparing this package. Results are committed as `7c4e172`. The [successful native metadata probe](../benchmarks/wheel-metadata-probe-retry.md) supplies connectivity evidence, not approval for further requests or binary handling.

Complete the remaining original WI artifact investigation: test the authored evaluation aids, fetch eight exact wheels, and inspect their metadata/RECORD/notices/native inventory without installing or importing them. Obtain fresh metadata for all eight releases as part of acquisition; there is **no separate connectivity probe** and no reliance on the earlier response's current yank status.

This proposal explicitly replaces the stopped WI/WIC execution allocations. It retains the artifact scope and raises active time, suite count and acquisition timeout as listed below. No old ledger is reset or old runtime root reopened for writes.

## Exact artifact scope

The [original WI table](wheel-static-inspection.md) is incorporated for the eight complete filenames, expected SHA-256 values, exact/rounded size evidence and per-wheel caps. Pin that authored file to 14,161 bytes/SHA-256 `9d3ace13aa4e36099c197b4e960adc98b0fff83123531a3740206a292fe2c6b0`; changed bytes stop work before dependent execution.

| Distribution/version | Fixed wheel | Body cap |
| --- | --- | --- |
| HTTPX2 2.16.2 | `httpx2-2.16.2-py3-none-any.whl` | 256 KiB |
| httpcore2 2.16.2 | `httpcore2-2.16.2-py3-none-any.whl` | 256 KiB |
| AnyIO 4.16.0 | `anyio-4.16.0-py3-none-any.whl` | 256 KiB |
| Click 8.5.1 | `click-8.5.1-py3-none-any.whl` | 256 KiB |
| Filelock 4.2.10 | `filelock-4.2.10-py3-none-any.whl` | 256 KiB |
| Truststore 0.10.5 | `truststore-0.10.5-py3-none-any.whl` | 256 KiB |
| HF-Xet 1.8.0 | `hf_xet-1.8.0-cp38-abi3-win_amd64.whl` | 8 MiB |
| FSSpec 2026.9.0 | `fsspec-2026.9.0-py3-none-any.whl` | 1 MiB |

Fresh metadata must match each fixed filename/SHA, be non-yanked and provide a positive exact integer size within the cap. The first six must also match their original exact sizes. HF-Xet's 3.9 MB and FSSpec's 221.7 kB remain rounded historical observations, never exact byte admissions. Missing/ambiguous/changed entries stop the attempt; no version or artifact substitution.

FSSpec's absent provenance/Trusted Publishing metadata remains explicit. Approval here accepts the publisher-listed checksum for non-executing acquisition/inspection only. It does not establish independently verified origin, licence clearance or adoption. Build-source mapping remains an adoption item under the unchanged approved metadata-only timing deferral.

The two cached roots in `data/t17/input-fit-tokenizer-static-01/` may be read without reacquisition:

- `huggingface_hub-2.4.0-py3-none-any.whl`: 857,021 bytes/SHA-256 `42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801`.
- `tokenizers-0.23.3-cp310-abi3-win_amd64.whl`: 2,872,101 bytes/SHA-256 `1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3`.

Verify whole-file identity before ZIP access and reuse their prior full RECORD evidence. Do not rehash every cached member, reacquire these roots, or read the large Ollama archive/runtime, models, global installations or user documents.

## Ordered tasks and acceptance

| ID | Objective and prerequisites | Acceptance and verification | Status |
| --- | --- | --- | --- |
| AS1 | After approval, bootstrap and review architecture, dependency/tool identity and trust boundaries before aid implementation | Fresh accounting/frozen inputs; exact manifest and primitive dependency closure; reviewed reporting, worker startup/ownership, transport and ZIP design. Existing tool versions/limits verified; unresolved design conflicts stop dependent work. | Pending approval |
| AS2 | After AS1, implement two aids incrementally and test-first | Expected RED, smallest passing slices, abuse/regression and integrity-mutation checks, tested Windows Job/startup/teardown controls, final Ruff/format/code/security review. Shared counters cover every control/test process. | Pending AS1 |
| AS3 | After AS2 passes, one owned acquisition worker | Eight fresh metadata admissions, then eight once-only wheel requests; exact size/SHA and safe partial handling, source binding, monitored ownership and verified teardown. Failure stops; no refetch or later inspection of incomplete acquisition. | Pending AS2 |
| AS4 | After coherent AS3, one owned static-inspection worker | Bounded new-wheel RECORD/metadata/notices/native inventory plus admitted cached-root reads; preserved identities and verified teardown; no candidate code execution. | Pending AS3 |
| AS5 | At completion, stop or cutoff, close | Honest findings/resource/coverage evidence, task/readiness updates, preservation/scope/link/whitespace/readable-diff checks and validated non-null summary. Request a separate results commit; adoption remains gated. | Pending completion or stop |

Only two new versioned code files: `tests/evals/spikes/wheel_static_inspection.py` and `tests/evals/spikes/test_wheel_static_inspection.py`. Authored synthetic fixture definitions belong in the test; generated fixtures/requests/captures/artifacts stay in the fresh ignored root. No source edits to old aids or execution of their tests/workers/writers into closed roots.

AS1 verifies consistency with this approved evaluation design; covered steps require no additional project approval. It does not settle product architecture or G2. A consequential departure from this design still needs a new decision.

Use verified local incremental-implementation, test-driven-development, security-and-hardening, code-review-and-quality and documentation workflows. No external skill scripts, subagents or optional-tool installation. Use existing `F:/Python/Python314/python.exe -I -S -B` and project-local Ruff **0.17.5** as recorded in `uv.lock`; verify installed identity before use. Mismatch stops rather than installing/syncing. No pyproject/lock/PATH/global installation changes.

## Owned-code reuse and test-first review

The existing reporting control is a read-only source input: `data/t17/wheel-metadata-probe-01/control.py`, 5,397 bytes/SHA-256 `6f0ff9bf61b00a234be87b9f276ae111adaf876e59e7be90d4ec8e49586d72b7`. Preserve its passing evidence, verify its bytes before use and rerun its controls within the shared suite allocation. Do not treat it as Windows Job or memory-monitor implementation.

The ZIP primitive source is `tests/evals/spikes/standalone_static_verification.py`, 21,836 bytes/SHA-256 `691d86c9cc750a2f88b266230e0938936d92ce54c3b5f21684bd3a080fcd6d03`. After review, copy selected definitions with attribution into the new aid: `Failure`, `Limits`, `ReadBudget`, `checked_name`, `is_reparse`, `fingerprint`, `check_ancestors`, `open_regular`, `digest_stream`, `hash_regular`, `ChargedFile`, `central_admission`, `admitted_entries`, plus required stdlib imports and `CHUNK=1_048_576`. Verify source bytes before copying. Do not copy old runtime-root/archive constants, entry points, workers or writers. Review the complete transitive dependencies; do not call model-specific defaults.

These primitives provide partial admission, not every required safeguard. Instantiate their limits explicitly with this package's caps; the old 3 GiB expanded-size default is not authorized. Add missing local-layout/overlap, streaming expansion/CRC, metadata/RECORD and transport checks test-first. Never delete or weaken a test to obtain a passing run. Ordinary tests use mocked transport; no real negative HTTP request. Synthetic subprocess tests use authored code only and count inside the same leases.

Cover malformed/duplicate JSON and RECORD, wrong filename/version/hash/size, public/private/mixed DNS, credentials/redirect/TLS/framing refusals, partial transfers, path/ADS/device/alias/link/reparse/hardlink cases, corrupt CRC/overlaps, compression/expansion/read caps and a 513-entry pre-allocation refusal. Test inert import/hook/script traps without executing a candidate. Catch an in-memory integrity-guard mutation; retain RED/failure evidence. Reserve final regression/lint checks before refinements.

## Transport boundary

Request the required host permission before real acquisition. Version-specific JSON URLs are fixed under `https://pypi.org/pypi/<distribution>/<version>/json` (normalize HF-Xet's distribution identifier). All eight metadata responses are fresh in this attempt. Freeze a complete admitted manifest before payload requests; file URLs must come from matching entries, not guessed paths.

Only HTTPS port 443 to `pypi.org` for metadata and `files.pythonhosted.org` for listed wheel bodies. Validate every resolved IPv4/IPv6 address as public, reject mixed/private/reserved answers and pin the connection to one admitted address with origin Host/SNI and certificate verification. Reject userinfo/query/fragment, redirects, credentials, ambient proxy/authentication and unexpected encoding. One connection attempt/request, no address fallback, range resume, insecure TLS or automatic retry. Send only public package identifiers.

Maximum **16 HTTP transactions**: eight metadata plus eight payloads, including failures. Require status 200; bound headers to 64 KiB/response and metadata to 1 MiB/response. Explicitly admit supported framing and exact lengths, duplicate keys and schemas. Count HTTP status/header/body bytes; DNS/TLS/kernel overhead is outside that counter. A started transport failure stops acquisition and preserves partial evidence.

Write exclusive `.part` files under the owned root, streaming SHA/size accounting. Mark usable only after the full admitted exact size and fixed SHA match; retained partial/invalid data stays inert and charged. Never run an installer/package manager, extract to disk, import a wheel, execute embedded code or fetch a newly discovered dependency.

## Supervision choice and privacy boundary

Alternatives are continuing metadata-only supervision (insufficient for this payload-review gate), adding tested Windows Job supervision for inert review (**proposed**), or deferring artifact work. This proposal requests the second option; the successful PR probe did not approve it implicitly.

Before real network or candidate-file work, test the new stdlib/Windows API ownership controls on synthetic processes. Retain PID, birth and kernel handles; put each real worker in a verified kill-on-close Windows Job with a startup gate before payload access and a one-process/no-descendant policy. Prove assignment, gate refusal, timeout/kill and exit/teardown behavior. Assignment, ownership or uncertain teardown failure stops before candidate work. Do not relax a guard to get past a host restriction.

Bind tested aid/owned-source bytes before execution and execute those same verified bytes, without reopening unchecked mutable source. One acquisition worker: **300 seconds + 30 seconds teardown**. One inspector: **120 seconds + 30 seconds teardown**, sequential. No server, service, GUI or listening port.

Sample private memory across identifiable owned controllers/workers against the 512 MiB evaluation target and record sampling coverage. A verified sample above the target stops optional work; unavailable worker ownership/required samples block candidate work. This is a sampled monitor, not a guaranteed kernel ceiling or a physical 16 GB product benchmark. Kernel Job ownership does not establish filesystem/kernel-egress confinement. Documents, prompts, embeddings and user data never enter this trial or public research.

## ZIP/static boundary

Admit central-directory size/count/layout before `ZipFile` allocates its entry list. Refuse unsafe Windows-relative paths, aliases, file/directory collisions, links/reparse/hardlinks, overlapping/inconsistent local layouts, encryption, ZIP64/multidisk and unsupported compression. Stored/deflated only. New wheels: at most 512 entries each; cached Hub 256/Tokenizers 128. Aggregate 4,096 entries, central directory 256 KiB/wheel, expanded 64 MiB/wheel and 128 MiB/batch, including repeated decompression. Stream CRC/hash/size checks. Limit refusal is not proof that a wheel is defective.

For new wheels, verify RECORD coverage/hashes/sizes and required metadata, normalized name/version and wheel tags. Handle RECORD's unhashed self-entry and permitted legacy signature sidecars explicitly; inventory deprecated signatures without claiming verification. Check declared License-File locations for metadata version 2.4+. Preserve missing/over-cap/unsupported outcomes rather than truncating or inventing notices.

METADATA/RECORD: 256 KiB each; other metadata 64 KiB/file; notices 256 KiB/file and 4 MiB/batch. Strict decoding and safe JSON/text rendering; no untrusted instructions, terminal escapes, embedded links or rich content executed. Inventory native suffixes and startup hooks as inert data only. This does not establish native ABI safety, vendor-licence compliance, semantic offline behavior or comprehensive security.

Cached source-as-data remains limited, if present, to `huggingface_hub/constants.py`, `tokenizers/__init__.py`, `tokenizers/__init__.pyi`, `tokenizers/tokenizers.pyi`: 128 KiB/file, 512 KiB total. Declarations show intent, not actual offline operation. Do not follow embedded URLs or search outside the approved source inputs.

## Shared allocation and explicit changes

Fresh ignored root: **`data/t17/wheel-artifact-review-01/`**, refusing an existing/unsafe root. Bootstrap accounting before optional reads; freeze previous reports/receipts and relevant authored inputs. Parent alone writes the global meter and prepays non-refundable child leases. Controls, failures, negative tests and regressions cannot reset or bypass combined counters.

| Resource | Proposed ceiling |
| --- | --- |
| Work | 128 units: bootstrap/design/controls 16; aids/tests 48; acquisition 16; inspection 16; findings/checks 16; protected closure 16. Normal allocation 112. |
| Active time | **3,600 seconds** instead of the original 2,400. Start acquisition by 2,400, inspection by 2,760; stop optional work at 3,000; reserve 600 for closure. Save interim findings before cutoff. |
| Processes/checks | 64 owned starts across wrappers/controllers/tests/Ruff/negative/real workers/read-only Git. **At most 10 suite invocations** instead of 8; at most 8 Ruff invocations. All synthetic ownership/control starts share this allocation. Separately approved commits remain separate. |
| HTTP/read/disk | 24 MiB HTTP status/header/body and 16 transactions; 512 MiB streamed reads including 16 MiB ledger allocation and 16 MiB/suite within that total; 48 MiB retained artifacts including all captures, partials, wheels, fixtures, notices and authored outputs. |
| Reporting/records | 8 KiB combined stdout/stderr/invocation, 4 KiB normal display target, 128 KiB aggregate with 16 KiB protected closure reserve. At most 64 immutable ledger records/64 ledger validations, 4 KiB/record. Count capture/copy reads and disk too. |

Retain the PR timing method: prepare complete commands first, then persist submission and immediately request escalation inside one orchestration call without intervening model work. Prepay all possible starts before any early guard. Approved-command entry records its timestamp before guards. Exclude only explicitly measured host-review/queue intervals; keep active and wall totals distinct. Allow at most **three** such intervals for native control/diagnostic and acquisition commands, totaling at most 24 hours. No other work runs during them. Record denial/cancellation using a distinct decision-observation endpoint and close; reject ambiguous clocks/duplicate launches. Do not hide model reasoning, coding or ordinary tool time inside exclusions.

At most two trustworthy orchestration corrections within the same limits; source changes after tests require relevant revalidation inside the remaining suite budget. No candidate refetch, automatic retry, version change, guard weakening or fresh allocation after a stop. Host denial, phase/cap/identity/unsafe-input/reporting/capture/accounting/ownership failure stops optional work and retains truthful partial findings.

## Deliverables and approval

After execution approval: the two authored aids, `docs/benchmarks/wheel-artifact-review.md`, affected dependency/preflight and PLAN/TODO/README updates, plus ignored fixtures/manifests/artifacts/source-binding/ownership/accounting records. On early stop, retain partial evidence without empty reports or fabricated capability. No session-checkpoint files.

Request **AS1–AS5 approval**, including the exact eight inert acquisitions, cached-root reads, test-first aids, new tested Windows Job/sampled-memory boundary, measured host-wait exclusions and explicitly revised time/suite/timeout limits. Separately approve this proposal plus PLAN.md, TODO.md and README.md (**four-file planning commit**). Routine covered steps need no repeated project approval. Later results commits, installation/candidate imports, runtime/offline/parity adoption, G2 and stage transitions remain separately gated.

Preparation used the verified local planning/documentation/security workflows. No new root, helper, fixture, test, Job trial, acquisition or inspection started; old roots and historical checkpoint files remain untouched. Existing source/lock reads are planning evidence, not proof of the proposed controls.
