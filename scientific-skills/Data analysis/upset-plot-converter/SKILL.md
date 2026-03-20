---
name: upset-plot-converter
description: Convert complex Venn diagrams with more than 4 sets into clearer UpSet plots for publication-ready set intersection visualization.
license: MIT
skill-author: AIPOCH
---
# UpSet Plot Converter

Convert complex multi-set Venn diagrams (4+ sets) into clearer UpSet plots. Automatically sorts intersections by size and generates publication-ready figures.

## Input Validation

This skill accepts: set membership data (dicts of sets or paired name/list inputs) for converting multi-set Venn diagrams into UpSet plots.

If the request does not involve set intersection visualization — for example, asking to perform statistical tests on set overlaps, generate heatmaps, or create bar charts of non-set data — do not proceed. Instead respond:

> "upset-plot-converter is designed to visualize set intersections as UpSet plots. Your request appears to be outside this scope. Please provide set membership data with 4+ sets, or use a more appropriate tool for your task."

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py
```

## Audit-Ready Commands

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
# Inline test with 5 sets:
python -c "
from scripts.main import convert_venn_to_upset
sets = {'A':{1,2,3},'B':{2,3,4},'C':{3,4,5},'D':{4,5,6},'E':{5,6,7}}
convert_venn_to_upset(sets, output_path='test_upset.png')
print('OK')
"
```

## When to Use

- Visualizing intersections across 4+ gene sets, sample groups, or feature lists
- Replacing unreadable Venn diagrams in manuscripts
- Comparing overlap patterns across multiple experimental conditions
- Any set intersection analysis where clarity matters

## Usage

```python
from skills.upset_plot_converter.scripts.main import convert_venn_to_upset

sets = {
    'A': {1, 2, 3, 4, 5},
    'B': {4, 5, 6, 7, 8},
    'C': {3, 5, 7, 9, 10},
    'D': {2, 4, 6, 8, 10},
    'E': {1, 3, 5, 7, 9}
}
convert_venn_to_upset(sets, output_path="upset_plot.png")
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `sets` | Yes* | — | Dict of set names → sets/lists of elements |
| `set_names` | Yes* | — | List of set names (alternative input) |
| `lists` | Yes* | — | List of lists (paired with set_names) |
| `output_path` | Yes | — | Path to save output figure |
| `title` | No | None | Optional plot title |
| `min_subset_size` | No | 1 | Minimum intersection size to display |
| `max_intersections` | No | 30 | Maximum intersections to show |

*Provide either `sets` dict OR `set_names` + `lists` pair.

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

## Output

PNG file of the UpSet plot visualization with:
- Bar chart showing intersection sizes (top)
- Dot matrix showing which sets participate in each intersection (bottom)
- Intersections sorted by size for readability

## Output Requirements

Every response must make these explicit when relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced (including which input mode was used: dict or set_names+lists)
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If any set in the input is empty, emit a warning: "Warning: set [name] is empty and will appear with no intersections. Consider removing it or verifying your data."
- If an empty set causes a rendering error, invoke the Fallback Template with Blocked Steps noting the empty set issue.
- If the task goes outside documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what can still be completed safely, and provide the manual fallback above.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Response Template

Use this fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions (always state which input mode was used: dict or set_names+lists; list all non-default parameter values)
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

For simple requests, compress the structure but keep assumptions and limits explicit when they affect correctness.

## Prerequisites

```bash
pip install -r requirements.txt
# Requires: matplotlib, numpy, pandas
```
