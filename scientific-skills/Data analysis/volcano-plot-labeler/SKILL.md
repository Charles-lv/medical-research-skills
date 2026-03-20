---
name: volcano-plot-labeler
description: Automatically label top significant genes in volcano plots using a force-directed repulsion algorithm to prevent label overlap.
license: MIT
skill-author: AIPOCH
---
# Volcano Plot Labeler

Automatically identify and label the top N most significant genes in volcano plots using a repulsion algorithm to prevent label overlap.

## Input Validation

This skill accepts: DEG results tables (CSV/TSV) with log2 fold change, p-value, and gene identifier columns for automated volcano plot labeling.

If the request does not involve volcano plot labeling — for example, asking to perform DEG analysis, generate heatmaps, or create pathway enrichment plots — do not proceed. Instead respond:

> "volcano-plot-labeler is designed to label top significant genes in volcano plots. Your request appears to be outside this scope. Please provide a DEG results table with log2FC and p-value columns, or use a more appropriate tool for your task."

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## Audit-Ready Commands

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
# Test with inline CSV (requires a DESeq2-format CSV):
python scripts/main.py \
  --input data/deseq2_results.csv \
  --output test_volcano.png \
  --top-n 5
```

## When to Use

- Adding gene labels to existing volcano plots from DEG analysis
- Highlighting top significant genes without manual label placement
- Generating publication-ready labeled volcano plots
- Customizing label count, thresholds, and styling

## Usage

```bash
python scripts/main.py \
    --input data/deseq2_results.csv \
    --output volcano_labeled.png \
    --log2fc-col log2FoldChange \
    --pvalue-col padj \
    --gene-col gene_name \
    --top-n 10
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--input` | Yes | — | DEG results CSV/TSV file |
| `--output` | Yes | — | Output plot file path |
| `--log2fc-col` | No | log2FoldChange | Column name for log2 fold change |
| `--pvalue-col` | No | padj | Column name for p-value |
| `--gene-col` | No | gene_name | Column name for gene identifiers |
| `--top-n` | No | 10 | Number of top genes to label |
| `--pvalue-threshold` | No | 0.05 | P-value cutoff for significance coloring |
| `--log2fc-threshold` | No | 1.0 | Log2FC cutoff for significance coloring |

## Input Format

Expected CSV/TSV columns:
- `log2FoldChange`: Log2 fold change values
- `padj` or `pvalue`: Adjusted or raw p-values
- `gene_name`: Gene identifiers

## Workflow

1. Confirm objective, required inputs, and constraints before proceeding.
2. Validate request matches documented scope; stop early if unsupported assumptions are needed.
3. Run `scripts/main.py` with available inputs, or use the documented reasoning path.
4. Return structured result separating assumptions, deliverables, risks, and unresolved items.
5. On execution failure or incomplete inputs, switch to fallback path and state exactly what blocked completion.

## Fallback Template

If `scripts/main.py` cannot run (missing `--output` argument, malformed input), respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective      : <stated goal>
Blocked by     : <exact missing input or error>
Partial result : <what can still be assessed manually>
Next step      : Ensure --input and --output are both provided
───────────────────────────────────────
```

> **Note:** `--output` is required. Running without it will return exit code 2. Always provide both `--input` and `--output`.

## Algorithm

1. Calculate `-log10(pvalue)` for all genes
2. Rank genes by combined score: `|log2FC| × -log10(pvalue)`
3. Select top N genes with highest significance
4. Place labels at gene coordinates, then apply iterative force-directed repulsion
5. Draw connecting lines from final label positions to gene points

## Output

Labeled volcano plot with:
- Color-coded points (upregulated / downregulated / not significant)
- Top N gene labels with leader lines
- No overlapping text labels

## Output Requirements

Every response must make these explicit when relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced (including all non-default parameter values applied)
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what can still be completed safely, and provide the manual fallback above.
- If significant genes < top-N, emit a note: "Only [k] genes meet significance thresholds; labeling [k] instead of requested [N]."
- Validate that column name parameters (`--log2fc-col`, `--pvalue-col`, `--gene-col`) contain only alphanumeric characters, underscores, and hyphens before passing to the script.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Response Template

Use this fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions (always list all non-default parameter values applied)
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

For simple requests, compress the structure but keep assumptions and limits explicit when they affect correctness.

## Prerequisites

```bash
pip install -r requirements.txt
# Requires: pandas, matplotlib, numpy, scipy
```
