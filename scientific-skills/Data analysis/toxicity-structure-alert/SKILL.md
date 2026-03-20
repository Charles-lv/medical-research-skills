---
name: toxicity-structure-alert
description: Identify potential toxic structural alerts in drug molecules by scanning SMILES/SMARTS against known toxicophore patterns using RDKit, with risk level assessment and recommendations.
license: MIT
skill-author: AIPOCH
---

# Toxicity Structure Alert

Scan drug molecule structures (SMILES/SMARTS) against known toxic structural alert patterns. Identifies toxicophores, assesses risk levels (HIGH/MEDIUM/LOW), and generates structured reports with recommendations.

## Quick Check

```bash
python -m py_compile scripts/main.py
```

## Audit-Ready Commands

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py -i "O=[N+]([O-])c1ccccc1"
python scripts/main.py -i "O=C1OC1c1ccccc1" -f json
python scripts/main.py -i "c1ccc2c(c1)ccc1c3ccccc3ccc21" -d full
```

## When to Use

- Screen drug candidates for known toxic structural alerts before synthesis
- Identify toxicophores in SMILES strings as part of ADMET profiling
- Generate toxicity risk reports for medicinal chemistry review
- Flag high-risk substructures for structural optimization

## Workflow

1. **Validate input first (pre-flight gate):** Confirm the request involves SMILES-based structural alert screening. If ADMET profiling, docking, protein sequences, or non-chemical data is requested, emit the scope refusal before any processing.
2. Confirm the input SMILES string and desired output format/detail level.
3. Run `scripts/main.py -i <SMILES>` with optional `-f json` and `-d full` flags.
4. Return a structured result separating alerts found, risk level, and recommendations.
5. If execution fails or inputs are incomplete, switch to the Fallback Template below.

## Fallback Template

If `scripts/main.py` fails or required fields are missing, respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective        : <toxicity screening goal>
Inputs Available : <SMILES string provided>
Missing Inputs   : <list exactly what is missing>
Partial Result   : <any alerts identifiable from partial input>
Blocked Steps    : <what could not be completed and why>
  Note: SMILES parse errors indicate invalid input structure.
        Verify SMILES validity before re-running.
Next Steps       : <minimum info needed to complete>
───────────────────────────────────────
```

## Stress-Case Output Checklist

For complex multi-constraint requests, always include these sections explicitly:

- **Assumptions**: default detail level (standard), output format (text)
- **Constraints**: pattern-based only; cannot replace full toxicological assessment
- **Risks**: false positives and false negatives are inherent to structural alert methods
- **Unresolved Items**: SMILES parse failures, ambiguous substructures

## Supported Alert Structures

| Alert Structure | Toxicity Type | Risk Level |
|---|---|---|
| Aromatic Nitro | Mutagenicity | HIGH |
| Aromatic Amine | Carcinogenicity | HIGH |
| Epoxide | Alkylating Agent | HIGH |
| Hydrazine | Hepatotoxicity | HIGH |
| Haloalkyl | Alkylating Agent | HIGH |
| Aldehyde | Reactive Toxicity | MEDIUM |
| Acyl Chloride | Reactive Toxicity | MEDIUM |
| Michael Acceptor | Electrophilic Toxicity | MEDIUM |
| Quinone | Oxidative Stress | MEDIUM |
| Thiol-Reactive Groups | Protein Binding | LOW–MEDIUM |

## CLI Usage

```bash
# Basic text output
python scripts/main.py -i "O=[N+]([O-])c1ccccc1"

# JSON format
python scripts/main.py -i "O=C1OC1c1ccccc1" -f json

# Full detail report
python scripts/main.py -i "c1ccc2c(c1)ccc1c3ccccc3ccc21" -d full
```

## Parameters

| Parameter | Short | Description | Default |
|---|---|---|---|
| `--input` | `-i` | Input SMILES string | required |
| `--format` | `-f` | Output format: `json` or `text` | `text` |
| `--detail` | `-d` | Detail level: `basic`, `standard`, `full` | `standard` |

## Output Format (JSON)

```json
{
  "input": "O=[N+]([O-])c1ccccc1",
  "mol_weight": 123.11,
  "alert_count": 1,
  "risk_score": 0.85,
  "risk_level": "HIGH",
  "alerts": [
    {
      "name": "Aromatic Nitro",
      "type": "mutagenic",
      "smarts": "[N+](=O)[O-]",
      "risk_level": "HIGH",
      "description": "May cause DNA damage and mutagenicity"
    }
  ],
  "recommendations": [
    "Recommend Ames test validation",
    "Consider structural optimization to reduce toxicity"
  ]
}
```

**Risk score aggregation for multi-alert molecules:** The overall `risk_level` reflects the highest individual alert level. The numeric `risk_score` is a weighted sum of individual alert scores (HIGH=1.0, MEDIUM=0.5, LOW=0.2), normalized to [0,1].

## Risk Levels

- **HIGH**: Known significant toxicity — strongly recommended to avoid or redesign
- **MEDIUM**: Potential toxicity — further evaluation recommended
- **LOW**: Minor concern — consider based on specific context

## Input Validation

This skill accepts: valid SMILES strings representing drug or drug-like molecules for structural toxicity alert scanning.

If the request does not involve SMILES-based structural alert screening — for example, asking to predict ADMET properties beyond structural alerts, perform docking, analyze protein sequences, or process non-chemical data — do not proceed. Instead respond:

> "`toxicity-structure-alert` is designed to identify toxic structural alerts in drug molecules from SMILES input. Your request appears to be outside this scope. Please provide a valid SMILES string, or use a more appropriate tool."

## Error Handling

- If no SMILES string is provided, request it explicitly.
- If RDKit raises a SMILES parse error, report the invalid input and ask for a corrected SMILES.
- If the task goes outside documented scope, stop instead of guessing.
- If `scripts/main.py` fails, use the Fallback Template above.
- Do not fabricate alert matches, risk scores, or execution outcomes.

## Output Requirements

Every final response must include:

1. **Objective** — molecule screened and purpose
2. **Inputs Received** — SMILES string, format, detail level
3. **Assumptions** — defaults applied
4. **Result** — alerts found, risk level, risk score
5. **Risks and Limits** — pattern-based only; false positives/negatives possible
6. **Next Checks** — recommend Ames test or ADMET suite for HIGH-risk alerts

## Notes

1. This tool is based on known alert patterns and cannot replace comprehensive toxicological assessment.
2. False positives and false negatives are inherent to structural alert methods.
3. Recommended to use alongside other ADMET prediction tools.

## References

- Ashby J., Tennant R.W. (1988) Chemical structure, Salmonella mutagenicity and extent of carcinogenicity.
- Kazius J., McGuire R., Bursi R. (2005) Derivation and validation of toxicophores for mutagenicity prediction.
- Enoch S.J., Cronin M.T.D. (2010) A review of the electrophilic reaction chemistry involved in covalent DNA binding.

## Dependencies

- Python 3.8+
- RDKit
