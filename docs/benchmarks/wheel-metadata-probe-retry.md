# T17-IF-PR — native metadata probe passed

## Outcome

On 2026-11-17, the user approved PR1–PR3, including its explicit timing/supervision changes. Planning committed as `103a6f1`. The [approved probe-only package](../proposals/wheel-metadata-probe-retry.md) completed its controls and single metadata request. No wheel was downloaded, imported or installed.

The reused reporting controller passed all **12 synthetic checks**. The fixed native probe then returned `probe_passed`: one HTTP transaction, 14,674 received status/header/body bytes, and 11,931 metadata-body bytes. Its reported elapsed time was **0.227 seconds**. The response body SHA-256 is `8cb454b83f94ed17f8ffbb5b555f61d515d9c2e4925b8fdc3e789469706408f7`.

The probe's public-DNS/address, certificate, status/framing, duplicate-key/schema and fixed-entry checks passed on this response. [PyPI release metadata](https://pypi.org/pypi/httpx2/2.16.2/json) declared `httpx2-2.16.2-py3-none-any.whl`, size 97,893 bytes, non-yanked, with the expected publisher checksum `f05c13aade4c45dbf1c9060647a1058f0acad62398fad96e741269edb33d46f5`. These are verified response declarations; the wheel payload itself was not acquired or verified.

## Timing and ownership evidence

The submission marker and escalation request ran sequentially inside one orchestration call, without intervening model work. The native command recorded entry before guards. The measured **host-review/queue interval was 503.628 seconds**, excluded once under the newly approved rule. This is not a measurement of pure human waiting.

At the first result review, wall elapsed time was 679.753 seconds and active elapsed time was 176.124 seconds. Those are interim measurements; final active/wall totals are in the closed summary. No timer was silently reset, and no second request was attempted.

The controller captured the probe's streams concurrently, waited for its child and reported clean teardown. An outer owned wrapper supplied the controller's verified launcher bytes through stdin, concurrently copied both streams using finite buffers, retained its process handle/birth/exit evidence, and applied a 60-second timeout plus bounded teardown wait. Both processes exited with code 0; neither timeout nor output overflow occurred. Probe stdout/stderr were 224/0 bytes; controller stdout/stderr were 139/0 bytes.

Four samples of the controller's private memory peaked at 11,243,520 bytes. The probe child and total owned-process memory were not sampled. No 512 MiB enforcement, filesystem/kernel-egress confinement, offline-runtime capability or product memory/latency guarantee is claimed.

## Scope and retained evidence

The copied `control.py` and `probe.py` matched their fixed hashes and remained unchanged. One synthetic suite ran; no Ruff or new implementation suite was needed. No candidate package code, model/Ollama call, user document or large archive was involved. No new versioned helper or application feature was implemented. The earlier closed roots and historical checkpoint were not written.

Local evidence is retained under `data/t17/wheel-metadata-probe-01/`: controls, frozen inputs, fixed source copies, launcher identity, submission/entry clocks, suite/probe/capture/outer receipts, metadata body, meter, readable diff and validated closeout summary. Raw metadata is not echoed into reports. The source copies, metadata and other runtime artifacts remain excluded from Git.

Bootstrap/controls, probe, findings and protected closeout each prepaid eight work units, totaling 32. The ledger separately accounts for every shell/controller/child start, read/report leases and the single HTTP allowance. Closeout checks passed for the six-file scope, six touched local links, 17 unchanged frozen inputs, original/copied source pins, response hash, preserved specification/configuration/historical checkpoint, empty index, whitespace and readable diff. Final process/disk/time measurements and validated summary belong to the closeout receipts. The separately approved planning commit preceded this execution epoch.

## What this resolves and what remains

This attempt demonstrates that the reviewed native path could retrieve and validate this specific public metadata response at this time. It resolves the probe prerequisite for designing the next bounded artifact-review package. It does not establish that previous network failures shared one cause or that every endpoint/transport will work.

Wheel acquisition, test-first inspection aids, the other release metadata, RECORD/notices/native inventory, source mapping, licence/security/offline/parity review, installation and G2/runtime adoption remain unfinished. Next request a separate results commit and prepare the remaining bounded acquisition/static-inspection package, reusing the successful response only if that new package explicitly admits it. No further download or execution is authorized by this closeout.
