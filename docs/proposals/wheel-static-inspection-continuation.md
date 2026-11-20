# T17-IF-WIC — continuation with bounded reporting

## Status and purpose

**Proposed; WIC1–WIC5 execution and the four-file planning commit require approval.** The user approved committing the stopped WI results and preparing this proposal. Results are committed as `5ec1002`; the [report](../benchmarks/wheel-static-inspection.md) records the output-limit failure. No continuation root, control script, helper, fixture, network request or candidate activity has been created or started during this preparation.

Continue the same inert wheel review after correcting its reporting boundary. The prior failure occurred before any metadata probe; native access remains untested. This proposal does not establish that networking works or that any candidate is suitable for installation.

## Inherited artifact scope and controls

Incorporate the [original WI package](wheel-static-inspection.md), committed in `424962f`, except for the explicit reporting/workflow changes below. Its current authored bytes are 14,161 bytes, SHA-256 `9d3ace13aa4e36099c197b4e960adc98b0fff83123531a3740206a292fe2c6b0`. Freeze and verify those bytes before dependent execution; an unexpected change stops work rather than silently changing the manifest.

The eight filenames, versions, fixed checksums and per-wheel caps remain exactly those in its acquisition table: HTTPX2/httpcore2 2.16.2, AnyIO 4.16.0, Click 8.5.1, Filelock 4.2.10, Truststore 0.10.5, HF-Xet 1.8.0 and FSSpec 2026.9.0. Retain the rounded HF-Xet/FSSpec size caveats and FSSpec's missing provenance limitation. Fresh exact release sizes must be admitted before payload requests; no substitution, guessed URL or automatically discovered download.

The two cached Hub/Tokenizers wheels, their fixed hashes, source-as-data allowlist and RECORD reuse limits are unchanged. Do not reacquire them or read model assets, the large Ollama archive/runtime, global installations or user documents. The same reviewed owned ZIP primitives remain pinned to 21,836 bytes/SHA-256 `691d86c9cc750a2f88b266230e0938936d92ce54c3b5f21684bd3a080fcd6d03`.

Use the existing `F:/Python/Python314/python.exe -I -S -B` and stdlib. No interpreter/dependency installation, candidate import, pyproject/lock/PATH change, model request, application implementation, adoption or stage transition. Source mapping remains an open adoption item under the unchanged approved metadata-only timing deferral.

## Ordered tasks

| ID | Objective and prerequisite | Acceptance and verification | Status |
| --- | --- | --- | --- |
| WIC1 | After approval, bootstrap and verify reporting controls before the early native metadata probe | Shared accounting and frozen controls precede optional reads. Synthetic byte-boundary/capture checks pass. Then one fixed owned metadata probe succeeds, or the package stops before substantial helper work. | Pending approval |
| WIC2 | After WIC1 succeeds, implement the two original authored aids test-first | Expected RED, smallest passing implementation, abuse/regression cases, caught in-memory integrity mutation and final lint/format/code/security review. Tests use mocked transport only. | Pending WIC1 |
| WIC3 | After WIC2 passes, acquire the original eight pinned wheels once | Exact metadata admission, streamed hash/size checks, bounded partials and verified worker exit. Failure stops; no retry or inspection of failed acquisition. | Pending WIC2 |
| WIC4 | After coherent WIC3, perform the original bounded static inspection once | New-wheel RECORD/metadata/notice/native inventory and allowed cached-root text reads; no package code loading, extraction or runtime guarantee. | Pending WIC3 |
| WIC5 | At completion, stop or cutoff, close out | Honest findings and resource/ownership evidence, preservation/scope/link/whitespace/readable-diff checks, validated non-null summary and separate results-commit/adoption gates. | Pending completion or stop |

Only two new versioned code files are permitted: `tests/evals/spikes/wheel_static_inspection.py` and `tests/evals/spikes/test_wheel_static_inspection.py`. Runtime reporting/probe/controller source and synthetic fixtures belong in the fresh ignored root. Do not create substantial acquisition/inspection helpers until the early probe passes.

## Reporting correction before the probe

1. Bootstrap **`data/t17/wheel-static-inspection-02/`**, refusing an existing root or unsafe ancestor. Begin the fresh allocation explicitly; never modify, reset or append to the closed `wheel-static-inspection-01` root. Freeze the previous report/receipts and relevant authored inputs with bounded reads. No historical checkpoint writes.
2. Author and review the runtime capture control under the bootstrap lease. Capture both stdout and stderr before display, preserve exit codes and decode strictly. Read the streams concurrently with a shared bounded byte counter, finite buffers, deadline and owned-process termination on overflow. Avoid sequential stream draining or an unbounded `ReadToEnd`/`communicate` accumulator. Captured data and failures remain charged to the shared reporting/read/disk budgets.
3. Count combined stdout/stderr UTF-8 bytes against the existing **8,192-byte invocation cap**, before forwarding anything. Normal display targets at most **4,096 bytes**, including its authored summary/envelope. Reserve failure/closure output in advance. Capture does not waive a limit: actual excess, incomplete capture or tool truncation stops optional work even if no excess is displayed. If termination prevents complete measurement, retain a lower bound and label the total unknown. Never truncate evidence silently or reset the counters.
4. Verify the control in one synthetic-control suite: empty and valid non-null summaries, ASCII/multibyte UTF-8 boundaries, both streams, ordinary nonzero exits, invalid encoding, missing fields and overflow refusal. Simulate oversized payloads in memory without emitting an oversized report. Controls may exercise owned synthetic subprocesses only under prepaid leases; every start counts. Their stdout/stderr must themselves stay bounded. No real network or candidate code in these checks.
5. Read skills, instructions and source in small sections whose serialized output fits the normal display target. Capture raw source separately within read/disk caps. Do not concatenate multiple full documents into one console report. Use explicit field selection; parse and validate the summary before display. A search with no matches is a recorded search result, not an assumed network failure. No external skill scripts or subagents.

