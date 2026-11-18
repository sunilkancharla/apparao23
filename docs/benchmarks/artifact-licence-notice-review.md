# T17-IF-ALN — licence terms clarified; native notice/build gaps remain

## Outcome

The user approved ALN1–ALN5 and the four-file planning commit **`a1e3240`**. The [approved package](../proposals/artifact-licence-notice-review.md) verified saved evidence and completed four public calls/12 targets. All four complete tool responses were saved and identified before excerpts. No dependency was installed/imported, no wheel/native/model payload was read or run, and no runtime/application change or adoption occurred.

**Recommendation:** hold unconditional installation/adoption of these artifacts. No further identical source-search continuation is recommended. A user decision is now needed: keep the hold; request a separately bounded trial design explicitly carrying the named evidence gaps; or request a minimal local-file tokenizer design comparison to assess whether Hub/HF-Xet can be excluded. This review neither selects that alternative nor grants a trial-risk exception.

The recommended next preparation is the minimal local-file design comparison: assess dependency reduction before spending more effort on the full candidate bundle. It preserves the conditional standalone-tokenizer direction and makes no promise that the smaller route is feasible. Preparation itself requires a new package decision.

The overall 24 KiB author-controlled display ceiling was retained, but the final optional inspection used part of the 8 KiB protected closeout reserve. Optional work stopped and this deviation is recorded below; full execution-boundary compliance is **not** claimed. Findings already durably retained remain evidence with their stated limitations.

## Task results

| Task | Result / evidence |
| --- | --- |
| ALN1 | Nine fixed/eight protected identities matched; fresh ignored root and shared reservation established. Tested SLR helper identity retained, no helper changes or control reruns. |
| ALN2 | Two exact artifact records reconciled. HF-Xet's saved licence text exactly matches its recorded 11,558 bytes/SHA-256; Tokenizers still has zero selected notices in the saved 31-entry inventory. No archive reread. |
| ALN3 | Four calls/12 targets; four response files, 70,378 bytes including newlines. Eight targets returned source/release/manifest projections; three cache misses and one 404. No retry, lost response or helper correction. Display-reserve deviation after final inspection prevents claiming complete boundary compliance. |
| ALN4 | Per-artifact hold/next-action matrix below; no invented pin, automatic research continuation, risk acceptance or adoption. |
| ALN5 | Nine fixed/eight protected/four response identities, 488 local links, seven-document scope, whitespace, readable diff and empty index checked; non-null summary/resource/ownership evidence retained in the ignored root. Results commit remains a separate decision. |

No new application, model, parity or offline tests ran. The 23 passing SLR response-control assertions and RRC graph/profile evidence are inherited results, not new test passes.

## Tokenizers 0.23.3

