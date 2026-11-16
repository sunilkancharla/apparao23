# R1-I — proposed effective-limit and owned-image investigation

## Decision requested

Approve one bounded package to prepare, test and run **one synthetic standard-library worker**, recording effective job limits and any additional owned executable before a count mismatch triggers teardown. This document is a proposal only. No new code, research, allocation or trial ran while preparing it. The five proposal/status documents need separate commit approval; package approval covers the ordered steps below, while the later results commit remains separate.

R1-L source/results are committed as `91d6433`. Its [saved evidence](../benchmarks/public-source-launcher-results.md) shows count0before assignment,1after assignment and2after resume, including2active processes despite requesting a cap1. Cleanup succeeded. The extra image was missed because validation raised before the PID-list query. Effective limit settings were not retained from a readback. Do not infer the executable or cause from those observations.

## Change to the previous approach

Keep **expected count1**, the requested one-active-process limit and512MiB limits. Add checked limit readback before creation, after assignment and at the ready stage. Separate observing/recording from accepting/rejecting a count: capture bounded owned identities first, then issue a failed count verdict and stop. This is explicit permission sought for that short diagnostic observation window, not permission to adopt count2 or increase the configured active-process cap.

Reject an unchanged rerun, an expected-count increase, a system-wide process inventory or identification of old receipt PIDs after their handles have closed. The proposal does not change the app's requirements, native trust boundary or G2 status.

## Exact proposed allocation

| Boundary | Limit |
|---|---|
| Fresh ignored root | `data/t17/public-review-identity-01/`; refuse reuse |
| Shared starts |64 units:48 normal,16 protected stop/report/verification; all blocks prepaid before any action |
| Active time |900seconds including preparation, research, testing, real observation, review and cleanup; approval wait excluded before allocation |
| Combined authored/receipt output |2MiB |
| Authored executable changes | At most two new Python aids under `tests/evals/spikes/`; preserve previous sources, seals and closed ledgers |
| Prerequisite references | At most4 external tool calls, official Microsoft/Python documentation only, completed before worker admission; no document/user content or executable downloads |
| Test tools | Existing isolated `F:/Python/Python314/python.exe -I -S -B`, existing project Ruff; no installs, dependency/model changes or global configuration |
| Real workload | Exactly one direct launch attempt at most; controlled stdlib ready/release handshake, no embedded third-party or user code; no automatic retry |
| Diagnostic ceiling | At most2 cumulative job associations and2 observed active members; requested/effective active cap must still be1. Any higher observation triggers immediate owned teardown. Charge discoveries before recording the stop. |
| Memory | Requested512MiB worker/job memory, controller private at most512MiB, available physical at least4GiB; checked before launch and sampled during observation |
| Control/cleanup time | At most5seconds normal-control allowance, then at most5seconds forced cleanup/verification |
| Identity capture window | Target at most250ms for at most2owned handles, within the existing5second allowance; no further process launches or new allowance on mismatch |

The250ms target is not a validated hard real-time guarantee for Windows API latency. Record actual durations; a delayed/unavailable call fails the diagnostic rather than extending its approved deadline. Preparation must provide an independent deadline-triggered owned termination path and fake-test it before launch. Do not promise that every unresponsive OS call can be interrupted or that every short-lived process can be identified.

Proposed prepaid block amounts: preparation3, official references8, test authoring2, red4, implementation2, green/lint5, bounded corrections8, real trial6, report authoring2, review5, close3, protected stop16 =64. The trial6 covers orchestration/nested command/shell/controller4 plus one direct and one discovered association. Count each orchestration call, nested tool, shell, executable and descendant separately; retain failed reservations without refund. Close if the next block or protected stop reserve is unavailable. Git commits are separate explicitly approved actions, not experiment work funded by a closed ledger.

**Execution boundary proposed:** the host may remain connected, as in the approved R1-L synthetic trial. Only authored stdlib code and reviewed OS queries execute; neither controller nor worker has network code. Reference research cannot overlap workers. This is not filesystem/outbound-network confinement. No private document, parser, OCR, Ollama, model or SQLite-extension execution is included, and the application's native trust question remains open. A changed boundary requires a user decision before execution.

## Required observation sequence

