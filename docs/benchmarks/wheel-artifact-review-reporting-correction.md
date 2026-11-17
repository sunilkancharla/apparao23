# T17-IF-ASR — acquisition and inert inspection completed

## Outcome

On 2026-11-17, the user approved ASR1–ASR5 and its four-file planning commit, recorded as `42a2aea`. The [reporting correction](../proposals/wheel-artifact-review-reporting-correction.md) inherited the [AS artifact/security/resource scope](../proposals/wheel-artifact-review.md). Eight fresh metadata admissions and eight fixed downloads completed; their declared exact sizes and expected SHA-256 values matched. Static inspection then completed for all eight new wheels and two cached roots. Both real workers exited cleanly with verified teardown.

**No wheel was installed or imported. No product implementation, runtime adoption or G2 approval occurred.** This is completed evaluation tooling and static evidence, with the limitations below.

## Exact acquired artifacts and declarations

All fixed checksums are retained in the inherited manifest, authored aid and ignored admitted manifest. These are exact downloaded bytes, replacing the earlier rounded HF-Xet/FSSpec size observations.

| Wheel | Verified bytes | ZIP entries | RECORD payloads verified | Declared licence |
| --- | ---: | ---: | ---: | --- |
| HTTPX2 2.16.2 | 97,893 | 37 | 36 | BSD-3-Clause |
| httpcore2 2.16.2 | 85,551 | 37 | 36 | BSD-3-Clause |
| AnyIO 4.16.0 | 134,521 | 53 | 52 | MIT |
| Click 8.5.1 | 126,163 | 22 | 21 | BSD-3-Clause |
| Filelock 4.2.10 | 218,040 | 29 | 28 | MIT |
| Truststore 0.10.5 | 19,017 | 11 | 10 | MIT |
| HF-Xet 1.8.0 | 3,911,559 | 7 | 6 | Apache-2.0 |
| FSSpec 2026.9.0 | 221,738 | 62 | 61 | BSD-3-Clause |

The new wheels contain 258 entries and **250 verified RECORD payloads**. Their metadata/name/version/tags, CRC/local layout, recorded hashes/sizes and required licence-file locations passed the implemented checks. HF-Xet contains `hf_xet/hf_xet.pyd`; no native payload was loaded. The other seven new wheels had no inventoried native-suffix member.

Whole-file hashes of cached Hub 2.4.0 and Tokenizers 0.23.3 matched their fixed identities. Their 191/31 entries were admitted; prior full RECORD evidence was reused, not regenerated. The four allowed source-as-data members were present: Hub constants and Tokenizers' initializer/two typing files. Their declarations are intent evidence only. Hub supplied one separately selected notice file; cached Tokenizers supplied none under the implemented notice-name selection. Its metadata remains retained; this is not a conclusion that legally required notices are absent.

Across new/cached inspection: 480 entries, 13,677,132 expanded bytes and 32,346 selected notice bytes. Complete notices, dependency headers, hooks and source-as-data remain in ignored local evidence. Licence declarations and collected notices do not establish complete bundled-native/vendor compliance or independent publisher provenance.

## Dependency evidence and remaining gaps

Wheel declarations retain the earlier graph concerns. On Windows, HTTPX2 requires AnyIO, httpcore2, IDNA and Truststore; httpcore2 requires h11/Truststore. AnyIO declares `typing_extensions>=4.16.0` for Python below 3.15. Extra/platform-conditional edges are preserved separately in the raw metadata/results. This report does not install, resolve, override or certify the entire project lock against those declarations.

HF-Xet native ABI/vendor-notice review, FSSpec's absent publishing provenance, the retained Hub build-source mapping gap, applicable dependency/marker reconciliation, advisory coverage and actual offline/local-asset/parity behavior remain adoption work. No security, compatibility, source-origin or offline-runtime guarantee follows from matching wheel checksums.

## Test-first implementation and checks

Authored [evaluation aid](../../tests/evals/spikes/wheel_static_inspection.py) and [synthetic tests](../../tests/evals/spikes/test_wheel_static_inspection.py) use stdlib and attributed, checksum-pinned project-owned ZIP definitions. They have no candidate imports or new package dependencies. The aid explicitly applies package limits instead of the copied primitive's larger default.

