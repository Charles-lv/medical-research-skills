---
name: clinical-data-cleaner
description: Clean and standardize clinical trial data to CDISC SDTM standards for FDA/EMA regulatory submissions. Handles missing values, outlier detection, date standardization, and generates audit trails for DM, LB, and VS domains.
license: MIT
skill-author: AIPOCH
---

# Clinical Data Cleaner

Clean, validate, and standardize clinical trial data to meet CDISC SDTM standards for regulatory submissions to FDA or EMA.

**Key Capabilities:**
- **SDTM Domain Validation**: DM, LB, VS domain field checking
- **Missing Value Handling**: Multiple imputation strategies (mean, median, mode, forward, drop)
- **Outlier Detection**: IQR, z-score, and domain-specific clinical thresholds
- **Date Standardization**: Convert to ISO 8601 format
- **Audit Trail**: Full cleaning log for regulatory submission

---

## Input Validation

This skill accepts: a CSV file containing clinical trial data, a domain identifier (DM, LB, or VS), and optional cleaning strategy parameters.

If the request does not involve cleaning or standardizing clinical trial data for CDISC SDTM compliance — for example, asking to analyze genomic data, perform statistical modeling, or interpret clinical results — do not proceed. Instead respond:
> "Clinical Data Cleaner is designed to clean and standardize clinical trial data for CDISC SDTM regulatory submissions. Please provide a CSV input file and domain (DM, LB, or VS). For other data analysis tasks, use a more appropriate tool."

---

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## Workflow

1. Confirm the input file, domain (DM/LB/VS), output path, and cleaning strategy parameters.
2. Validate that the request matches the documented scope; stop if the task requires unsupported assumptions.
3. Run the script or apply the documented cleaning path with only the inputs available.
4. Return a structured result separating assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

**Fallback:** If `--input`, `--domain`, or `--output` is missing, respond: "Required parameters missing. Please provide `--input` (CSV file), `--domain` (DM, LB, or VS), and `--output` (output path). Cannot clean without all three."

---

## Core Capabilities

### 1. SDTM Domain Validation

```python
from scripts.main import ClinicalDataCleaner
cleaner = ClinicalDataCleaner(domain='DM')
is_valid, missing = cleaner.validate_domain(data)
```

**Required Fields:**
- **DM**: STUDYID, USUBJID, SUBJID, RFSTDTC, RFENDTC, SITEID, AGE, SEX, RACE
- **LB**: STUDYID, USUBJID, LBTESTCD, LBCAT, LBORRES, LBORRESU, LBSTRESC, LBDTC
- **VS**: STUDYID, USUBJID, VSTESTCD, VSORRES, VSORRESU, VSSTRESC, VSDTC

### 2. Missing Value Handling

```python
cleaner = ClinicalDataCleaner(domain='DM', missing_strategy='median')
cleaned = cleaner.handle_missing_values(data)
```

Strategies: `mean`, `median`, `mode`, `forward`, `drop`

### 3. Outlier Detection

```python
cleaner = ClinicalDataCleaner(domain='LB', outlier_method='domain', outlier_action='flag')
flagged = cleaner.detect_outliers(data)
```

**Clinical Thresholds:**

| Parameter | Range | Unit |
|-----------|-------|------|
| Glucose | 50–500 | mg/dL |
| Hemoglobin | 5–20 | g/dL |
| Systolic BP | 70–220 | mmHg |

### 4. Date Standardization

```python
standardized = cleaner.standardize_dates(data)
# Converts to ISO 8601: 2023-01-15T09:30:00
```

### 5. Complete Pipeline

```python
cleaner = ClinicalDataCleaner(
    domain='DM', missing_strategy='median',
    outlier_method='iqr', outlier_action='flag'
)
cleaned_data = cleaner.clean(data)
cleaner.save_report('output.csv')
# Outputs: output.csv + output.report.json (audit trail)
```

---

## CLI Usage

```text
# Clean demographics domain
python scripts/main.py \
  --input dm_raw.csv \
  --domain DM \
  --output dm_clean.csv \
  --missing-strategy median \
  --outlier-method iqr \
  --outlier-action flag

# Clean lab data with clinical thresholds
python scripts/main.py \
  --input lb_raw.csv \
  --domain LB \
  --output lb_clean.csv \
  --outlier-method domain
```

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--input` | string | **Yes** | Input CSV file path |
| `--domain` | string | **Yes** | SDTM domain (DM, LB, VS) |
| `--output` | string | **Yes** | Output CSV file path |
| `--missing-strategy` | string | No | Missing value strategy |
| `--outlier-method` | string | No | Outlier detection method |
| `--outlier-action` | string | No | Outlier action (flag, remove, cap) |

---

## Output Requirements

Every final response must make these explicit:

- Objective or requested deliverable
- Inputs used (file, domain, strategies) and assumptions introduced
- Cleaning actions applied and counts (rows modified, outliers flagged)
- Core result: cleaned CSV path and audit trail path
- Constraints and risks (all cleaning actions must be reviewed before submission)
- Unresolved items and next-step checks (validate against CDISC SDTM IG)

---

## Error Handling

- If `--input`, `--domain`, or `--output` is missing, state the missing parameters and request them.
- If the domain is not DM, LB, or VS, state the supported domains and request clarification.
- If `scripts/main.py` fails, report the failure point and provide manual fallback guidance.
- Do not fabricate cleaning results, imputed values, or audit trail entries.

---

## Quality Checklist

**Pre-Cleaning:**
- [ ] IACUC approval obtained (animal studies)
- [ ] Sample size adequately powered
- [ ] Randomization method documented

**Post-Cleaning:**
- [ ] Validate against CDISC SDTM IG
- [ ] Review all cleaning actions in audit trail
- [ ] Test import to analysis software

---

## References

- `references/sdtm_ig_guide.md` — CDISC SDTM Implementation Guide
- `references/domain_specs.json` — Domain-specific field requirements
- `references/outlier_thresholds.json` — Clinical outlier thresholds
- `references/common-patterns.md` — Detailed usage patterns
- `references/troubleshooting.md` — Problem-solving guide
