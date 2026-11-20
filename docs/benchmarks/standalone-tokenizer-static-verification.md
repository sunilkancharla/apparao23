# T17-IF-SA — partial static identity verification

## Latest result — continuation 03

User approved the five prior findings/status files and corrected continuation. Commit 740dc3a contains those five files. Fresh epoch 03 bootstrapped accounting before optional reads; earlier epochs remain preserved.

**The cached Ollama archive matches its recorded identity, and all 75 installed runtime files match their archive members.** The inventory contains 71 executable/library files and four UTF-8 license/notice files. The installed ollama.exe also matches its separately recorded SHA-256. This proves byte agreement with the local archive, not publisher attestation, source-build provenance, native safety or tokenization compatibility.

Tokenizers 0.23.3's exact wheel identity and 31-member RECORD passed. Its metadata declares Python >=3.10 and runtime dependency huggingface-hub >=0.16.4,<3.0; extras were not selected. Bundled-native notices, ABI and offline/parity evidence remain unresolved.

Hub 2.4.0's exact wheel size/SHA passed. Its central-directory header then declared **191 entries**, exceeding the approved **128-entry** limit. Admission stopped before ZipFile parsed the member list. Hub RECORD/metadata/notices and conditional dependency research were not repeated. The cap applies to all archives as written; no exception was inferred.

Worker result: stopped_no_retry, exit 0, 149.885773 seconds. Controller retained-handle/wait evidence verifies teardown; captured stdout/stderr was empty. Sampled peak private memory was 22,077,440 bytes, a static-worker observation rather than total app/Ollama or physical 16 GB acceptance.

## Implementation and testing

Created only the two approved stdlib aids: tests/evals/spikes/standalone_static_verification.py and tests/evals/spikes/test_standalone_static_verification.py. They inspect inert bytes; candidate-looking fixtures are never executed.

Focused RED failed because the aid did not exist. Initial tests exposed incomplete Windows DirEntry.stat link metadata; path lstat fixed admission while retaining separate repeated path/handle checks. **Final 26 tests passed in 0.155 seconds.** An in-memory integrity-guard mutation was detected by its gold test.

Controls cover names/aliases/traversal/depth, reparse/hardlinks/types/changed identities, missing/extra files, archive identity/CRC/central/count/expansion limits, read admission/interruption/overflow, notice caps, synthetic wheel RECORDs and launch refusal. These checks do not certify native safety or a hostile concurrent filesystem snapshot.

Five suite invocations include RED, initial failures, an intermediate pass, mutation control and final pass. Four Ruff invocations include two formatting and two lint runs; final lint passed. The last automated format preceded manual import/nested-context cleanup; no subsequent automated format check is claimed. Final edits were manually reviewed.

## Accounting and stop

Bootstrap and a measured-output gate preceded optional reads. Oversized synthetic text and two metadata projections were blocked before raw emission. A PowerShell array-shape error was corrected before inherited hashing, with a conservative 1 MiB source/failed-projection allowance. A documentation-command JavaScript syntax error occurred before execution. A readability edit was corrected by restoring exact committed historical document bodies before adding the new sections. These agent/debug events are retained honestly; no artifact failure or retroactive compliance is inferred.

All 36 inherited hashes matched; 43 direct identities were frozen. Final preservation, links, diff/scope, elapsed time, artifact upper bound and counters are in closeout.json. No large input is rehashed at closure.

Worker reads were 7,786,285,990 bytes, counting compressed/decompressed/installed reads and probes. Shared reads after the worker were 8,123,386,371 bytes, including five conservative 64 MiB synthetic-suite allowances and source/preservation reads. Closure reads remain in the same 8 GiB budget. Reservations include the full worker allocation and protected closeout allowance; no old allocation was reset.

The cap is a mandatory stop: **no further tests, lint, payload inspection or public research occurred afterward.** SA4 was not started. No download, installation, extraction to disk, candidate import/launch, build, model/inference/API access, PATH/global-package or lockfile change occurred. Application implementation and G2 remain gated.

## Next decision

Separately commit the nine reviewed source/results/status files. Then prepare a narrow **Hub-only** continuation proposing a bounded 256-entry allowance, rechecking the existing wheel and finishing RECORD/metadata/notices before conditional dependency/provenance research. Avoid repeating the 1.6 GB runtime archive comparison.

The exact follow-up package, helper changes and limits still require approval. Native notices/advisories, Hub source .dev0-to-wheel mapping, applicable hf-xet/httpx2 graph, actual offline behavior and standalone/native rendering/token-ID/context/output-headroom parity remain unresolved. No installation, native trial, runtime adoption or application readiness follows.

Earlier process-stop history is retained below.

---
# T17-IF-SA — bootstrap/reporting stop

## Result

User approved the exact package and its five planning-document commit. That commit is `fca4bb9`. Execution stopped before any permitted artifact payload inspection, inspector implementation, tests, research or candidate execution.

