# T17-IF-S — partial static artifact review

## Outcome

The approved input-fit design/IF-S package was committed as `145278f`. This metadata-only investigation verified both selected manifest hashes but stopped when the subsequent layer-inspection shell did not finish. That identified shell was terminated and its exit verified. No layer completion receipt was persisted: template/config contents and hashes are **not verified by this investigation**.

No dependency/model/parser/OCR/extension was loaded; no inference, service, installation, download, web call, fixture generation or new executable aid was used. No private documents or saved prompts/answers/token output were read. No adapter or G2 runtime adoption occurred. Existing provisional settings remain unchanged.

## Verified manifests and declared layers

The two manifests were read below the project-owned `data/ollama/models/manifests-v2/ollama.com/library` root after containment, ancestor reparse-point, type, size and expected-hash checks.

| Manifest | Bytes | Verified SHA256 |
|---|---:|---|
| Qwen2.5:1.5b-instruct-q4_K_M |857|`65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b`|
| nomic-embed-text:v1.5 |708|`0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f`|

These referenced files are **manifest declarations**, not fresh file verification:

| Role | Declared bytes | Declared SHA256 |
|---|---:|---|
| Qwen config |487|`377ac4d7aeefd5b870c9fccff9a6d4df36901d99fe3277c2f755bc401601ba1c`|
| Qwen system |68|`66b9ea09bd5b7099cbb4fc820f31b575c0366fa439b08245566692c6784e281e`|
| Qwen template |1,482|`eb4402837c7829a690fa845de4d7f3fd842c2adee476d5341da8a46ea9255175`|
| Qwen license |11,343|`832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e`|
| Nomic config |420|`31df23ea7daa448f9ccdbbcecce6c14689c8552222b80defd3830707c0139d4f`|
| Nomic parameters |17|`ce4a164fc04605703b485251fe9f1a181688ba0eb6badb80cc6335c0de17ca0d`|
| Nomic license |11,357|`c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`|

Qwen declares separate system/template layers; Nomic declares no separate template/system layer. Neither observation establishes effective rendering, special tokens or context. Declared weight identities/sizes match the carried-forward inventory: Qwen `183715c435899236895da3869489cc30ac241476b4971a20285b1a462818a5b4`/986,048,512bytes; Nomic `970aa74c0a90ef7482477cf803618e776e173c007bf957f635f1015bfcfef0e6`/274,290,656bytes. No weights were read, parsed or rehashed.

Verified metadata reads total1,565bytes. Conservatively charge the unfinished command's entire intended25,174bytes as potentially inspected:26,739bytes total against1MiB. This is a charge, not a claim that seven layers were opened or verified. Declared per-file sizes are below64KiB; actual layer acceptance was not established.

## Inspection failure and verified cleanup

The layer command returned no output after approximately10seconds. I retained only its output field, losing any session identifier/exit metadata. A subsequent durable-state check showed only the manifests/1,565bytes, with no layer result. This did not establish that the shell had exited.

Sandboxed read-only process discovery was denied; the required escalated check found the inspection PowerShell still running. Before termination its known command markers, process ID and creation time were checked against a retained process object. Killing that owned shell and waiting up to5seconds verified exit. The discovery command also matched itself; it was not targeted. No candidate worker was started.

The exact stall point/cause is unproven. Do not infer corrupt model assets or a native/runtime defect. No replacement read, metadata retry, missing-layer download or old-allocation reset occurred. A failed documentation patch was also counted; it changed no files and was corrected within report authoring.

For a successor: retain the full execution result/session handle, bound inspection-controller duration, persist per-file progress and test ancestor-walk termination with synthetic path values before another metadata read. These corrections were not implemented here and require a new exact package.

## Adapter comparison and next decision

| Option | Evidence / costs still to establish | Decision |
|---|---|---|
| Public exact count-only operation |[R1-W](public-source-web-review.md) did not establish one for the pinned version |No invented endpoint or zero-output workaround |
| Exact rendering plus matching tokenizer |Tokenizer artifact/version, special-token parity, license/native dependencies, Windows compatibility, offline behavior and latency/memory footprint unestablished |Promising design; no dependency selected or installed |
| Owned runner internal operations |Could reuse its tokenizer, but rendering/context parity, endpoint ownership/lifetime, native trust and resource cost need validation |No internal port discovery/attachment or runtime calls approved |
| Runtime modification |Changes evaluated build/provenance and maintenance/security scope |No build or modification approved |
| Byte guards/truncation refusal |Resource safeguards do not prove exact count or output headroom |Insufficient alone for the unchanged gate |

**Recommendation:** repair the bounded inspection first, then finish the two configs, Qwen system/template and Nomic parameter metadata. Compare a matching-tokenizer integration against the owned-runner option using those facts and an explicit dependency/trust decision. Retain the adapter blocker rather than select from incomplete evidence.

Actual renderer/template, serializer, effective context, special-token parity and192-token output/termination accounting remain unresolved. Separate Nomic prefixes/768dimensions, fail-closed admission, the proposed eight packing candidates and all provisional R01 byte/context settings remain unchanged. No native/vendor notices or transitive advisory gaps listed in R1-W are cleared. Windows11/16GB/CPU-only resource targets were not measured.

## Accounting and handoff

Fresh ignored record: `data/t17/input-fit-static-01/meter.json`. Full64units/900seconds/2MiB prepaid before optional inspection: initialization8, metadata12, design8, review12, close8, protected16. Fourteen source/spec/lock/old-meter identities were captured. The separately approved Git closeout preceded this epoch.

Initialization used two4-unit blocks. Metadata used three4-unit blocks, including the unfinished call. Review used three4-unit blocks: state check, denied discovery and escalated discovery. Owned-shell termination used4close units. Report edits (including the failed patch), documentation verification and receipt closeout use remaining design/close/protected reporting slots; no new research. Full reservations are retained without refund. Final elapsed/output/preservation/admission values are recorded locally.

Read-back review verified308local links, all14preservation hashes and whitespace;362.798seconds elapsed at that check. No new application tests or vulnerability audit were run. Four protected reporting/verification units cover closeout overhead; total conservative admissions are52of64prepaid units. Final elapsed/output values are stored locally. Only six authored findings/status documents are proposed for Git, with separate commit approval. Preserve old closed sources/ledgers and unrelated user assets. No retry under this allocation or claim that input-fit/native-trust/G2 acceptance is satisfied.
