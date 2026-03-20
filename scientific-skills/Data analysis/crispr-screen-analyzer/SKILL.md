---
name: crispr-screen-analyzer
description: Process CRISPR screening data to identify essential genes and hit candidates. Performs quality control, log fold change calculation, z-score-based sgRNA scoring, and hit calling for pooled CRISPR screens including viability, drug resistance, and synthetic lethality studies.
license: MIT
skill-author: AIPOCH
status: beta
---
# CRISPR Screen Analyzer

Analyze pooled CRISPR screening data from count matrix to hit identification. Covers QC assessment (Gini index, read depth, dropout, replicate correlation), log fold change calculation, z-score-based sgRNA scoring, and multi-threshold hit calling.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## When to Use

- Identifying essential genes from viability screens (T0 vs T14)
- Calling drug resistance or sensitivity hits from treatment vs control comparisons
- Assessing screen quality before downstream pathway analysis

**Upstream:** `fastqc-report-interpreter` → `crispr-screen-analyzer`
**Downstream:** `crispr-screen-analyzer` → `go-kegg-enrichment` → `hit-validation-planner`

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

**Fallback template:** If `scripts/main.py` fails or required files are absent, report: (a) which file is missing, (b) which QC metrics can still be computed, (c) the manual command equivalent for the failed step.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--counts`, `-c` | string | Yes | sgRNA count matrix file |
| `--samples`, `-s` | string | Yes | Sample annotation CSV file |
| `--control` | string | No | Control sample names (comma-separated) |
| `--treatment`, `-t` | string | No | Treatment sample names (comma-separated) |
| `--output`, `-o` | string | No | Output directory |
| `--fdr` | float | No | FDR threshold (default: `0.05`; must be between 0 and 1) |
| `--seed` | int | No | Random seed for reproducibility (default: `42`) |

## Usage

```text
# QC assessment only
python scripts/main.py --counts sgrna_counts.txt --samples samples.csv --output qc_results

# Full differential analysis
python scripts/main.py \
  --counts sgrna_counts.txt --samples samples.csv \
  --control "Ctrl_1,Ctrl_2,Ctrl_3" \
  --treatment "Drug_1,Drug_2,Drug_3" \
  --output drug_screen --fdr 0.05 --seed 42
```

## Key QC Thresholds

| Metric | Target | Action if Failed |
|--------|--------|-----------------|
| Gini index | < 0.3 | Check MOI; consider repeating screen |
| Total reads | > 10M/sample | Increase sequencing depth |
| Zero-count sgRNAs | < 5% | Verify library quality at transduction |
| Replicate correlation | > 0.7 | Investigate batch effects; flag in output |

**Note:** Replicate correlation (Pearson or Spearman) is computed between replicate samples. Samples with correlation < 0.7 are flagged with a warning in the QC output. This metric is documented but not yet computed in the current script — implementation gap noted.

## Hit Classification

| Category | Criteria | Interpretation |
|----------|----------|----------------|
| Essential | FDR < 0.05, LFC < −1 | Required for cell viability |
| Drug Sensitive | FDR < 0.05, LFC < −1 | Synthetic lethal with treatment |
| Drug Resistant | FDR < 0.05, LFC > 1 | Confers resistance |

## Statistical Method Note

The scoring method uses z-score normalization at the sgRNA level (not true Robust Rank Aggregation). LFC uses pseudocount +1: `log2((treatment+1)/(control+1))`. FDR correction uses Benjamini-Hochberg. For true gene-level RRA, use MAGeCK or BAGEL2 as downstream tools.

## Reproducibility

Set `--seed` (default: 42) to ensure reproducible results across runs. The seed is recorded in the output metadata file. The script must call `np.random.seed(args.seed)` at the start of `main()`.

## Stress-Case Output Structure

For complex multi-constraint requests, always produce all of these sections:

1. **Assumptions** — list every assumption made about sample groupings, thresholds, and data quality
2. **Constraints** — state which parameters are fixed vs configurable
3. **Risks** — flag QC failures, low replicate counts, or potential batch effects
4. **Unresolved Items** — list anything that requires human decision before proceeding

## Output Requirements

Every response must make these explicit:

- Objective and deliverable
- Inputs used and assumptions introduced
- Workflow or decision path taken
- Core result: QC metrics, hit list, summary statistics
- Constraints, risks, caveats (e.g., single-sgRNA hits, off-target concerns)
- Unresolved items and next-step checks

## Input Validation

This skill accepts: sgRNA count matrices and sample annotation files from pooled CRISPR screens.

If the request does not involve CRISPR screen data analysis — for example, asking to design sgRNA libraries, perform RNA-seq differential expression, or interpret non-CRISPR genomic data — do not proceed. Instead respond:

> "`crispr-screen-analyzer` is designed to analyze pooled CRISPR screening data. Your request appears to be outside this scope. Please provide an sgRNA count matrix and sample annotation file, or use a more appropriate tool for your task."

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If sample names in `--control` or `--treatment` do not match columns in the count matrix, report the mismatch and list available sample names.
- If `--fdr` is not between 0 and 1, reject with: `Error: --fdr must be between 0 and 1.`
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Response Template

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks
