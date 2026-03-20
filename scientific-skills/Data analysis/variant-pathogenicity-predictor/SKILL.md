---
name: variant-pathogenicity-predictor
description: Integrate REVEL, CADD, PolyPhen-2, SIFT, and MutationTaster scores to predict variant pathogenicity with ACMG guideline interpretation.
license: MIT
skill-author: AIPOCH
---
# Variant Pathogenicity Predictor

Integrate multiple in-silico prediction scores (REVEL, CADD, PolyPhen-2, SIFT, MutationTaster) to predict variant pathogenicity with ACMG guideline interpretation.

## Input Validation

This skill accepts: genomic variant coordinates (chr:pos:ref:alt format) or VCF files for in-silico pathogenicity prediction using integrated scoring tools.

**Data Safety Check:** VCF files may contain patient-identifiable genomic data. Before processing any VCF file, confirm that the data has been de-identified or that you have appropriate IRB/ethics approval for the analysis.

If the request does not involve variant pathogenicity prediction — for example, asking to perform variant calling from BAM files, run GWAS analysis, or interpret somatic mutation signatures — do not proceed. Instead respond verbatim:

> "variant-pathogenicity-predictor is designed to integrate in-silico scores for variant pathogenicity prediction. Your request appears to be outside this scope. Please provide variant coordinates or a VCF file, or use a more appropriate tool for your task."

Do not include speculative variant interpretation in refusal responses.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --demo
```

## When to Use

- Prioritizing variants of uncertain significance (VUS) in clinical genetics
- Integrating multiple prediction tools into a single pathogenicity call
- ACMG/AMP guideline-based variant classification support
- Batch scoring of VCF variants for research pipelines

## Usage

```bash
# Single variant
python scripts/main.py --variant "chr17:43094692:G:A" --gene "BRCA1"

# Batch from VCF
python scripts/main.py --vcf variants.vcf --output report.json
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--variant` | Yes* | Variant in format chr:pos:ref:alt |
| `--vcf` | Yes* | VCF file with variants (alternative to --variant) |
| `--gene` | No | Gene symbol for context |
| `--scores` | No | Scores to use: REVEL,CADD,PolyPhen (default: all) |
| `--output` | No | Output file path (default: stdout) |

*Provide either `--variant` or `--vcf`.

## Integrated Scores

| Tool | Score Range | Pathogenic Threshold |
|------|-------------|----------------------|
| REVEL | 0–1 | ≥ 0.75 |
| CADD | 0–99 (Phred) | ≥ 20 |
| PolyPhen-2 | 0–1 | ≥ 0.85 (probably damaging) |
| SIFT | 0–1 | ≤ 0.05 (deleterious) |
| MutationTaster | 0–1 | ≥ 0.5 (disease causing) |

## Workflow

1. Confirm objective, required inputs, and constraints before proceeding.
2. Validate request matches documented scope; stop early if unsupported assumptions are needed.
3. Run `scripts/main.py` with available inputs, or use the documented reasoning path.
4. Return structured result separating assumptions, deliverables, risks, and unresolved items.
5. On execution failure or incomplete inputs, switch to fallback path and state exactly what blocked completion.

## Fallback Template

If `scripts/main.py` cannot run (missing inputs, environment error), respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective      : <stated goal>
Blocked by     : <exact missing input or error>
Partial result : <what can still be assessed manually>
Next step      : <minimum action to unblock>
───────────────────────────────────────
```

## Returns

- Pathogenicity classification (Pathogenic / Likely Pathogenic / VUS / Likely Benign / Benign)
- ACMG guideline interpretation with supporting criteria
- Individual score breakdown per tool
- **Conflicting evidence flag**: When ≥2 tools disagree on pathogenicity direction, a `CONFLICTING_EVIDENCE` flag is emitted listing the disagreeing tools
- When classification is VUS with conflicting evidence: "Recommend clinical genetics review for definitive classification."

## Output Requirements

Every response must make these explicit when relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs (including CONFLICTING_EVIDENCE flags)
- Unresolved items and next-step checks
- For VUS with conflicting evidence: clinical genetics review recommendation

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside documented scope, stop instead of guessing or silently widening the assignment. Do not include speculative variant interpretation in refusal responses.
- If `scripts/main.py` fails, report the failure point, summarize what can still be completed safely, and provide the manual fallback above.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Response Template

Use this fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

For simple requests, compress the structure but keep assumptions and limits explicit when they affect correctness.

## Risk Assessment

| Risk Indicator | Assessment | Level |
|----------------|------------|-------|
| Code Execution | Python scripts executed locally | Medium |
| Network Access | No external API calls | Low |
| File System Access | Read VCF input, write report output | Medium |
| Data Exposure | VCF files may contain patient genomic data — de-identify before processing | High |

## Prerequisites

No additional Python packages required beyond standard library.
