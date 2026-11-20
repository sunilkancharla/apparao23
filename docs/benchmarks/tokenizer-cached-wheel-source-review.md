# T17-IF-WSP — cached Python source findings and accounting stop

## Outcome

**Stopped, incomplete, pending review; no adoption.** Planning commit: `4a8275a`. The user approved WSP1–WSP5. The static reader obtained useful evidence, but the parent did not correctly enforce the approved combined process/report budgets. These findings do not constitute compliant package acceptance or permission to install/run a tokenizer or CPU reference.

Local evidence is under the ignored `data/t17/tokenizer-wheel-source-01/` root. `summary.json` and immutable `receipt-007.json` record the stop. No session-checkpoint file was created or updated. No further processes were launched after detecting the accounting problem, so final Git/diff/link/preservation checks remain **not run**.

## Static evidence obtained

- Reverified the cached Tokenizers 0.23.3 Windows wheel's 2,872,101-byte outer identity: SHA-256 `1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3`.
- Admitted all **31** ZIP entries against the frozen names/sizes and metadata/layout rules. Read only the **16 Python members**, **66,467 bytes**, and matched every frozen member hash. No `.pyd`, DLL, metadata, notice, stub or other unselected payload was opened/decompressed. Raw outer hashing necessarily included compressed native bytes.
- Retained text as escaped JSON, not extracted executable files: `sources.json`, **130,664 bytes**, with **6,652 AST nodes** and syntactic import/call/definition maps. The reader recorded **3,093,151 charged bytes**, including conservative preleases and actual expansion charges; this is not measured OS I/O.
- The one static worker exited 0; bounded capture records its direct handle/birth identity, both stream EOFs and reaped exit. No tokenizer import, candidate native execution, model inference, installation or network operation occurred in that reader.

All sixteen files have syntactic maps. Semantic review is partial:

| Files within the wheel | Observed role / remaining question |
| --- | --- |
| `tokenizers/__init__.py` | Exposes `Tokenizer` and other symbols from the native `.tokenizers` extension and imports implementation classes. Python text does not establish extension initialization behaviour. |
| `implementations/__init__.py` | Imports the wrapper implementations; not an independent pure-Python tokenizer. |
| `implementations/base_tokenizer.py` | Wrapper source retained and mapped. Its complete file-loading/pretrained contract has not been semantically reviewed in this package. |
| `implementations/bert_wordpiece.py`, `byte_level_bpe.py`, `char_level_bpe.py`, `sentencepiece_bpe.py` | Implementation wrappers depend on native-backed tokenizer components; source retained, hashes and syntactic maps verified. Their runtime behaviour is untested. |
| `implementations/sentencepiece_unigram.py` | Includes an additional `sentencepiece_model_pb2` import edge. Reachability/optional-use implications remain unreviewed. |
| `decoders`, `models`, `normalizers`, `pre_tokenizers`, `processors`, `trainers` package initializers | Re-export native-backed package namespaces; native implementations were not read or executed. |
| `tools/__init__.py`, `tools/visualizer.py` | Visualization imports include IPython edges. Reachability and generated HTML/resource behaviour remain unreviewed; no preview was rendered. |

The earlier Rust `from_file` source observation remains inherited evidence, not a newly proven complete Python/native import contract. All **17 declared dependencies** remain in scope for dependency review, including the required Hub dependency; local-file use does not authorize dependency omission or packaging changes.

## Public CPU-reference evidence

All **three permitted calls / nine explicit targets** were used. Complete tool responses were saved before interpretation; each serialized JSON value passed local byte-size/UTF-8/JSON-roundtrip verification and received a retained SHA-256. Serialized sizes were **29,193 / 30,493 / 29,516 bytes**. These are parsed tool projections, not guarantees of complete source files or binary correspondence.