The publisher's version-specific release page calls this a Python-only release and links commit **`301277072263fb3830eb66eec7e47adadf76f1dc`**. The followed commit view supplies the full coordinate. GitHub's displayed signature status was not independently verified here. This establishes a release-to-source observation, **not a reproduced mapping from that source to the selected Windows wheel**. [Release record](https://github.com/huggingface/tokenizers/releases/tag/v0.23.3), [linked commit](https://github.com/huggingface/tokenizers/commit/301277072263fb3830eb66eec7e47adadf76f1dc).

At that revision the root licence text identifies Apache License 2.0. The Python binding's Cargo manifest declares version 0.23.3, and its packaging metadata lists licence/version as dynamic alongside an Apache classifier. This improves the earlier classifier-only observation; it does not fill the missing packaged-notice evidence. [Root licence](https://raw.githubusercontent.com/huggingface/tokenizers/301277072263fb3830eb66eec7e47adadf76f1dc/LICENSE), [binding manifest](https://raw.githubusercontent.com/huggingface/tokenizers/301277072263fb3830eb66eec7e47adadf76f1dc/bindings/python/Cargo.toml), [Python packaging metadata](https://raw.githubusercontent.com/huggingface/tokenizers/301277072263fb3830eb66eec7e47adadf76f1dc/bindings/python/pyproject.toml).

The nested `tokenizers/LICENSE` request returned a cache miss; the candidate root `NOTICE` returned 404. Neither proves there are no applicable third-party notices elsewhere. The prior saved wheel inspection still has a native `tokenizers/tokenizers.pyd`, missing licence field and zero selected notices. Exact bundled native/vendor notice completeness and independent wheel/build-source linkage remain unverified. No source revision was adopted as a build pin.

## HF-Xet 1.8.0

The saved artifact licence at `hf_xet-1.8.0.dist-info/licenses/LICENSE` contains Apache 2.0 text and matches SHA-256 **`1eb85fc97224598dad1852b5d6483bbcf0aa8608790dcc657a5a2a761ae9c8c6`**, 11,558 UTF-8 bytes. This checks the retained notice text against its saved artifact observation; it is not a fresh wheel RECORD check.

At the previously observed publisher coordinate **`e551f0a75f989b8ee1a474c5f83c80ad4903f84d`**, the root licence is Apache 2.0 and the workspace manifest states version 1.8.0/Apache-2.0. A Cargo lockfile projection provides source dependency information, not proof of all code compiled into this Windows binary. The returned projection is not treated as an exhaustive lockfile or vendor-notice inventory. [Source licence](https://raw.githubusercontent.com/huggingface/xet-core/e551f0a75f989b8ee1a474c5f83c80ad4903f84d/LICENSE), [workspace manifest](https://raw.githubusercontent.com/huggingface/xet-core/e551f0a75f989b8ee1a474c5f83c80ad4903f84d/Cargo.toml), [lockfile projection](https://raw.githubusercontent.com/huggingface/xet-core/e551f0a75f989b8ee1a474c5f83c80ad4903f84d/Cargo.lock).

The single permitted raw-text workflow alternative and candidate root `NOTICE` both returned cache misses; neither was retried. Checkout/build inputs and native/vendor notice completeness remain unresolved. The coordinate retains its publishing role, not an approved build-source role. [Workflow attempted](https://raw.githubusercontent.com/huggingface/xet-core/e551f0a75f989b8ee1a474c5f83c80ad4903f84d/.github/workflows/release.yml). The [SLR exact-artifact publisher observation](source-licence-followup.md) remains the authority for its registry claim, not an independently verified signature/build.

## Dependency decision and affected actions

| Artifact | Publisher / packaged evidence | Source terms / native inventory | Remaining gap and next-action recommendation |
| --- | --- | --- | --- |
| Tokenizers wheel SHA `1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3` | Version-specific Apache classifier; saved missing licence field/zero selected notices | Release-linked root Apache-2.0 text; Python binding version matches; saved native `.pyd` | Hold unconditional installation/adoption. A bounded trial would need explicit approval carrying the packaged/vendor and build-linkage gaps, or a different dependency approach. |
| HF-Xet wheel SHA `92188598dedc1e1f5609bd718d4db8687a6c89915553912571e2f587892eecec` | Apache-2.0 declaration; saved notice identity checked; retained exact-artifact publisher claim | Publisher-coordinate source licence/manifest agree; saved native `.pyd`; source dependency projection | Hold unconditional installation/adoption. Workflow/build and compiled/vendor scope remain unknown; a separately approved trial design must name these gaps. |
| Hub/FSSpec | Existing retained evidence only; not queried | Existing source-role conditions unchanged | Preserve approved metadata-only timing deferral and affected adoption conditions; no newly invented metadata-review prerequisite or installation waiver. |

Top-level licence identification is stronger evidence now. It is not a comprehensive legal/security clearance, native ABI result, proof of offline behaviour or tokenizer parity. Missing notices do not mean absence of obligations. No need for a commercial licence is asserted by this review, and no permission to omit notices is inferred.

## Accounting, preservation and limits

Ignored root **`data/t17/artifact-notice-review-01/`** retains immutable ledgers, fixed/protected identities, saved-evidence matrix, all four serialized web-tool responses and identity records, decision, readable diff/checks and final summary. Only public package/source identifiers were sent. No documents, prompts, answers, private paths, lock/graph text or machine identifiers were sent externally. Web observations are parsed/cached publisher projections, not independent builds or guaranteed complete source-file downloads.

| Response | Bytes | SHA-256 |
| --- | ---: | --- |
| 01 | 19,841 | `95a6e526405d87b4eb68d25c05f43991ce463292012eaf5a2c8a1f0786347aed` |
| 02 | 12,052 | `d6b67c3fcf2793fa16362e3e99c7b0384803bd65c011f579dd5cdaba59d22209` |
| 03 | 16,790 | `c8cb0700298c8ae5b3580d85f624dc7f93172494579f436f85ea3ea689aaedb5` |
| 04 | 21,695 | `180de52a16633b150ee414fc5275134e549adf44981fac80c351f947777a992b` |

All 24 units, 16-start allowance and 16 MiB explicit-read leases were prepaid/non-refundable; actual starts, elapsed time, retained bytes and displayed-text count belong to the final summary. Reservations are not measured OS I/O or actual use. Author-controlled reporting excludes platform-generated envelopes. The optional inspection crossed its 16 KiB portion of reporting before closeout; the exact shortfall is in ledger 006. No extra allowance was claimed or correction/retry attempted. Decision/closeout used the remaining overall allowance, and the deviation stays visible.

Only local metadata/identity/Git checks ran natively; direct shell exit evidence is retained, with no child worker/server/service to tear down. No containment, kernel egress or machine-wide process audit is claimed. AGENTS/SPEC/project/lock/evaluation sources/manifest/historical checkpoint and old roots remain unchanged; no session-checkpoint file was created. Seven results documents await commit approval. G2, provisioning/native evaluation, runtime adoption and stage transition remain separate gates.
