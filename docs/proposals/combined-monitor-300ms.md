# Proposed 300-ms combined-trial monitoring ceiling

**Status: approved for the exact fake-only implementation package and five proposal documents' commit.** On 2026-11-14 the user answered "yes continue please" to the explicit package/commit request. New native execution remains unapproved. Combined-06 preparation/partial results are committed in `eeda648`; that run and every older allocation remain closed. This changes a future evaluation policy, not Stage 1 product limits or hardware requirements.

## Evidence and alternatives

[Combined-06](../benchmarks/combined-ocr-model-sixth-stop.md) stopped at a completed-reading gap of **287.7155 ms**, exceeding its approved 250-ms ceiling by 37.7155 ms. Its loop-start gap was109.3241 ms and current collection took204.7855 ms. Only the reading gap violated that packet's timing limits. Four controls and15answers completed; nine completed OCR/chat pairs overlapped. Qwen3 and the full36-answer matrix were not completed. Underlying scheduling/collection delay remains unresolved.

| Choice | Benefit | Consequence |
|---|---|---|
| Keep250ms | Preserves the strictest existing observation policy | The observed gap would still stop a new run |
| Raise only reading_gap to300ms | Narrower change | Leaves related start/resource/phase checks at250ms and introduces different timing policies |
| Use300ms consistently for combined monitor checks | One explicit ceiling across related checks; the recorded287.7155-ms gap would be allowed | Permits50ms more between checks, a20% increase; another larger gap can still stop execution |

Recommend the third choice, with the desired100-ms cadence unchanged. This is a deliberate policy relaxation requiring approval, not a demonstrated fix or guarantee of completion. Sampled free-memory/controller checks may detect problems later; kernel job/worker memory caps remain independent. Software checks run when the controller regains execution and cannot interrupt a blocked call at precisely300ms.

## Exact proposed policy

- Introduce one named300-ms ceiling in `combined_trial.py`, used by `check_timing` and `check_resources` and their sanitized failure-limit packets.
- Apply it to `loop_start_gap`, `reading_gap`, `collection_seconds`, `tcp_seconds`, `storage_seconds`, `iteration_seconds` and resource `sampling_gap`. Accept exact equality; refuse anything greater. Continue rejecting negative, Boolean, nonnumeric and nonfinite intervals and unknown timing fields.
- Keep work-aware100-ms waiting, every current collection/network/storage/accounting check, failure persistence, fail-closed shutdown and no-retry behavior. Do not add smoothing, grace periods, repeated overruns, watchdogs, threads, scheduling privileges or dynamic/adaptive limits.
- Preserve aggregate8GiB, OCR1.5GiB, controller512MiB and at least4GiB free physical RAM; CPU/model/OCR settings, storage caps, deadlines, physical disconnection, local-only processing, ownership and cleanup rules remain unchanged. Standalone OCR policy is outside this change.
- Preserve combined-06's250-ms historical evidence and seal. No old ledger, source seal or runtime receipt may be altered, reset, resealed or rerun. Source changes will invalidate the old seal; that is intentional, not permission to replace it.

## Proposed fake-only implementation package

Approval authorizes **32 shared process starts/attempts and ten active minutes** in a fresh ignored `data/t11/monitor-300ms-01/` allocation. Count initialization, inspection, failed launches, regressions, negative controls, lint and closeout. Reserve initial commands before launch; human/host approval waits are excluded. Preserve16starts for verification/closeout rather than spending the full allocation on editing iterations. Stop without extension on time/count exhaustion or unexpected execution.

Hash-link the closed combined-06 meter and source seal at initialization and verify unchanged at closeout. Use the existing standard-library bounded fake-test bootstrap with its512MiB/single-process cap and temporary fixtures inside the new allocation. No native OCR/model imports or inference, API calls, rendering, installs, downloads, real documents/answers or environment/global/PATH changes. No new native run identity or handoff is created by this package.

Source scope: `tests/evals/spikes/combined_trial.py` and `tests/evals/spikes/test_combined_trial.py` only. Review `combined_native.py` call sites without changing their logic. Update README/TODO/checkpoint and a factual benchmark report after verification. No changes to SPEC, dependencies, model assets, old reports or runtime adoption.

| ID | Prerequisite and objective | Acceptance and verification |
|---|---|---|
| T11-T300-1 | Package approval; establish allocation and baseline | Initial starts reserved; prior meter/seal hashes, current sources and applicable skill instructions verified. Stop on drift or unavailable bootstrap |
| T11-T300-2 | T300-1; write failing policy tests | Deterministic tests fail against250ms:287.7155ms and exact300ms accepted for all named intervals;300.001ms rejected. Existing memory/control regressions preserved |
| T11-T300-3 | T300-2; implement single ceiling | Both guard functions and reported limits use0.300s. Real observer/sample flow with fake clocks covers delayed wake-up, collection, TCP, storage and full iteration; no skipped checks or retries |
| T11-T300-4 | T300-3; verify and document | Full combined and standalone OCR fake suites, focused Ruff/format, privacy/diff review pass within the shared allocation; hashes unchanged, actual elapsed/counts and limitations recorded; ask separately before commit |

Keep negative/invalid-time, backwards-clock, durable-failure and receipt-write-error cases. Update existing250-ms violation fixtures to values above300ms where their purpose is stopping; retain explicit250/251-ms acceptance tests so the new contract is demonstrated. In particular, the old resource-receipt test that fails at exactly0.3s must use a strictly greater value and assert the reported0.3s limit. Do not simply delete failing tests or replace all numeric literals indiscriminately. Memory thresholds and their one-byte-over/under controls must remain intact.

## Gates after implementation

The completed S01–S15 local semantic review is still pending and is independent of this timing proposal. Schema/citation identifiers alone do not prove factual support. Keep raw content local.

After fake verification, propose a **separate fresh native run** with exact cached identities, shared process/API/time budgets, the approved300-ms policy, frozen experiment, new source seal and disconnected user-operated execution. No runnable command is provided now. Native feasibility/adoption requires actual results and user review;300ms may still be exceeded. Git staging/commit, new native package, further limit changes and stage transition require their separate explicit approvals under [AGENTS](../../AGENTS.md).

**Requested decision:** approve the consistent300-ms policy and this exact32-start/ten-minute fake-only implementation package. Proposal-document commit approval can be given separately; no commit is inferred from approving the package.

## Approved implementation outcome

The user approved the package and five-document commit, saved as `7586f68`. [Implementation evidence](../benchmarks/combined-monitor-300ms.md) records61passing fake contracts in1.901s after the expected red result; focused Ruff lint/format passed. One300-ms constant now supplies both guards and diagnostic limits. No native run or other limit change occurred. The requested-decision paragraph above is historical; later implementation/results commit and fresh native package remain separately gated.
