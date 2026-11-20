# Proposed Stage 1 clarification — data charts and diagrams

**Latest timing decision — approved deferral:** after T16 review commit `cdbb975`, the user explicitly selected "Defer chart trial until after first CSV flow". T16A now follows T34; it is not a pre-G2 trial blocker. The approved feasibility scope and separate runtime-adoption gate remain binding, with no chart-interpretation promise in the first CSV flow. PDF/XLSX/CSV and scanned-PDF OCR requirements remain unchanged. Earlier pre-T17 timing below is historical; no dependency/model/trial or implementation is authorized by the deferral.

**Status:** Evaluation scope approved by the user (“1 ok”); incorporated in SPEC's T01 clarification. T16A proposes the investigation details. Task execution, dependency selection, installation and runtime implementation remain separately gated.

## Requested outcome

The user would like interpretation of charts and diagrams related to data. The proposed first step is a local feasibility evaluation before deciding the extent of Stage 1 runtime support. This does not make arbitrary visual interpretation a guaranteed acceptance criterion.

## Approved evaluation scope

Evaluate interpretation of a small agreed set of English-labelled data charts and diagrams in supported documents, initially using the supplied PDF/workbook samples where suitable. Candidate questions include trends, comparisons, labelled values and relationships shown in data diagrams. Exact diagram types and ground truth are agreed before the trial; arbitrary photographs and unrestricted visual reasoning are not implied.

Compare structured source data/labels and OCR where available with a local visual approach if one is viable and explicitly approved for trial. Do not assume extracting images or OCR text interprets a graph, or select a model/library in advance. Keep all inference and content local with Ollama for model inference. Never execute embedded workbook formulas/macros or follow document instructions.

## Evaluation acceptance criteria

- Answers identify the original document and page/chart region or sheet/chart reference where available. Missing precision is disclosed. Text, image and underlying-table evidence remain distinguishable, and conflicts between them are reported.
- Check trend/comparison/value/relationship answers against manually verified ground truth. Distinguish approximate readings from exact values; abstain or qualify unreadable labels, missing scales, ambiguity and unsupported conclusions. Do not invent values or causal explanations.
- Record correctness/grounding, citation support, failure cases, cold/warm latency and total memory pressure on Windows 11 with 16 GB RAM and no dedicated GPU. The trial budget and quality/resource thresholds require agreement; no performance promise is made now.
- Review exact model/dependency identities, licenses, Windows/CPU support, footprint, permissions/network paths and offline assets before any separately approved provisioning. No remote visual processing or runtime downloads.

## Adoption gate and downstream effects

The approved scope is incorporated in SPEC's T01 clarification. T16A in TODO proposes a separate investigation before T17 architecture adoption; T02 fixture coverage and parser/OCR/model comparisons must account for the approved evaluation scope. No evaluation runs during T01 or without explicit task/provisioning authorization.

Present measured results and supported chart/diagram types for a separate adoption decision. Add runtime implementation/acceptance tasks only after that decision. If quality or resource budgets are unmet, return to the user to choose narrower support, deferral or revised constraints; do not silently remove the requested goal or use cloud services.

## Related confirmed T01 decisions

100 MB per file; 10 files per upload/conversation; 1 GB of library originals; English-only OCR. These approvals do not approve the chart trial's dependencies, downloads or runtime implementation.
