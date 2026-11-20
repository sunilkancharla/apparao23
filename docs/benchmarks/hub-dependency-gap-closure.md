# T17-IF-GC — identifiers improved; static-inspection proposal next

The [approved GC package](../proposals/hub-dependency-gap-closure.md), committed as `0768aea`, reused MR evidence and made two public calls/eight targets. It identified the normal Windows HF-Xet artifact and both missing publisher checksums/licence declarations. No payload was downloaded or inspected. Installation readiness remains incomplete; the next step is a bounded acquisition/static-inspection proposal.

## New publisher evidence

| Candidate | Declared artifact | Publisher SHA-256 | Size / licence |
| --- | --- | --- | --- |
| HF-Xet1.8.0 | `hf_xet-1.8.0-cp38-abi3-win_amd64.whl` | `92188598dedc1e1f5609bd718d4db8687a6c89915553912571e2f587892eecec` | Displayed3.9MB; Apache-2.0 |
| FSSpec2026.9.0 | `fsspec-2026.9.0-py3-none-any.whl` | `8dd6e646e99ea382bd85f97a45e6b526a442d79423a7dc673f1e2756d05fcb5f` | Displayed221.7kB; BSD-3-Clause |

[HF-Xet version/file details](https://pypi.org/project/hf-xet/1.8.0/), [FSSpec version/file details](https://pypi.org/project/fsspec/2026.9.0/). HF-Xet's selected tag is normal Windows x86-64 ABI3, not the separately listed free-threaded wheel. This is declared platform compatibility, not a load/ABI test. Exact byte counts were not exposed; displayed sizes are rounded.

FSSpec's page states no Trusted Publishing/provenance metadata for these files and declares Beta maturity. Those are explicit trust/maturity limitations, not proof of tampering. The checksum and filename bind a prospective inspection artifact; this review does not approve a provenance exception for adoption.

Six universal-wheel identities and the four HTTPX2 advisory assessments remain in the unchanged [MR report](hub-metadata-dependency-review.md). Do not repeat that review. The two new checksums were associated with their file-detail headings; a nearby sdist/ARM checksum was not substituted.

## Retained-pin context and remaining work

The frozen lock records packaging26.3, PyYAML6.0.3, tqdm4.70.1, typing-extensions4.16.0, IDNA3.20, h110.16.0 and Colorama0.4.6. Its tqdm record lists Colorama; the other six records list no resolved dependency edge. This is local resolution context, not independent publisher METADATA or licence attestation. Markers and actual wheel declarations still need inspection. No pin/lock changed.

HF-Xet/FSSpec runtime requirements remain unestablished from the returned JSON projections; absence of exposed fields was never interpreted as no dependencies. Complete native/bundled notices, retained-node declarations, offline/local-asset control documentation and actual network/ABI/parity behavior remain open. The planned offline-doc request was refused by the source cutoff before being issued.

## Decision for the next proposal

Sufficient filename/checksum information now exists to prepare a concrete static-inspection proposal for the newly catalogued artifacts, reusing MR identities and existing root evidence. It must explicitly disclose FSSpec's missing attestation and rounded sizes. If proposing conservative download ceilings, label them limits, not verified sizes; for example HF-Xet8MiB and FSSpec1MiB would be proposed ceilings needing approval.

The next package must fix its exact allowlist, origins/hash checks, byte/expansion/member caps, owned worker/teardown and synthetic controls before acquisition. Inspect METADATA/licence/notice contents as inert data; no install/import/native execution is implied. This report authorizes none of those actions. Exact build-source mapping remains an adoption item under the unchanged metadata-only deferral.

## Process and closeout

GC1 passed immutable/Unicode/response/phase/non-null-summary controls and froze25 inputs. The initial gap matrix was saved early. GC2 improved artifact/licence evidence and lock context but remains partial on requirements/exact bytes. GC3 records an inspection-readiness decision with notice/offline gaps, not installation clearance.

No new external request was issued after the600-second cutoff. Optional work was fenced; all later processing classified existing responses or saved protected findings/checks. A protected PowerShell projection used invalid `-Depth6`, was corrected to `-Depth 6`, and retained the original matrix. Its host error bypassed controlled emission; prepaid failure margin was retained without retrospective compliance. Actual phase/total timing and resource records remain local.

No application suite/Ruff, candidate payload read/download/import, worker/service, model/Ollama API/native trial, build/install, environment/PATH/lock/runtime/application/G2/stage change occurred. Old roots remain unchanged. At the user's new direction, session-checkpoint files are not updated; progress is recorded in TODO/PLAN and reports.

Closure checks passed:23 frozen inputs unchanged,2 exact historical suffixes,7 touched local links, exact six-file result scope, empty index and whitespace. Session-checkpoint file unchanged. Readable diffs and statically validated final command retained; actual phase/time/error totals remain local. These checks do not clear payload/runtime gaps.

Request the results commit and approval to prepare the exact static-inspection proposal. Acquisition/execution/adoption remain later gates.