The first post-approval command read local workflow instructions and the proposal before creating the required durable accounting records. It also returned more than the approved 8 KiB controlled-output limit (tool reported 12,775 original tokens). Exact byte count and elapsed time from approval were not recorded before that output; they remain unknown. This is a process failure, not evidence that an artifact, dependency or model failed.

## Evidence and containment

- A late, explicitly noncompliant stop record was created at `data/t17/standalone-static-verification-01/stop.json`; it does not retroactively satisfy bootstrap requirements.
- No archive, installed executable/DLL, wheel or model payload was inspected. No inspector/test aid was created. No test, Ruff check, public research, install, native launch or model/API request occurred.
- No owned worker started; none needed termination. The stop record states this basis for teardown verification.
- Protected closeout capacity was reserved conservatively. The original epoch remains stopped, without a reset or automatic retry.
- Git actions are separately approved and outside the execution epoch. The first commit command stopped on a harmless line-ending warning before staging; the next captured warnings, checked exit codes, enforced the exact five-file allowlist and committed successfully. Whitespace checks passed and the staged index was empty afterward.
- The session summary and unrelated user files were excluded. Existing source/design reports and prior trial receipts were not modified.

## Task status

| Task | Outcome |
| --- | --- |
| IF-SA1 | Failed: accounting/reporting order; mandatory stop |
| IF-SA2 | Not started |
| IF-SA3 | Not started |
| IF-SA4 | Not started |
| IF-SA5 | Partial-stop evidence and checkpoint recorded; findings commit pending |

No installation/trial readiness, dependency clearance, runtime adoption, application completion or 16 GB acceptance follows. G2 remains open.

## Proposed fresh continuation — requires approval

Use a fresh `data/t17/standalone-static-verification-02/` and retain the stopped first epoch unchanged. Reuse the exact artifact identities, task order, permitted files and all IF-SA caps from the approved proposal: 128 prepaid units (104 normal/24 protected), 2,400 active seconds, 8 MiB new artifacts, 8 GiB cumulative streamed reads, one 600-second static worker plus 30-second teardown, six focused suites, four Ruff invocations, eight public calls/24 targets/20 distribution names, and the existing archive/notice/report boundaries. No installation, candidate execution, model reads or payload downloads.

The first execution invocation must do only exclusive root creation and durable accounting/report reservations, before skill reads, Git status, inspection or other optional output. Workflow instructions already read can be reused; any further reading must be precharged and summarized within 8 KiB per invocation/64 KiB aggregate, retaining the 8 KiB closure reserve. Record approval and commit separately before that first execution invocation. Do not start this continuation without explicit approval.

## Continuation 02 — stopped on unmeasured source output

The user approved the five closeout-file commit and fresh continuation. Commit `9462a08` contains exactly the five approved closeout files; the session summary and unrelated files were excluded. The fresh epoch's first invocation correctly created durable accounting before optional reads.

The subsequent source-convention read emitted raw output without measuring its UTF-8 size before emission. Its 8 KiB reservation and the tool's reported 3,452 original tokens do not establish compliance; exact output bytes were not retained. Optional work stopped rather than claiming the bound held. This repeated output-control error is attributable to the agent, not to the project's dependencies or machine.

Read-only source/configuration excerpts and permitted directory filenames were seen. No archive/wheel/executable/DLL/model payload inspection, helper creation, suite, Ruff check, web research, candidate execution, API request or installation occurred. No owned worker was started. `data/t17/standalone-static-verification-02/meter.json` records the stop, elapsed time and conservative charges; neither epoch may be reset.

SA1 is incomplete: bootstrap succeeded but reporting/preservation acceptance did not. SA2–SA4 are unstarted. SA5 records this partial stop. Remaining software/dependency questions are unchanged. No new capability or readiness claim is supported.

### Proposed correction for a separately approved continuation 03

Retain all original identities, task ordering, allowed files, execution/resource/read/research/test limits and stop conditions, using only fresh `data/t17/standalone-static-verification-03/`. Before any optional command, establish a single output gate: capture command output in memory or a bounded local file, verify its UTF-8 byte size, and emit only measured summaries. Never send raw source reads, search results, Git warnings or test logs directly to the conversation. Reserve the output budget before each operation and include failures; retain the 8 KiB closure reserve. The first post-bootstrap check must demonstrate this gate using synthetic text, including an oversized result, without emitting it. Do not consume a native worker or test-suite invocation for a shell output-size check. No silent truncation or claim that token limits are byte limits.

This is a proposed change to reporting mechanics, not permission to start another epoch. Both the five current findings/status files and continuation 03 require explicit approval. No tests of the software have yet run in this package.

Closeout note: Git line-ending warnings and a PowerShell hashtable measurement error escaped the display gate. The captured output measured 1521 UTF-8 bytes against its 2,048-byte reservation; it was not measured before emission. This reporting-order deviation is preserved, not described as compliant. Artifact accounting was corrected using explicit byte summation; no tests, research or payload work was resumed.