- Expected RED: a valid fixed-entry assertion failed against the contract stub; the receipt is retained.
- The first full suite passed 12 tests. Expanded regression passed **19 tests**, including five Windows Job cases. After separating retained artifact-data size from console-report size, the final focused run passed **15 pure extraction/transport tests**. The Job implementation stayed unchanged. Together these cover 20 distinct unit tests; they are not represented as one final 20-test invocation.
- Native tests exercised assignment/startup gating, timeout teardown, kill-on-close, descendant payload blocking, parent-shell/worker memory samples and assignment refusal. In-memory integrity mutation was caught. Fixtures covered malformed manifests/JSON, DNS/URL/TLS refusal, framing/partial bodies, RECORD/CRC/local overlaps, licence/tag checks, inert hooks, unsafe paths and early 513-entry refusal.
- The new host-display path passed five controls. The reused child-report controller passed its 12 controls before acquisition. Neither emitted an oversized negative-control report.
- Final formatting and Ruff 0.17.5 checks passed. All eight approved Ruff invocations were consumed, including version/format/intermediate lint checks. Seven earlier suite reservations plus the final reused-control suite consumed eight of ten suite allocations.

Historical test commands include `F:/Python/Python314/python.exe -I -S -B tests/evals/spikes/test_wheel_static_inspection.py -f` (19 tests at that revision) and the same command with `PureTests` appended (final 15). These aids/fixtures target this evaluation root. Reuse requires a fresh approved root/source review; do not rerun them into the closed root or invoke internal workers outside the validated launcher.

## Runtime/resource evidence

The acquisition worker made exactly **16 HTTP transactions**, receiving 4,942,831 status/header/body bytes. Its reported read count was the same; new payloads totaled 4,814,482 bytes. The inspector made no network request and charged 27,759,191 reads. DNS/TLS/kernel overhead and interpreter/OS loading are outside those application counters.

Verified Job assignment preceded delivery of each real worker's Python source through stdin. Source hashes were checked and those same bytes were executed. The one-process Job policy, retained handles, birth/exit evidence, timeout/wait logic and safe teardown were exercised. Acquisition sampled owned private memory 205 times, peaking at **120,217,600 bytes**; inspection sampled 25 times, peaking at **114,356,224 bytes**. Samples included the worker, Python controller and invoking PowerShell process. Sampling is not a guaranteed kernel ceiling or physical 16 GB product benchmark; filesystem/kernel-egress confinement is not claimed.

One measured host-review/queue interval was **73.791 seconds**, excluded under the approved rule. Final active/wall totals, prepaid process/read/report/disk accounting and closeout checks belong to the closed summary. Process leases include unused/failed reservations; they are not an exact count of successful OS creations. Suite leases use the approved shared explicit allocations; no counter/allocation was silently reset.

## Corrections and evidence limits

The saved PowerShell control file could not load under the existing script policy. Its reviewed literal inline definitions passed instead; no policy/PATH/global setting changed. One intermediate lint display was withheld without retaining its complete diagnostic text. Subsequent structured lint receipts retain the issues and final clean result. These two orchestration corrections are recorded; no actual overflowing/truncated report or candidate retry occurred in this allocation.

A native test initially assumed Job close must return a nonzero exit status. Observed zero status led to a stronger appropriate check: the gated interpreter exits while its stdin remains open. The descendant test checks that child payload cannot create its marker. Tests were retained and their observable conditions corrected; no guard was relaxed for acquisition.

The remaining source/ABI/licence/advisory/offline questions are explicit. The aid is an evaluation tool with an internal worker entry and fixed root, not a hardened product runner. Static inspection does not verify semantic functionality or complete supply-chain safety.

## Evidence and next step

Ignored evidence under `data/t17/wheel-artifact-review-02/` includes host/control/test/lint receipts, frozen inputs, source bindings, fresh metadata, admitted manifest, wheels, acquisition/inspection results, ownership/capture records, notices/source text, readable diffs and validated final summary. Earlier closed roots and historical checkpoint files remain unchanged. Runtime artifacts, model/user data and local databases remain excluded from Git.

Request a separate **eight-file results commit**: the two authored aids, this report and the five affected task/readiness documents. Next prepare a bounded reconciliation of the actual dependency/licence/native/source findings and remaining adoption blockers. Installation, candidate imports, further downloads, model/input-fit execution and G2/runtime adoption need their own reviewed package/decision.
