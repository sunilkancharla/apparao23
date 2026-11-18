# T17-IF-PBF — retained-source findings and readiness

## Result and scope

Planning committed as **`55ecaf3`** after the user approved the four-file commit and PBF1–PBF6. The bounded static review produced **13 frames in five groups**, covering sixteen Python file roles and three saved CPU/build-source responses. It did not install or run a candidate. Native readiness, offline behaviour and token-count parity remain unproved.

Evidence is local under `data/t17/tokenizer-preflight-frames-01/`: frozen identities, accounting/formatter controls, frame manifests, `python-review.json`, `readiness-matrix.json`, verification and terminal receipts. These ignored artifacts are not application features or committed data. The [proposal](../proposals/tokenizer-preflight-frame-continuation.md) defines the package and limits. Earlier RBF/RSR failures remain unchanged.

## What the Python review establishes

The root initializer imports the native `.tokenizers.Tokenizer`, then imports five Python wrapper classes. The shown Python import graph does not import Hub or the visualization tools directly. This describes inspected Python projections; it does **not** establish what native initialization, dependencies or unprojected definition-time expressions do.

| Files under `tokenizers/` | Reviewed role / evidence |
| --- | --- |
| `__init__.py` | Full normalized initializer: type aliases/enums, native exports and wrapper imports. Frame f01; original module lines 1–111. |
| `implementations/__init__.py` | Full normalized imports of BaseTokenizer and five wrappers. f02; original lines 1–6. |
| `decoders`, `models`, `normalizers`, `pre_tokenizers`, `processors`, `trainers` initializers (six files) | Native aliases/re-exports; the normalizer name-dispatch helper is also displayed. f03–f05, including all three continuation parts. |
| `implementations/base_tokenizer.py` | Imports native/typing aliases; constructor default projection. Bodies unread. f06; coarse original module range 1–477. |
| `implementations/bert_wordpiece.py`, `byte_level_bpe.py`, `char_level_bpe.py`, `sentencepiece_bpe.py`, `sentencepiece_unigram.py` (five files) | Imports, class bases and selected constructor/file-helper default-expression projections; selected annotation-call lists are empty. SPM conversion has an indented `sentencepiece_model_pb2` import edge. Constructor, training and file/SPM helper bodies remain unread. f07–f09, all three parts. |
| `tools/__init__.py` | Imports the visualizer; absent from the shown root/default wrapper import graph. f05. |
| `tools/visualizer.py` | Optional visualization module with a module-level CSS-file read and indented IPython/HTML display edges. Bodies and CSS payload unread. f10; coarse original range 1–420. |

Frames preserve original source identities and coarse module ranges. Their displayed code was normalized with docstrings removed; normalized positions are not precise original-line quotations. Constructor/file-helper projections used AST-only inspection of declarations, never execution. Other method defaults, decorators, class statements and annotations outside the selection remain unverified.

The direct local-file target is the native `tokenizers.Tokenizer` API. Python wrapper helpers are separate optional paths. Previous Rust binding/core local-read evidence is retained, but the native initialization and exact packaged/source correspondence are still open. No pretrained/download API was invoked and no assumption that local-file loading waives the declared dependency graph is made.

**Evidence-description correction:** `python-frame-ledger.json` inherited an overbroad selection description about complete file/SPM bodies. The actual frames contain projections, not those complete bodies. `python-review.json` and this report correct that description explicitly; no body-completeness conclusion relies on it.

## CPU/server/build projections

The three saved response envelopes remain hash-bound. Upstream llama.cpp is pinned to `6c01da6278ab6c69ed67d9124806b50d2b299ba7`; the saved Ollama compatibility projections are from v0.40.16.

- **f11:** the server role branch chooses an instance when a model path, Hub repository or Docker repository is present; otherwise it chooses a router. This supports requiring an explicit local model path in a future design. It does not prove a no-download policy.
- **f12:** the argument projection accepts numeric GPU-layer values through integer parsing and separately handles automatic/all settings. Zero has a numeric interpretation; packaged CPU-only behaviour and other device settings still need validation. The selection also contains unrelated argument matches; they do not support additional conclusions.
- **f13:** compatibility is included before fetching/building llama.cpp and extra compatibility sources enter the target. Upstream source is consequently not proof of exact packaged-server behaviour or a complete DLL load set.

Local bind, authentication, route handlers and request/token-ID semantics were **not established** by the admitted excerpts. Some route matches exist in saved evidence but did not fit this selection. The CPU ledger preserves selected and unread matching response-line numbers. Missing matches in partial projections are not evidence of absence; complete source files were not reviewed.

## Readiness matrix and next decision

| Category | Conclusion |
| --- | --- |
| Supported by static evidence | Saved identities; sixteen Python role/import projections; root native alias; selected numeric GPU-flag and model-role branches; compatibility source injection. |
| Runtime validation needed | Native initialization and local-only file behaviour; actual DLL loading; rendered token IDs/BOS/EOS/template/prefix parity; separate embedding policy; CPU-only behaviour, complete-answer latency and total memory. |
| Indispensable prelaunch gaps | Unprojected Python definition-time behaviour; exact native/dependency provenance and load-set controls; localhost/auth/routes/request contracts; mapping CPU/server settings and compatibility changes to the exact packaged artifact. Existing licence/build/17-dependency gates remain open. |
| Optional/deferred | Wrapper construction/training/file/SPM helper bodies and tools/visualization paths outside the shown default Python graph. Deferral does not remove declared dependencies or waive mandatory acceptance criteria. |

Recommend **preparing a narrow prelaunch-gap closure**, starting with retained default-expression and server control-plane evidence, then naming any indispensable native/DLL facts that require new source access. Compare this with a native trial now, which remains blocked, or deferring standalone-tokenizer work, which would require a separate input-fit approach decision. No option is adopted by this report. Do not repeat wheel/archive inspection or expand into unrelated optional helpers.

## Controls, failures and closeout

PBF1 verified nine pins, 44 carried identity rows and six reviewed skills. The actual gateway smoke and duplicate, undercharge, stopped-state, start-cap and zero-write report controls passed. Prepaid prelude starts are reconciled separately; this is owned-graph accounting, not machine-wide auditing.

PBF2 observed meaningful missing-bound RED. The first GREEN attempt failed because the Unicode fixture's frame was still within the permitted size; its rejection expectation was wrong. The same case was corrected to an unambiguously oversized escaped frame, without relaxing production limits. Final sixteen-case GREEN, caught response-bound mutation, exact owned-source restoration and restored GREEN passed. Every supervised child, including the initial exit-1 control, finished with complete capture/EOF/reap.

Python selection preparation had six pre-output size refusals and one syntax error before writing a manifest or printing candidate frames. Narrowing/grouping corrected these inside the same allocation. No returned source capture was truncated, no limit was raised and no counter was reset. Constructor/helper bodies were explicitly deferred, not silently represented as reviewed.

Final checks cover preserved identities, frame/count/size totals, control results, exact authored scope, local links, UTF-8/whitespace, readable tracked/new-file review, empty index and known child exits. Exact resource reservations/observations, read leases, measured artifacts and terminal-tail reservations are in the local terminal receipt. Optional source work finished at 51 reserved starts; closeout uses the protected allocation. A final reply is prepaid before the terminal snapshot.

No public calls, downloads, installations, candidate imports/executable compilation, native/model/service runs, wheel/model/tokenizer asset reads, pytest/Ruff calls, global changes or checkpoint writes occurred. G2/application implementation, a native trial, final adoption and the results commit retain separate approval gates. Five result documents await review/commit.
