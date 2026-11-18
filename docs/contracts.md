# Stage 1 application boundary contracts

## Validation addendum — 2026-11-19

[Consolidated T17 evidence](benchmarks/t17-consolidated-closeout.md) adds fake FP01–FP08 contract checks and actual packaged-reference counts. The evaluation helper is not a public API, an authenticated admission capability or implemented application integration. Real counts/proof flags must come from a trusted bound runtime, never a user-supplied count or equality Boolean.

C07's provisional 2,048 context/192 output remains unchanged. Both reference processes actually reported a 2,048 slot; Nomic's earlier 8,192 auxiliary setting is not verified capacity. The reference default n_predict=-1 is not a safe application default: new test requests explicitly set max_tokens=1 and do not validate a full 192-token output/EOS reservation. Unknown overhead still refuses admission; equality still needs proof. The evaluator demonstrates bounded eight-candidate history/evidence removal, source/runtime/rendering identity checks and refusal paths only with injected counts; NP01–NP08 are not fully passed.

Loopback listener ownership and wrong-key rejection were checked for the temporary reference, not the future FastAPI/browser boundary. Existing Host/Origin/CSRF, scope, deletion/recovery, privacy and resource contracts remain requirements for implementation. No application filesystem confinement, strict disconnected runtime or physical-16-GB acceptance is claimed.

## Status, authority and decisions

**Proposed architecture contracts; no application code or G2 adoption.** Prepared under T17-A after readiness commit `e9d107e`. [SPEC](../SPEC.md), approved [T16 design](retrieval-design.md) and explicit user policy decisions take precedence. Mechanisms below are concrete proposals for G2 review; recorded acceptance targets are not measured results or runtime-trial permissions. See [architecture ADR](ADR/0001-stage1-architecture.md) for alternatives and blockers.

During T17-A the user approved: metadata/history/index databases and retained journals count against5GB processed data; upload staging/render scratch/temporary copies count against1GB temporary data; conversation-only originals have a10GB aggregate cap, once per stored content hash. No silent eviction. Existing decimal100MB/file,10references/upload/conversation,1GB unique library originals and all T16 retention rules remain unchanged.

The user also approved validation targets: one heavy job at a time, warm full answers within30seconds,90-second hard answer timeout, at most8GiB across owned app/workers/Ollama and at least4GiB available RAM. These must be tested on the unchanged16GB CPU-only target. They do not adopt the trial harness as application isolation or prove that the full app fits.

## C01 — configuration and local request boundary

Proposed defaults for G2: app at `127.0.0.1:8000`; project-owned Ollama at `127.0.0.1:11435` with an explicit project model store. Ports are configurable; refuse a collision instead of attaching to an unknown service, killing unrelated processes or selecting another host. No LAN, remote model host, DNS-resolved external endpoint, proxy forwarding or cloud fallback. Disable inherited HTTP proxy use for loopback model requests; redirects are not followed.

Use a configured managed application root, proposed `data/app/`, separate from project model/tool assets and historical evaluation allocations. A root must be writable, validated and free of unexpected reparse/symlink ancestry. Never derive it from a model reply, display filename or browser-supplied path. Do not create it in this static package.

Serve assets locally; restrict Host to the configured loopback authority and browser Origin to the exact application origin. No wildcard CORS. State-changing browser requests require a per-process unpredictable anti-CSRF value conveyed by the same-origin app and checked server-side; keep it out of URLs/logs and browser persistent storage. This is a local browser-request safeguard, not multi-user authentication/RBAC. Arbitrary local processes under the same account remain outside that protection.

Treat document text, filenames, persisted imported strings, model replies and local-service responses as untrusted at their boundaries. Escape UI text, disallow raw model HTML/scripts/URLs, and serve previews through scoped IDs. Recommended image preview responses use local PNG rendering with safe content type, `nosniff` and no-store; originals are explicit attachment downloads, never executable HTML previews. Exact CSP/response headers are verified with the implemented browser later; no CDN/telemetry/remote fonts.

## C02 — logical storage and identity

