# T17-IF-CC — capture verified; parser guard conflict diagnosed

## Outcome

The user approved CC1–CC5 and its planning commit, made as `86bdaa9`. Complete subprocess capture is now demonstrated by eight synthetic controls. The single permitted parser attempt still failed, but its **entire 1,791-byte error** was retained. The audit guard rejected `socket.gethostname` while packaging asked Python for platform information. No dependency graph, licence/provenance research, installation or runtime adoption followed.

The [approved package](../proposals/reconciliation-capture-correction.md) and the [earlier incomplete-capture result](wheel-evidence-reconciliation.md) remain the boundaries and historical context. Ignored evidence is under `data/t17/reconciliation-capture-correction-01/`; older roots were read-only throughout.

## Work and checks

| Task | Evidence / result |
| --- | --- |
| CC1 | Four pinned prior inputs matched; 20 installed packaging source hashes matched; its installed METADATA and RECORD were frozen. Only the four reviewed loader/control/support functions were copied, excluding old graph/inspection/command dispatch. |
| CC2 | A deterministic staged-read assertion failed as expected: a first read omitted the final diagnostic. Capture now drains separate binary streams concurrently to EOF, with aggregate admission, timeout and ownership evidence. |
| CC3 | Eight GREEN cases passed: empty streams, delayed stdout/stderr, full nonzero traceback, exact 8 KiB aggregate boundary, split UTF-8 bytes, intentional overflow, timeout and injected reader failure. All eight synthetic children exited. |
| CC4 | Exactly one parser attempt; child exit 1, complete stderr capture, empty stdout, exit verified. The controller exited 0 because it successfully recorded the failed parser result; this is not a passing parser check. |
| CC5 | Findings and receipt recorded. Final preservation/scope/link/whitespace/readable-diff/empty-index checks are recorded below. |

Three ordered check invocations were used: RED, GREEN, parser. All three host controllers exited; the expected RED controller exited 1. No rerun or orchestration correction was needed. Eight synthetic children plus the one parser child exited. Zero Ruff runs, web calls, model calls or candidate installations/imports occurred. Packaging 26.3 was imported only as the already approved review tool.

The harness and fixture source were authored together before the RED command. Execution followed RED then GREEN, but this does **not** establish strict test-before-implementation authoring order. This sequencing deviation is retained rather than claiming full test-first compliance. The RED assertion tests the original short-read defect; the GREEN cases exercise the new capture function.

## What the parser error establishes

The retained traceback follows `default_environment()` → `platform.machine()` → `platform.uname()` → `_node()` → `socket.gethostname()`. The review's audit hook rejects every event starting with `socket.`, including that hostname query. The traceback does not show a connection or download attempt. It does not prove that every remaining platform/helper call would pass after this event is allowed.

The initial `os.uname` AttributeError appears inside Python's Windows fallback handling; the final terminating error is `RuntimeError: Forbidden parser operation: socket.gethostname`. There is no evidence here of corrupt wheels, incompatible dependency versions, insufficient RAM or a model failure. The parser marker assertions have not passed, and its graph remains unexecuted.

The guard was left unchanged. No second parser attempt was made. No hostname value, user documents, prompts or model data were collected or sent externally.

## Limits and reproducibility

The local receipt records the exact interpreter commands, PIDs, exit codes, raw stream bytes in base64, decoded display text, EOF/overflow/timeout/reader-error flags and monotonic durations. Scripts remain ignored evaluation artifacts, not verified application functionality or a general hardened runner.

| Authored local source | Bytes | SHA-256 |
| --- | ---: | --- |
| `capture.py` | 4,482 | `15849ddbd03c992da78baee314b48731c036d7ab5563e1719e61892f64b590d3` |
| `controls.py` | 5,956 | `a1588c81a7cdeeed9c862ce39a49bbfd9ae93560b18bcd48bbd9ff2d7bdaabc3` |
| `parser_controls.py` | 3,072 | `41261c05e5f876c72a24b1a0818650e58a562209e46359b8fc3858b526fcbc53` |

The approved negative overflow produced 8,193 bytes; capture retained the 8 KiB allowance plus its one-byte sentinel, explicitly marked incomplete. Timeout/reader-failure results were also intentionally incomplete, with child teardown verified. Normal admitted results reached both stream EOFs. These narrow controls do not prove behavior for arbitrary commands or descendants. No Job, filesystem confinement, kernel egress guarantee or memory benchmark is claimed.

At the interim result receipt: 236.352 active/wall seconds, no host-wait exclusion; 48 work units and 32 process starts prepaid. Final conservative leases, elapsed time and retained bytes are in the local summary. Read accounting covers the explicit inspection/capture leases, not total operating-system/interpreter I/O.

## Smallest next decision

| Option | Benefit / consequence |
| --- | --- |
| Review a narrow exception for `socket.gethostname` only | Retains packaging's normal marker-environment construction. First inspect its actual platform call path; keep connection/DNS-resolution/subprocess restrictions and avoid recording the hostname. This changes the reviewed guard and requires approval before execution. |
| Review a supplied marker environment | Avoids collecting unnecessary machine identity, but must establish whether the library still invokes its default environment internally. Do not assume that passing a dictionary alone avoids the blocked call or monkeypatch private internals without review. |

Recommend preparing a small source-only comparison of these options, then approving one exact correction and control attempt. Do not broadly permit `socket.*`, disable the guard, alter dependency pins or resume graph/research automatically. This review closes the capture diagnosis, not the dependency/adoption or G2 gates.

Closeout checks passed: six-document scope; 10 frozen inputs preserved, including SPEC, lock/configuration, dependency records, evaluation manifests, existing versioned tests and the historical checkpoint; 20 tool-source/two installed metadata hashes unchanged; 22 local links, whitespace, readable diff, empty index and non-null summary checked. The inserted preflight section was moved to the top and its extra EOF blank line removed before the check. Results commit and follow-up preparation/execution retain their approval gates. The strict authoring-order deviation in CC2 remains open for review.
