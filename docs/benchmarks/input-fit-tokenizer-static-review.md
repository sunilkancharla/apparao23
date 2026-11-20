# T17-IF-N — partial static artifact review and persistence stop

## Outcome — 2026-11-16

Approved [IF-N package](../proposals/input-fit-tokenizer-static-reconciliation.md), proposal commit `b8ebed3`. Built and tested two stdlib inspection aids, then made the single authorized static acquisition attempt. **Both wheels and one Qwen asset were acquired and identity-checked.** The worker stopped with `PermissionError` during durable accounting for the next request. It exited cleanly; no retry. Ten other data assets remain unacquired. No installation, candidate import/native-library execution, inference, model-store/private-data read or application implementation occurred.

This is partial static evidence, not readiness for provisioning or adoption. The [parity requirements](../proposals/input-fit-tokenizer-parity-validation.md), dependency/native notice review, source-to-release reconciliation and trustworthy runtime oracle remain open. G2 remains open.

## Test-first implementation and actual checks

New authored files: `tests/evals/spikes/tokenizer_static_review.py` and `test_tokenizer_static_review.py`. They use stdlib HTTPS/JSON/ZIP/RECORD handling, fixed artifact identities, precharged accounting, explicit redirects, proxy refusal, bounded streams, path/reparse checks and a one-pass CLI. Downloaded code is never imported or extracted into executable paths. The old sqlite-vec aid was a read-only reference; no old controller/epoch was executed or changed.

- Initial test-first run failed because the new module did not yet exist. The first implementation passed15tests in1.058s; expanded controls passed18tests in1.175s.
- Temporarily disabling RECORD integrity verification produced the expected test failure. Original source bytes were restored; all18tests then passed in1.506s. Five focused suite invocations total: red, two green increments, mutation and final regression. A separate attempted Python `-c` mutation command failed at argument parsing before modifying files or running tests; its interpreter/tool start was charged.
- Ruff formatting reformatted both files. The next lint invocation fixed5findings and reported6remaining findings. These were corrected; the user explicitly approved **one additional Ruff check**, retaining every other limit. That final check passed. Three Ruff invocations total, with the extension recorded in the meter. No final format-check claim beyond the formatting actually applied.

Tests cover durable precharge/refusal, receipt interruption, body/size/hash limits, unsafe URLs/private DNS, traversal/reparse/overwrite, ZIP aliases/links/expansion/RECORD, wheel identity, missing publisher attestation, HTTP encoding, redirect bounds and charged error bodies. These are synthetic controls, not comprehensive native/security certification. No candidate code or real sockets ran in routine tests.

## Verified downloaded bytes — inert static artifacts

| Artifact | Exact bytes | SHA256 | Static evidence |
|---|---:|---|---|
| `tokenizers-0.23.3-cp310-abi3-win_amd64.whl` |2,872,101 |`1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3` |Matches approved registry hash;31members/8,241,663expanded bytes; expected name/version/tag and all RECORD entries verified |
| `huggingface_hub-2.4.0-py3-none-any.whl` |857,021 |`42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801` |Matches approved registry hash;191members/3,326,406expanded bytes; expected name/version/tag and all RECORD entries verified |
| Qwen `tokenizer.json` at `5fee7c4ed634dc66c6e318c8ac2897b8b9154536` |7,031,645 |`c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539` |Matches publisher size and Git blob `443909a61d429dff23010e5bddd28ff530edda00`; computed SHA256 identifies observed bytes, not independent publisher SHA256 attestation |

