# T17-IF-RC — dependency, licence and provenance reconciliation

**Proposed; RC1–RC5 execution and the four-file planning commit await approval.** ASR results are committed as `8bf88b3`. The user approved that commit and preparation of this package. [Static findings](../benchmarks/wheel-artifact-review-reporting-correction.md) establish exact artifact/RECORD evidence, not installation or adoption readiness.

## Purpose and fixed inputs

Reconcile the eight acquired wheels and cached Hub 2.4.0/Tokenizers 0.23.3 with the current project lock, then produce an explicit readiness/blocker matrix. Retain the approved baseline and metadata-only source-mapping timing deferral. No candidate version change, root removal, lock override or architecture selection is implicit.

Read existing authored reports, `pyproject.toml`/`uv.lock` and these immutable local inputs under `data/t17/wheel-artifact-review-02/`:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `inspect-result.json` | 127,374 | `2b03271be8c491c648ba2d5e31d9fe86cf112d9180bad06788b4e03afdf73141` |
| `acquire-result.json` | 3,496 | `5185fb521c89b74afdfa282c6d12433cb7e47b2aab60cd83d1dccbdddfc6ef18` |
| `summary.json` | 2,248 | `f0f214c7052983d1613ceb63e3a250a6fa3aaaaecfbe1b9c8685dc016438ca6e` |

Use retained notices/requirements/source-as-data rather than reopening wheels, native payloads or archives. Earlier roots remain read-only. No model assets, user documents, prompts, global installation inventory or unrelated project data enter this review.

## Ordered tasks

| ID | Objective/prerequisite | Acceptance/evidence | Status |
| --- | --- | --- | --- |
| RC1 | After approval, bootstrap/freeze and review the local parser/tool boundary | Fixed input hashes match; inspect existing packaging tool imports/outbound/native behavior before use; synthetic marker checks and bounded reporting pass. No new dependency installed. | Pending approval |
| RC2 | After RC1, reconcile applicable dependency edges and lock constraints | Marker/extras/environment assumptions explicit; fixed roots and at most 20 total distribution nodes; satisfied/conflicting/missing/unknown edges distinguished, with no automatic pin change. | Pending RC1 |
| RC3 | After RC2 or a bounded partial graph, reconcile licences/notices/native evidence | Declared licences, actual selected notices, missing evidence and native/vendor questions separated; Tokenizers notice selection and HF-Xet `.pyd` limitations explicit. No licence/security/ABI clearance inferred. | Pending graph review |
| RC4 | After local review, targeted primary-source/provenance investigation | Exact publisher/source claims and build relationship distinguished; evidence/unknowns for Hub, Tokenizers, HF-Xet and FSSpec recorded with primary links. Query limits/cutoff respected. | Pending local review |
| RC5 | At completion/stop, recommend readiness and close | Concrete blocker/decision matrix, remaining smallest next package, preservation/scope/link/whitespace/readable-diff/non-null-summary checks and separate results-commit/adoption gates. | Pending completion/stop |

## Existing review tool and graph assumptions

The project already contains **packaging 26.3**, matching `uv.lock`; its installed metadata declares **Apache-2.0 OR BSD-2-Clause**. Proposed use is parsing requirement/specifier/marker strings for this review only. Manual interpretation of the Hub's 106 headers is more error-prone; marking all conditional edges unknown would give a weaker partial review. Inspect the relevant installed source/metadata/RECORD and freeze its identity before importing it. Its outbound/native behavior has not been verified by this preparation.

Use existing `F:/Python/Python314/python.exe -I -S -B`, with only the reviewed project-local packaging path explicitly admitted. No implicit global/site imports, installer, resolver download or candidate-package import. Fail on a tool identity/boundary mismatch. A small ignored review script and synthetic cases may exercise marker/extras/constraint handling; no new versioned application/helper code. At most two synthetic-check invocations, including failures/reruns.

Compare Windows CPython's actual existing evaluation environment with a **hypothetical Windows CPython 3.11.0 minimum-marker case**. Record the full marker dictionaries and exact actual interpreter version. These are declarative compatibility checks, not tested runtime support or a new Python deployment decision. Hardware remains Windows 11/16 GB/CPU-only.

Start without optional extras; propagate only extras explicitly required by an active edge. Preserve inactive edges and why they are inactive. Compare fixed candidate versions against incoming specifiers, project constraints and retained lock versions. Read matching project-local installed METADATA where needed (at most 256 KiB/file); otherwise retain unknowns. Do not infer candidate compatibility from a differently installed version. Direct-URL/private/non-registry requirements are unresolved inputs, not permission to fetch them. Stop graph expansion at 20 distinct distributions and report partial closure honestly.

## Licence and source/provenance review

Use the retained licence declarations, selected notice texts and native inventory as separate evidence categories. Cached Tokenizers' lack of a separately selected notice file is not proof that legal notices are missing; inspect its retained metadata and relevant publisher text. HF-Xet's declared Apache-2.0 does not establish complete bundled-native/vendor compliance. FSSpec's absent publishing provenance remains a gap until explicitly resolved or accepted by a later user decision.

