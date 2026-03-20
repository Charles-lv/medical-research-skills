---
name: phylogenetic-tree-styler
description: Beautify phylogenetic trees with taxonomy color blocks, bootstrap values, and timelines. Accepts Newick format and outputs PNG, PDF, or SVG.
license: MIT
skill-author: AIPOCH
status: beta
---
# Phylogenetic Tree Styler

Beautify phylogenetic trees, add taxonomy color blocks, Bootstrap values, and timelines. Accepts standard Newick format input.

## Input Validation

This skill accepts: Newick format phylogenetic tree files (.nwk, .newick) and optional taxonomy CSV annotation files, for the purpose of generating beautified tree visualizations.

If the user's request does not involve phylogenetic tree visualization — for example, asking to build a phylogenetic tree from sequences, run alignment, or perform evolutionary analysis — do not proceed with the workflow. Instead respond:
> "phylogenetic-tree-styler is designed to beautify existing phylogenetic trees in Newick format. It does not build trees from sequences. Your request appears to be outside this scope. Please provide a Newick tree file, or use a more appropriate tool for your task."

Do not continue the workflow when the request is out of scope, missing the required `-i` input file, or would require unsupported assumptions. For missing inputs, state exactly which fields are missing.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py -i tree.nwk -o tree_styled.png
```

## When to Use

- Beautify phylogenetic trees with taxonomy color blocks, bootstrap values, and timelines
- Generate publication-ready tree output (PNG, PDF, SVG) from Newick format files
- Add taxonomy color annotations to existing trees

**Composability:** Output PNG/PDF/SVG files can be consumed by multi-panel-figure-assembler or graphical-abstract-wizard for composite figure assembly.

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Features

- Beautify phylogenetic trees with customizable branch and leaf colors
- Add taxonomy color blocks from CSV annotation file
- Display Bootstrap values with configurable threshold
- Add geological timeline with root age
- Output to PNG, PDF, or SVG

## Usage

```text
python3 scripts/main.py --input <input_tree.nwk> --output <output.png> [options]
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `-i`, `--input` | Input Newick format phylogenetic tree file | Required |
| `-o`, `--output` | Output image file path | tree_styled.png |
| `-f`, `--format` | Output format: png, pdf, svg | png |
| `-w`, `--width` | Image width (pixels) | 1200 |
| `-h`, `--height` | Image height (pixels) | 800 |
| `--show-bootstrap` | Show Bootstrap values | False |
| `--bootstrap-threshold` | Only show Bootstrap values above this threshold | 50 |
| `--taxonomy-file` | Species taxonomy CSV (name,domain,phylum,class,order,family,genus) | None |
| `--show-timeline` | Show timeline | False |
| `--root-age` | Root node age (million years ago) | None |
| `--branch-color` | Branch color | black |
| `--leaf-color` | Leaf node label color | black |

## Examples

### Basic Beautification
```text
python3 scripts/main.py -i tree.nwk -o tree_basic.png
```

### Show Bootstrap Values
```text
python3 scripts/main.py -i tree.nwk -o tree_bootstrap.png --show-bootstrap --bootstrap-threshold 70
```

### Add Taxonomy Color Blocks
```text
python3 scripts/main.py -i tree.nwk -o tree_taxonomy.png --taxonomy-file taxonomy.csv
```

### Add Timeline
```text
python3 scripts/main.py -i tree.nwk -o tree_timeline.png --show-timeline --root-age 500
```

## Input Formats

### Newick Tree Format
```
((A:0.1,B:0.2)95:0.3,(C:0.4,D:0.5)88:0.6);
```
Bootstrap values can be placed at node label positions (e.g., 95, 88 above).

**Supported format:** Standard Newick only. Extended Newick variants (NHX, NEXUS) are not supported. If your file uses NHX or NEXUS format, convert to standard Newick first (e.g., using FigTree or Dendropy).

### Taxonomy CSV Format
```csv
name,domain,phylum,class
Species_A,Bacteria,Proteobacteria,Gammaproteobacteria
Species_B,Bacteria,Firmicutes,Bacilli
Species_C,Archaea,Euryarchaeota,Methanobacteria
```

## Dependencies

- Python 3.8+
- ete3
- matplotlib
- numpy
- pandas

```text
pip install ete3 matplotlib numpy pandas
```

## Fallback Behavior

If `scripts/main.py` fails or required inputs are incomplete:
1. Report the exact failure point and error message — include the exact error line from stderr in the Blocked by field.
2. If the error is `No module named 'ete3'`, instruct: `pip install ete3 matplotlib numpy pandas` then retry with: `python3 scripts/main.py -i tree.nwk -o out.png`
3. State what can still be completed (e.g., input format validation without rendering).
4. Manual fallback: verify the Newick file is valid format, then re-run with minimal options: `python3 scripts/main.py -i tree.nwk -o out.png`.
5. Do not fabricate execution outcomes or tree data.

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
- If the Newick file uses NHX or NEXUS format, note this is not supported and recommend converting to standard Newick first.
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
