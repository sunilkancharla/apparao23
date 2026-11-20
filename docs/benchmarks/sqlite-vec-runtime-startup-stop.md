# T12 PartB — startup stopped before native execution

## Observed outcome

Preparation was committed as `d5e8c68`. The user ran the standalone runtime-01 launcher, attested `OFFLINE`, and reported `RuntimeError: Preparation time boundary` from `offline()` calling `charge("workers", 2, ...)`.

Read-only inspection found the meter still `ready`, with `execution_started` and `execution_deadline` null, workers0, and the existing56/96 conservative reservations unchanged. The directory contained only inputs, meter, readiness, launcher and seal; no summary or worker request/results existed. These counters omit the failed user launcher/controller attempt because charging failed before saving; they must not be represented as a complete actual-start count. Preserve this discrepancy for any successor allocation.

No test worker or extension load was reached on this call path. The uncaught exception ended the controller; once the launcher has returned to the PowerShell prompt, there are no trial-created workers requiring teardown. A live process inventory via CIM was denied by the host, so no independent process-table verification is claimed. This conclusion follows from the traceback, saved state and launch ordering, not a successful process scan.

## Cause and missing coverage

`charge()` compares the current wall-clock time with `preparation_started_utc` whenever the native epoch is unset, including after the user has waited to run an already prepared package. It therefore counts human handoff waiting against the1800-second preparation allowance. This conflicts with the approved package's exclusion of human/host waiting. The static readiness receipt measured724.167active preparation seconds; it does not establish that the current wall-clock span is active work.

The failing charge precedes `Runner()` construction and the enclosing try/finally. Consequently the usual summary, closed status and teardown/reconnect messages were not written. The saved `ready` status is stale and must not be treated as permission to rerun. Existing fake tests did not exercise this delayed handoff path.

## Preserved boundary and proposed correction

Do not retry/reset/reseal runtime-01, edit its sources/assets, alter its timestamps, or increase its limits. No native compatibility, recovery, speed, memory or adoption result exists. The original meter/seal/readiness and prior allocations remain untouched; this authored report records the stop without manufacturing a runtime receipt.

A separately reviewed successor package should retain the same artifact/workload/resource limits, use fresh run/cache identities, and carry the previous reservations plus the failed launcher/controller accounting explicitly. It should separate accumulated active preparation time from human waiting, start the single45-minute native epoch only at the approved handoff transition, and catch pre-worker startup failures so a durable terminal receipt and truthful no-worker cleanup message are produced. Never renew an expired native epoch.

Before another offline handoff, test delayed user waiting, genuine preparation exhaustion, expired/started native epochs, failed attestation, pre-worker failure reporting, and rejection of reused allocations. Use fake time/loading/processes while connected; preserve all existing resource and no-load controls. Review and seal the correction independently. These are proposed follow-up requirements, not authorization to implement or run a replacement package.

## Verification and status

This closeout used read-only source/launcher/meter/directory inspection and documentation consistency/whitespace review. No benchmark, candidate load, test subprocess, download, installation or Git commit was performed. T12-B4 is stopped before its workload; B5 native teardown is not exercised; B6 records this partial outcome. T12 and G2 adoption remain open. A successor package and this documentation's commit require their respective approvals.
