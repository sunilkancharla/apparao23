# T17-IF-MR — partial readiness; installation not ready

The [approved MR package](../proposals/hub-metadata-dependency-review.md), committed as `ed7ec1b`, ran in fresh ignored `data/t17/hub-metadata-dependency-review-01/`. Keep Hub2.4.0 as candidate. The review obtained concrete dependency/artifact/advisory evidence but did not close the graph, native notices or offline checks. The approved build-source deferral remains metadata-only; mapping stays open for adoption.

## Exposed dependency metadata

| Candidate / retained pin | Applicable declaration |
| --- | --- |
| HTTPX2 2.16.2 | Windows: AnyIO>=4.10, httpcore2==2.16.2, IDNA>=3.18, truststore>=0.10; typing-extensions>=4.5 for Python<3.13. Python>=3.11, BSD-3-Clause, non-yanked. |
| httpcore2 2.16.2 | h11>=0.16 and truststore>=0.10. Python>=3.11, BSD-3-Clause, non-yanked. |
| AnyIO 4.16.0, retained | IDNA>=2.8 and typing-extensions>=4.16 for Python<3.15. Python<3.11-only exceptiongroup excluded. MIT, non-yanked. |
| Click 8.5.1, retained | Empty runtime requirements; Python>=3.10, BSD-3-Clause, non-yanked. |
| Filelock 4.2.10, proposed | Empty runtime requirements; Python>=3.11, MIT, non-yanked. Major-version behavior untested. |
| Truststore 0.10.5, proposed | Empty runtime requirements; Python>=3.10, MIT, non-yanked. Actual OS certificate behavior untested. |
| HF-Xet 1.8.0 / FSSpec 2026.9.0, proposed | Published filenames identify versions; full pinned requirements/licences/artifacts remain unestablished. Normal Windows/native HF-Xet coverage is missing. |

Primary metadata: [HTTPX2](https://pypi.org/pypi/httpx2/2.16.2/json), [httpcore2](https://pypi.org/pypi/httpcore2/2.16.2/json), [AnyIO](https://pypi.org/pypi/anyio/4.16.0/json), [Click](https://pypi.org/pypi/click/8.5.1/json), [Filelock](https://pypi.org/pypi/filelock/4.2.10/json), [Truststore](https://pypi.org/pypi/truststore/0.10.5/json); filename observations: [HF-Xet](https://pypi.org/project/hf-xet/), [FSSpec](https://pypi.org/project/fsspec/).

Existing AnyIO4.16.0, IDNA3.20, h110.16.0 and typing-extensions4.16.0 satisfy exposed ranges. Existing HTTPX0.28.1/httpcore1.0.9 remain distinct distributions; no replacement occurred. HTTPX2 documents a separate import name, but actual wheel coexistence remains untested. [Declaration](https://pypi.org/project/httpx2/).

Packaging26.3, PyYAML6.0.3, tqdm4.70.1 and typing-extensions4.16.0 meet Hub's direct lower bounds, without refreshed complete retained/native/notice coverage. Evaluation pins are not adopted as application runtime. Unselected extras/Emscripten-only edges were excluded. Eighteen names including existing HTTPX/httpcore context were considered, within twenty. No complete conflict-free graph is claimed.

## Publisher artifact proposals

| Universal wheel | Bytes | Declared SHA-256 |
| --- | ---: | --- |
| httpx2-2.16.2-py3-none-any.whl | 97893 | `f05c13aade4c45dbf1c9060647a1058f0acad62398fad96e741269edb33d46f5` |
| httpcore2-2.16.2-py3-none-any.whl | 85551 | `16051ae2a42f776007543f32de9349a317b23d2cbb4e1456b4bac0e88b87419a` |
| anyio-4.16.0-py3-none-any.whl | 134521 | `c66ae634e0b8228396b801741beb3294326d4b6102f7bba4041c0dfb58c29026` |
| click-8.5.1-py3-none-any.whl | 126163 | `8bb5376d2006950386f8c6427613334a2acadc5f559cb80e638d00b4df957e37` |
| filelock-4.2.10-py3-none-any.whl | 218040 | `9479aaeb4db20b5a53e3da28493edd24720b66b8a0b84030aa56ccdf243d6857` |
| truststore-0.10.5-py3-none-any.whl | 19017 | `9aaaedaefaf06d8b206278cf8b5012bc897f485a874503501e12d776df78951c` |

Values come from the version-specific registry sources above; no candidate payload was acquired or hashed. Universal tags do not validate native transitives. Declared SPDX licences are not complete notice/bundled-native clearance. Installed footprint, RAM, ABI, offline operation and parity remain unmeasured.

## Advisory ranges

| Official advisory | Affected HTTPX2 | Patched |
| --- | --- | --- |
| [GHSA-pf96-p4fj-6566](https://github.com/pydantic/httpx2/security/advisories/GHSA-pf96-p4fj-6566) | <2.11.0 | 2.11.0 |
| [GHSA-7mj9-2mp8-4m2p](https://github.com/pydantic/httpx2/security/advisories/GHSA-7mj9-2mp8-4m2p) | <2.10.0 | 2.10.0 |
| [GHSA-h4x7-gw46-3wm6](https://github.com/pydantic/httpx2/security/advisories/GHSA-h4x7-gw46-3wm6) | <2.11.0 | 2.11.0 |
| [GHSA-f2fp-rgf2-35cp](https://github.com/pydantic/httpx2/security/advisories/GHSA-f2fp-rgf2-35cp) | >=2.5.0,<2.10.0 | 2.10.0 |

Candidate2.16.2 is outside these listed ranges, not security-cleared overall. Full transitive/native coverage remains open. [Hub's index](https://github.com/huggingface/huggingface_hub/security/advisories) showed no published advisories, not proof of no vulnerabilities.

## Stop, limitations and next step

MR1 passed controls and froze27 inputs. MR2/MR3 are partial; MR4 saves precise gaps. Nine calls used all36 targets. Unexposed fields remained unknown, never assumed empty requirements.

The normal findings reservation was refused after the1,200-second deadline, before its document edits ran. Research stopped; a terminal ledger prepaid protected findings/checks/closure. Protected closeout extends beyond the planned all-in time. The deadline exception bypassed controlled emission; its failure allowance was retained without retrospective compliance. A protected patch-format error was corrected without source retry. Source-response guards worked, but full time/reporting compliance is not claimed.

No candidate payload read/download/import, application suite/Ruff, worker/service, install, model/Ollama API/native trial, build, environment/PATH/lock/runtime/application/G2/stage change occurred. Inline controls/static parsing are workflow checks. Old roots remain unchanged.

Protected checks passed:25 frozen identities unchanged,2 exact historical suffixes,443 local links, exact six tracked status updates plus this new report, empty index, whitespace and ignored runtime-root checks. Readable diffs retained/reviewed; exact protected final command passed static parsing. Actual final delivery/resource/error records remain local; the time/reporting deviation is not erased by these checks.

Next: prepare bounded gap closure for HF-Xet's normal Windows artifact/requirements/licence, FSSpec pinned metadata, retained-node/native notices and documented offline controls. Installation/parity execution is not ready. Request a separate seven-file results commit and approval to prepare that proposal; no automatic retry or new allocation.
