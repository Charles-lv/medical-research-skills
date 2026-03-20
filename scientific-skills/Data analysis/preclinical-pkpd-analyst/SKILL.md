---
name: preclinical-pkpd-analyst
description: Automate non-compartmental pharmacokinetic analysis from preclinical concentration-time data, computing AUC, Cmax, T1/2, clearance, and volume of distribution.
license: MIT
skill-author: AIPOCH
status: beta
---
# Pre-clinical PK/PD Analyst

Automate non-compartmental pharmacokinetic analysis from preclinical concentration-time data.

## Input Validation

This skill accepts: concentration-time data files (CSV) from preclinical PK studies for non-compartmental analysis.

**Is this preclinical NCA?** Check before proceeding:
- ✅ Rat, mouse, dog, or other preclinical species PK data → proceed
- ✅ IV, oral, or other route concentration-time profiles → proceed
- ❌ Clinical trial PK analysis → refuse and redirect
- ❌ PD modeling, GWAS, or non-PK data → refuse and redirect

If the request does not involve computing PK parameters from preclinical concentration-time data — for example, asking to perform PD modeling, clinical trial analysis, or process non-PK data — do not proceed. Instead respond:

> "preclinical-pkpd-analyst is designed to automate non-compartmental PK analysis from preclinical concentration-time data. Your request appears to be outside this scope. Please provide a CSV file with time and concentration columns, or use a more appropriate tool for your task. For clinical PK analysis, consider a validated clinical NCA tool or consult a clinical pharmacokineticist."

Do not attempt any partial analysis before emitting this refusal.

## When to Use

- Computing NCA parameters (AUC, Cmax, Tmax, T1/2, CL, Vd) from rat, mouse, or dog PK studies
- IND-enabling study PK report generation
- Dose selection and drug candidate ranking based on PK profiles
- WinNonlin-alternative analysis for early-stage drug discovery

## Workflow

1. **Validate input** — apply the preclinical NCA gate above before any analysis begins.
2. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
3. Validate that the data file path does not contain `../` or point outside the workspace. Do not pass the path to `np.loadtxt` or any file reader before this check.
4. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
5. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
6. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--data` / `-d` | path | No* | PK data file (CSV with time, concentration columns) |
| `--demo` | flag | No | Run with built-in demo dataset |

*One of `--data` or `--demo` is required.

## Usage

```text
# Analyze PK data from CSV file
python scripts/main.py --data pk_data.csv

# Run demo analysis
python scripts/main.py --demo

# Check available options
python scripts/main.py --help
```

## Input Data Format

CSV file with at minimum:
```csv
time,concentration
0,0
0.5,125.3
1,98.7
2,65.2
4,32.1
8,12.4
24,1.8
```

## Output

- AUC (area under the curve, ng·h/mL)
- Cmax (maximum concentration)
- Tmax (time to maximum concentration)
- T1/2 (elimination half-life)
- Clearance (CL, mL/min/kg)
- Volume of distribution (Vd, L/kg)
- Non-compartmental analysis report
- PK parameter summary table

**Demo mode note:** When `--demo` is used, output includes a header: `[DEMO MODE] Results are from a built-in synthetic dataset for validation purposes only.`

## Example

Input: Rat IV PK data, 10 mg/kg dose  
Output: AUC = 1250 ng·h/mL, T1/2 = 4.2h, CL = 8.3 mL/min/kg

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --demo
```

## Error Handling

- If `--data` is missing and `--demo` is not specified, state this and request the data file path.
- If the data file path contains `../` or points outside the workspace, reject with a path traversal warning. Do not pass the path to `np.loadtxt` or any file reader.
- If required columns (time, concentration) are missing from the CSV, report the missing columns and stop.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate PK parameters, AUC values, or half-life estimates.

## Fallback Template

When execution fails or inputs are incomplete, respond with this structure:

```
FALLBACK REPORT
───────────────────────────────────────
Objective      : [restate the goal]
Blocked by     : [exact missing input or error]
Partial result : [what can be completed — e.g., NCA method description]
Assumptions    : [route of administration, dose, units assumed]
Constraints    : [minimum time points required for NCA]
Risks          : [sparse sampling, below-LOQ values]
Unresolved     : [what still needs user input]
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

```text
pip install -r requirements.txt
```
