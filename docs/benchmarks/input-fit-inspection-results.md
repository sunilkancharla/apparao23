# T17-IF-R — bounded inspection stopped at open-handle identity check

## Outcome — 2026-11-16

The user approved the [exact IF-R package](../proposals/input-fit-inspection-correction.md) and its five-document commit, recorded as `dee832a`. Two standard-library aids were authored test first. All20focused tests and Ruff passed, and an in-memory mutation of second-attempt admission was caught. The one permitted real metadata child then stopped on its first file, before reading content. Its exit was verified; there was no retry.

This is a **partial investigation, not successful metadata verification**. The earlier IF-S manifest evidence remains valid as historical evidence; this attempt verified no new model contents. Config/template/license layers, tokenizer/rendering parity, exact input fit, native trust and G2/application adoption remain unresolved. No model weights, user documents, prompts or answers were read; no model/native dependency was loaded, installation performed, service started or network request made.

## What changed and what was tested

- [Inspection aid](../../tests/evals/spikes/input_fit_metadata.py): finite lexical ancestry, ancestor type/reparse checks, before/open/after identity checks, pinned digest/size,64KiB+1bounded reads, conservative1MiB aggregate charging, flushed per-file receipts, explicit single-child dispatch,30-second communication timeout and5-second kill/reap wait.
- [Fake tests](../../tests/evals/spikes/test_input_fit_metadata.py): drive roots/case/trailing separators, traversal/outside/root/depth/non-progress, wrong types/reparse, digest/size/oversized/cumulative reads, changed handle/path identity, read/receipt errors, malformed/empty/oversized/stderr/nonzero output, timeout/kill/reap failure, spawn failure and second-attempt refusal. They do not launch trial/control children or read real metadata.
- Review corrected pipe cleanup: if reap fails, do not synchronously close pipes that Windows communication reader threads may still own. Unknown cleanup remains a failure, never success. This was verified with mocks; real kill/reap failure was not induced.

Commands actually executed from the repository root:

```powershell
& 'F:/Python/Python314/python.exe' -I -S -B tests/evals/spikes/test_input_fit_metadata.py
.\.venv\Scripts\ruff.exe check tests/evals/spikes/input_fit_metadata.py tests/evals/spikes/test_input_fit_metadata.py
.\.venv\Scripts\ruff.exe format tests/evals/spikes/input_fit_metadata.py tests/evals/spikes/test_input_fit_metadata.py
& 'F:/Python/Python314/python.exe' -I -S -B tests/evals/spikes/test_input_fit_metadata.py mutation
```

Initial red: expected `ModuleNotFoundError` before implementation. First green:19tests/0.036s; initial Ruff found six style/import/exception/mutation-annotation issues and unformatted files. These were corrected. Next green:20tests/0.032s, Ruff passed; mutation correctly exited1 with one failed second-attempt test/0.004s. After the pipe-cleanup review,20tests passed0.033s and Ruff passed again. Final whitespace/format/preservation/document checks accompany closeout. No unrelated historical/native suite was rerun.

## One real attempt and cleanup evidence

The controller was invoked once, after controls and three seals passed:

```powershell
& 'F:/Python/Python314/python.exe' -I -S -B tests/evals/spikes/input_fit_metadata.py controller
```

**Historical command only: the allocation is consumed; do not run it again.** The controller consumed the durable attempt flag and exclusive claim before spawning the sole metadata child with an explicit argument vector, `shell=False` and base Python `-I -S -B`. No venv redirector or descendant-spawning path was used. Whole tool return fields were retained in `data/t17/input-fit-inspection-01/execution.json`; no active tool session was lost.

| Observation | Recorded evidence |
|---|---|
| Controller status / exit |`stopped_no_retry` /1 |
| Sole child |PID36180, retained owned process object; no process-name discovery/attachment |
| Child exit / reap |1 /true |
| Communication duration |0.4796100999810733seconds; timeout did not fire |
| Captured output |53bytes stdout,0stderr; sanitized failure packet |
| First file |`qwen_manifest`, status`refused`, error type`Boundary` |
| Content bytes read |0 |
| Conservative charged metadata bytes |65,537of1,048,576; reserves the entire possible bounded read |
| Remaining files |Not attempted; no findings file completed |

The source path reached `charged_bytes +=65537` but never reached `read_bytes +=len(raw)`. The only `Boundary` check between these points compares the open handle's identity tuple with the prior path stat. This locates the refusal to the **open-handle/path identity comparison**. The receipt did not retain individual stat fields, so which field differed and why are unknown. It is not evidence of a corrupt model, a hostile file replacement or a Python/native-library defect. The fake tests use matching synthetic stat fields; they did not establish real Windows stat/fstat equivalence.

No missing layers were reread/downloaded, no guard weakened and no old allocation reset. Retain the refusal and keep this aid withdrawn from further real execution pending a new bounded decision.

## Sealed artifacts and accounting

| Artifact | SHA256 at attempt |
|---|---|
| Inspection aid |`2d47b7c816dba4092c755a4787fee6f394e4bd628a9d77f4829b3da98ed04204` |
| Fake tests |`e4371ff8834d90a3488187d271f7f3e88e4832f105dd8c25ab1728f6a90724e8` |
| Base Python executable |`03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38` |

Fresh ignored root: `data/t17/input-fit-inspection-01/`. Before optional work, persisted the full80-unit manifest (64normal/16protected),1,200-second clock and2MiB output ceiling. Eight prior specification/rules/lock/source/closed-meter identities were captured and rechecked before launch. All orchestration/shell/test/lint/mutation/controller/child/report work is covered by the same prepaid phase blocks; no start counter limited only to the adapter is claimed. Three pre-epoch approval/commit inspection actions belong to the separately approved Git closeout, outside this epoch.

All64normal units are retained as conservative phase reservations, with protected capacity used only for final preservation/reporting. No refunds or new work after the real refusal. Final observed elapsed time, charged time, output count, seals and preserved hashes are recorded in the closed meter. No synthetic files were generated; all negative controls were mocked/in-memory. This connected stdlib/public-metadata boundary has **no filesystem/outbound confinement or kernel RAM-cap claim**. Captured-output limits rely on the sealed worker's fixed small output; they are not a general malicious-child memory limiter. No real process-creation or failed-cleanup deadline was measured.

## Next decision

Recommend a narrowly bounded **synthetic-only Windows file-identity comparison**, using a tiny owned fixture and retaining the exact path/open-handle fields. Decide which stable identity/mutation checks are valid on this interpreter/filesystem before proposing another model metadata attempt. Do not merely remove the comparison. No such follow-up, new fixture, replacement metadata run, tokenizer integration or application implementation is authorized by this report.

Separate approval is required to commit the two aids and six findings/status documents. Existing [IF-S findings](input-fit-static-review.md), [input-fit design](../proposals/input-fit-preflight-design.md) and [public-source review](public-source-web-review.md) remain unchanged.
