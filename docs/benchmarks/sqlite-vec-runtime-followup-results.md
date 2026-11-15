# T12-C — native trial partial results, MATCH permission refusal

## Outcome and authority

The user ran the approved disconnected runtime-02 trial from preparation commit `960fa7c` and reported its final output. The sanitized summary confirms **stopped_no_automatic_retry**, **teardown_verified:true** and **receipt_persisted:true**. Owned workers stopped and the controller printed the safe reconnect message. The allocation is closed; do not retry/reset/reseal it or change its sealed sources/assets.

This report uses sanitized summary/meter scalars, the user-provided traceback, authored source/manifest review and hash checks. No runtime database/vector/request bytes or private document content were opened. No native execution, extra tests, installation or downloads were performed during closeout. Original30sealed identities and13prior records still match.

## Completed and missing coverage

| Work | Observed result |
|---|---|
| Deadline sentinel | Completed with expected owned termination, exit125 |
| Memory sentinel | Completed, exit0 and memory_refused |
| A before-commit crash/reopen | Completed, integrity ok; baseline original metadata/chunk counts recovered |
| A after-commit crash/reopen | Completed, integrity ok; committed rows recovered |
| A file-before-commit crash/reopen | Completed, integrity ok; one orphan marker reported |
| A commit-before-cleanup crash/reopen | Completed, integrity ok; pending cleanup reported |
| B before-commit crash/reopen | Crash worker ran; reopen worker failed at recovered search; pair incomplete |
| Remaining B recovery cases | Not reached |
| Paired32/1000measurements | Not reached; zero measurements/speedup results |

The summary phase is B-before-commit. The controller records RuntimeError after its failed child, while the user's child traceback supplies the specific sqlite3.OperationalError: `not authorized to use function: MATCH`. The traceback reached `verify_crash()` → `Adapter.search()` after constructor/integrity/count checks. This supports successful native loading and reaching that pre-search path; it does not establish complete B recovery, retrieval correctness, scope/tie behavior or performance. Native module compatibility is only partially exercised.

## Confirmed harness defect and test limitation

The approved B query uses `embedding MATCH ?`. The connection authorizer lowercases each SQLITE_FUNCTION callback name and allows only names in the fixed manifest. That manifest contains vector functions but omits `match`. SQLite requested permission for MATCH and the authorizer refused it. The query therefore stopped at our permission boundary; this is not evidence that the extension cannot perform the approved search.

Our positive authorizer test exercised `abs`, and connected B loading/query behavior was deliberately fake. Even the complete future-handoff fake schedule did not execute native SQL. Those tests proved timing/control flow and selected denials, not authorization of the full query's operator-dispatch surface. This coverage gap was missed before handoff. The restriction was left intact when the actual trial exposed it, as required by the approved stop conditions.

## Accounting and sampled resources

The meter is closed with **70/96conservative reservations**: preparation24,tests16,workers14,reporting16,cleanup0. Workers14 includes two user launcher/controller reservations plus12actual owned worker attempts: two sentinels, eight A crash/reopen workers, one B crash worker and the failed B reopen worker. Unused allowances do not authorize a restart. Preparation accounting/recovery history remains unchanged at1372.7285902conservative seconds; native epoch timestamps are retained. An exact final controller elapsed duration was not persisted, so none is invented here.

Across73samples: minimum available physical memory12109021184bytes; maximum sampled controller private18432000bytes; maximum observed job peak40693760bytes; maximum observed runtime disk3578872bytes. Maximum completed-reading gap0.1519015000seconds and collection/full-iteration observation0.0620814000seconds stayed within the approved300ms boundary in these samples. These are observations from this partial run, not future guarantees or proof on a physical16GB target. Staged assets remain separately capped and hashed.

## Next decision and preserved state

Recommend a narrowly scoped successor proposal: add only the required MATCH callback to the reviewed function allowlist; first demonstrate the missing permission with local stdlib SQLite and a harmless registered match stub, then verify the exact query's authorization callbacks and existing dangerous-function/ATTACH/PRAGMA denials. A stub can test the permission contract, not native vector correctness. Preserve current SQL/filtering/tie semantics and all resource/privacy limits. Any necessary additional permission remains a separate finding; never turn off the authorizer or allow arbitrary functions.

Review fresh accounting, source/artifact identities, preparation timing/checkpoints and the exact next native schedule before implementation or another trial. No successor allocation, source modification, new package approval or runtime adoption is implied by these results. Keep runtime-01/runtime-02 and all previous evidence unchanged; withdraw the runtime-02 handoff. T12 comparison, T16/T17/G2, larger-scale capacity, final retention and physical16GB validation remain open. Results-documentation commit and preparation of a successor package require their own decisions.
