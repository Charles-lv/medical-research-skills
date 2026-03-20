---
name: table-1-generator
description: Automatically generate baseline characteristics tables (Table 1) for clinical research papers with appropriate statistics, group comparisons, and APA formatting.
license: MIT
skill-author: AIPOCH
---
# Table 1 Generator

Automated generation of baseline characteristics tables (Table 1) for clinical research papers. Handles variable type detection, appropriate statistics, group comparisons, and publication-ready formatting.

## Input Validation

This skill accepts: patient-level CSV datasets with demographic and clinical variables for generating baseline characteristics tables in clinical research manuscripts.

**Data Safety Check:** Patient-level CSV data may contain PII (names, dates of birth, identifiers). Before processing, confirm that the data has been de-identified or that you have appropriate IRB/ethics approval. Do not include patient identifiers in Table 1 output.

If the request does not involve Table 1 generation — for example, asking to perform survival analysis, run regression models, or generate results tables for outcomes — do not proceed. Instead respond:

> "table-1-generator is designed to create baseline characteristics tables for clinical research. Your request appears to be outside this scope. Please provide a patient-level CSV dataset, or use a more appropriate tool for your task."

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## When to Use

- Generating Table 1 for RCT or observational study manuscripts
- Summarizing baseline demographics and clinical characteristics
- Comparing treatment vs control group characteristics
- Reporting missing data patterns in clinical datasets

## Usage

```bash
python scripts/main.py \
  --data patients.csv \
  --group treatment \
  --output table1.csv
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--data` | Yes | — | Patient data CSV file path |
| `--group` | No | — | Grouping variable (e.g., treatment/control) |
| `--vars` | No | all | Variables to include in the table |
| `--output` | Yes | — | Output file path for Table 1 |

## Features

- Automatic variable type detection (continuous, categorical, binary)
- Appropriate statistics: mean±SD, median[IQR], n(%)
- Group comparisons: t-test, Mann-Whitney, chi-square, Fisher's exact
- Missing data reporting per variable
- APA-formatted output (CSV/Excel)
- **Fisher's exact trigger**: When expected cell count < 5 in any cell, a note is emitted: "Fisher exact applied due to small expected cell count (< 5)."
- **Multiple testing correction**: When group count > 2, note that Bonferroni or FDR correction should be considered for publication

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

## Output Requirements

Every response must make these explicit when relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks
- For >30% missing data in any variable: recommend consulting a statistician
- For multi-group comparisons (>2 groups): note multiple testing correction requirement

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside documented scope, stop instead of guessing or silently widening the assignment.
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
| File System Access | Read patient CSV, write table output | Medium |
| Data Exposure | Patient CSV may contain PII — de-identify before processing | High |

## Prerequisites

```bash
pip install -r requirements.txt
```
