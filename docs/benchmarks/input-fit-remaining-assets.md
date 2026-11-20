# T17-IF-P — remaining tokenizer data assets acquired

## Outcome — 2026-11-16

Approved [IF-P package](../proposals/input-fit-remaining-assets-continuation.md), proposal commit `2533f27`. **All ten remaining data files were acquired and matched publisher size/Git identities.** Together with the earlier Qwen tokenizer.json, all11listed publisher data assets now have exact observed byte identities. The two previously verified wheels and earlier Qwen file were preserved, not redownloaded or loaded.

This completes this static acquisition package, not tokenizer/runtime adoption. Nothing was installed, no downloaded code/tokenizer was imported or executed, and no model/API/inference call occurred. Remaining gates include dependency closure, native notices/advisories, source-to-release provenance, offline runtime behavior and exact tokenizer/rendering/context/output-headroom parity. G2/application implementation remains open.

## Test-first wrapper and trust boundary

Added only `tests/evals/spikes/remaining_asset_review.py` and `test_remaining_asset_review.py`. The wrapper imports the exact hash-verified **locally authored** IF-N helper through an isolated normal source loader consuming verified bytes; no old main/acquire/default schedule runs. The stricter URL policy applies inside inherited redirects, with a per-fetch identity check that refuses switching to another otherwise permitted asset. The new-root budget enforces40requests,8MiBasset/4MiBmetadata reservations and16MiBartifact output despite older larger helper constants.

Bookkeeping retains the exclusive-pending/write/flush/fsync/close/replace sequence and fail-closed/no-retry behavior. An independent append-only journal records each operation and exception class/errno/winerror without raw paths or arbitrary error text. Reporting admits scalar values only, rejects provider/arbitrary objects and precharges controlled UTF-8 output. No unique-temporary strategy, backoff, permission change or repair of an old ledger was introduced.

Initial missing-module red was followed by12passing tests in2.403s and expanded14tests in1.510s. Temporarily weakening the40-request guard to the older48limit produced the intended failure in `test_precharge_and_lower_request_limit`; original bytes were restored. Final14tests passed in1.784s. Five suite invocations total. Ruff initially fixed2findings, then formatting, final lint and final format check passed; four Ruff invocations total. All routine HTTP tests used injected transports/private-DNS stubs, not real sockets or candidate code.

Controls cover per-stage persistence failures preventing transport, successful durable precharge before open, exact files/revisions/hosts, cross-artifact/registry redirects, narrower inherited limits, body encoding/partial reads, metadata size/Git/LFS mismatch, path/reparse/output refusal, old-root/closed-claim refusal, diagnostic failure and both scalar-reporting caps. These tests are meaningful boundary evidence, not a full native/security certification.

## Exact new observed asset identities

Qwen publisher `Qwen/Qwen2.5-1.5B-Instruct`, revision `5fee7c4ed634dc66c6e318c8ac2897b8b9154536`:

| Filename | Exact bytes | Observed SHA256 |
|---|---:|---|
| `tokenizer_config.json` |7,305 |`5b5d4f65d0acd3b2d56a35b56d374a36cbc1c8fa5cf3b3febbbfabf22f359583` |
| `vocab.json` |2,776,833 |`ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910` |
| `merges.txt` |1,671,839 |`599bab54075088774b1733fde865d5bd747cbcc7a547c5bc12610e874e26f5e3` |
| `config.json` |660 |`98d2ff8cc47488d08a2b0b3acf4eb99ef210779b42bd48605f6b8e36acdbf670` |
| `LICENSE` |11,343 |`832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e` |

Nomic publisher `nomic-ai/nomic-embed-text-v1.5`, revision `541c5a6fadb4da793505a2bb4d3ee910de7f39ea`:

| Filename | Exact bytes | Observed SHA256 |
|---|---:|---|
| `tokenizer.json` |711,396 |`d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66` |
| `tokenizer_config.json` |1,191 |`d7e0000bcc80134debd2222220427e6bf5fa20a669f40a0d0d1409cc18e0a9bc` |
| `special_tokens_map.json` |695 |`5d5b662e421ea9fac075174bb0688ee0d9431699900b90662acd44b2a350503a` |
| `vocab.txt` |231,508 |`07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3` |
| `config.json` |1,568 |`5b9a18bac1e0df08e736e84054b5aa59959a8e3f2972e4ea8abe7da2cbc3410f` |

New payload total **5,414,338bytes**. Every file matched its publisher-provided Git blob identity and size. All retain `publisher_digest_unavailable=true` for independent publisher SHA256: locally computed SHA256 values identify observed bytes, while Git blob identity is a different check. No hash was relabelled as an independent publisher attestation or proof of cached GGUF/tokenizer equivalence. No full vocabulary/configuration/template content is printed here.

Per-file Git identities, original public requests and observed byte hashes are retained under ignored `data/t17/input-fit-assets-remaining-01/`. The combined reference manifest distinguishes these ten new observations from the earlier two wheels/Qwen tokenizer.json in [IF-N](input-fit-tokenizer-static-review.md); it does not copy or alter old payloads or receipts.

## Connected run, diagnostics and teardown

One isolated owned worker PID33748, birth2026-11-16T05:51:21.2924080Z, completed in24.4665316seconds, exited0/reapedtrue, no timeout and zero active descendants found. Worker console49bytes/stderr0. No second worker, retry, alternate transport or optional public-source research ran.

Exactly22HTTPtransactions: two pinned tree requests and ten payload fetches with their same-host redirects, within40allowed. Actual received bodies5,420,008bytes. Conservative reservations retained without refunds: asset5,414,348bytes (payloads plus overflow probes), metadata2,187,286bytes (metadata caps and per-transaction error/redirect allowances), wheel0. All per-file/category caps stayed in force.

The independent operation journal contains1,896packets and **zero operation failures**. No accounting pending file is needed after successful replacement. The earlier PermissionError did not recur in this attempt; these observations do not establish its cause or prove a permanent fix. No atomic-write semantics were changed, and no claim that telemetry prevents contention is made.

## Reporting and accounting

The original112prepaid units(96normal/16protected),1,800seconds/16MiBlocal artifact allocation remained unchanged. Five-of-six focused suites, four-of-four Ruff invocations and one-of-one continuation worker were used. Helper work recorded32conservative units within48; wrappers, shell/interpreter/HTTP/negative/control/reporting/cleanup operations shared their phase allocations. Unused reservations are not refunded.

Controlled stdout is charged before emission in `reporting.jsonl`, separately from local artifact files, with16KiB/invocation and128KiBaggregate limits/16KiBclosure reserve. An additional512-byte conservative reservation covers line-ending differences and earlier measurement margins; subsequent controller emission explicitly includes its newline. Worker output was also captured and conservatively charged again when the controller emitted its summary. No Get-Content provider objects were serialized and no reporting overrun was observed. Tool-provider envelopes remain outside a claimed kernel byte bound.

Closeout verified358local links,31prior preservation hashes, both new source hashes and all ten new payload byte identities. At verification elapsed time was1,236.648seconds and conservative local artifact upper6,216,555bytes. Reporting precharges at that checkpoint were10,123bytes including conservative margins, with largest entry4,946bytes; later closeout output is charged in the same ledger. Final counters/time/status are recorded in the meter/closeout. Both old aid/test pairs, reports/receipts and three earlier payloads remain immutable. No old acquisition/synthetic run was reopened. Nine source/findings/status files require separate commit approval; no host /status or /compact invocation claimed.

## Recommended next step

Prepare a bounded review to close the remaining dependency/native-notice/provenance gaps and establish a trustworthy runtime counting oracle before any installation/native parity trial. Complete data identities remove the missing-file blocker; they do not waive those other gates. The unchanged16GB CPU-only target, provisional2,048context/192output, R01 settings, mandatory formats/OCR/privacy requirements and stage boundaries remain binding.
