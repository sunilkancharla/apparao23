# T12-C — replacement offline trial instructions

**READY for the approved user-operated offline trial.** The user approved the one-time accounting recovery, original evidence was preserved, and final readiness.json records1372.729conservative preparation seconds/56reservations,30verified sealed identities/13prior records, no open segment and no native epoch. No native trial has started. Keep all sealed source/assets unchanged and follow the disconnection instructions below.

These instructions apply only to **sqlite-vec-runtime-02** after final static readiness. The [correction report](../benchmarks/sqlite-vec-runtime-startup-correction.md) records21passing tests,30sealed identities,13unchanged prior records and a successful14-day delayed-handoff fake gate. Actual native compatibility remains unverified. Runtime-01 is withdrawn; do not run its launcher again.

## Before running

Save these instructions locally. Keep all sealed project source and assets unchanged. Close heavy applications and runtime-file viewers/watchers. Use ordinary PowerShell, without elevation, firewall/policy changes or edits that bypass a stop. Waiting before starting no longer consumes the preparation allowance.

The trial uses only synthetic data and has **no filesystem confinement**: the DLL retains your Windows account's file access. Never add real documents. Disconnect Wi-Fi, unplug Ethernet, disable tethering and every other external link. Remain disconnected even while the console is quiet.

## One fresh run

After final readiness has been confirmed and all external links are disconnected:

```powershell
& 'F:\document_assistant\data\t12\sqlite-vec-runtime-02\run.ps1'
```

Type `OFFLINE` exactly. There is no READY prompt. The single45-minute epoch begins after attestation, covers startup/verification/controls/measurements/cleanup, and never renews. All workers retain120-second limits. The schedule compares the same A/B32and1000synthetic vectors, four real crash/reopen boundaries per adapter, and memory/deadline controls. The old10000-row case is not repeated. No installation/download/model/OCR/server/API work is required.

Wait for final status, **`TEARDOWN VERIFIED: True`**, and **`Owned workers stopped. You may reconnect and report status.`** Only then reconnect and share the final status. Startup failures should now produce a terminal receipt and truthful cleanup message; an error alone is not a reconnect signal. `RECEIPT PERSISTED: True` confirms the terminal report was written.

The local sanitized report is `F:\document_assistant\data\t12\sqlite-vec-runtime-02\summary.json`. `completed_pending_review_no_adoption` means the schedule finished, not adoption or Stage1 acceptance. `stopped_no_automatic_retry` means preserve all state and report the stop. Never repeat/reset/reseal this allocation. Do not send database bytes, vectors, private paths or raw outputs.

## If cleanup or persistence is uncertain

Stay disconnected if teardown is false, the console is hung or the safe reconnect message is absent. Ctrl+C requests owned controller cleanup. If needed, inspect Task Manager locally for this exact `sqlite_vec_runtime_followup.py` run and its request IDs; do not terminate unrelated Python/Ollama processes. Establish cleanup locally before reconnecting for help. A persistence failure does not itself establish whether workers stopped: use the explicit cleanup result, and report the persistence problem after safe reconnect.

The approved package and no-filesystem-confinement boundary cover this fresh trial. No repeated task-start approval is needed; meaningful changes, additional trials and commits retain their separate gates.
