# T17-IF-HS — Hub wheel verified; source provenance remains unresolved

## Result and scope

The user approved HS1–HS5 and its five planning documents, committed as `9834ce4`. The [approved package](../proposals/hub-only-static-review.md) used fresh `data/t17/hub-only-static-review-01/`; earlier runs and the older inspector/tests were preserved.

**Static inspection passed for the exact existing Hub 2.4.0 wheel.** All 191 entries were admitted under the wheel-only 256-entry ceiling; 190 payload-member hashes/sizes matched RECORD, whose self-entry is intentionally unhashed. The exact full-wheel SHA covers that self-entry too. Metadata and one UTF-8 license file were read without extraction, installation or candidate import/execution.

Public review then found an unresolved relationship between the approved source coordinate and the official release coordinate. The package's required-provenance stop was applied before expanding transitive dependency research. This is partial research completion, not runtime/dependency adoption or evidence of a bad wheel.

## Exact static evidence

| Item | Observed result |
| --- | --- |
| Wheel | `huggingface_hub-2.4.0-py3-none-any.whl`, 857,021 bytes |
| SHA-256 | `42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801` — matches fixed input |
| ZIP/RECORD | 191 entries, 190 hashed payload members verified; no cap expansion outside this wheel |
| Packaged identity | Name `huggingface_hub`, version `2.4.0`, Python `>=3.10.0`, declared license `Apache-2.0` |
| License | `huggingface_hub-2.4.0.dist-info/licenses/LICENSE`; SHA-256 `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`; UTF-8 read, no legal/native-transitive clearance inferred |
| Native suffix inventory | No `.dll`/`.exe`/`.pyd`/`.so`/`.dylib` filenames detected in this wheel; this says nothing about native transitives |
| Worker | One owned stdlib worker, exit 0, 10.558894 seconds; stdout/stderr empty; retained-handle/wait teardown verified |
| Worker reads | 5,164,397 charged bytes, including owned source, compressed/member reads and probes |
| Memory observation | Sampled peak private bytes 15,065,088; not total application/Ollama memory or physical 16 GB acceptance |

The borrowed module matched SHA-256 `691d86c9cc750a2f88b266230e0938936d92ce54c3b5f21684bd3a080fcd6d03` before its exact authored bytes were compiled. Its old worker, writer, tests and closed root were never used. Its default archive limit remains 128. No candidate source bytecode or native library was loaded.

## Verified direct requirements — no resolved transitive graph

| Distribution | Packaged runtime requirement |
| --- | --- |
| click | `>=8.4.2,<9.0.0` |
| filelock | `>=3.10.0` |
| fsspec | `>=2023.5.0` |
| hf-xet | `>=1.6.0,<2.0.0`; declared machine marker includes the AMD64 target |
| httpx2 | `>=2.0.0,<3`; distinct distribution from installed HTTPX |
| packaging | `>=20.9` |
| pyyaml | `>=5.1` |
| tqdm | `>=4.42.1` |
| typing-extensions | `>=4.1.0` |

`tomli>=1.1.0` is restricted to Python<3.11 and excluded for this project's Python>=3.11 target. Unselected extras remain excluded. Eleven runtime distribution names were identified including Tokenizers/Hub roots, below the 20-name ceiling; exact new versions/artifacts and transitive closure were not selected or established.

## Public source evidence and mandatory stop

Three precharged web calls covered 12 targets, including four unsuccessful fetches. A PyPI provenance endpoint and pinned raw pyproject returned cache misses; the pinned workflow-directory API was inaccessible through the tool; the pinned commit page also returned a cache miss. These are tool observations, not proof that the upstream objects do not exist. No retry or alternate HTTP transport was used.

