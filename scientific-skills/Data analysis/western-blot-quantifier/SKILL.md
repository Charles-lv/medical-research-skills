---
name: western-blot-quantifier
description: Automatically detect Western blot gel bands, perform densitometric analysis, and calculate normalized protein expression values relative to loading controls.
license: MIT
skill-author: AIPOCH
---
# Western Blot Quantifier

Automatically identify Western blot gel bands, perform densitometric analysis, and calculate normalized values relative to loading controls (GAPDH, β-actin, Tubulin).

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --demo
```

## When to Use

- Quantifying protein expression from Western blot gel images
- Normalizing target protein bands to loading controls
- Batch processing multiple gel images
- Generating reproducible densitometry results for publication

## Usage

```bash
python scripts/main.py \
    --image path/to/wb_image.png \
    --reference GAPDH \
    --targets p53,Bcl-2 \
    --lanes 4 \
    --output results.csv
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--image` | Yes | — | Gel image file path (PNG/TIFF) |
| `--reference` | Yes | GAPDH | Loading control protein name |
| `--targets` | Yes | — | Target protein name(s), comma-separated |
| `--lanes` | No | auto | Number of lanes (or auto-detect) |
| `--output` | No | stdout | Output CSV file path |
| `--threshold` | No | 0.1 | Band detection threshold |
| `--background` | No | rolling_ball | Background correction: rolling_ball, median, none |

## Workflow

1. Confirm objective, required inputs, and constraints before proceeding.
2. Validate request matches documented scope; stop early if unsupported assumptions are needed.
3. **Image Quality Check:** Before band detection, assess image contrast. If contrast is below threshold, emit: "Low contrast detected — consider adjusting --threshold or improving image quality before quantification."
4. Run `scripts/main.py` with available inputs, or use the documented reasoning path.
5. Return structured result separating assumptions, deliverables, risks, and unresolved items.
6. On execution failure or incomplete inputs, switch to fallback path and state exactly what blocked completion.

## Fallback Template

If `scripts/main.py` cannot run (missing image, unsupported format), respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective      : <stated goal>
Blocked by     : <exact missing input or error>
Partial result : <what can still be assessed manually>
Next step      : <minimum action to unblock>
───────────────────────────────────────
```

## Output Format

```csv
Lane,Protein,Raw_Intensity,Background,Corrected_Intensity,Normalized_to_Reference
1,GAPDH,125000.5,5000.2,120000.3,1.00
1,p53,85000.2,3000.1,82000.1,0.68
```

## Algorithm

1. Image preprocessing: grayscale conversion → background correction → denoising
2. Lane detection: vertical projection analysis for boundary identification
3. Band detection: 1D Gaussian fitting or peak detection
4. Optical density: integrate grayscale values in band region, subtract background
5. Normalization: target protein value ÷ loading control value

## Image Quality Notes

- High resolution, good contrast grayscale images recommended
- Common loading controls: GAPDH, β-actin, Tubulin
- If auto-detection is inaccurate, specify lane positions manually with `--lanes`
- For images with more than 6 lanes, recommend specifying lane positions manually with `--lanes` to improve detection accuracy
- Low contrast images: adjust `--threshold` parameter before quantification

## Output Requirements

Every response must make these explicit when relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced (including whether lane detection was automatic or manual; if manual, list specified positions)
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what can still be completed safely, and provide the manual fallback above.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Input Validation

This skill accepts: Western blot gel images (PNG/TIFF) with specified loading control and target protein names for automated densitometric quantification.

If the request does not involve Western blot quantification — for example, asking to analyze flow cytometry data, process immunofluorescence images, or interpret ELISA results — do not proceed. Instead respond:

> "western-blot-quantifier is designed to quantify protein bands in Western blot gel images. Your request appears to be outside this scope. Please provide a gel image with loading control and target protein names, or use a more appropriate tool for your task."

## Response Template

Use this fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions (including lane detection mode: automatic or manual)
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
| File System Access | Read gel image, write CSV output | Medium |
| Data Exposure | Output files saved to workspace | Low |

## Prerequisites

```bash
pip install -r requirements.txt
# Requires: numpy, opencv-python, pandas, matplotlib, scipy, scikit-image
```
