---
name: spatial-transcriptomics-mapper
description: Map spatial transcriptomics data from 10x Genomics Visium or Xenium onto tissue section images, visualizing gene expression and spatial clustering distributions.
license: MIT
skill-author: AIPOCH
---

# Spatial Transcriptomics Mapper

Process 10x Genomics Visium or Xenium spatial transcriptomics data and project gene expression onto tissue section images. Supports single-gene visualization, multi-gene overlays, and spatial clustering maps.

## Quick Check

```bash
python -m py_compile scripts/main.py
```

## Audit-Ready Commands

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --platform visium --data-dir ./test_data/visium_sample --gene GENE_0000 --output ./test_output/
```

## When to Use

- Visualize spatial gene expression from Visium or Xenium data
- Overlay multiple gene expression maps on tissue images
- Display spatial distribution of Seurat/Scanpy clustering results
- Generate publication-quality spatial maps for research reports

## Workflow

1. Confirm platform (visium/xenium), data directory, target gene(s), and output path.
2. **Platform auto-detection:** If `--platform` is missing, check the data directory for `filtered_feature_bc_matrix.h5` + `spatial/` (→ Visium) or `transcripts.parquet` (→ Xenium) and infer the platform automatically. Report the inferred platform before proceeding.
3. Validate that the request involves spatial transcriptomics mapping; stop early if not.
4. Run `scripts/main.py` with the appropriate platform and gene flags.
5. Return a structured result separating assumptions, output files, and unresolved items.
6. If execution fails or inputs are incomplete, switch to the Fallback Template below.

## Fallback Template

If `scripts/main.py` fails or required fields are missing, respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective        : <mapping goal>
Inputs Available : <platform, data-dir, gene(s) provided>
Missing Inputs   : <list exactly what is missing>
Partial Result   : <any steps completed safely>
Blocked Steps    : <what could not be completed and why>
Next Steps       : <minimum info needed to complete>
───────────────────────────────────────
```

## Stress-Case Output Checklist

For complex multi-constraint requests, always include these sections explicitly:

- **Assumptions**: platform defaults, missing gene names substituted, DPI used
- **Constraints**: data size limits, memory requirements, crop region applied
- **Risks**: large Xenium datasets may require `--crop`; missing genes will be skipped
- **Unresolved Items**: genes not found in dataset, files not present

## Features

- **Visium**: Space Ranger output (`.h5`, `tissue_positions_list.csv`, tissue images)
- **Xenium**: Xenium Explorer output (`.h5`, `transcripts.parquet`, `nucleus_boundaries.parquet`)
- **Gene Expression Mapping**: Projects expression onto tissue images
- **Spatial Clustering**: Displays Seurat/Scanpy cluster distributions
- **Multi-gene Joint Analysis**: Overlay or grid visualization
- **High-resolution Output**: Configurable DPI up to 600+

## CLI Usage

```bash
# Single gene — Visium
python scripts/main.py --platform visium --data-dir /path/to/spaceranger/outs/ \
  --gene PIK3CA --output ./output/

# Single gene — Xenium
python scripts/main.py --platform xenium --data-dir /path/to/xenium/outs/ \
  --gene PIK3CA --output ./output/

# Multiple genes
python scripts/main.py --platform visium --data-dir /path/to/data/ \
  --genes PIK3CA,PTEN,EGFR --mode overlay --output ./output/

# With clustering results
python scripts/main.py --platform visium --data-dir /path/to/data/ \
  --cluster-file ./clusters.csv --output ./output/
```

## Key Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `--platform` | str | required | `visium` or `xenium` |
| `--data-dir` | str | required | Data directory path |
| `--gene` | str | optional | Single gene name |
| `--genes` | list | optional | Multiple genes, comma-separated |
| `--mode` | str | `single` | `single` / `overlay` / `multi` / `cluster` |
| `--cluster-file` | str | optional | Clustering result CSV |
| `--output` | str | `./output` | Output directory |
| `--dpi` | int | 300 | Output image DPI |
| `--cmap` | str | `viridis` | Color map |
| `--crop` | str | optional | Crop region `x1,y1,x2,y2` |

→ Full parameter reference: [references/parameters.md](references/parameters.md)

## Output Files

- `{gene}_spatial_map.png` — Single gene spatial expression map
- `{gene}_heatmap.png` — Gene expression heatmap
- `multi_gene_overlay.png` — Multi-gene overlay (with `--mode overlay`)
- `cluster_spatial_map.png` — Cluster spatial distribution
- `combined_report.html` — Comprehensive HTML report

## Input Validation

This skill accepts: 10x Genomics Visium or Xenium output directories with valid Space Ranger or Xenium Explorer file structures, plus at least one gene name or cluster file.

If the request does not involve spatial transcriptomics mapping — for example, asking to perform bulk RNA-seq analysis, process scRNA-seq without spatial coordinates, or analyze non-genomics imaging data — do not proceed. Instead respond:

> "`spatial-transcriptomics-mapper` is designed to map 10x Genomics Visium/Xenium spatial transcriptomics data onto tissue images. Your request appears to be outside this scope. Please provide a valid Visium or Xenium data directory, or use a more appropriate tool."

If the data is from a non-10x spatial platform (Slide-seq, MERFISH, seqFISH, etc.), note that this skill supports Visium and Xenium only, and recommend the appropriate platform-specific tool or pipeline.

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside documented scope, stop instead of guessing.
- If `scripts/main.py` fails, use the Fallback Template above.
- Do not fabricate gene expression values, output files, or execution outcomes.

## Output Requirements

Every final response must include:

1. **Objective** — genes/clusters mapped and platform used
2. **Inputs Received** — data directory, platform, gene list, parameters
3. **Assumptions** — defaults applied (DPI, cmap, mode)
4. **Result** — output file paths generated
5. **Risks and Limits** — large datasets, missing genes, memory constraints
6. **Next Checks** — verify gene names exist in dataset before full run

## Notes

- Visium uses low-resolution images by default; use `--hires` for high resolution
- For large Xenium datasets, use `--crop` to specify region of interest
- Color map reference: https://matplotlib.org/stable/tutorials/colors/colormaps.html

## Dependencies

```
scanpy
squidpy
matplotlib
seaborn
pillow
numpy
pandas
h5py
pyarrow      # Xenium only
dask         # Xenium only
opencv-python  # optional, advanced image processing
```
