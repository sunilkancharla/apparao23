# T09 - Consolidated isolation validation: permission boundary stop

**Report date:** 2026-11-14 (Asia/Calcutta). **Authorization:** User explicitly requested the consolidated bounded isolation validation without CREATE_NO_WINDOW, covering the remaining checks in one approval. [Package and retained limits](../proposals/consolidated-isolation-validation.md). **Outcome:** Startup/native positive controls passed; profile creation succeeded; the first permission grant failed. The package stopped, and this Windows diagnostic chain ends here without another automatic investigation.

## Gate results

| Gate | Evidence/outcome |
|---|---|
| Policy tests and static review | Three new tests first failed for missing functions; final **11 policy tests passed in 0.011 s**. Ruff passed after the final accounting changes. Tests cover omission of only the no-window flag, fresh run/profile with unchanged cached runtime, cleanup capacity, prior safety policies. |
| Runtime/config/previous runs | Rehashed 810 selected staged/original runtime entries against the preserved manifest, 38,852,581 staged bytes. Baseline config and all four previous trial meters verified; final `prior_identities_unchanged=true`. No copy/install/download. |
| Positive staged startup | Passed with extended/suspended/Unicode flags `0x00080404`, the child-process restriction and original authored control helper. Exit 0; worker Job total=1/active=0; controller total advanced from 1 to 2, active=1. |
| Native positive networking | IPv4 TCP/UDP and IPv6 TCP/UDP all returned success; all four controller-owned loopback listeners received the synthetic marker. No DNS, LAN bind or external endpoint. Both positive workers passed their process accounting controls. |
| Temporary profile | Fresh run profile created with zero requested capabilities; create HRESULT `00000000`. This created the previously disclosed per-user Windows storage outside the repository. |
| Permission grants | First required `icacls /grant` returned exit 5: zero files processed successfully, one failed. No completed grant receipt. No broadening of rights, administrator elevation, global-runtime permissions change or grant retry. |
| Restricted AppContainer tests | **Not reached:** actual worker token/startup, file allow/deny, native network denial, blocked child attempt, timeout/resource sentinel. No AppContainer worker or OCR process was launched. |
| Cleanup | Profile deletion returned HRESULT `00000000`; the helper's subsequent storage existence check did not report a profile remnant. SID-removal utility also returned access denied, retained in `cleanup_errors`. Independent read-only inspection found **no occurrence of this SID in any of the 11 candidate grant/ancestor DACLs**. This audit is limited to those planned targets; it is not an exhaustive filesystem audit or a successful utility cleanup result. |

Final controller Job accounting was total=5, active=1, terminated=0: controller, two positive workers and two ACL utility calls, with no unexplained cumulative addition. Only the controller was active at the recorded final check; it subsequently exited with the intentional stop exception. No active worker remained. No mandatory-label change was reached. The stopped report preserves the cleanup command failure even though the subsequent target-DACL audit found no SID entry.

## Execution context and interpretation

The native controller ran with explicit host-tool permission outside its filesystem sandbox because the approved temporary Windows profile uses per-user storage outside the workspace. This did not request an administrator/elevated worker, breakaway, disabled host security or altered firewall. Worker Job/resource limits remained unchanged, and AppContainer token checks would still have been required before restricted-worker resume. Earlier diagnostics used their recorded contexts; do not attribute every difference solely to removing a flag across different host contexts.

The positive result establishes that this staged control helper and four local positive network paths can work with the chosen flag/child-policy settings in this execution context. It does **not** validate AppContainer execution, file/network denial, OCR libraries or application offline behavior. Windows refused the required permission operation in this context; exact ownership/token-policy reasons were not investigated further. Do not claim that AppContainer itself is unsupported or broken, or that an OCR engine failed.

No permission repair, ownership takeover, UAC elevation, alternate profile, extra native trial or additional grant attempt was performed after the stop. The profile was deleted through its owned API; no recursive deletion of OS-managed paths. Cached runtime bytes, user samples, global Python, PATH, Windows features and existing trial meters were preserved.

## Budget, receipts and source

One shared fresh meter: **32/96 conservative process reservations including final documentation closeout**. The two positive roots and both ACL utility calls are included; blocked child/resource/restricted roots were never attempted. No counter reset or spent old allocation. Unit helpers/tests, tool/wrapper allowances and closeout are charged. Native execution stayed within its preparation/execution caps; later report checks are not additional trials.

Ignored receipts under `data/t09-isolation/consolidated-01/` include baseline/verified identities, red/green/final tests and Ruff, execution context, positive worker/network results, profile ownership, `result.json`, `execution.txt`, `read-only-grant-audit.json`, meter and events. Final source changes are opt-in fresh-run configuration/reused runtime verification, no-window omission, protected cleanup capacity and controller accounting around workers/ACL utilities. No product functionality or dependencies were added.

## Decision after this package

The promised consolidated attempt is complete **to its required stop**, not accepted as isolation success. T09 OCR comparison and Part B remain incomplete/gated. Do not start another small Windows diagnostic by default.

Present the user with alternatives: a user-operated disconnected, synthetic-only trial in the existing project environment (explicitly accepting that this does not confine filesystem access), or a separately reviewed isolated environment with installation/resource/Windows compatibility implications. Neither alternative is adopted or authorized by this result. OCR assets/packages must still use the approved local-only provisioning rules; no real documents, OCR installation or inference has been approved by this isolation package. Runtime selection/security changes and Git commits retain their gates.
