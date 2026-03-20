---
name: forest-plot-styler
description: Beautify meta-analysis forest plots with customizable odds ratio points, confidence interval styles, and subgroup analysis support. Outputs PNG, PDF, or SVG.
license: MIT
skill-author: AIPOCH
status: beta
---
# Forest Plot Styler

Beautifies meta-analysis or subgroup analysis forest plots, customizes Odds Ratio point sizes and confidence interval line styles.

## Input Validation

This skill accepts: CSV or Excel files containing meta-analysis study data with OR values and confidence intervals, for the purpose of generating forest plots.

If the user's request does not involve forest plot generation or meta-analysis visualization — for example, asking to run statistical meta-analysis from scratch, perform systematic literature search, or generate other chart types — do not proceed with the workflow. Instead respond:
> "forest-plot-styler is designed to beautify and generate forest plots from existing meta-analysis data. Your request appears to be outside this scope. Please provide a CSV/Excel file with study OR values and confidence intervals, or use a more appropriate tool for your task."

Do not continue the workflow when the request is out of scope, missing the required `--input` file, or would require unsupported assumptions. For missing inputs, state exactly which fields are missing.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --demo --output demo_forest_plot.png
```

## When to Use

- Generate or beautify forest plots for meta-analysis or subgroup analysis
- Customize OR point sizes, CI line styles, and publication-ready output
- Use a documented fallback path for missing inputs, execution errors, or partial evidence

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Features

- Reads meta-analysis data (CSV/Excel format)
- Draws high-quality forest plots
- Customizes Odds Ratio point sizes, colors, and shapes
- Customizes confidence interval line styles (color, thickness, endpoint style)
- Supports subgroup analysis display with per-subgroup summary diamonds
- Automatically calculates and displays pooled effect values (inverse variance weighting)
- Outputs to PNG, PDF, or SVG format

## Usage

```text
python scripts/main.py --input <data.csv> [options]
```

### Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--input`, `-i` | string | - | Yes* | Input data file (CSV or Excel) |
| `--output`, `-o` | string | forest_plot.png | No | Output file path |
| `--format`, `-f` | string | png | No | Output format (png/pdf/svg) |
| `--point-size` | int | 8 | No | OR point size |
| `--point-color` | string | #2E86AB | No | OR point color |
| `--ci-color` | string | #2E86AB | No | Confidence interval line color |
| `--ci-linewidth` | int | 2 | No | Confidence interval line thickness |
| `--ci-capwidth` | int | 5 | No | Confidence interval endpoint width |
| `--summary-color` | string | #A23B72 | No | Pooled effect point color |
| `--summary-shape` | string | diamond | No | Pooled effect point shape |
| `--subgroup` | string | - | No | Subgroup analysis column name |
| `--title`, `-t` | string | Forest Plot | No | Chart title |
| `--xlabel`, `-x` | string | Odds Ratio (95% CI) | No | X-axis label |
| `--reference-line` | float | 1.0 | No | Reference line position |
| `--width`, `-W` | int | 12 | No | Image width (inches) |
| `--height`, `-H` | int | auto | No | Image height (inches, auto-scales with study count) |
| `--dpi` | int | 300 | No | Image resolution |
| `--font-size` | int | 10 | No | Font size |
| `--style`, `-s` | string | default | No | Preset style (default/minimal/dark) |
| `--demo` | flag | - | No | Run with synthetic 5-study dataset |

*Required unless `--demo` is used.

## Input Data Format

CSV/Excel files must contain the following columns:

| Column Name | Description | Type |
|-------------|-------------|------|
| `study` | Study name | Text |
| `or` | Odds Ratio value | Numeric |
| `ci_lower` | Confidence interval lower bound | Numeric |
| `ci_upper` | Confidence interval upper bound | Numeric |
| `weight` | Weight (optional, for point size) | Numeric |
| `subgroup` | Subgroup label (optional) | Text |

### Sample Data

```csv
study,or,ci_lower,ci_upper,weight,subgroup
Study A,0.85,0.65,1.12,15.2,Drug A
Study B,0.72,0.55,0.94,18.5,Drug A
Study C,1.15,0.88,1.50,12.3,Drug B
Study D,0.95,0.75,1.20,14.8,Drug B
```

## Examples

### Basic Usage
```text
python scripts/main.py -i meta_data.csv
```

### Custom Style
```text
python scripts/main.py -i meta_data.csv \
    --point-color="#E63946" \
    --ci-color="#457B9D" \
    --point-size=10 \
    --ci-linewidth=3 \
    -t "Meta-Analysis of Treatment Effects"
```

### Subgroup Analysis
```text
python scripts/main.py -i meta_data.csv \
    --subgroup subgroup_column \
    --summary-color="#F4A261" \
    -o subgroup_forest.png
```

### Demo Mode
```text
python scripts/main.py --demo --output demo_forest_plot.png
```

## Preset Styles

- `default` — Blue color scheme, standard font size, white background
- `minimal` — Clean lines, grayscale color scheme, no grid lines
- `dark` — Dark background (#1E1E1E), bright data points, suitable for presentations

## Dependencies

- Python >= 3.8
- matplotlib >= 3.5.0
- pandas >= 1.3.0
- numpy >= 1.20.0
- openpyxl >= 3.0.0 (for reading Excel)

## Prerequisites

```text
pip install -r requirements.txt
```

## Fallback Behavior

If `scripts/main.py` fails or required inputs are incomplete:
1. Report the exact failure point and error message.
2. State what can still be completed (e.g., data validation without rendering).
3. Manual fallback: verify input CSV has required columns (`study`, `or`, `ci_lower`, `ci_upper`) and re-run with `--format png` as the simplest output mode.
4. Do not fabricate execution outcomes or file contents.

## Output Requirements

Every final response must make these items explicit when relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate files, citations, data, search results, or execution outcomes.
- If any `or` value is ≤ 0, reject with: `Error: OR values must be > 0 (found invalid values at rows: {indices}).`
- If any `ci_lower >= ci_upper`, reject with: `Error: ci_lower must be less than ci_upper (found invalid rows: {indices}).`
- **Subgroup labels:** When `--subgroup` is used, each subgroup summary diamond is labeled with the subgroup name on the y-axis. If subgroup labels are missing from the output, this is a known rendering gap — report it in the Risks section.
- **OR label clipping:** For wide CI ranges, OR labels positioned at the right axis edge may be clipped. Use `--width` to increase figure width if labels are cut off.

## Notes

1. Ensure input file encoding is UTF-8
2. OR values are automatically converted when log scale is suggested
3. Studies with confidence intervals crossing 1 are not statistically significant
4. Weight values are used to adjust point size, reflecting study contribution
5. Pooled effect uses inverse variance weighting: `SE = (log(ci_upper) - log(ci_lower)) / (2 * 1.96)`

## Response Template

Use the following fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

For stress/multi-constraint requests, also include:
- Constraints checklist (compliance, performance, error paths)
- Unresolved items with explicit blocking reasons

If the request is simple, you may compress the structure, but still keep assumptions and limits explicit when they affect correctness.
