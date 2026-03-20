---
name: fastqc-report-interpreter
description: Interprets FastQC quality control reports for NGS data. Identifies quality issues, diagnoses root causes, and provides actionable recommendations for RNA-seq, DNA-seq, and ChIP-seq datasets.
license: MIT
skill-author: AIPOCH
status: beta
---
# FASTQC Report Interpreter

Analyze FastQC quality control reports for Next-Generation Sequencing data. Identifies per-base quality issues, adapter contamination, duplication levels, and sequence bias, then provides application-specific remediation recommendations.

## Input Validation

This skill accepts: FastQC HTML or JSON report files from Illumina, PacBio, or Oxford Nanopore sequencing runs.

If the request does not involve FastQC report interpretation — for example, asking to perform alignment, call variants, or analyze non-sequencing data — do not proceed. Instead respond:

> "`fastqc-report-interpreter` is designed to interpret FastQC quality control reports for NGS data. Your request appears to be outside this scope. Please provide a FastQC report file, or use a more appropriate tool for your task."

Do not generate any output or analysis before emitting this refusal. Validate scope first.

## When to Use

- Assessing sequencing data quality before downstream analysis
- Diagnosing quality failures in RNA-seq, DNA-seq, or ChIP-seq datasets
- Generating batch QC summaries across multiple samples
- Deciding whether trimming or filtering is required before alignment

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --demo
```

## Workflow

1. **Validate input first** — confirm the request involves a FastQC report before any processing.
2. Confirm the user objective, required inputs, and non-negotiable constraints.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

**Fallback template:** If `scripts/main.py` fails or the report file is unreadable, report: (a) the failure point, (b) which metrics can still be assessed manually from the FastQC HTML, (c) the recommended manual review checklist.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--report`, `-r` | string | No* | FastQC JSON or HTML report file |
| `--demo` | flag | No | Run with built-in demo data |
| `--batch` | string | No | Glob pattern for batch analysis (e.g., `"*_fastqc.json"`) |
| `--application` | string | No | Sequencing type: `rna_seq`, `dna_seq`, `chip_seq` |
| `--output`, `-o` | string | No | Output file path (default: stdout) |
| `--output-format` | string | No | `text` or `json` (default: `text`) |

*Required unless `--demo` or `--batch` is used.

**Implementation note:** `--batch` and `--application` flags are documented here and must be present in `scripts/main.py` argparse. If the script returns "unrecognized arguments", add these flags to the argparse definition and implement: (1) a batch processing loop for `--batch`, and (2) application-specific threshold overrides for `--application`.

## Usage

```text
# Single report
python scripts/main.py --report sample_fastqc.json --application rna_seq

# Batch analysis
python scripts/main.py --batch "*_fastqc.json" --output batch_summary.csv

# Demo mode
python scripts/main.py --demo

# JSON output for agent consumption
python scripts/main.py --report sample_fastqc.json --output-format json
```

## Key Quality Metrics

| Metric | Good | Warning | Fail |
|--------|------|---------|------|
| Per base sequence quality | Q > 28 | Q 20–28 | Q < 20 |
| Per sequence quality scores | Peak >= Q30 | Peak Q20–30 | Peak < Q20 |
| Per base N content | < 5% | 5–20% | > 20% |
| Sequence duplication | < 20% | 20–50% | > 50% |
| Adapter content | < 5% | 5–10% | > 10% |

**Application-specific thresholds:**
- RNA-seq: duplication up to 40% acceptable (transcript abundance effect)
- DNA-seq: strict quality required for variant calling
- ChIP-seq: moderate quality; focus on enrichment metrics

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- If the report file is not found, print a user-friendly error to stderr and exit with code 1 (do not show raw Python traceback): `Error: Report file not found: {path}`
- Do not fabricate files, citations, data, search results, or execution outcomes.
- Unicode symbols require `PYTHONIOENCODING=utf-8` on Python 3.6 terminals; ASCII fallbacks (PASS/WARN/FAIL) are used when encoding is unavailable.

## Output Requirements

Every response must make these explicit:

- Objective and deliverable
- Inputs used and assumptions introduced
- Workflow or decision path taken
- Core result: quality status per metric, issues found, recommendations
- Constraints, risks, caveats (e.g., platform-specific artifacts)
- Unresolved items and next-step checks

## Response Template

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

## Prerequisites

```bash
pip install -r requirements.txt
```
