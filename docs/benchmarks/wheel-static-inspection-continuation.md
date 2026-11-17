# T17-IF-WIC — reporting controls passed; probe deadline stopped execution

## Outcome

On 2026-11-17, the user approved WIC1–WIC5 and its four-file planning commit, recorded as `2aa9ea7`. The [approved continuation](../proposals/wheel-static-inspection-continuation.md) began in a fresh ignored root. Its reporting-control suite passed **12 checks**. The single native metadata probe **did not start**: the command's entry guard found that the approved 360-second probe-start deadline had expired. Optional work stopped without resetting the allocation.

This is a preparation/timing failure, not a failed network request, TLS test or candidate evaluation. The host permission step was requested, but its waiting time was not measured separately. The receipt recorded 905.722 seconds elapsed when protected closeout began; that is not the exact time the earlier guard failed. No claim is made that permission waiting alone caused the missed deadline.

## Completed and verified

- Committed only the four approved planning files; unrelated user files were preserved.
- Created shared accounting, controls and frozen authored-input identities before optional execution. The inherited artifact proposal matched its fixed checksum.
- Authored two ignored runtime sources: the bounded reporting controller and fixed metadata probe. Neither is a product module or installed dependency.
- Ran one synthetic-control suite. It checked empty/boundary streams, multibyte UTF-8, combined stdout/stderr limits, invalid encoding, missing/non-null summary fields, display overflow and captured nonzero exit handling. Oversized cases stayed in memory. One synthetic child emitted three bytes on each stream, exited with code 3, and was reaped.
- The suite emitted 83 bytes; the deadline-rejection command emitted 344 bytes. Both fit the 8,192-byte invocation cap. The reporting overflow from the previous attempt did not recur.

These checks cover the exercised controller behavior. They do not prove all concurrent-capture overflow/timeout/ownership cases, Windows Job supervision, native networking, package integrity or runtime behavior. No process-memory samples were collected, so the 512 MiB monitor target was not validated. The probe source was authored and reviewed but not executed. Seventeen authored inputs were frozen; the earlier attempt's receipt files were not included in that initial manifest, although no action wrote to its closed root.

## Skipped work and process evidence

Zero HTTP transactions, metadata downloads, wheel acquisitions, candidate imports, installations, Ruff runs or native inspections occurred. WIC2–WIC4 did not start; neither proposed versioned helper exists. No model/Ollama call, user-document read or giant archive read occurred. No trial service, listening port or persistent worker started; the synthetic worker exited and was waited for.

The failed command reached its deadline check before source loading and Python/probe startup. Its PowerShell start was reconciled during protected closeout because the command's later accounting update was never reached. This is one recorded accounting correction, not permission to retry or silently renew the time budget. There were no live trial workers at teardown.

## Retained evidence

Local-only evidence is under `data/t17/wheel-static-inspection-02/`: frozen inputs, controls, owned-source identities, the control-suite receipt, failure record, meter, reviewed diff and validated closeout summary. The first attempt's closed root remains untouched.

| Authored runtime input | Bytes | SHA-256 |
| --- | ---: | --- |
| `control.py` | 5,397 | `6f0ff9bf61b00a234be87b9f276ae111adaf876e59e7be90d4ec8e49586d72b7` |
| `probe.py` | 5,267 | `fc9efd62b5c6eadb9723b0a9cccaf1aa2be0efad29a5d62df53e7262ad7a2770` |

Bootstrap prepaid 16 work units; protected closeout prepaid another 16. One of eight suites was used; no HTTP or Ruff allowance was consumed. Closeout checks passed for the six-file scope, seven touched links, 14 unchanged frozen inputs, preserved specification/configuration/historical checkpoint, empty index, whitespace and readable diff. Final elapsed/process/disk/report measurements and validated summary are retained in the closeout receipts. The separately approved planning commit and its prerequisite review preceded this execution epoch.

## Current status and next decision

Reporting controls have useful passing evidence; the intended artifact review remains unperformed. Original checksums, exact-size/provenance caveats, source mapping, licence/native/offline/parity questions, installation and G2/adoption gates remain unchanged.

Request a separate results commit. For the next attempt, reuse these frozen controller/probe bytes instead of authoring them again before the probe. Propose a small probe-first package with explicit accounting for host permission waiting and all shell starts, including guards that fail early. Do not claim the current approval permits another attempt or change the time limits without a new decision. No session-checkpoint file is created or updated.
