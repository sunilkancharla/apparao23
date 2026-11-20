# T17-SV2 — exact dependency review and tokenizer validation status

## Result

The user authorized completing dependency/input-fit work and its commit without another project-approval request. [Scope and limits](../proposals/t17-standalone-validation-closeout.md). Standalone Hugging Face Tokenizers remains the selected direction; Ollama remains the inference service.

**The static dependency checks below passed, but items 1 and 2 are not fully finished.** Existing build-source/native-notice prerequisites remain unresolved. Consequently no candidate was installed or imported, and no new standalone-versus-Ollama parity trial ran. This is an evidence blocker, not a detected tokenizer malfunction or a new request for routine approval. It must not be reported as successful provisioning or G2 readiness.

## What was verified now

| Check | Observed result |
| --- | --- |
| Ten cached exact wheels | All expected whole-file sizes and SHA-256 values match; 8,543,604 bytes total. |
| Wheel contents | 470 listed payload hashes verified; nine wheels contain selected notice files, Tokenizers contains none. No `.pth`, `sitecustomize.py` or `usercustomize.py` startup hook was found. |
| Seven reused distributions | 158 installed payload hashes verified against their own RECORDs, totaling 2,005,208 bytes. Only the seven RECORD files themselves lack hashes. This is internal integrity evidence, not independent publisher attestation. |
| Full dependency graph | All 17 nodes and 19 active requirements resolve to the retained exact versions; 242 extra/platform requirements are inactive for this profile. No dependency was omitted. |
| Actual environment | Windows 11, AMD64, regular CPython 3.14.6. All ten wheel tags and Python-version declarations fit this environment. Tags do not prove native imports work. |
| Current registry identity | All ten wheel filenames, sizes and digests match the fresh PyPI version records; none of those selected files is marked yanked. |
| Advisory metadata | All 17 exact PyPI version responses returned empty vulnerability lists. This is registry coverage only, not a complete native/transitive security audit or a guarantee of safety. |
| Exact publisher records | Three retained PyPI attestations name the selected Tokenizers, Hub and HF-Xet wheel filenames and their exact SHA-256 values. All are publication statements with a null predicate; none supplies build inputs or a compiled-component inventory. Signatures/transparency proofs were not independently verified. |