Publisher/registry URLs and inventories are retained locally in the inspection/identity receipts. Source provenance context: [Tokenizers registry](https://pypi.org/project/tokenizers/0.23.3/), [Hub registry](https://pypi.org/project/huggingface-hub/2.4.0/), [pinned Qwen tree](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/tree/5fee7c4ed634dc66c6e318c8ac2897b8b9154536). No full vocabulary/configuration contents are printed in reports. Payloads remain ignored under `data/t17/input-fit-tokenizer-static-01/`, unapproved for loading.

The inspected Tokenizers wheel declares Python>=3.10 and Hub>=0.16.4,<3.0. Its native inventory contains `tokenizers/tokenizers.pyd`; no filename matching the license/notice scan and no License/License-Expression value were found by this aid. Earlier Apache2.0 source evidence does not reconcile this wheel's bundled native notices. This is a review gap, not a legal conclusion. No import/ABI3 compatibility, installed footprint or runtime RAM/latency measurement was made.

Hub's actual wheel METADATA declares version2.4.0/Python>=3.10.0, includes a LICENSE inventory entry and console-entry-point metadata, and contains no native file matching the aid's suffix scan. It was not installed and no entry point ran. Its source publishing commit's2.4.0.dev0 declaration still needs workflow/source-to-wheel reconciliation; final wheel metadata establishes the packaged version but not how it was produced.

## Actual wheel dependency evidence — graph still incomplete

Hub's runtime requirements match the previously reviewed source-level ranges: click>=8.4.2,<9; filelock>=3.10; fsspec>=2023.5; hf-xet>=1.6,<2 with the machine marker; httpx2>=2,<3; packaging>=20.9; pyyaml>=5.1; tqdm>=4.42.1; typing-extensions>=4.1. Tomli's Python<3.11 marker excludes it on the target. No extras selected. Existing click8.5.1/packaging26.3/pyyaml6.0.3/tqdm4.70.1/typing-extensions4.16.0 satisfy those direct ranges. Locked HTTPX0.28.1 is distinct from HTTPX2.

No new transitive versions/artifacts were selected or downloaded. Twelve runtime distribution names including the excluded tomli were encountered; nested requirements and the complete compatible graph remain unverified within the20-name ceiling. Python metadata equality/range checks are not resolver results or native security clearance. Lock and project dependency declarations remain unchanged.

Public-source research used2web calls/7targets. The pinned [Tokenizers release workflow](https://raw.githubusercontent.com/huggingface/tokenizers/301277072263fb3830eb66eec7e47adadf76f1dc/.github/workflows/python-release.yml) contains tag/version checking and Windows build/test entries; this is source intent, not independent evidence that the downloaded wheel was built reproducibly or works on this machine. Hub's pinned release workflow/version utility/constants and Tokenizers' pinned Python initializer returned cache misses; no retries/alternate transports. [Tokenizers](https://github.com/huggingface/tokenizers/security/advisories) and [Hub](https://github.com/huggingface/huggingface_hub/security/advisories) advisory pages again displayed no entries; coverage remains incomplete, not vulnerability-free. Offline import/outbound behavior was not established.

## Persistence stop and verified teardown

Owned isolated Python worker PID53448, birth2026-11-16T04:33:31.7542479Z, exited1 and was reaped after10.4989248seconds; zero active descendants found, stdout37bytes/stderr0, no timeout. Controller receipt: `teardown.json`. No further acquisition/inspection worker was launched.

The original durable meter contains8HTTP events; the complete `meter.pending` contains a ninth event marked `reserved_before_send` with0bytes. The worker's sanitized result is `PermissionError`/`transport_or_os_failure`. Code places the ninth event's persistence before opening its transport. **Inference:** the stop occurred in saving that precharge, not in a ninth network exchange. The failed I/O operation/Windows error number/path were not retained, so a precise cause such as file contention or host security software is unproved.

Observed transactions:8, including2received307redirect responses; actual received bytes10,811,431. Two wheel payloads and one data asset succeeded. Qwen's tokenizer-config request received its redirect response, but its follow-up transport did not start. This evidence does not support a general network-blocking diagnosis.

Original meter bytes were preserved as `meter-at-worker-stop.json`; the failed `meter.pending` is unchanged. Final accounting conservatively retains9request precharges and the higher pending metadata reservation, with no refunds. No failed record was deleted, silently replaced by a fresh ledger, retried or used to authorize another acquisition. A later synthetic-only persistence investigation is recommended before another runtime attempt.

## Limits, preservation and remaining gates

The original128-unit allocation (104normal/24protected),1,800seconds/32MiB remains unchanged. Helper work recorded31conservative units within32, including the failed command and approved extra Ruff check. Web research/acquisition/review/closure share their separate prepaid blocks; unused reservations are not refunded. HTTP body reservations after conservative reconciliation: wheel3,729,124bytes, asset7,038,952bytes, metadata3,182,601bytes; all category caps retained. ZIP expanded total11,568,069bytes, below32MiB.

Closeout verified352local links,19prior preservation hashes, both stopped receipt hashes and all3downloaded payload hashes. An initial check caught an update to the frozen prior parity design; only that added paragraph was removed and original byte identity restored. At verification elapsed time was964.765seconds and conservative local output upper11,409,025bytes, within the unchanged limits; final meter records closure time. No further tests, lint, downloads or candidate execution were run. Readiness is partial: remaining asset identities, atomic-receipt failure, native license/advisory/ABI/offline evidence, dependency closure and rendering/token-count/output-headroom parity all remain open. The helpers are evaluation aids, not application functionality. Nine source/results/status files require separate commit approval; no stage/adoption approval inferred. No /status or /compact invocation claimed.
