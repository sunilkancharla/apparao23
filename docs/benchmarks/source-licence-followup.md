# T17-IF-SLR — response capture verified; source/licence decisions remain

## Outcome

The user approved SLR1–SLR6 and planning commit **`a382e7e`**. The [approved package](../proposals/source-licence-followup.md) completed both response controls and all four public calls/12 targets. All four admitted response files were retained and checked before excerpts; no processing correction, lost response or automatic retry occurred. **No installation, candidate import, native/model run, runtime adoption or stage transition.** The passed [RRC local checks](remaining-artifact-readiness-continuation.md) were not rerun.

| Task | Evidence / result |
| --- | --- |
| SLR1 | Fresh root; 11 fixed and eight protected identities matched before optional work. |
| SLR2 | Expected behavioural RED demonstrated lost recovery under the old ordering. GREEN passed 23 assertions, including seven UTF-8 vectors, exact response boundary/over-cap refusal, JSON round-trip, display withholding, same-response recovery and bad-order mutation detection. No real web call in either control. |
| SLR3 | Saved publisher URLs, exact artifact identities, prior failed endpoints and metadata-only timing deferral retained in `triage.json`. |
| SLR4 | Four calls/12 targets; four complete serialized response files, 84,310 bytes including file newlines. One source endpoint returned a cache miss; another source view returned a header without licence text. No unretained response used as evidence. |
| SLR5 | Consolidated decision matrix below; no source-pin substitution, automatic research retry or unconditional provisioning recommendation. |
| SLR6 | Final identity/scope/link/whitespace/diff/index/resource/ownership checks and non-null receipt retained in the ignored root. Results commit requires separate user approval. |

The controls are workflow checks, not application accuracy, tokenizer parity or offline tests. The new handler stores raw results before processing, uses the previously successful standard JavaScript code-point counter, and measures the serialized representation. TextEncoder/Buffer/Node dependencies were not used. The intermediate conversation store is a recovery aid; admitted local response files and their identities are the retained evidence.

## Findings and limits

