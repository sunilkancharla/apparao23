# T17-IF-N — bounded static tokenizer artifact reconciliation

## Status and purpose

Proposed; execution awaits approval. IF-M findings and validation requirements are committed as `2275acc`. The user approved preparing this follow-up. [IF-M findings](../benchmarks/input-fit-tokenizer-manifest-review.md) identify the source/release mismatch, incomplete dependency metadata and missing exact asset hashes. [Parity requirements](input-fit-tokenizer-parity-validation.md) remain binding.

This package proposes **static acquisition and inspection**, with no installation/import/inference. It can reconcile the actual wheel metadata with publishing source and record exact asset bytes for later review. Success does not establish tokenizer/GGUF parity, offline runtime behavior, native safety or G2 adoption.

## Exact artifact set and trust policy

Only these two wheels may be acquired, once each, after registry identity/size/URL checks:

| Filename | Required SHA256 | Maximum body |
|---|---|---|
| `tokenizers-0.23.3-cp310-abi3-win_amd64.whl` |`1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3` |4MiB |
| `huggingface_hub-2.4.0-py3-none-any.whl` |`42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801` |2MiB |

No HTTPX2 or other transitive wheel, source archive, model weight, native runtime or alternative version is authorized. Downloaded wheels stay inert inside the ignored review root. Verify complete bytes against the required SHA256 before ZIP inspection; reject registry hash/name/version/size disagreement. No package manager, source build, installation, wheel import or native-library loading.

The following **11 data assets only** may be acquired once each from full-revision HTTPS resolve URLs, at most8MiB per file and14MiB aggregate:

- `Qwen/Qwen2.5-1.5B-Instruct`, revision `5fee7c4ed634dc66c6e318c8ac2897b8b9154536`: `tokenizer.json`, `tokenizer_config.json`, `vocab.json`, `merges.txt`, `config.json`, `LICENSE`.
- `nomic-ai/nomic-embed-text-v1.5`, revision `541c5a6fadb4da793505a2bb4d3ee910de7f39ea`: `tokenizer.json`, `tokenizer_config.json`, `special_tokens_map.json`, `vocab.txt`, `config.json`.

**Explicit proposed acquisition policy for assets lacking publisher SHA256:** permit bounded retrieval of these exact revision/filename pairs for static review, compute local SHA256/exact size, and compare publisher Git/LFS identity wherever available. A computed hash identifies observed bytes; it is not independent publisher attestation. Preserve `publisher_digest_unavailable` where appropriate. Such bytes remain unapproved for loading until subsequent artifact review/adoption. Do not relabel Git object IDs as SHA256 or a first-observed hash as prior verification. If approval does not cover this policy, do not fetch those assets.

No model-store/private-data reads or user fixtures. This newly proposed full-asset acquisition is additional scope beyond IF-M's metadata-only permission; it requires this package's approval.

## Ordered tasks and acceptance

| ID | Objective / prerequisite | Acceptance and evidence | Status |
|---|---|---|---|
| IF-N1 |After approval, freeze inputs and shared accounting |Clock, complete phase/HTTP/output reservations and preservation manifest persisted before optional work; no old epoch reopened |Pending approval |
| IF-N2 |After N1, implement only a small stdlib inspection aid test-first |Meaningful failing cases then passing focused suite/Ruff and a caught guard mutation; no network/candidate imports during fake tests |Pending N1 |
| IF-N3 |After N2, collect bounded public metadata and statically inspect exact files |Registry/payload identity, wheel METADATA/RECORD/notice findings and asset size/hash manifest; honest version/graph/provenance gaps; no installation |Pending N2 |
| IF-N4 |After N3 or bounded stop, review and close |Source-linked findings, artifact distinctions, preserved old evidence, budget/link/diff/checkpoint checks and separate results/source commit request |Pending N3 |

Potential new authored files: `tests/evals/spikes/tokenizer_static_review.py` and `test_tokenizer_static_review.py` only. Review the existing `sqlite_vec_artifact.py` patterns without changing/importing its old controller or opening its closed epoch; reuse only independently reviewed, context-appropriate patterns. Avoid a general downloader framework or a full copy of that script. No product code or source changes outside these two aids. Documentation-only preparation does not create them.

Tests must cover request precharge/closed epochs, interrupted receipt writes, exact host/path/version identities, redirect/cap/size/hash failures, partial files, reparse/traversal refusal, duplicate/unsafe ZIP members, decompression limits, RECORD integrity, wheel name/version/dependency markers and missing publisher-digest distinctions. All fake tests use local synthetic bytes/injected transports; no sockets/native candidate code. At most6focused test invocations including red/green/mutation/regression, plus2Ruff invocations; all count in the same shared allocation. Do not weaken tests to fit the budget.

## Metadata, release and dependency review

Use fixed Tokenizers publishing commit `301277072263fb3830eb66eec7e47adadf76f1dc` and displayed Hub publishing commit `178e1a1797858724c79fd9d12d79d0902d730497`. Inspect the relevant pinned release workflow/version-setting source and final wheel METADATA to explain2.4.0versus2.4.0.dev0 if supported. No guessed new tags, newer versions or dependency omission. This package explicitly permits one fresh metadata request for a previously unavailable source where needed; IF-M itself remains closed. No automatic retry within this package.

Compare Python3.14/Windows AMD64 requirements against the unchanged lock. Review at most **20 runtime distribution names**, including existing applicable packages, rather than IF-M's12-name ceiling; the previous graph was not closed. Record exact candidate versions/artifact metadata and markers where available. This is a proposed bounded graph-review increase, not permission to install20packages. No resolver/build execution or lock editing. If the graph cannot be closed within scope, stop expansion and report the omitted boundary.

