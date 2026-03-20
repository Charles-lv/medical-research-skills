---
name: lipinski-rule-filter
description: Filter small molecule compound libraries based on Lipinski's Rule of Five to identify drug-like compounds with acceptable oral bioavailability.
license: MIT
skill-author: AIPOCH
status: beta
---
# Lipinski Rule Filter

Filter small molecule compound libraries based on Lipinski's Rule of Five to identify compounds with poor absorption or permeability.

## Input Validation

This skill accepts: SMILES strings, SMILES files (.smi), or SDF files (.sdf) containing small molecule structures for Lipinski Ro5 filtering.

If the request does not involve drug-likeness filtering of small molecules — for example, asking to analyze proteins, predict ADMET beyond Ro5, perform docking, or process non-chemical data — do not proceed. Instead respond:

> "lipinski-rule-filter is designed to screen small molecule libraries against Lipinski's Rule of Five. Your request appears to be outside this scope. Please provide a SMILES string or compound file, or use a more appropriate tool for your task."

Do not generate any output or property calculations before emitting this refusal. Validate scope first — this is the absolute first action before any other processing.

**Important:** Ro5 predicts oral bioavailability likelihood but does not cover metabolic stability, toxicity, or other ADMET properties. For full ADMET profiling, complement with tools such as SwissADME, pkCSM, or ADMETlab.

## When to Use

- Screening compound libraries for oral drug-likeness
- Prioritizing hits from HTS campaigns
- Flagging compounds that violate Ro5 before synthesis investment
- Generating rule-violation reports for medicinal chemistry review

## Workflow

1. **Validate input first** — confirm the request involves small molecule Ro5 filtering before any processing. Refuse out-of-scope requests immediately using the documented redirect message above.
2. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
3. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
4. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
5. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
6. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Lipinski's Rules

- MW < 500 Da
- LogP < 5
- H-bond donors < 5
- H-bond acceptors < 10

One violation is typically tolerated; two or more violations predict poor oral bioavailability.

## Limitations

- **Ro5 is a guideline, not a complete ADMET predictor.** Passing Ro5 does not guarantee oral bioavailability; it is a necessary but not sufficient condition.
- Ro5 does not predict metabolic stability, hERG toxicity, solubility, or permeability beyond the basic rules.
- Biologics (peptides, antibodies) are explicitly excluded from Ro5 scope.
- For full ADMET profiling, use complementary tools: SwissADME, pkCSM, ADMETlab, or Schrödinger QikProp.

## Usage

```text
# Filter a SMILES/SDF file
python scripts/main.py --input compounds.smi --output filtered.smi

# Check a single SMILES string
python scripts/main.py --smiles "CC(=O)Oc1ccccc1C(=O)O" --check

# Allow up to 2 violations
python scripts/main.py --input compounds.smi --output filtered.smi --violations 2
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--input` | str | No | - | Input SMILES or SDF file path |
| `--smiles` | str | No | - | Single SMILES string to check |
| `--output` | str | No | - | Output file path for passing compounds |
| `--violations` | int | No | 1 | Maximum allowed Lipinski rule violations |

## Output

- Filtered compound list (passing compounds)
- Per-compound rule violation report (MW, LogP, HBD, HBA values)
- Drug-likeness summary statistics

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
# Test with aspirin (should pass Ro5):
python scripts/main.py --smiles "CC(=O)Oc1ccccc1C(=O)O" --check
```

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate files, citations, data, search results, or execution outcomes.
- If `--input` file path contains `../` or absolute paths outside the workspace, reject with a path traversal warning.
- **Unicode encoding**: Status symbols use ASCII equivalents ([PASS], [FAIL], [INVALID]) for Python 3.6 terminal compatibility. If you see UnicodeEncodeError, set `PYTHONIOENCODING=utf-8` before running.

## Fallback Template

When execution fails or inputs are incomplete, respond with this structure:

```
FALLBACK REPORT
───────────────────────────────────────
Objective      : [restate the goal]
Blocked by     : [exact missing input or error]
Partial result : [what can be completed without the missing input]
Manual path    : Apply Ro5 rules manually: MW<500, LogP<5, HBD<5, HBA<10
Next step      : [minimum action needed to unblock]
───────────────────────────────────────
```

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

No additional Python packages required beyond the standard library.
