---
name: metagenomic-krona-chart
description: Generate interactive Krona charts (sunburst plots) for metagenomic samples from Kraken2, Bracken, or custom TSV taxonomy abundance data.
license: MIT
skill-author: AIPOCH
status: beta
---
# Metagenomic Krona Chart

Generate interactive sunburst charts (Krona Chart) to display taxonomic abundance hierarchies in metagenomic samples. Supports Kraken2, Bracken, Centrifuge, and custom TSV formats.

## Input Validation

This skill accepts: TSV/report files from metagenomic classifiers (Kraken2, Bracken, Centrifuge) or custom TSV taxonomy abundance tables, for the purpose of generating interactive Krona sunburst charts.

If the user's request does not involve metagenomic taxonomy visualization — for example, asking to run taxonomic classification, perform diversity analysis, or generate other chart types — do not proceed with the workflow. Instead respond verbatim:
> "metagenomic-krona-chart is designed to generate interactive Krona sunburst charts from metagenomic taxonomy abundance data. Your request appears to be outside this scope. Please provide a Kraken2/Bracken report or custom TSV file, or use a more appropriate tool for your task. To generate a report file, run Kraken2 or Bracken first and provide the output."

**This refusal must fire as the absolute first action — before any taxonomy lookup, context processing, or partial analysis. Do not generate any taxonomy-related output before emitting this refusal. Validate scope first.**

**Limitations:** This skill generates charts for single samples only. For multi-sample comparison, run the skill once per sample and combine outputs manually.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py -i example/input.tsv -o krona_chart.html
```

## When to Use

- Generate interactive Krona/sunburst charts from metagenomic taxonomy abundance data
- Visualize Kraken2, Bracken, or Centrifuge classification outputs
- Explore taxonomic hierarchy with zoom and click support
- Create standalone HTML files viewable offline

## Workflow

1. **Validate input** — confirm scope and emit verbatim refusal before any processing for out-of-scope requests.
2. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
3. Validate that the `-i` input file path does not contain `../` or point outside the workspace.
4. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
5. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
6. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Usage

```text
python scripts/main.py -i input.tsv -o krona_chart.html
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `-i, --input` | Input file path (TSV format) | Required |
| `-o, --output` | Output HTML file path | krona_chart.html |
| `-t, --type` | Input format type (kraken2/bracken/custom) | auto |
| `--max-depth` | Maximum display hierarchy depth | 7 |
| `--min-percent` | Minimum display percentage threshold | 0.01 |
| `--title` | Chart title | Metagenomic Krona Chart |

## Input Formats

### Kraken2/Bracken Report Format
```
100.00  1000000 0   U   0   unclassified
 99.00  990000  0   R   1   root
 95.00  950000  0   D   2   Bacteria
 50.00  500000  0   P   1234    Proteobacteria
```

### Custom Format (TSV)
```
taxon_id	name	rank	parent_id	reads	percent
2	Bacteria	domain	1	950000	95.0
1234	Proteobacteria	phylum	2	500000	50.0
```

## Dependencies

- Python 3.8+
- plotly >= 5.0.0
- pandas >= 1.3.0

```text
pip install plotly pandas
```

## Output Features

- Interactive sunburst chart with zoom and click support
- Color-coded different taxonomic levels
- Hover to display detailed information (reads, percentage)
- Center displays total reads
- Responsive design, adapts to different screens
- Standalone HTML file — viewable offline

## Fallback Behavior

If `scripts/main.py` fails or required inputs are incomplete:
1. Report the exact failure point and error message.
2. If the error is `No module named 'plotly'`, instruct: `pip install plotly pandas` then retry.
3. State what can still be completed (e.g., input format validation without rendering).
4. Manual fallback: verify input TSV has required columns (`taxon_id`, `name`, `rank`, `parent_id`, `reads`, `percent`) and re-run with `--type custom`.
5. Do not fabricate execution outcomes or taxonomy data.

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
- If the `-i` input file path contains `../` or points outside the workspace, reject with a path traversal warning.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Response Template

Use the following fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

## Prerequisites

```text
pip install -r requirements.txt
```