- The pinned argument projection recognizes main-model `--n-gpu-layers`/`--gpu-layers`/`-ngl` and parses numeric values. This supports the flag's syntax; it does not prove that a particular packaged binary loads only CPU backends or stays within the target memory budget. [Pinned arguments](https://raw.githubusercontent.com/ggml-org/llama.cpp/6c01da6278ab6c69ed67d9124806b50d2b299ba7/common/arg.cpp)
- The server projection distinguishes a supplied model from no-model router mode and registers tokenization/template/counting routes. An explicit local model is relevant to the future design. Bind/auth policy, endpoint request semantics and absence of unwanted remote behaviour were not completely established. [Pinned server](https://raw.githubusercontent.com/ggml-org/llama.cpp/6c01da6278ab6c69ed67d9124806b50d2b299ba7/tools/server/server.cpp)
- Ollama's compatibility build text describes an ordered compatibility patch layer and linked Ollama-owned sources. Unmodified upstream source is therefore insufficient to establish the exact packaged loader/runtime contract. [Compatibility integration](https://raw.githubusercontent.com/ollama/ollama/v0.40.16/llama/compat/compat.cmake)
- Server-context/common and Ollama server-build/compatibility README responses were retained, but their full interpretation was not completed before the stop. No further source request, archive comparison, build, native endpoint request or model asset read followed.

Exact CPU/device-only selection, complete DLL/load set, owned local endpoint/auth/request policy, import/offline behaviour, tokenizer parity and total answer latency/memory remain **unproven**. No native-ready verdict is issued.

## Tests and review

Two authored evaluation files implement the bounded reader and inert controls. The initial targeted RED reproduced the optional-output reserve breach. The first broad run had **31 passed / 1 failed** because its monkeypatch also blocked writing the synthetic fixture; moving fixture construction before the guard corrected the setup without weakening the assertion. Final result: **32 passed**. A deliberately weakened report guard was caught, then original bytes were restored. Final Ruff lint passed.

Controls cover frozen identities, wrong sizes/hashes, missing/extra members, traversal/aliases/types/encryption, local/central disagreement, CRC/truncation, strict UTF-8/source/AST limits, inert source, no native member reads/old dispatch, read precharge, changed/missing inputs and policy denials. Denial tests call the policy directly without external traffic; they are not OS isolation or complete audit-hook integration proof. The controlled reader is not filesystem confinement or machine-wide egress enforcement.

There were **four actual pytest child invocations** (five conservatively charged slots including an initial host-quoting failure before pytest started) and **four Ruff invocations**. Formatting/import/lint issues were corrected before final checks. A later console-encoding error occurred while printing already-retained Python excerpts; public verification and UTF-8 evidence had been saved before that print. No real-wheel/public retry occurred.

## Accounting failure and closeout limits

The tested reader `ReportGate` protected its own output and was reused for later controller summaries. **It did not enforce all parent output or parent process starts.** The parent maintained a mixed conservative/measured reporting counter, but displayed optional excerpts without consistently checking that counter first. It reached **54,201** against the **49,152-byte optional allowance**, crossing the reserved boundary by **5,049**. This is the parent accounting value, not an exact reconstructed UTF-8 total. The overall approved ceiling was 65,536 bytes; the remaining reserve was reduced without authorization.

The parent start counter showed **42**, but counted some shell-plus-interpreter operations as one and omitted several Git/helper starts. Reconstructing visible launches gives **at least 62** against the **48-start combined cap**; exact descendant counts were not measured. Consequently the parent accounting and package compliance cannot be certified. After recognizing this, execution stopped; closeout uses file writes only, without another shell, test, Git or candidate process. This failure is not waived by passing reader tests.

The initial 12 fixed/eight protected identities passed. The final preservation/link/whitespace/diff/index checks, complete artifact/read totals and exact combined process accounting were **not completed**. Their absence must be resolved explicitly before a results commit; no clean-index or complete-preservation claim is made. Initial allocations (64 units, 64 MiB read leases, 16 MiB artifact cap) are reservations, not measured consumption. Elapsed time and the counter snapshot are in the stop receipt; no host wait was excluded.

Known supervised test/check/static children have saved exit/EOF/reap receipts. No candidate service was started. Machine-wide teardown and native safety are not claimed.

## Decision and next step

Keep native trial, dependency installation, runtime adoption/G2 and application implementation closed. Preserve the useful static evidence rather than automatically rerunning it. The next bounded package should first repair **one shared parent meter** for every shell/controller/Git/test/source/display operation, reproduce this combined accounting failure, test pre-admission and reserved closeout behaviour, and complete the omitted closeout checks. Only then resume the unreviewed retained source evidence and decide whether a separately approved native validation is ready.

The result set is six documents plus two evaluation source files. This results commit has **not** been made or implicitly authorized by the planning commit approval.
