# T17-IF-AR — retain the current release; decide the evidence gate

## Recommendation and approval needed

**Keep Hub 2.4.0 as the research baseline. This review found no demonstrated benefit from downgrading to 2.3.0 or 2.2.0.** None has been runtime-tested here; published release status is not a stability benchmark. The [approved AR package](../proposals/stable-tokenizer-alternatives-review.md) was committed as `e1a1571` and ran in fresh ignored `data/t17/stable-alternatives-review-01/`.

Request this specific decision before further dependent work:

> Defer exact Hub build/source mapping as a prerequisite **only for the next metadata, notice, advisory and dependency review** of the already verified 2.4.0 artifact. Use the displayed registry publisher link as publication evidence. Keep build-source mapping explicitly unresolved for the later adoption decision. Do not infer runtime behavior from unbound source code or authorize installation, execution, adoption or G2.

**Approved by the user on 2026-11-17**, together with the seven-file results commit and preparation of the next bounded review proposal. The deferral applies only before metadata/notices/advisory/dependency review; exact build-source mapping remains unresolved for the later adoption decision. It authorizes no installation, execution, source-pin substitution, runtime adoption or G2. No SPEC requirement or persistent rule was changed. Earlier proposal wording above is retained as the exact decision approved.

## Why the review stopped

[SPEC](../../SPEC.md) calls for a reproducible lockfile and dependency review. The immediate halt is explicitly in the approved [HS package](../proposals/hub-only-static-review.md), which stops expansion on a necessary unresolved provenance link. [SC findings](hub-source-coordinate-review.md) established the registry's exact-wheel publishing identity, but did not establish the source revision built. A reproducible lockfile, a publisher claim, source mapping and an independently reproducible build are distinct evidence. This report proposes changing the timing of that package-specific gate; it does not claim any missing evidence was obtained or erase the approved halt.

| Evidence | Current baseline status |
| --- | --- |
| Published release | 2.4.0 is marked Latest in the official release history. |
| Exact artifact integrity | HS verified its wheel identity and RECORD. No payload reread in AR. |
| Publishing identity | SC recorded PyPI's displayed publisher claim for that checksum. |
| Independent signature verification | Not performed. |
| Exact build/source relationship | Unresolved; publishing and prior release coordinates retain separate roles. |
| Runtime stability, Windows/native behavior and offline operation | Not established by this review. |
| Dependency/security readiness | Full graph, native notices, affected/fixed ranges and later trial gates remain open. |

## Bounded candidate comparison

The official history lists 2.3.0 and 2.2.0 before the current release. Both fit the reviewed Tokenizers 0.23.3 requirement `huggingface-hub>=0.16.4,<3.0`; this is declared-range compatibility, not a tested integration. [Release history](https://github.com/huggingface/huggingface_hub/releases).

| Candidate | Published evidence reviewed | Compatibility and dependency implications | Decision |
| --- | --- | --- | --- |
| **2.4.0 baseline** | Latest official release; exact wheel/static integrity and displayed publisher-origin evidence already recorded in HS/SC. | Existing metadata declares Python>=3.10 and Apache-2.0. Direct runtime/native/transitive and parity work remains unfinished. | Retain baseline; no runtime adoption. |
| **2.3.0 alternative** | Normal release tag; registry JSON explicitly reports `yanked:false`. Version page declares Apache-2.0 and Python>=3.10. | Tagged setup retains `httpx2>=2,<3` and `hf-xet>=1.6,<2`, so it does not remove those dependency families. Exact candidate wheel and source/build binding were not validated. | No demonstrated reason to replace baseline. |
| **2.2.0 alternative** | Normal release tag; registry JSON explicitly reports `yanked:false`. Version page declares Apache-2.0 and Python>=3.10. | Same HTTP/native-transfer families remain in tagged setup. This is source intent, not verified wheel behavior or a Windows/native guarantee. | No demonstrated reason to replace baseline. |

Version-specific sources: [2.3.0 release](https://github.com/huggingface/huggingface_hub/releases/tag/v2.3.0), [2.3.0 registry](https://pypi.org/pypi/huggingface-hub/2.3.0/json), [2.3.0 package declaration](https://pypi.org/project/huggingface-hub/2.3.0/), [2.3.0 tagged requirements](https://github.com/huggingface/huggingface_hub/blob/v2.3.0/setup.py); [2.2.0 release](https://github.com/huggingface/huggingface_hub/releases/tag/v2.2.0), [2.2.0 registry](https://pypi.org/pypi/huggingface-hub/2.2.0/json), [2.2.0 package declaration](https://pypi.org/project/huggingface-hub/2.2.0/), [2.2.0 tagged requirements](https://github.com/huggingface/huggingface_hub/blob/v2.2.0/setup.py).

The two alternatives were selected only for comparison as preceding normal release tags in the same major line. No alternative artifact was acquired; exact wheel hash/size and full candidate dependency closure were not established from the returned projections. A generic Python wheel tag does not validate native transitives on Windows. All three still need the appropriate license/native/offline/resource/parity review before adoption.

The [official advisory index](https://github.com/huggingface/huggingface_hub/security/advisories) was retrieved, but version-specific affected/fixed ranges and complete transitive coverage were not established. No security-clearance or older-is-safer claim is made. Eleven distribution names were used for context, within the twelve-name ceiling; optional extras were not selected.

## Execution and limitations

- AR1 passed durable bootstrap, immutable append/fresh-selection/negative controls, seven known UTF-8 cases, output boundary and string/object/oversized-response handling. Twenty-six small identities were frozen before review.
- AR2 traced the current gate and separated the evidence categories. AR3 completed a bounded comparison with the unknowns above. AR4 recorded the recommendation and closure evidence; the user subsequently approved the narrow timing deferral described above.
- Six web calls covered 21 targets. Public responses were preserved before bounded, explicitly selected output. Some registry projections omitted fields; attempted local JSON classification was recorded as unparsed rather than treated as valid metadata. Later source finds exposed the non-yanked values. No failed target was refetched or transport substituted.
- No application tests/Ruff, candidate payload read/download/import, worker/service, installation, model/API/native trial, build, environment/PATH/lock change, application implementation, runtime adoption or stage transition occurred. Inline workflow controls/static command parsing are not runtime tests.
- Actual allocation/artifact/reporting/read totals, source/control records, static final-command identity and final seven-file delivery hashes remain in the ignored review root. No controlled reporting/accounting failure was observed; provider envelopes are not claimed kernel-bounded.

## Next step

The user approved preparation of a bounded metadata/dependency/notices/advisory review for the unchanged 2.4.0 candidate, carrying the unresolved source item forward explicitly. The new package's execution still needs approval. Installation, native/parity execution and adoption require later concrete packages/decisions; do not automatically downgrade or repeat research.

Closure checks passed: 24 frozen identities unchanged, two exact historical baseline suffixes, 438 local links, exact six tracked updates plus this new report, empty index, whitespace and ignored runtime-root checks. Readable tracked/new-file diffs retained and reviewed; exact final command passed static parsing. Final delivery hashes and resource totals remain local.

The seven-file results commit and timing decision were approved. Stage 1 PDF/XLSX/CSV, OCR/privacy and the 16 GB CPU-only target remain unchanged.