The guard is proposed work, not a previously verified capability. Its synthetic-control suite consumes one of the eight total suite invocations, leaving at most seven for RED/GREEN/regression/mutation/final checks. Required workflow/security review and control failures remain inside the same accounting and time limits.

## Network and worker boundary

Keep the original single early probe: `https://pypi.org/pypi/httpx2/2.16.2/json`, at most 1 MiB and 30 seconds plus 15 seconds teardown. Request the required host network permission before the first started request. Denial or started transport/TLS/ownership/JSON failure stops the attempt; no proxy, firewall, TLS downgrade, alternate transport or automatic retry. Reuse a successful response as the first of eight metadata requests.

The original public-only DNS validation, address pinning, origin Host/SNI/certificate checks, HTTPS/host allowlist, no redirects/credentials/ambient proxies and exact metadata/URL/hash/size admission remain binding. Maximum 16 HTTP transactions includes all eight metadata and eight payload requests; failures count. No private content is sent.

Probe ownership/timeout/wait evidence must be retained. Acquisition and inspection require tested owned bytes, startup gating and verified kill-on-close Windows Job ownership before payload work. Acquisition runs once for at most 180 seconds plus 30 seconds teardown; inspection once for at most 120 seconds plus 30 seconds teardown, sequentially. Uncertain ownership or teardown stops work. No descendants, service, GUI or listening port. The unchanged 512 MiB owned-private-memory monitor is sampled evidence, not filesystem/kernel-egress confinement or a 16 GB product benchmark.

## Shared allocation — unchanged ceilings

| Resource | Ceiling and allocation |
| --- | --- |
| Work | 128 prepaid units: bootstrap/reporting control/probe 16; aids/tests 48; acquisition 16; inspection 16; findings/checks 16; protected closure 16. Normal work 112; no refunds/resets. |
| Time | 2,400 seconds total; probe starts by 360 seconds, acquisition by 1,200, inspection by 1,440. Optional work stops at 1,800; reserve 600 for closure. If controls cannot finish by the probe cutoff, stop before networking. |
| Processes/checks | 64 owned starts across all wrappers, controls, probe, test/negative/regression/Ruff workers and read-only Git. At most 8 suites and 8 Ruff invocations total, including controls and corrections. Separately approved commits remain separate. |
| Network/read/disk | 24 MiB HTTP status/header/body, 16 transactions; 512 MiB streamed reads including 16 MiB ledger preallocation and 16 MiB per suite; 48 MiB retained artifacts including captures, partials, fixtures and authored outputs. DNS/TLS/kernel overhead is not claimed inside the HTTP byte counter. |
| Reporting/ledger | 8 KiB combined stdout/stderr per invocation, 128 KiB aggregate with 16 KiB protected closure reserve; normal displayed summary target 4 KiB. At most 64 immutable records and 64 validations, 4 KiB per record. Capture/log copies also count toward read/disk caps. |

Keep all original ZIP/member/central-directory/expansion/metadata/notice limits, strict decoding, source-as-data bounds and synthetic abuse cases. Parent alone writes the global meter and prepays non-refundable child leases; child-local counters cannot reset combined accounting. Include controller, negative-control, failed and regression starts. Reserve final checks before refinements.

At most two trustworthy orchestration corrections within the same allocation; no candidate refetch. Stop on the original cap/deadline/host-denial/unsafe-input/identity/capture/reporting/ownership conditions. The reporting failure in the closed first attempt is preserved; this proposal requests a new allocation explicitly rather than silently renewing it.

## Deliverables and review gate

After execution approval: the two aids if the probe succeeds, `docs/benchmarks/wheel-static-inspection-continuation.md`, affected dependency/preflight and PLAN/TODO/README updates, plus ignored control/probe/manifests/artifacts/receipt evidence. On early stop, report the partial outcome without creating empty helper files or fabricating checks. No session-checkpoint files.

Request **WIC1–WIC5 approval**, including reporting-control implementation/checks, the unchanged probe/eight acquisitions/static reads and the allocation above. Separately approve the **four-file planning commit**: this proposal, PLAN.md, TODO.md and README.md. That approval covers routine steps inside this package; later results commits, installation, candidate imports, runtime/parity adoption, G2 and stage transitions remain separately gated.

Preparation used the verified local planning, documentation and security workflows. No skill script, trial control, test, network request or new execution root was run or created; no new public-source research was needed to amend the reporting design.
