# T17-IF-SMC — findings

Approved planning commit: 68e012c. Six public responses/16 visits/three verified batches and two exact manifests were reviewed. No installation, candidate/native/model run or application implementation.

## Source findings

The initializer initializes logging; the fork hook is Unix-only. The local-file constructor delegates to the underlying loader. Generated exports, dependencies and packaged Windows effects remain unproved. [Initializer](https://raw.githubusercontent.com/huggingface/tokenizers/301277072263fb3830eb66eec7e47adadf76f1dc/bindings/python/src/lib.rs), [constructor](https://raw.githubusercontent.com/huggingface/tokenizers/301277072263fb3830eb66eec7e47adadf76f1dc/bindings/python/src/tokenizer.rs).

The template handler returns a prompt without inference. Tokenize defaults: add_special=false, parse_special=true, with_pieces=false; the default response contains IDs. Bind/auth and packaged behavior remain unproved. [Handlers](https://raw.githubusercontent.com/ggml-org/llama.cpp/6c01da6278ab6c69ed67d9124806b50d2b299ba7/tools/server/server-context.cpp).

The device helper recognizes none without its named-device loading branch. This does not prove process-wide CPU/DLL policy. Frame s05 is only device-list printing; s06 stops before complete launch selection. [Device helper](https://raw.githubusercontent.com/ggml-org/llama.cpp/6c01da6278ab6c69ed67d9124806b50d2b299ba7/common/arg.cpp), [Ollama entry](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/llm/server.go).

The candidate HTTP source and pinned directory page were unavailable; no retry/fallback. Failed name searches are not absence proofs.

## Manifest findings

Both expected lengths/hashes matched; 1,565 bytes read. Each declares one model layer:

| Role | Declared SHA-256 | Declared bytes |
| --- | --- | ---: |
| Chat | 183715c435899236895da3869489cc30ac241476b4971a20285b1a462818a5b4 | 986,048,512 |
| Embedding | 970aa74c0a90ef7482477cf803618e776e173c007bf957f635f1015bfcfef0e6 | 274,290,656 |

No blob open/stat or store enumeration. Payload existence/hash, publisher-tokenizer mapping and runtime parity remain unverified.

## Readiness

**Hold native execution.** A concrete trial still needs exact artifacts/provisioning, endpoint/CPU/DLL boundaries, asset mapping, shared limits and explicit residual-risk decisions. A runnable trial is not sufficiently specified here.

| Item | Conclusion |
| --- | --- |
| G01 | Prior syntax evidence retained; no absence-of-effects claim. |
| G02 | Native/local-file entry narrowed; packaged/dependency effects open. |
| G03 | Handler defaults narrowed; bind/auth open. |
| G04 | Device helper narrowed; full DLL/backend/launch policy open. |
| G05 | Seventeen dependencies; artifact/ABI/root-lock/provisioning gates unchanged. |
| G06 | Licence/notice/Hub/FSSpec timing unchanged; no risk exception. |
| G07 | Manifests/descriptors verified; payload/tokenizer equivalence open. |
| G08 | FP01–FP08/NP01–NP08 retained; no native parity passes. |
| G09 | Future ownership/isolation/privacy/resource execution remains gated. |
| G10 | Optional helpers deferred; mandatory dependencies retained. |

## Checks and limits

107 identities matched. Local smoke/five refusals and sixteen combined bridge/parser cases passed final GREEN after RED/mutation/restoration. Formatter oversize refusal passed. Supervised controls exited zero with EOF/reaping. No application tests or Ruff/pytest.

A fixed-metadata quoting failure occurred before response reads; correction consumed starts, without refund/source retry. A premature caller stop flag was corrected before any real gateway boundary. Failed control/update attempts remain recorded.

15 frames persisted/14 displayed; 14,412 frame bytes. Optional reporting refused the last provisional note before output at 24,426 used bytes; protected closeout followed. Four owned annotations have zero-hash sentinels, not source proof. Other source hashes identify retained responses; projections are partial.

Ignored root data/t17/tokenizer-source-metadata-02/ retains controls, responses, projections, readiness checklist and terminal reconciliation/check results. No machine-wide confinement/offline claim. Five results await commit approval; no new native trial/adoption/G2. [Historical stop](tokenizer-source-metadata-review.md) unchanged.

Closeout limitation: the Git-status child persisted its capture, but the frozen controller reporter then rejected its status with report_reserve. The other two controller-based Git checks were not run. Final verification uses the saved status and direct identity/link/format checks; no full Git-diff/controller-closeout pass is claimed. Next propose a bounded correction allowing closure reports to use the protected reserve, with refusal/mutation tests and existing evidence reused; no new research or native actions.

## Follow-up — 2026-11-18

The approved RPT reporting correction (planning commit 8c07563) addresses the missing closure phase and status reservation. See [its separate findings](tokenizer-closeout-report-fix.md) for test and supervised integration evidence. This addendum does not rewrite the earlier failed controller outcome or change the native-readiness hold.
