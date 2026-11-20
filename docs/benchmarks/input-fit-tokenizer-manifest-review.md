# T17-IF-M — tokenizer manifest review

## Outcome — 2026-11-16

Completed the approved [metadata/design package](../proposals/input-fit-tokenizer-manifest-review.md), proposal commit `6b67433`. **The manifest is partial and is not ready for acquisition or installation.** No tokenizer/model/native code was loaded, no full asset/binary/archive was downloaded and no private/model-store content was read. [The validation design](../proposals/input-fit-tokenizer-parity-validation.md) records the next proof obligations, without an executable trial permit.

Research stopped at **10 visible web calls / 37 explicit targets**. The Hub publishing-source version could not be reconciled with its advertised release. Do not silently choose another Hub release, modify dependency declarations or install without dependencies. This is an unresolved provenance/packaging question, not a finding that the release is malicious. Existing standalone-direction approval remains conditional; G2 stays open.

## Partial acquisition manifest — metadata_only / not_downloaded

Every row below is publisher/registry metadata. No downloaded-byte hash or cached-GGUF/tokenizer parity has been verified. Displayed sizes are rounded; exact sizes and direct distribution download URLs remain acquisition blockers. Model resolve locators can be constructed from publisher/full revision/filename, but only the configuration pages below explicitly displayed their resolve URL; the other endpoints have not been requested or validated.

### Distribution candidates

| Candidate | Filename / displayed size | Registry SHA256 | Evidence and status |
|---|---|---|---|
| Tokenizers0.23.3 |`tokenizers-0.23.3-cp310-abi3-win_amd64.whl`,2.9MB |`1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3` |[Version-specific registry page](https://pypi.org/project/tokenizers/0.23.3/); agrees with IF-L; regular ABI3 Windows x64 candidate, not an import test |
| Hub2.4.0 |`huggingface_hub-2.4.0-py3-none-any.whl`,857.0kB |`42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801` |[Observed registry page](https://pypi.org/project/huggingface-hub/); source/release reconciliation blocked |
| HTTPX2 2.16.0 |`httpx2-2.16.0-py3-none-any.whl`,97.9kB |`fd2c5d7909e8d86fe92d53020c310ca0e4e431b838c207c5754b9bbf0308d49a` |[Observed registry page](https://pypi.org/project/httpx2/); newly declared dependency candidate, not a replacement for locked HTTPX |

Tokenizers' page reports Trusted Publishing/source commit `301277072263fb3830eb66eec7e47adadf76f1dc`; Hub's page reports `178e1a1797858724c79fd9d12d79d0902d730497`. These are displayed provenance claims, not independently verified attestations or wheel payload attestations by this review. HTTPX2's page identifies Pydantic's repository and BSD-3-Clause/Python>=3.11, with no file provenance displayed. No native compatibility/security clearance follows from wheel tags.

### Publisher asset snapshots

**Qwen** publisher `Qwen/Qwen2.5-1.5B-Instruct`, full revision **`5fee7c4ed634dc66c6e318c8ac2897b8b9154536`**. The [pinned tree](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/tree/5fee7c4ed634dc66c6e318c8ac2897b8b9154536) lists:

| Filename | Displayed size | Digest status |
|---|---|---|
| `tokenizer.json` |7.03MB |No per-file SHA256/object identity obtained |
| `tokenizer_config.json` |7.31kB |No per-file SHA256/object identity obtained |
| `vocab.json` |2.78MB |No per-file SHA256/object identity obtained |
| `merges.txt` |1.67MB |No per-file SHA256/object identity obtained |
| `config.json` |660bytes |No per-file SHA256/object identity obtained |
| `LICENSE` |11.3kB |Listed, not payload-reviewed in this package |

The [pinned tokenizer configuration](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/blob/5fee7c4ed634dc66c6e318c8ac2897b8b9154536/tokenizer_config.json) declares no automatic BOS, no prefix space and explicit special-token IDs. Its publisher Jinja template is not permission to replace runtime rendering. Configuration and vocabulary requirements need full-byte verification before narrowing the minimum asset set.

**Nomic** publisher `nomic-ai/nomic-embed-text-v1.5`, full revision **`541c5a6fadb4da793505a2bb4d3ee910de7f39ea`**. The [pinned tree](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5/tree/541c5a6fadb4da793505a2bb4d3ee910de7f39ea) lists:

| Filename | Displayed size | Digest status |
|---|---|---|
| `tokenizer.json` |711kB |No per-file SHA256/object identity obtained |
| `tokenizer_config.json` |1.19kB |No per-file SHA256/object identity obtained |
| `special_tokens_map.json` |695bytes |No per-file SHA256/object identity obtained |
| `vocab.txt` |232kB |No per-file SHA256/object identity obtained |
| `config.json` |1.57kB |No per-file SHA256/object identity obtained |

The [pinned configuration](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5/blob/541c5a6fadb4da793505a2bb4d3ee910de7f39ea/tokenizer_config.json) declares lower-casing, BertTokenizer and CLS101/SEP102. Its8192maximum is metadata, not an adopted application context. The tree labels the model Apache2.0 but does not list a root LICENSE file; asset-specific license/notice reconciliation remains open. Custom-code examples are not executed or approved.

Both revision metadata API requests were inaccessible through the web tool. Planned tree/configuration page inspection independently supplied the observations above; no failed API was retried and no alternate transport was used. A repository revision is not a per-file SHA256. Neither a publisher “Safe” badge nor the full revision proves model-store equivalence.

## Dependency and baseline comparison — incomplete

The [pinned Tokenizers project](https://raw.githubusercontent.com/huggingface/tokenizers/301277072263fb3830eb66eec7e47adadf76f1dc/bindings/python/pyproject.toml) declares Python>=3.10 and Hub>=0.16.4,<3.0. Source metadata alone is not wheel METADATA verification. No extras or build dependencies are selected.

Hub2.4.0's displayed publishing commit contains [setup declarations](https://raw.githubusercontent.com/huggingface/huggingface_hub/178e1a1797858724c79fd9d12d79d0902d730497/setup.py), but its [version source](https://raw.githubusercontent.com/huggingface/huggingface_hub/178e1a1797858724c79fd9d12d79d0902d730497/src/huggingface_hub/__init__.py) declares **2.4.0.dev0**. A release-time rewrite may explain this; it was not established here. Stop this candidate branch before treating those declarations as final release metadata. The following is a source-level comparison only:

| Declared runtime requirement | Existing project baseline | Review result |
|---|---|---|
| click>=8.4.2,<9 |8.5.1 |Satisfies declared range |
| packaging>=20.9 |26.3 |Satisfies declared range |
| pyyaml>=5.1 |6.0.3 |Satisfies declared range |
| tqdm>=4.42.1 |4.70.1 |Satisfies declared range |
| typing-extensions>=4.1.0 |4.16.0 |Satisfies declared range |
| filelock>=3.10.0 |Absent |No exact version/artifact approved |
| fsspec>=2023.5.0 |Absent |No exact version/artifact approved |
| hf-xet>=1.6.0,<2.0.0, applicable machine marker |Absent |Windows AMD64 satisfies source marker; additional native artifact review needed |
| httpx2>=2,<3 |Absent; httpx0.28.1 is distinct |2.16.0 observed, full constraints/transitives not resolved |
| tomli>=1.1, Python<3.11 |Not needed on target3.14 |Excluded by source marker |

Twelve distribution names encountered including Tokenizers/Hub and the excluded tomli. The applicable runtime graph contains11known names; it is not closed because nested requirements were not established. No further graph expansion or automatic baseline upgrades occurred. The guessed HTTPX2 `2.16.0` source-tag path returned404; no alternate tag/release was substituted. The moving Hub pyproject inspected earlier is not used as pinned release metadata.

## Native, license, advisory and offline gaps

Tokenizers' [pinned Cargo declarations](https://raw.githubusercontent.com/huggingface/tokenizers/301277072263fb3830eb66eec7e47adadf76f1dc/bindings/python/Cargo.toml) identify a compiled extension, PyO3/ABI3, Rayon/Tokio and other Rust components. Exact built crate graph/features, wheel contents/RECORD/notice coverage and bundled native advisories remain unverified. [Pinned source license](https://raw.githubusercontent.com/huggingface/tokenizers/301277072263fb3830eb66eec7e47adadf76f1dc/LICENSE) is Apache2.0; it does not clear all bundled components.

The [Tokenizers](https://github.com/huggingface/tokenizers/security/advisories) and [Hub](https://github.com/huggingface/huggingface_hub/security/advisories) maintainer advisory pages displayed no published entries. This is not a complete ecosystem/native audit or evidence of vulnerability absence. Hub's pinned license/constants source requests returned cache misses; no retries. Its registry license label is Apache2.0, while payload notices/offline controls remain unverified.

Local `Tokenizer.from_file` is a candidate API from earlier official documentation, not a complete import/outbound audit. Do not invoke `from_pretrained`, Hub login/download/telemetry, custom model code or source installers. Installed disk/RAM, loading latency, actual Python3.14 behavior and offline no-fetch operation remain unmeasured.

## Accounting and closeout

Ignored `data/t17/input-fit-tokenizer-manifest-01/` holds the full80-unit reservation,1,200-second/2MiB clock/output boundary,12preservation hashes and exact10-call/37-target ledger. Research reserved32units for16wrappers/16web calls; actual research used10of each, with all reservations retained and no refunds. The16/48 ceilings were not exhausted; the source/release mismatch closed research early. No further optional research or fallback is authorized in this closed epoch.

Manifest/design, review and closure share their prepaid12/8/4normal blocks;20protected units remain solely for partial closure. Final meter records links/preservation/whitespace/time/output checks. Documentation checks replace application tests here. No host /status or /compact invocation, runtime adoption, dependency/lock edit or application capability is claimed. Results/design/status documents require separate commit approval.

## Recommended next decision

Keep installation blocked. Recommend preparing a narrowly scoped reconciliation package for the observed Hub release/source-version difference, authoritative dependency metadata and exact publisher file hashes/sizes. Do not yet approve an executable parity trial: the complete distribution graph, payload trust and trustworthy runtime token oracle are all unresolved. The following validation document is a requirements matrix, not a prepared or approved execution package.