**Tokenizers 0.23.3:** the version-specific PyPI page supplies an Apache licence classification. This fills the earlier missing publisher-classification observation; it does not identify an SPDX version or prove which native/vendor notices accompany the inspected Windows wheel. [PyPI version metadata](https://pypi.org/project/tokenizers/0.23.3/).

The publisher page links to the Rust implementation repository, whose moving-branch view lists a licence file. Following that link returned a file-view header without licence contents. The tool reported cached moving-branch content, not a source revision bound to this wheel. Consequently **exact licence terms and native/vendor completeness remain unverified here**. Zero selected notices in the earlier wheel inspection still does not mean no legal obligations. [Publisher-linked source view](https://github.com/huggingface/tokenizers/tree/main/tokenizers), [licence-file view](https://github.com/huggingface/tokenizers/blob/main/tokenizers/LICENSE).

**HF-Xet 1.8.0:** PyPI's artifact/provenance projection names `hf_xet-1.8.0-cp38-abi3-win_amd64.whl` and SHA-256 `92188598dedc1e1f5609bd718d4db8687a6c89915553912571e2f587892eecec`, matching the retained artifact identity. Its publishing configuration points to commit **`e551f0a75f989b8ee1a474c5f83c80ad4903f84d`**, `release.yml`, and run **`41036139993`**. This is the registry's publisher claim, not independent signature verification or proof of all build inputs. Apache-2.0 remains the publisher declaration. [PyPI artifact metadata/provenance](https://pypi.org/project/hf-xet/1.8.0/).

The pinned workflow fetch returned a cache miss; it was not retried. Build checkout details and native/vendor notices therefore remain unknown. A publishing revision must not silently become the approved build-source pin. [Publisher-linked workflow](https://github.com/huggingface/xet-core/blob/e551f0a75f989b8ee1a474c5f83c80ad4903f84d/.github/workflows/release.yml).

**FSSpec 2026.9.0:** the version page remains consistent with the retained BSD-3-Clause declaration. The exact-digest lookup did not yield a matching artifact/publisher record in the returned projection. Historical releases' provenance labels are not evidence about the selected 2026.9.0 wheel. No new exact-artifact publishing linkage was established, and this is not proof that such evidence does not exist. [PyPI version page](https://pypi.org/project/fsspec/2026.9.0/).

**Hub 2.4.0:** retain the earlier publisher observation `178e1a1797858724c79fd9d12d79d0902d730497` / `release.yml` / run `40902019488`, separately from release observation `3739729b86489e4ae28b5a62e622be320b141493`. This package did not establish their build relationship or retry the known inaccessible comparison/workflow/log/metadata endpoints. The approved metadata-only source-mapping timing deferral is unchanged. [Retained source-coordinate findings](hub-source-coordinate-review.md), [original PyPI artifact reference](https://pypi.org/project/huggingface-hub/2.4.0/#files).

All web observations are parsed publisher/registry page projections with their retrieval/cache context, not independently reproduced builds or an exhaustive licence/security audit. Missing text, a cache miss or an unsuccessful digest lookup does not establish absence or an artifact mismatch. No new artifact digest or version was substituted.

## Consolidated decision matrix

| Topic | Established | Remaining gap / affected action |
| --- | --- | --- |
| Response handling | Seven known UTF-8 vectors and 23 GREEN assertions; four admitted responses retained and identified | No remaining orchestration blocker observed in this package; this does not prove other hosts or future responses. |
| Tokenizers | Version-specific Apache classification and publisher-linked source location | Exact licence terms and native/vendor notices remain necessary evidence or an explicit scoped decision before affected provisioning/adoption. |
| HF-Xet | Retained wheel digest agrees with PyPI's named publisher record | Workflow/build inputs and native/vendor notice completeness remain unresolved; no native-runtime adoption. |
| FSSpec | Retained BSD-3-Clause/selected-notice evidence and current publisher metadata | Exact-artifact publisher/source linkage remains unknown; preserve the approved source-mapping timing and identify it at the affected adoption gate. |
| Hub | Existing publishing and release roles remain separate | Build-source relationship remains an adoption condition under the existing timing deferral; not an invented blocker for metadata-only review or an installation waiver. |

**Recommended next decision:** keep the affected artifacts on hold for unconditional installation/adoption and prepare one narrowly scoped, artifact-level licence/vendor-notice review for Tokenizers/HF-Xet. It should define exact source/notice artifacts and provenance expectations before any new acquisition or execution, and conclude with a dependency decision. Carry the named FSSpec/Hub source conditions forward under the approved timing rule. Do not automatically schedule another identical web-search round.

The user may instead defer the independent-tokenizer dependency route and request an alternative counting-design review. Any trial-specific residual-risk exception must state its exact unresolved evidence, permitted action and limits; it cannot be inferred from this report. No alternate design or exception was selected here. Provisioning, ABI/native loading, model-input/tokenizer parity, offline operation and runtime adoption still need their own approved packages and evidence.

## Accounting, preservation and ownership

Ignored root: `data/t17/source-licence-review-01/`. Evidence includes immutable ledgers, input/preservation identities, authored control definitions/helper, RED/GREEN outcomes, triage, four request/admission/response identity records, complete serialized responses, Git diff/checks and final non-null `summary.json`. Each response was written through structured file arguments, parsed locally, byte-count checked and SHA-256 identified before excerpts. This is workflow identity evidence, not cryptographic attestation by the web publisher.

| Response | Retained bytes | SHA-256 |
| --- | ---: | --- |
| 01 | 27,627 | `ca26c5a79f4f62872f9899da3d6bb617c2e7657bdaac33f2d13b5e7bd6d60c11` |
| 02 | 21,690 | `9f08ea2b85a51683f95bd3bb4c96413f16090b09e95d9b75267769ab700359b3` |
| 03 | 12,472 | `8bbcda72f46e71767927e96f448d46b18154a289f7a0ada7f9a38f5912d7ee1a` |
| 04 | 22,521 | `8ce8367b83c38648e6f8f78d04d91757f0ca453247d2d66dce282a29cf4e1152` |

All 24 units and the 16-start allowance remain prepaid/non-refundable; actual owned starts and final elapsed time are in the summary. Four calls/12 targets and both control invocations are used; no renewed allowance or automatic retry. Explicit read/report reservations are not measured OS/interpreter I/O or actual output totals. The 32 KiB reporting allocation and 8 KiB closure reserve remain charged, but a complete aggregate emitted-text counter was not retained; do not present the prepaid ceiling as fully measured reporting compliance. Complete raw web envelopes are retained as artifact evidence rather than printed. Native command streams, ownership and final scope checks belong to the closeout receipt.

Only public package/version/digest/source identifiers were sent; no document/prompt/answer, private path, lock/graph text or machine identifier. No candidate payload, model or repository archive was downloaded/read, no package was installed/imported, and no historical graph/model/capture worker ran. Native activity is limited to local metadata/identity and Git checks, with exit evidence; no server/worker required teardown. No confinement, kernel egress or machine-wide audit is claimed.

Preserve AGENTS/SPEC/project/lock, versioned evaluation source/manifests, old reports/proposals/roots, historical checkpoints and unrelated user files. The seven authored result documents require a separate commit decision; this report does not authorize a next package or adoption.