Propose one metadata/history SQLite database also holding the selected vector mapping/index so metadata/vector changes can share a transaction. Tables are logical responsibilities, not executable DDL here: content objects, document identities, conversation/library references, extraction generations, chunks/vector mappings, messages/answers/citations, processing operations, quota reservations and cleanup intents.

Store immutable originals by server-computed SHA256, with hash/type/size verification before reuse. Logical document IDs/reference IDs remain distinct from content hashes. Multiple conversations may reference one library document without new stored bytes; same-byte exclusive attachments do not grant access to each other's reference. Idempotent indexing is unique by content/extraction/chunk/model/prefix/version, not upload filename. Store parser/OCR method/version/confidence/warnings and the exact source coordinates from T16.

Use SQLite foreign keys and explicit transaction boundaries. Proposed first implementation retains DELETE journaling and FULL synchronous behavior from the evaluated storage path; WAL would be a separately reviewed choice because it changes locking/recovery/quota behavior. Never expose half-indexed generations: promote a complete generation in one metadata transaction, and retrieve only the ready generation. On version mismatch mark reindex required, never mix embeddings. No ORM or separate vector server is proposed.

The exact sqlite-vec DLL/hash/notice set is in [dependencies](dependencies.md#t17-a1--static-reconciliation-and-proposed-runtime-set). Load only the pinned absolute file after identity checks, enable extension loading only around that call and disable it in `finally`. SQL `load_extension`, ATTACH/DETACH and unlisted optional functions remain denied. Retain the reviewed cosine MATCH/eligible-rowid/k=eligible-count/stable-top5 semantics and the necessary `match` callback. Parameterize values; identifiers are fixed server schema, never model/user text. The SQL authorizer is not native-code filesystem confinement.

## C03 — quota classes and reservation rules

| Class | Approved cap / counting | Examples and exclusions |
|---|---|---|
| Library originals | 1,000,000,000bytes, unique stored content currently required by library items | Multiple logical library items with identical bytes share the byte charge; references still count separately |
| Conversation-only originals | 10,000,000,000bytes, unique stored content required only by conversation attachments | Content already charged as a live library original is not also conversation-only; class transitions require an atomic destination reservation |
| Processed/retained application data | 5,000,000,000bytes | Normalized text, embeddings/indexes/previews, metadata/history/index database files and retained journals, plus proposed retained operational records/log files; model/tool/evaluation assets excluded |
| Temporary processing data | 1,000,000,000bytes | Upload staging, render scratch, partial outputs, temporary copies and in-flight journal/sort scratch classified below |

Reference-count limit is logical: at most10distinct attached document references per conversation and10files per upload. Repeating the same reference ID does not create an extra reference; creating a new attachment identity for identical bytes still consumes a reference slot. An idempotent request replay consumes no extra slot. An upload is rejected/aborted before committed originals exceed100,000,000bytes per file; Content-Length alone is not enforcement.

Proposed accounting protocol: serialize quota admission in a short SQLite transaction; include actual managed bytes plus active worst-case reservations, accounting for the ledger's own growth. Reserve original destination, temporary staging and processed growth independently before materializing them. Incrementally reserve before each bounded expansion step; if expansion cannot be bounded or the next reservation fails, stop visibly and preserve consistent prior state. Never claim100MB of compressed PDF/XLSX guarantees bounded extracted size. Available disk can fail before a class cap; surface disk-full safely without bypassing quotas.

Retained main databases/journals count as processed. A temporary journal/copy can be charged to temporary while in flight only under an explicit state/classification record; persistent retention transfers its reservation to processed before commit. Never count a file zero times during a transition. Charge logical managed-file lengths conservatively, not inferred compressed NTFS allocation; retained database free pages still occupy quota until an explicitly designed compaction occurs. Automatic vacuum/eviction is not approved. Exact growth upper bounds, journal classifications and compaction policy require validation before storage implementation.

When a library object becomes conversation-only, reserve its entire unique byte charge in the destination class before removing the library charge. Reject a user-requested transition that cannot fit; never delete still-required bytes to force it. Deleting shared data releases original quota only when no surviving content reference needs it and physical removal/class transfer is verified. Cleanup-pending bytes keep their charge; reserve both old/new generations while rebuilding. Model/runtime/cache assets have their own provisioning/disk needs and do not disappear into these quotas; total workstation disk requirements must be disclosed separately.

## C04 — operation idempotency and publication

Propose state-changing creation/processing requests require a client-generated idempotency key reused for retries of that same intent. SQLite atomically claims a unique key scoped to operation/target and persists an intent before side effects. Compare a canonical request fingerprint, including server-verified content hash when bytes are supplied. Same key/different payload returns409`IDEMPOTENCY_CONFLICT`; an in-progress replay returns202with the same operation ID; a finished replay returns the same safe result. Never decide "not seen" with a read followed by an unguarded insert, or release an unknown-outcome intent because a timeout occurred.

Upload admission may claim an intent before its body hash is known; mark the owner and declared metadata, permit only that owner to stream bounded bytes, then seal the fingerprint with verified bytes before promotion. A repeated upload body must be consumed/hashed within bounds before claiming equality, or refused without replaying a success; matching filename/declared size is not proof of matching content. Resumable byte-range uploads are not part of the first slice. Duplicate requests in uncertainty remain pending/conflict until reconciliation, not an extra upload/index/generation.

Accepted operation states: received→validating→processing→ready, with explicit failed/interrupted/reindex-required/deleting/cleanup-pending states as applicable. Publish originals/extractions using owned temporary paths plus atomic file promotion and durable intent; because SQLite and the filesystem have no shared atomic commit, reconcile orphan/promoted/pending artifacts after interruption. A worker never promotes another worker's generation or overwrites an existing immutable original.

At answer start capture conversation selection revision, source/extraction/index versions and supplied-evidence manifest. Before saving/publishing the completed answer, atomically verify those revisions/reference states in the same metadata transaction that inserts the answer/citations. A deletion/selection change invalidates the request; return409`SOURCE_CHANGED` rather than publishing stale evidence or silently rerunning. Serialize new content references and physical cleanup for the same content so a stale refcount cannot delete newly referenced bytes.

Keep active idempotency records while their effects can be retried. The user explicitly approved keeping content-free deleted-target records (opaque IDs, deletion/cleanup status and retry-key digests) until an explicitly approved maintenance policy removes them, charged against5GB. After cleanup, remove document/chat text, quotations, paths and content-bearing request fingerprints that are no longer required; do not retain them inside a tombstone. A replay of a deleted-target key returns410/GONE without recreating the effect, even though the old payload fingerprint has been purged. No expiry/pruning is silently enabled; later maintenance must preserve non-resurrection semantics before removing these records.

## C05 — deletion and restart recovery

In a transaction, reject library deletion if saved conversations reference it; otherwise validate ownership, mark affected references unavailable, increment revision, delete/mark the approved exclusive messages/quotations and persist cleanup intent. Commit before destructive filesystem work. Retrieval, previews and answer publication honor the unavailable state immediately. Surviving library/shared content remains eligible through its own references.

One coordinated cleanup worker rechecks ownership/live references under the same content coordination used by attachment admission, deletes only exclusively owned files/index rows, and persists progress. Resolve paths below the allowlisted managed root, reject links/reparse targets and verify server ownership evidence before removal; never recursively clear a computed broad directory. An external file lock or crash leaves pending status/quota charges and sanitized error codes. Idempotent cleanup treats already-removed owned files as complete only after the path/reference checks; it cannot broaden deletion on failure.

On restart, reconcile durable intents before allowing affected resources to become ready. Proposed first policy: one bounded recovery pass per startup or explicit user retry, no spin loop/backoff daemon; exact duration/process/byte allocation remains for validation. Failed cleanup stays pending and blocks reuse of that deletion target. Mark physical cleanup complete only after verifying required removals, then release charges. Logical deletion is not secure erasure of SSD blocks/backups/OS caches.

If a source unexpectedly becomes missing/corrupt in a retained conversation, keep saved answer text readable with an unavailable-source label, block its live preview and exclude it/history-derived quotes from new answers. Do not create a fresh quote snapshot, infer a path from a filename or resurrect a deleted chat. Existing saved answer text is historical, not current evidence.

## C06 — proposed HTTP surface

All routes are proposals under the configured loopback app origin. IDs are opaque server-generated UUID strings; JSON uses snake_case consistently with Python models. Proposed type bounds for G2: revisions/byte counts are nonnegative signed64-bit integers; titles≤200Unicode characters, display filenames≤255Unicode characters, cursors≤256ASCII characters and idempotency keys16–128ASCII letters/digits/underscore/hyphen. File labels never become paths; reject header newlines/control characters. Questions retain R01's provisional512UTF-8-byte guard. Validate IDs/enums/lengths/selected-reference membership at entry. Return typed envelopes with `data` or `error:{code,message,request_id}`; never stack traces, private paths, raw source text or model internals in errors. Responses containing evidence use no-store. State-changing operations obey C04.

Logical response types: a conversation contains ID/title/revision/state/selected-reference IDs; an operation contains ID/target ID/state/warning codes and optional completed/total work counts (unknown progress stays null); an answer contains ID/status/selection revision/claim-text blocks/citation-ID lists/evidence-warning codes/completion status. A citation resolves a supplied evidence ID to document/extraction/version/location and optional mapped quote spans. Values are bounded typed data, not arbitrary model-provided HTML or paths. Exact serialized schema tests belong to the approved implementation tasks; these declarations make the proposed surface reviewable without creating code now.

| Route | Input / success output | Main refusal behavior |
|---|---|---|
| GET `/api/health` | No body; readiness/component-state summary, not asset paths |503if required prerequisites unavailable; no startup downloads |
| POST `/api/conversations` | Bounded title + idempotency key;201conversation ID/revision |422invalid shape;409key conflict; quota-full error if metadata cannot fit |
| GET `/api/conversations` | Cursor and limit; data items + `next_cursor` |422bad cursor/limit; proposed default20/max100items |
| GET `/api/conversations/{id}` | Conversation ID; messages/status/selected-reference IDs with bounded pagination |404unknown/out-of-scope; gone/deleting status has no deleted text |
| POST `/api/conversations/{id}/attachments` | Raw bounded file body, escaped display-name metadata, idempotency key;202document/operation ID |413file/count limit;415unsupported type;409busy/key/revision conflict; quota error; no multipart dependency added implicitly |
| GET `/api/operations/{id}` | Operation ID; bounded status/warnings/progress/cleanup state |404unknown; never return raw worker output |
| PUT `/api/conversations/{id}/selection` | Complete selected-reference ID list + expected revision;200new revision |409stale revision;404unrelated reference; empty selection stays empty |
| POST `/api/conversations/{id}/answers` | Question + expected selection revision + idempotency key;202answer operation |409busy/stale/invalid-reference;422question bound;503models/context-fit not ready |
| GET `/api/conversations/{id}/answers/{answer_id}` | Answer ID; completion/status/claim blocks/citation IDs/support warnings |404unrelated; incomplete/error never returned as complete answer |
| GET `/api/conversations/{id}/sources/{citation_id}` | Scoped saved citation ID; sanitized preview/location/warnings |404unrelated;410source unavailable; coarse precision disclosed |
| GET/POST `/api/library` | Paginated library listing / bounded original upload with idempotency | Same upload/quota/type rules; no automatic attachment to every chat |
| POST `/api/conversations/{id}/library-references` | Library document ID + revision/idempotency;201reference ID |409conversation10-limit/stale;404unknown; no stored-byte copy |
| DELETE `/api/conversations/{id}` | ID/revision/idempotency;202logical deletion + cleanup operation |409stale/unknown outcome; never claims physical removal early |
| DELETE `/api/library/{id}` | ID/revision/idempotency;202deletion if unreferenced |409`LIBRARY_REFERENCED` with bounded impact summary; preserve surviving bytes |

Proposed status mapping:400malformed request,404unknown/ineligible ID,409scope/revision/idempotency/busy/reference conflict,410unavailable deleted source,413file/count limit,415unsupported format,422schema/policy validation,503missing assets/service/input-fit/resource readiness,507managed quota/disk full,500sanitized unexpected failure. User-facing text explains action needed; retryability is explicit and never overrides idempotency. Pagination/limits and exact asynchronous response schema are G2 contract proposals, not implemented API documentation or validated commands.

## C07 — resource, generation and offline controls

User-approved validation targets are one heavy ingestion/embedding/OCR/generation/cleanup job at a time; warm complete answers≤30seconds, hard answer timeout90seconds, aggregate owned app/workers/Ollama≤8GiB and available physical RAM≥4GiB. Warm timing starts at accepted answer request on ready indexed sources with the adopted model resident, and includes query embedding, retrieval, generation, citation checks and persistence until the complete answer is available; returning202alone does not finish this measurement. Measure final answer delivery separately as well. A visible warning/incomplete response does not pass the30-second complete-answer target. Cold answers still obey the90-second hard bound; initial indexing is measured separately, not hidden in warm timings. Reject/return busy for a new expensive operation when the lease is occupied; no unbounded in-memory queue.

Record all relevant process memory and OS headroom, including extra native descendants; monitor cadence/kernel job/worker/controller caps and parser/OCR/deletion/recovery deadlines require exact validation before execution. The8GiB cap is not permission for each process to consume8GiB. Browser/OS/unowned background applications affect headroom even when not in the owned job. Target-machine proof remains outstanding because earlier trials ran on about19.911GiB physical RAM. No silent target revision or host-memory extrapolation.

Use evaluated CPU-only/four-thread/2048context/192output settings only as the R01 provisional baseline; do not adopt a model merely by repeating trial parameters. Load/unload owned models explicitly; no unapproved alternate model. Stop if wrong artifact, prefix/dimension/version, OOM, unexpected network/download or ownership uncertainty appears. Missing local assets fail readiness rather than triggering retrieval from a registry.

**Input-fit blocker:** no trustworthy pre-generation template/token-fit method has been validated for this application. A3000-byte envelope, returned token count or a model's claim of seeing a footer does not prove all input was consumed. Proposed next investigation compares exact local tokenizer/template accounting or a verified pinned-runtime fit interface; neither a new dependency nor such an interface is selected/executed here. Until one is verified with over-limit/truncation and multi-file controls, dependent generation adoption is blocked. Safe degradation is refusal, not silent truncation or cloud fallback.

Separate finite invocation/time/process/disk budgets are required for every future native validation package, including controls/regressions/cleanup. Application acceptance targets are not those package budgets. Preserve all prior trial meters and source seals; do not reuse their unused allowances. Local/offline/no-telemetry behavior and real CSV-first restart/persistence must be demonstrated after implementation under approved execution, not inferred from this document.

## C08 — traceable verification obligations

| Boundary | Design trace / future test-first acceptance |
|---|---|
| Reference/dedup isolation | Same bytes in unrelated attachments never leak chunks/history/previews; library shared bytes survive deleting either conversation |
| Quota/full-disk | Concurrent reservations cannot exceed class caps; overflow/unknown expansion fails before the next write; class transition/rebuild reserves both generations |
| Idempotency | Same key/same verified payload has one effect; different payload conflicts; pending/unknown operation is never duplicated; deleted target not recreated |
| Crash/restart | Before/after metadata/file promotion/deletion/publish boundaries reconcile consistently; pending charges retained; source changes prevent stale answer publication |
| Provenance/grounding | Unchanged Q01–Q06/Q10–Q16/Q20 and T16-E cases trace actual anchors; Q18/Q19 remain deferred charts with unchanged gold, not passing/excluded cases |
| Model fit/resources | True token/template accounting and over-limit refusal, packed multi-file evidence, hard timeouts/OOM/headroom controls and physical16GB strategy require bounded validation |
| Trust/local operation | Traversal/reparse/raw HTML/model-path/input-injection controls, local assets/loopback Origin/Host/CSRF, sanitized logs and no startup/runtime downloads verified in actual app |

These are static negative-case walkthroughs/future tests, not passing runtime results. Keep routine model tests mocked; actual native/model/offline trials remain separate approved packages. Final adoption also requires current relevant advisory/license/notice reconciliation, validation of the approved retention/recovery design and explicit G2 approval of the concrete architecture. Content-free tombstone retention itself is already decided and must not be reopened without a requested policy change.