For Hub, investigate the recorded publishing coordinate `178e1a1797858724c79fd9d12d79d0902d730497`, workflow/run claim and the separately recorded release/source relationship. Do not infer artifact-to-source equivalence from matching names/tags. Reuse saved responses/known coordinates first; avoid previously failed URLs or blind endpoint guessing. Preserve the approved deferral's scope; do not reopen it as a new requirement or silently waive the adoption gap.

Allow targeted public research through the available web tool: **at most eight calls and 24 explicit targets**, including failed opens/searches. Use primary PyPI/provenance metadata, publisher-linked GitHub repositories/releases/commits/workflows and official project/licensing/advisory documentation. Known projects include huggingface/huggingface_hub, huggingface/tokenizers, huggingface/xet-core and fsspec/filesystem_spec; verify publisher links rather than treating these hints as proof. No archive, wheel, native binary or model download, cloning, code execution, authentication or remote evaluation service.

Send only public distribution/version/digest/source identifiers; never send local paths, lock contents, user data or prompts. Record publish/event/retrieval context for time-sensitive claims. Parsed web representations establish what a publisher states; they do not cryptographically verify an attestation or an actual build. Retain cited primary URLs near supported conclusions and distinguish inference from observation.

## Boundaries, accounting and stop conditions

Fresh ignored root **`data/t17/wheel-evidence-reconciliation-01/`**; refuse an existing/unsafe root. Bootstrap before optional reads. Freeze source/report/configuration/previous-receipt identities; parent alone writes shared accounting and prepays non-refundable parser/check/closure leases. No writes or test reruns into closed roots.

Retain the tested host-reporting discipline: complete UTF-8 output checked before display, at most **3,000 displayed bytes**, 8 KiB combined raw streams/invocation. Bound native producers, source sections and capture buffers. Planned oversized displays are withheld before emission; actual overflow/truncation or incomplete evidence stops optional work. Store all admitted diagnostic detail before withholding a display. Token-return settings are not byte guards.

| Resource | Proposed ceiling |
| --- | --- |
| Work | 64 prepaid units: bootstrap/tool/graph 16; licence/native review 12; source/provenance 16; findings/checks 4; protected closure 16. Normal allocation 48. |
| Active time | 1,800 seconds; source research begins by 600, optional work stops at 1,200, reserve 600 for closure. Save interim findings before cutoff. |
| Processes/checks | 32 owned starts across shells/parser/check/negative/regression/read-only Git. Two synthetic-check invocations, zero Ruff runs; no new versioned code. A parser subprocess has a 60-second timeout plus 15-second teardown allowance. |
| Research | Eight web-tool calls/24 explicit targets; at most 512 KiB retained serialized response/call and 8 MiB total public-response evidence. Provider-internal fetch/fan-out/buffering is not measured or claimed bounded by these counters. No native HTTP acquisition worker. |
| Reads/disk | 64 MiB streamed reads including 8 MiB ledger allocation and prepaid parser/check leases; 16 MiB retained artifacts including captured responses, diagnostics and authored outputs. No binary/archive rereads. |
| Reporting/ledger | 64 KiB aggregate with 16 KiB closure reserve; 8 KiB raw/invocation and 3,000-byte display limit. At most 48 immutable ledger records/48 ledger validations, 4 KiB/record. |

If host permission is required, use at most two PR-style measured submission-to-entry/decision-observation intervals, totaling at most 24 hours; no intervening model work or hidden exclusion of ordinary tool/preparation time. Record active/wall/host totals separately. Direct ownership/timeout/wait evidence is required for parser processes; no new Job, native memory-monitor or hardware benchmark implementation/claim.

Allow one trustworthy orchestration correction within the same limits. Stop optional work on cap/cutoff/host denial, unsafe input, tool/source identity mismatch, lost accounting/capture, actual reporting failure or uncertain ownership. No automatic allocation reset, extra research, new tool, dependency selection or provisioning.

## Deliverables and approval

After approval: `docs/benchmarks/wheel-evidence-reconciliation.md`, affected dependency/preflight and PLAN/TODO/README updates, ignored parser/check/query/evidence/accounting records and a validated summary. The report recommends whether a separately approved provisioning proposal is supportable, additional bounded evidence is needed, or a different architecture should be proposed for user review. It adopts none of those options automatically.

Request **RC1–RC5 approval**, including existing packaging 26.3 as a review-only tool, the explicit marker matrix and bounded primary-source research. Separately approve the **four-file planning commit** (this proposal, PLAN.md, TODO.md, README.md). Later results commits, installations, candidate imports, model/input-fit execution, architecture/adoption/G2 and stage transitions retain separate gates. No session-checkpoint files.

Preparation used the verified local planning/documentation/security workflows and existing evidence. No new root, parser script, import/check execution or public research started during preparation. All acquired artifacts remain inert.