Fresh public records: [Tokenizers](https://pypi.org/pypi/tokenizers/0.23.3/json), [Hub](https://pypi.org/pypi/huggingface-hub/2.4.0/json), [HF-Xet](https://pypi.org/pypi/hf-xet/1.8.0/json). The other fourteen exact-version URLs and complete responses are retained locally. The exact [Tokenizers publication statement](https://pypi.org/integrity/tokenizers/0.23.3/tokenizers-0.23.3-cp310-abi3-win_amd64.whl/provenance), [Hub publication statement](https://pypi.org/integrity/huggingface-hub/2.4.0/huggingface_hub-2.4.0-py3-none-any.whl/provenance) and [HF-Xet publication statement](https://pypi.org/integrity/hf-xet/1.8.0/hf_xet-1.8.0-cp38-abi3-win_amd64.whl/provenance) support publisher identity, not a reproduced build.

## Exact retained graph

These are evaluation candidates/reuse pins, not a new runtime adoption. Existing HTTPX 0.28.1 remains separate from HTTPX2; no baseline package was replaced.

| Distribution | Version | Licence evidence / native notes |
| --- | --- | --- |
| tokenizers | 0.23.3 | Publisher Apache-2.0 classification/root-source licence; no selected wheel notice; native `.pyd`; notice/build closure remains open. |
| huggingface-hub | 2.4.0 | Apache-2.0 declaration and selected notice; pure-Python wheel; publishing/build-source relationship remains open. |
| hf-xet | 1.8.0 | Apache-2.0 declaration and selected notice; native `.pyd`; bundled-native/build scope remains open. |
| httpx2 | 2.16.2 | BSD-3-Clause declaration and selected notice; no listed native member. |
| httpcore2 | 2.16.2 | BSD-3-Clause declaration and selected notice; no listed native member. |
| anyio | 4.16.0 | MIT declaration and selected notice; no listed native member. |
| click | 8.5.1 | BSD-3-Clause declaration and selected notice; no listed native member. |
| filelock | 4.2.10 | MIT declaration and selected notice; no listed native member. |
| fsspec | 2026.9.0 | BSD-3-Clause declaration and selected notice; exact artifact/build-source linkage remains unestablished. |
| truststore | 0.10.5 | MIT declaration and selected notice; no listed native member. |
| idna | 3.20 | Reused installed BSD-3-Clause metadata and verified RECORD. |
| typing-extensions | 4.16.0 | Reused installed PSF-2.0 metadata and verified RECORD. |
| h11 | 0.16.0 | Reused installed MIT metadata and verified RECORD. |
| packaging | 26.3 | Reused installed Apache-2.0 OR BSD-2-Clause metadata and verified RECORD. |
| pyyaml | 6.0.3 | Reused installed MIT metadata and verified RECORD; includes a CPython 3.14 Windows AMD64 native extension. |
| tqdm | 4.70.1 | Reused installed MPL-2.0 AND MIT metadata and verified RECORD. |
| colorama | 0.4.6 | Retained BSD-family review; new metadata has no licence expression/text field; installed RECORD verified. |

The exact cached-wheel hashes remain in the linked [artifact findings](wheel-artifact-review-reporting-correction.md) and their admitted manifest, plus the original Tokenizers/Hub identities. The fresh reconciliation binds those same hashes to current registry records. No substitute artifact or version was selected.

## Source findings and installation disposition

The previously requested root Cargo lockfile was not found. The lockfile **does exist under `bindings/python/Cargo.lock`** at the recorded Tokenizers release revision. Its binding manifest declares the expected version and stable-ABI feature. The release workflow includes Windows wheel builds with locked Cargo resolution. This narrows the source/ABI review, but does not establish that the selected binary contains exactly that source/dependency set or supply its bundled notices. [Binding lockfile](https://raw.githubusercontent.com/huggingface/tokenizers/301277072263fb3830eb66eec7e47adadf76f1dc/bindings/python/Cargo.lock), [binding manifest](https://raw.githubusercontent.com/huggingface/tokenizers/301277072263fb3830eb66eec7e47adadf76f1dc/bindings/python/Cargo.toml), [release workflow](https://raw.githubusercontent.com/huggingface/tokenizers/301277072263fb3830eb66eec7e47adadf76f1dc/.github/workflows/python-release.yml).

The release-tagged FSSpec source licence agrees with its BSD-3-Clause declaration; it does not identify the exact wheel's build inputs. [Source licence](https://raw.githubusercontent.com/fsspec/filesystem_spec/2026.9.0/LICENSE). Hub/HF-Xet workflow/source requests did not yield the missing build relationship. Failed access is not proof that the evidence does not exist.

Maintain the existing installation hold from [ALN](artifact-licence-notice-review.md) and the Hub/FSSpec source-mapping conditions. This review found no new basis to declare complete native/vendor notice coverage. Current authorization covers the work and commit; it does not fabricate missing records or establish legal/security facts. No requirement for a commercial licence was found or asserted.

**The precise remaining dependency work is publisher/build-source evidence and applicable compiled-component notices, not another version-range/graph/RECORD audit.** Avoid repeating the successful checks or reopening the chosen tokenizer direction. Matching signatures or publication subjects alone would still not supply a missing compiled-component inventory.

## Input-handling disposition

The existing 21 metadata/FP contract tests and eleven packaged-reference count matches remain valid with their original limits; they were not rerun or relabelled as new passes. All [FP01–08 and NP01–08 requirements](../proposals/input-fit-tokenizer-parity-validation.md) remain tracked.

| Group | Current evidence and missing result |
| --- | --- |
| FP01–08 | Existing evaluation-only fake-contract coverage; no application admission endpoint. |
| NP01–04 | Prior vocabulary/merge mapping and packaged-reference observations; actual installed standalone IDs, selected Ollama rendering and special-marker/branch parity remain unexecuted. |
| NP05 | Prior Nomic vocabulary representation and reference count checks; standalone normalization/prefix/CLS/SEP parity remains unexecuted. |
| NP06 | Local refusal arithmetic exists; live below/equal/above capacity, verified 192-output/EOS reservation and truncation semantics remain unexecuted. |
| NP07 | Existing fake lifetime/drift/cancel controls; complete owned-runtime lifetime/publication matrix remains unexecuted. |
| NP08 | Earlier synthetic local trials remain supporting evidence; no new installed standalone cold/warm or disconnected complete-path trial. |

No native group is newly passed. Provisioning and native parity depend on the unresolved artifact prerequisites. The physical 16 GB target/proxy issue remains separate and unchanged; G2 is still Proposed and T18 has not begun.

## Verification and delivery

Ignored evidence: `data/t17/standalone-closeout-02/`, including full current registry/provenance responses, exact decoded publication statements, wheel reconciliation, reused RECORD/graph results, scripts and shared ledger. No model, user document, prompt or answer was sent externally. A first sandbox network request failed with WinError 10013; the host-approved bounded rerun succeeded. One local review command used the Windows default text encoding and failed; explicit UTF-8 corrected the read, and all ten registry matches/three publication subjects then passed. Neither issue was a package defect.

The shared allocation includes 24 public calls and 33 targets, including the failed network attempt; research is closed without a counter reset. New authored changes are documentation only. Eight documents, 540 local links, UTF-8/whitespace, the empty index and four protected files passed the closeout checks; readable tracked diffs and new documents were reviewed. Two initial multi-file patches refused unmatched context before changing files; corrected exact-context patches succeeded. No artificial application tests, new runtime code, installation, model launch, environment/lock change, G2 adoption or checkpoint was introduced. Final start/time/scope and approved scoped-commit evidence belong to the ignored closure receipt.
