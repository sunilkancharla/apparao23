# T17-IF-MG — policy checks passed; platform subprocess remains blocked

## Outcome

The user approved MG1–MG5 and its four-file planning commit, made as `299498d`. The unchanged guard failed the expected RED assertion. After the exact hostname exception was added, **20 policy cases passed**. The single parser attempt retained its complete **3,114-byte error**: Windows version detection requested a subprocess, which the unchanged subprocess denial blocked. No additional exception or retry followed.

The [approved package](../proposals/marker-environment-guard-review.md) and [CC findings](reconciliation-capture-correction.md) remain the scope and capture evidence. Local ignored evidence is in `data/t17/marker-environment-guard-01/`. This is a review result, not a product capability, package adoption or completed dependency reconciliation.

## Tasks and evidence

| Task | Result |
| --- | --- |
| MG1 | Eight pinned inputs matched; 20 packaging source hashes and two installed metadata identities matched. The copied capture aid retained its exact verified bytes. Old graph/inspection/dispatch code was excluded. |
| MG2 | Expected RED recorded against the unchanged guard before correction. Original guard SHA-256 `c58b576024f5efaa341fb324295d8aa98c81ad3b45be735e5db58611fe758490`; recorded RED timestamp precedes corrected source timestamp. |
| MG3 | Only the exact hostname event was exempted; 20 GREEN cases passed against the actual predicate later loaded by the parser. No networking was performed by policy tests. |
| MG4 | One parser child, exit 1, complete admitted stderr and empty stdout; verified exit. The controller exited 0 because it successfully recorded this failed parser outcome. The ten marker/report controls did not reach their assertions. |
| MG5 | Findings/receipt recorded; final preservation, scope, link, whitespace, readable-diff, empty-index and summary checks below. |

The semantic guard diff was exactly:

```diff
 def audit(event, args):
+    if event == 'socket.gethostname':
+        return
```

Line endings were normalized, and the resulting source was compared with the original plus those two lines before GREEN. Its SHA-256 was recorded by GREEN and rechecked by the parser child before loading it. No cache prewarming, library-factory override or further policy change was used.

The 20 cases cover exact hostname allowance; socket creation, connection, binding, resolution/service lookup and near-match event denials; subprocess/native-loading/OS-command denials; and representative allowed/denied imports. They test policy decisions directly, not kernel network isolation. The actual parser progressed beyond the earlier hostname rejection and stopped at the retained subprocess restriction. No hostname value or raw machine-name object was saved or displayed.

## What failed and what remains unknown

The traceback reaches Python's Windows-version fallback, `_syscmd_ver()` → `subprocess.check_output(..., shell=True)` → `subprocess.Popen`. The final error is `RuntimeError: Forbidden parser operation: subprocess.Popen`. The source comparison had identified this possible fallback; its execution was not silently authorized. The requested helper creation was denied by the audit hook.

This establishes a conflict between default platform discovery and the chosen review boundary. It does not establish dependency incompatibility, parser corruption or application failure. The trace does not establish why earlier Windows-version discovery failed to supply a usable value, and that cause was not investigated here. Marker correctness, actual/minimum environment matrices, lock conflicts, licence/provenance reconciliation and runtime adoption remain unresolved.

The original ten-control fixture is preserved. No control was weakened, no version pin changed, and no second parser attempt or graph/research/model run occurred.

## Process correction and limits

One orchestration correction was consumed. A bookkeeping shell assigned to PowerShell's read-only `Host` variable and failed after its lease was persisted. The already queued, approved two-line source patch still ran. The shell's complete error was available in the tool transcript; `correction-sequence.json` records the correction and subsequent evidence checks, not a fabricated original stream capture. The variable was renamed, and original RED/hash/exit evidence, authoring order and exact source difference were verified before GREEN or parser execution. No check invocation was retried.

Three check invocations were consumed: expected RED, GREEN policy suite, one parser attempt. A separate source-preparation controller did not import packaging or run parser controls. All four controllers and the sole parser child exited. No helper subprocess was permitted, no Ruff/web/model run occurred, and no candidate was installed/imported. Packaging 26.3 remained the existing approved review tool.

The reused capture aid's eight synthetic cases are **historical CC evidence**, not eight additional tests in this run. Complete parser bytes were retained before an oversized detail display was withheld; a bounded diagnostic tail was then displayed. No admitted diagnostic was lost or truncated.

Interpreter: CPython **3.14.6**, 64-bit AMD64, using the existing isolated executable. This is not a new interpreter selection or a Windows 11/16 GB/CPU-only performance result. No filesystem confinement, Job, kernel egress or memory guarantee is claimed.

| Authored/copied local source | Bytes | SHA-256 |
| --- | ---: | --- |
| `run.py` | 7,683 | `f71bca4f9ef7008fabd55f3efe15f4c2f6811bf3f07c92f5d5cd066c1baf9556` |
| `guard.py` | 477 | `ad565dfffcc3450fa6e50e3d359858e8e9db37f26b2fef92d5b976bafc20a5c2` |
| `parser_controls.py` | 2,961 | `ac2f2b8ab435dd83d36dd0a86eab9ace8db86f17c0dd6ca26f05a27deba58547` |
| `capture.py` | 4,482 | `15849ddbd03c992da78baee314b48731c036d7ab5563e1719e61892f64b590d3` |

At the interim receipt: 252.504 active/wall seconds, no host-wait exclusion; 48 work units/32 process starts prepaid. Final elapsed time and conservative read/report/process allocations are in the local summary. Read leases do not measure total OS/interpreter I/O. Runtime scripts, receipts and fixtures remain excluded from Git.

## Smallest next review

| Option | Benefit / consequence |
| --- | --- |
| Review an explicit environment adapter that avoids platform discovery | Retains subprocess denial. A supplied dictionary alone is insufficient; review whether a controlled environment factory can be substituted in the isolated review child. Any library override must be explicit, version-pinned and tested, with real interpreter facts separated from hypothetical target assumptions and unknown marker fields. No override is approved here. |
| Permit an exact Windows version helper | Preserves default discovery, but adds shell/descendant execution and new ownership/accounting requirements. The current package forbids it. Do not broadly allow `subprocess.Popen`. |

Recommend preparing the first option for source-only review before choosing an exact adapter/control package. Preserve the subprocess restriction; do not automatically widen this guard further. Passing a later marker suite would only enable proposing the remaining dependency/licence/provenance review, not installation, G2 or a stage transition.

Closeout checks passed: six-document scope; 10 frozen inputs and eight pinned prior/source identities preserved; 20 tool-source/two installed metadata hashes unchanged; 22 local links, whitespace, readable diff, empty index and non-null receipt checked. SPEC, dependency/lock/configuration records, existing tests/manifests, historical checkpoints and unrelated user files were preserved. Results commit and next-package preparation/execution retain separate approval gates. Historical CC authoring-order evidence remains unchanged; MG recorded RED before its implementation.
