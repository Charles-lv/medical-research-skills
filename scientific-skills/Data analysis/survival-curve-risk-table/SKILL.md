---
name: survival-curve-risk-table
description: Generate publication-quality Kaplan-Meier survival curves with aligned "Number at risk" tables meeting NEJM, Lancet, and JCO journal standards.
license: MIT
skill-author: AIPOCH
---

# Survival Curve Risk Table Generator

Automatically add "Number at risk" tables to Kaplan-Meier survival curves. Aligns time points precisely with the curve X-axis and generates publication-quality combined figures for clinical oncology journals.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --input survival_data.csv --time-col time --event-col event --group-col treatment --output risk_table.png
```

## When to Use

- Add "Number at risk" tables to existing KM survival curves
- Generate survival plots meeting NEJM, Lancet, or JCO requirements
- Produce risk tables for clinical trial reports
- Standardize medical paper charts before journal submission

## Workflow

1. Confirm input CSV path, time column, event column, and optional group column.
2. Validate that the request involves KM survival curve risk table generation; stop early if not.
3. Run `scripts/main.py` with the appropriate style and time-point flags.
4. Return a structured result separating assumptions, output files, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the Fallback Template below.

**Group count check:** If more than 6 groups are provided, emit a warning, split into pages of 6 groups each, and name paginated output files as `risk_table_page1.png`, `risk_table_page2.png`, etc.

## Fallback Template

If `scripts/main.py` fails or required fields are missing, respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective        : <risk table generation goal>
Inputs Available : <file, columns, style provided>
Missing Inputs   : <list exactly what is missing>
Partial Result   : <any steps completed safely>
Blocked Steps    : <what could not be completed and why>
  Note: If lifelines is not installed, survival analysis features are limited.
        Install with: pip install lifelines
Next Steps       : <minimum info needed to complete>
───────────────────────────────────────
```

## Stress-Case Output Checklist

For complex multi-constraint requests, always include these sections explicitly:

- **Assumptions**: style defaults (NEJM), time points auto-calculated, DPI=300; always state the journal style applied, noting if it differs from the NEJM default
- **Constraints**: max 6 groups per page; >6 groups triggers pagination (see Group count check above)
- **Risks**: `lifelines` optional but required for full survival analysis
- **Unresolved Items**: missing columns, unsupported file formats

## CLI Usage

```bash
# Basic risk table
python scripts/main.py \
  --input survival_data.csv \
  --time-col time --event-col event --group-col treatment \
  --output risk_table.png

# Journal style
python scripts/main.py \
  --input survival_data.csv \
  --time-col time --event-col status --group-col arm \
  --style NEJM --time-points 0,6,12,18,24,30,36 \
  --output figure_1a.pdf

# Combined figure (KM curve + risk table)
python scripts/main.py \
  --input survival_data.csv \
  --time-col months --event-col death --group-col group \
  --km-plot km_curve.png --combine \
  --output combined_figure.png
```

## Required Input Columns

| Column | Description | Type |
|---|---|---|
| time | Follow-up time (months) | Numeric |
| event | Event flag | 0=Censored, 1=Event |
| group | Treatment group (optional) | Text/Categorical |

Supported file formats: CSV, Excel (.xlsx/.xls), SAS (.sas7bdat), RData (.rda/.rds), pickle (.pkl)

## Key Parameters

| Parameter | Description | Default |
|---|---|---|
| `--input` | Input data file | required |
| `--time-col` | Time column name | required |
| `--event-col` | Event column name | required |
| `--group-col` | Group column name | None (single-arm: labeled "All patients") |
| `--style` | Journal style: NEJM/Lancet/JCO | NEJM |
| `--time-points` | Comma-separated time points | auto |
| `--format` | Output format: png/pdf/svg | png |
| `--dpi` | Image resolution | 300 |
| `--combine` | Combine with KM curve | False |

→ Full parameter and journal style reference: [references/parameters.md](references/parameters.md)

## Input Validation

This skill accepts: CSV or tabular survival data files with time-to-event and event indicator columns, for generating Kaplan-Meier risk tables.

If the request does not involve KM survival curve risk table generation — for example, asking to perform Cox regression, compute hazard ratios, or analyze non-survival time-series data — do not proceed. Instead respond:

> "`survival-curve-risk-table` is designed to generate 'Number at risk' tables for Kaplan-Meier survival curves. Your request appears to be outside this scope. Please provide a survival data CSV with time and event columns, or use a more appropriate tool."

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If `lifelines` is not installed, report the warning and provide the install command: `pip install lifelines`.
- If the task goes outside documented scope, stop instead of guessing.
- If `scripts/main.py` fails, use the Fallback Template above.
- Do not fabricate survival statistics, risk counts, or execution outcomes.

## Output Requirements

Every final response must include:

1. **Objective** — what risk table was generated and for which journal style
2. **Inputs Received** — file path, column names, style, time points
3. **Assumptions** — defaults applied (style, DPI, time points); always state the journal style applied, noting if it differs from NEJM default; if no group column, label as "All patients"
4. **Result** — output file paths generated
5. **Risks and Limits** — lifelines dependency, group count limits, pagination if >6 groups
6. **Next Checks** — manually spot-check number-at-risk calculations

## Dependencies

```
numpy >= 1.20.0
pandas >= 1.3.0
matplotlib >= 3.4.0
seaborn >= 0.11.0
lifelines >= 0.27.0   # optional but recommended
Pillow >= 8.0.0
```
