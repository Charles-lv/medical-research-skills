---
name: motif-logo-generator
description: Generate publication-quality sequence logos for DNA or protein motifs from FASTA files or raw sequence lists.
license: MIT
skill-author: AIPOCH
status: beta
---
# Motif Logo Generator

Generate sequence logos for DNA or protein motifs to visualize conserved positions and information content.

## Input Validation

This skill accepts: aligned DNA or protein sequences in FASTA format or as a newline-separated string, for sequence logo generation.

If the request does not involve generating a sequence logo from biological sequences — for example, asking to perform sequence alignment, run BLAST, or analyze non-sequence data — do not proceed. Instead respond:

> "motif-logo-generator is designed to generate sequence logos for DNA or protein motifs. Your request appears to be outside this scope. Please provide aligned sequences in FASTA format or as a raw list, or use a more appropriate tool for your task. For sequence alignment, consider MUSCLE, MAFFT, or Clustal Omega."

Do not generate any output, alignment, or sequence analysis before emitting this refusal. Validate scope first — this is the absolute first action before any other processing.

## When to Use

- Visualizing conservation patterns in aligned DNA or protein sequences
- Generating publication-quality sequence logos for papers or presentations
- Comparing motif conservation across sequence sets
- Producing logos from FASTA files or raw sequence lists

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python -c "import numpy, matplotlib, logomaker, pandas; print('deps OK')"
```

## Workflow

1. **Validate input first** — confirm the request involves aligned sequences for logo generation. Refuse out-of-scope requests immediately using the documented redirect message above. Do not generate any output before this check.
2. Confirm the user objective, required inputs, and non-negotiable constraints.
3. Verify sequences are all the same length before proceeding — alignment is required if lengths differ.
4. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
5. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
6. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Usage

```text
# Generate logo from FASTA file
python scripts/main.py --input sequences.fasta --output logo.png --type dna

# Generate logo from raw sequences
python scripts/main.py --sequences "ACGT\nACCT\nAGGT" --output logo.png --type dna

# Protein sequences with custom styling
python scripts/main.py --input proteins.fasta --output logo.pdf --type protein --title "Conserved Domain"
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--input` | path | No* | Input FASTA file (or use `--sequences`) |
| `--sequences` | str | No* | Raw sequences separated by newline (or use `--input`) |
| `--output` | path | Yes | Output file path (.png, .pdf, .svg) |
| `--type` | enum | No | `dna` or `protein` (default: `dna`) |
| `--title` | str | No | Logo title |
| `--width` | int | No | Figure width in inches (default: 10) |
| `--height` | int | No | Figure height in inches (default: 3) |
| `--colorscheme` | str | No | Color scheme: `classic`, `base_pairing` (DNA); `chemistry`, `hydrophobicity` (protein) |

*One of `--input` or `--sequences` is required.

## Output

Generates a sequence logo showing:
- Letter height = information content (conservation in bits)
- Letter stack = frequency at each position
- Y-axis: bits for DNA, relative frequency for protein

## Example

Input (FASTA):
```
>seq1
ACGT
>seq2
ACGT
>seq3
ACCT
>seq4
AGGT
```

Output: Logo with position 2 showing C/G variability; other positions conserved.

## Error Handling

- If neither `--input` nor `--sequences` is provided, state this and request one of them.
- If sequences are not all the same length, report the mismatch and stop — alignment is required before logo generation.
- If the task goes outside the documented scope, stop immediately and emit the documented redirect message verbatim.
- If `scripts/main.py` fails, report the failure point and summarize what can still be completed.
- Do not fabricate sequence data or conservation scores.
- Reject file paths containing `../` with a path traversal warning.
- If numpy/matplotlib/logomaker are absent, the script falls back to ASCII logo output. Install with: `pip install numpy matplotlib logomaker pandas`.

## Fallback Template

When execution fails or inputs are incomplete, respond with this structure:

```
FALLBACK REPORT
───────────────────────────────────────
Objective      : [restate the goal]
Blocked by     : [exact missing input or error]
Partial result : [what can be completed without the missing input]
Next step      : [minimum action needed to unblock]
───────────────────────────────────────
```

## Response Template

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

Dependencies: `logomaker`, `pandas`, `numpy`, `matplotlib`