1. **Validate declarations and fake paths.** Reuse prior reviewed declarations only after verifying their identity. Review newly needed process-handle/creation-time queries against official documentation within4calls; record signatures, constants and limitations. Maintain separate raw-buffer decoding checks for the selected x64 job fields. If declarations or the deadline/ownership method cannot be verified, stop before any real creation.
2. **Set and read back limits before creation.** Retain raw returned bytes, returned length, required flag bits, forbidden breakaway bits, active limit and both memory limits. Require the requested protections to be present, active limit1 and memory limits512MiB before allowing creation. A successful setter return alone is insufficient. Record unrelated returned fields without silently assuming they must remain zero.
3. **Create suspended, assign once, read back again.** Retain the direct process/thread handles and membership checks. Preserve the stage accounting and effective limits before resume. Reject any mismatch before running the worker.
4. **Observe ready without immediately throwing on count2.** Keep the direct worker waiting for parent release. Persist the raw accounting/readback and charge any discovery. For count2within the diagnostic ceiling, perform the bounded owned-PID capture before recording rejection. Never release the worker to do more work merely to obtain evidence.
5. **Verify handle-based ownership and image identity.** Query only the newly owned job's PID list, with bounded capacity and explicit truncation/error handling. Reuse the retained direct handle; for at most one additional listed PID, request only the minimal query access verified in step1. On the same retained handle, check membership in this exact job, capture creation-time identity and query executable image. If membership cannot be established, close the handle and retain only a generic unresolved/access-error result; do not query its image or search unrelated processes. Keep handles until the relevant identity observation is complete to reduce PID-reuse ambiguity.
6. **Preserve minimal evidence and reject mismatch.** Save basename, creation-time identifier, owned membership, per-query monotonic timestamps and return codes. Full image paths, command lines, environment, user files and file-content hashes for the unknown executable are unnecessary and excluded. Snapshots are sequential and may race; do not present them as one atomic view. Record vanished processes or incomplete capture honestly. Drain raw job notifications as supporting evidence; notification delivery is not assumed complete.
7. **Teardown and close.** Count conformity, effective-limit conformity, identity coverage and cleanup get separate verdicts. Count2always fails the expected-count check, even if an executable is identified. Terminate the owned job, reap the direct child, query remaining active members, check every handle-close return and persist a receipt even when accounting/identity calls fail. If count stays1and all checks pass, release the synthetic worker to exit0, then verify the same cleanup. No second control is included.

The core change is observation order, not weaker acceptance. Resource exhaustion or count above2requires teardown without spending the capture window. If membership, privacy boundaries or the remaining deadline are unclear, prefer an explicitly incomplete identity record to broader inspection or continued execution.

## Tasks and evidence

Root [TODO](../../TODO.md) tracks state; all execution tasks below await package approval.

| ID | Objective / prerequisite | Acceptance and verification |
|---|---|---|
| R1-I1 | Freeze fresh allocation; exact package approval | Complete prepaid64-unit manifest, persistent clock and preservation hashes before preparation; existing sources/ledgers unchanged. |
| R1-I2 | Verify declarations and test-first successor; I1 | At most4official calls; failing/passing fake cases for limit readback, count2capture-before-reject, unknown ownership, truncation, PID-reuse ambiguity, deadline termination, independent cleanup and receipt failure; R1-A regressions and Ruff pass before real launch. |
| R1-I3 | One instrumented observation; I2 and resource admission | Checked limit readback before resume; at most one direct attempt/two cumulative associations; bounded owned-identity evidence or explicit unresolved error; no retry. |
| R1-I4 | Review and close; I3 or earlier stop | Separate four verdicts, durations, full shared charges and preservation hashes; evidence saved, no unearned launcher/adoption claim; request separate results commit. |

**Acceptance is split:** evidence collection is successful only if the effective settings and additional owned image (when present) are captured with stated coverage, or count remains1with all required observations. Operational single-worker validation passes only when count, effective limits, resource checks and cleanup all conform. A clearly documented unresolved/access-error outcome closes the investigation but does not pass either validation gate. An identified executable alone does not explain why the requested limit permitted the observed count.

## Stop and subsequent decisions

Stop for declaration/readback disagreement, missing seal/receipt, identity/ownership uncertainty, ceiling/headroom/time/output exhaustion, unaccounted actions or any request for additional launches/downloads/privileges. Cleanup is restricted to owned objects. No automatic elevation, global service changes, antivirus exclusions, breakaway flag or larger job cap is permitted.

Close the allocation after the single attempt or any earlier admission failure. Preserve all evidence; do not modify/reseal a completed probe for rerun. Any follow-up execution, changed limits, public-source review, runtime adoption, G2 transition or results commit retains its separate approval gate.
