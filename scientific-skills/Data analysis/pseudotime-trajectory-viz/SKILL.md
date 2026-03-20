---
name: pseudotime-trajectory-viz
description: Visualize single-cell developmental trajectories and cellular differentiation processes using pseudotime analysis on AnnData (.h5ad) files.
license: MIT
skill-author: AIPOCH
status: beta
---
# Pseudotime Trajectory Visualization

Visualize single-cell developmental trajectories showing cellular differentiation processes using pseudotime analysis.

## Input Validation

This skill accepts: AnnData (.h5ad) files from single-cell RNA-seq experiments for pseudotime trajectory inference and visualization.

If the request does not involve pseudotime analysis of single-cell data — for example, asking to perform bulk RNA-seq analysis, run differential expression, or process non-AnnData inputs — do not proceed. Instead respond:

> "pseudotime-trajectory-viz is designed to visualize single-cell developmental trajectories using pseudotime analysis. Your request appears to be outside this scope. Please provide an AnnData (.h5ad) file with preprocessed single-cell data, or use a more appropriate tool for your task."

## When to Use

- Inferring developmental trajectories from single-cell RNA-seq data
- Calculating pseudotime values representing cellular differentiation progress
- Visualizing trajectory trees, lineage branching, and gene expression dynamics
- Generating publication-ready trajectory plots from AnnData files

## Technical Difficulty

**High** — Requires understanding of single-cell analysis, dimensionality reduction, trajectory inference algorithms, and Python visualization libraries.

## Workflow

1. **Validate input** — confirm scope and path safety before any processing.
2. Validate that the `--input` file path does not contain `../` or point outside the workspace. Reject with a path traversal warning if it does. Do not proceed with the traversal path.
3. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
4. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
5. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
6. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Usage

```text
# Basic trajectory analysis from AnnData file
python scripts/main.py --input data.h5ad --output ./results

# Specify starting cells and inference method
python scripts/main.py --input data.h5ad --start-cell stem_cell_cluster --method diffusion --output ./results

# Visualize specific gene expression along trajectories
python scripts/main.py --input data.h5ad --genes SOX2,OCT4,NANOG --output ./results
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--input` | path | Required | Input AnnData (.h5ad) file path |
| `--output` | path | `./trajectory_output` | Output directory |
| `--embedding` | enum | `umap` | Embedding: `umap`, `tsne`, `pca`, `diffmap` |
| `--method` | enum | `diffusion` | Trajectory method: `diffusion`, `paga` |
| `--start-cell` | str | auto | Root cell ID or cluster name |
| `--genes` | str | - | Comma-separated gene names to plot along pseudotime |
| `--format` | enum | `png` | Output format: `png`, `pdf`, `svg` |
| `--dpi` | int | `300` | Figure resolution |
| `--seed` | int | `42` | Random seed for reproducibility (passed to sc.pp.neighbors and sc.tl.umap) |

## Input Format

Required AnnData (.h5ad) structure:
```
AnnData object with n_obs × n_vars = n_cells × n_genes
    obs: 'leiden', 'cell_type'   # Cluster and cell type annotations
    var: 'highly_variable'        # Highly variable gene marker
    obsm: 'X_umap', 'X_pca'       # Pre-computed embeddings (optional)
```

Assumes input data is already normalized and log-transformed.

## Output Files

```
output_directory/
├── trajectory_plot.{format}
├── pseudotime_distribution.{format}
├── lineage_tree.{format}
├── pseudotime_values.csv
├── lineage_assignments.csv
└── analysis_report.json   # includes random seed used
```

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## Error Handling

- If `--input` is missing, state this and request the AnnData file path.
- If the file path contains `../` or points outside the workspace, reject with a path traversal warning. Do not proceed with the traversal path. Provide corrected safe path guidance: use an absolute path within the workspace, e.g., `/workspace/data/sample.h5ad`.
- If the AnnData object lacks required obs keys (`leiden` or `cell_type`), report the missing keys and stop.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails (e.g., returncode=2 from unrecognized `--format` argument), report the exact error and provide the correct command syntax.
- Do not fabricate pseudotime values, lineage assignments, or trajectory structures.

## Fallback Template

When execution fails or inputs are incomplete, respond with this structure:

```
FALLBACK REPORT
───────────────────────────────────────
Objective      : [restate the goal]
Blocked by     : [exact missing input or error]
Partial result : [what can be completed — e.g., method selection guidance]
Assumptions    : [embedding, method, start cell assumed]
Constraints    : [preprocessing requirements, memory limits]
Risks          : [batch effects, cell cycle confounding, sparse data]
Unresolved     : [what still needs user input]
Next step      : [minimum action needed to unblock]
───────────────────────────────────────
```

## Limitations

- Requires high-quality single-cell data with good cell type coverage
- Assumes differentiation is the main source of variation
- Circular or cyclic processes not well represented by linear pseudotime
- Large datasets (>50k cells) may require 16GB+ RAM
- **PAGA pseudotime reproducibility**: PAGA adds small random noise to pseudotime values. Use `--seed 42` (default) for reproducible results. The seed is recorded in `analysis_report.json`. The script must call `np.random.seed(args.seed)` before the noise addition step to ensure full reproducibility.

## Safety & Best Practices

- Validate trajectories with known marker genes and biological knowledge
- Multiple methods recommended for critical analyses
- Correct batch effects before trajectory inference
- Do not overinterpret precise pseudotime values as absolute time

## Response Template

Use the following fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

If the request is simple, compress the structure but keep assumptions and limits explicit when they affect correctness.

## Prerequisites

```text
pip install -r requirements.txt
```

Dependencies: `scanpy>=1.9.0`, `palantir`, `scikit-learn`, `matplotlib>=3.5.0`, `seaborn`, `pandas`, `numpy`, `anndata`