The [official release page](https://github.com/huggingface/huggingface_hub/releases/tag/v2.4.0) links [release commit `3739729b86489e4ae28b5a62e622be320b141493`](https://github.com/huggingface/huggingface_hub/commit/3739729b86489e4ae28b5a62e622be320b141493). Its diff changes the release-candidate version to `2.4.0`; the [tagged initializer](https://github.com/huggingface/huggingface_hub/blob/v2.4.0/src/huggingface_hub/__init__.py) also declares that version. This narrows source identification, but does not prove that the inspected wheel was built from those exact bytes.

The package's approved source reference remains `178e1a1797858724c79fd9d12d79d0902d730497`. Its relationship to the release commit and inspected wheel was not established; prior `.dev0` observations remain historical evidence. The [registry project page](https://pypi.org/project/huggingface-hub/2.4.0/) did not expose matches for the queried old commit prefix or wheel-hash prefix in the returned text. That negative search does not establish missing publisher attestation in general.

**Stop applied:** do not silently replace the approved source pin or continue graph/advisory/offline/native investigation under an unresolved necessary provenance link. No further tests, lint, payload inspection or research occurred after this stop. Installation/trial readiness remains **not established**.

## Test-first implementation and review

New files only: `tests/evals/spikes/hub_static_review.py` and `tests/evals/spikes/test_hub_static_review.py`. Focused RED failed because the aid did not exist. The initial 14 tests passed; four additional identity/root controls brought the final suite to **18 passing tests in 0.567 seconds**. An in-memory payload-identity guard mutation made the gold test fail as expected.

Controls cover 191-entry acceptance, 257-entry refusal before member parsing, unchanged runtime defaults, exact payload/source identities, malformed/CRC/RECORD cases, unsafe aliases/paths, read/expansion/text/notice limits, hardlinks/reparse points, file changes, no old worker/writer/root, no candidate launch/import and receipt confinement. Routine synthetic tests never read the candidate wheel.

Four suite invocations and five Ruff invocations were used. Final lint and final automated format check passed. A single `S102` suppression is local to compiling the exact hash-pinned, explicitly authorized authored source bytes; no general execution permission or candidate-code exception was introduced. Source review checked that the old entry points and writer are unused.

## Workflow use

The six local written workflows used in this continuation were:

| Workflow | Concrete application |
| --- | --- |
| planning-and-task-breakdown | Ordered HS tasks, prerequisites, limits and approval gates |
| incremental-implementation | Synthetic aid first, then the single real-wheel attempt |
| test-driven-development | Expected RED, passing regression suite and caught mutation |
| security-and-hardening | Exact owned-source binding, ZIP/RECORD/file boundaries and provenance stop |
| code-review-and-quality | Focused source review, lint and final format verification |
| documentation-and-adrs | Findings, dependency/preflight notes and saved checkpoints; no adoption ADR |

No skill scripts were executed. `git-workflow-and-versioning`, `interview-me` and `context-engineering` were not applied in this continuation; Git actions followed AGENTS.md.

## Accounting, preservation and next decision

Bootstrap/output controls preceded optional reads. The full metadata projection was withheld when too large, then a measured runtime-only projection was emitted. No output was silently truncated. At entry, all 43 inherited identities matched; 58 direct source/evidence identities were frozen. Final preservation, link/diff/scope checks and resource totals are recorded in the ignored run's `closeout.json` and `meter.json`.

The shared 128 MiB read budget includes four prepaid 8 MiB synthetic-suite allowances, real-wheel reads and small evidence/source/closure reads. All wrappers, controls, worker/polling, research and closeout share the original allocation; no refunds or reset. Runtime/archive/tokenizer/model payloads were not reread.

Request a separate commit of the nine source/results/status files. Next, prepare a bounded **source-coordinate reconciliation** proposal: distinguish the historical approved reference from the observed official release commit and establish the publisher/build relationship before any pin change or dependent graph expansion. Preserve this successful wheel evidence rather than rerunning its payload inspection.

Native notice/advisory coverage for transitives, exact Windows artifacts, offline/cache/telemetry behavior, standalone/native parity, context/output reservations and G2 remain open. The unchanged Stage 1 formats/OCR/privacy and 16 GB CPU-only target remain binding. No installation, candidate execution, inference/API use, global/PATH/lock change, application implementation or stage transition occurred.
