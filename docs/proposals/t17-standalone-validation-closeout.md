# T17-SV2 — standalone dependency and input-fit closeout

**Outcome:** [Review closed with explicit blockers](../benchmarks/t17-standalone-validation-closeout.md). Static checks passed; build-source/native-notice prerequisites were not cleared, so provisioning and native parity did not run. The user-authorized reviewed documentation commit closes this attempt; it does not complete T17. Earlier package allowances are not renewed.

## Authority and scope

On 2026-11-19 the user explicitly authorized finishing items 1 and 2, reporting the outcome and committing the reviewed work without further project approval. The selected direction remains standalone Hugging Face Tokenizers 0.23.3 with pinned local assets, with Ollama 0.40.16 for inference. This is evaluation work, not G2 approval or T18 application implementation. Existing licence/provenance conditions are not silently waived.

## Ordered tasks

| ID | Objective and prerequisite | Acceptance and evidence |
| --- | --- | --- |
| SV2-1 | Reconcile the exact seventeen-distribution graph and retained artifacts | Actual wheel metadata, tags, notices, RECORDs, installed reuse and current primary advisory/source evidence; explicit per-artifact disposition before installation. |
| SV2-2 | Provision only if SV2-1 clears the existing prerequisites | uv, project-local environment/cache, full graph and reviewed lock diff; no source builds, dependency omission or global changes. A failed prerequisite blocks this task. |
| SV2-3 | Validate exact standalone/model input handling after SV2-2 | Preserve FP01–08/NP01–08; exact IDs, actual Ollama rendering/preprocessing, special tokens, embedding policy and context/output boundaries. Fake tests cannot substitute for native parity. |
| SV2-4 | Review, report and commit | Tests appropriate to actual changes, readable diff, accurate TODO/PLAN/README and dependency/ADR status; scoped approved commit. Report unresolved prerequisites rather than inventing clearance. |

## Shared execution boundary

Fresh ignored evidence root: `data/t17/standalone-closeout-02/`. Earlier ledgers are closed and unchanged. Include bootstrap inspection/research, negative controls, tests, provisioning, native work and closeout in this allocation: at most 160 owned starts (32 reserved for closeout), four hours elapsed (last hour reserved), 24 public research calls/80 targets, 32 MiB public response/download data, 8 GiB explicit local reads and 256 MiB fresh evaluation artifacts. Before each operation record conservative starts and research allocations in one shared ledger; never reset counters. The initial inspection commands and first four-target web call are conservatively precharged as 32 starts/one public call/four targets. These are allocations, not measured OS process counts.

Native work, if prerequisites pass: synthetic text only; cached weights and tokenizers; no model downloads or cloud evaluation; one heavy job; existing owned Windows Job teardown; CPU-only, loopback, no proxy/redirect; no global adapter/firewall/PATH changes. Reserve at most 20 native starts and 256 local requests within the same total, 900 seconds native activity, 90 seconds per answer, at most 8 GiB owned and at least 4 GiB available RAM. No private sample files. No physical-disconnection or filesystem-confinement claim. Stop native/dependent work on mismatch, missing prerequisite, unsafe ownership, resource failure or uncertain teardown. Independent safe review/reporting may continue.

No package version substitutions, source builds, dependency stubs or edited third-party metadata. Retain exact existing graph and publisher revisions. Hardware validation remains separate; this host does not become the approved physical 16 GB target. No session-checkpoint files. The requested commit is authorized; host write permissions remain separate.