Review publisher/native license/notice and known advisory evidence for the identified versions, without declaring unexamined Rust/binary dependencies safe. Record whether local-only loading APIs can avoid Hub/network paths; do not execute them. No source-to-wheel equivalence or vulnerability-free claim from RECORD/registry hashes alone. A version mismatch may have a release-workflow explanation; do not infer maliciousness without evidence.

## Connected static execution and acquisition limits

Public web research: at most **14 visible calls /42 explicit targets**, short/medium responses. Eligible primary domains: `pypi.org`, `github.com`, `api.github.com`, `raw.githubusercontent.com`, `huggingface.co`, `docs.ollama.com`. Include failures/navigation/duplicates in precharged counts. Provider-internal fetches/redirects/bytes/RAM remain opaque.

The owned stdlib acquisition aid may make at most **48 HTTP transactions including redirects**, shared across metadata and13payloads. HTTPS only; exact public artifact paths, no credentials/query secrets, proxy/environment inheritance or custom endpoint. Approved acquisition hosts: `pypi.org`, `files.pythonhosted.org`, `huggingface.co` only. Maximum2validated redirects per logical fetch, charging each before submission; no downgrade/new host. Refuse unexpected hosts/private addresses, validate resolved addresses, and document DNS check/use limits. No alternative transport or automatic failed-fetch retry. Use existing trusted TLS defaults; never disable verification.

Bound metadata bodies to1MiB each/8MiB aggregate and wheel bodies to the table limits. Total accepted HTTP bodies at most **28MiB** (6MiB wheels+14MiB assets+8MiB metadata), with conservative reservations persisted before requests and no refunds. For each asset, reserve its exact publisher-declared size plus a charged overflow probe within the aggregate allowance; if unavailable, reserve the full per-file maximum or stop when the aggregate cannot cover it. Charge redirect/error bodies and overflow probes too; rejected transfers do not restore the allowance. Use bounded streaming reads, exact-size/hash checks where expected, no overwrite of existing outputs, and mark incomplete artifacts unusable. Disable automatic content decoding/redirects that evade accounting. Raw bodies are untrusted data, never scripts to execute.

No wheel extraction to executable/import paths. Inspect in memory with at most2,000members/wheel,16MiB/member and32MiB aggregate decompressed bytes across both wheels; reject duplicate names, links, traversal, encryption and unsupported structures before reading members. Verify RECORD hashes/sizes where required; record declared exclusions. Keep reports content-free apart from public metadata/license/source observations; do not log tokenizer vocabularies or full configuration/templates.

Use the existing stdlib interpreter in isolated mode, with no dependency installation, environment/PATH/policy changes or saved PowerShell-script bypass. One direct owned inspection worker maximum, supervised to completion with retained process identity; account for controller/console descendants. Acquire/inspect within300seconds, per-request timeout10seconds, then bounded30-second teardown; all included in package time. No service or candidate subprocess. Uncertain teardown stops work and must be reported.

This is a connected public-artifact/static-only boundary, with **no filesystem/outbound confinement or kernel RAM-cap claim**. Files remain under the configured ignored review root. Host permission requirements remain distinct from project approval. Any required escalation must name this exact operation; do not silently change transports, scope or execution policy.

## Shared accounting and stopping rules

After approval only: ignored `data/t17/input-fit-tokenizer-static-01/`. **128prepaid conservative units:104normal/24protected**: initialization8, public research28, helper/test work32, acquisition16, review12, close8, protected24. All wrappers, shell/interpreter/test/lint, positive/negative/control/acquisition/cleanup/check operations share these blocks. Separately approved Git actions are outside this epoch. At mostoneactual acquisition/inspection worker; no retry/reset/reseal after stop. Partial independent metadata may be reported; no artifact/version substitution.

**1,800active seconds /32MiB new local outputs** including quarantined files, temporary copies, fake artifacts, reports and receipts. Avoid full-body duplicate staging. Preserve AGENTS/SPEC/pyproject/lock, corrected metadata source/test files and IF-K meter/summary, IF-L meter/ledger/findings/comparison, IF-M meter/ledger/manifest/findings/parity design and the old sqlite-vec aid/test. Hash-check at closure. Reserve protected units solely for preservation/partial closeout, never more optional downloads/tests.

Stop on any applicable cap, publisher/hash/size/path mismatch, unsafe archive, unsupported metadata, host denial or deadline. A documented source-version difference may proceed only to its already-approved static reconciliation; unresolved mismatch prevents adoption and further dependent provisioning. New dependency versions/assets/hosts, broader execution or another acquisition attempt require a new decision. No cloud/user-data submission, candidate imports, local model API calls, inference, application implementation or G2 adoption.

## Deliverables and approval request

After approval, deliver `docs/benchmarks/input-fit-tokenizer-static-review.md`, local exact-byte manifest/inspection/ledger/teardown receipts, the two reviewed stdlib aids and affected dependency/preflight/parity/PLAN/TODO/README/checkpoint updates. Separate verified file identity from publisher attestation, source declarations from actual wheel metadata and static review from native parity. Do not promise all trust/oracle blockers will be resolved by acquisition.

Requested now: approve IF-N1–N4, including the explicit static-download trust policy and connected execution limits, and separately commit the five proposal/status documents. This one approval covers the ordered routine work. Installation, native/runtime trial, dependency/runtime adoption, later source/results commits and stage transition retain separate gates.
