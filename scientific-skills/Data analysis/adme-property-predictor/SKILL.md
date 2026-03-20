---
name: adme-property-predictor
description: Predict ADME pharmacokinetic properties and drug-likeness of small molecules using validated cheminformatics models. Supports absorption, distribution, metabolism, excretion prediction, QED/MPO scoring, and batch library screening from SMILES input.
license: MIT
skill-author: AIPOCH
---

# ADME Property Predictor

Comprehensive pharmacokinetic prediction tool that assesses drug-likeness and ADME properties of small molecules using validated cheminformatics models, molecular descriptors, and structure-property relationships.

**Key Capabilities:**
- **Multi-Property Prediction**: Absorption, Distribution, Metabolism, Excretion
- **Drug-Likeness Scoring**: Lipinski's Rule of 5, Veber rules, QED score
- **Batch Processing**: Analyze compound libraries efficiently
- **Structure-Based Insights**: Identify liability hotspots and optimization opportunities
- **Comparative Analysis**: Rank candidates by predicted PK profile

---

## Input Validation

This skill accepts: valid SMILES strings for small molecules (MW 100–800 Da), or input CSV/SMI files containing a SMILES column, plus optional property and format flags.

If the request does not involve predicting ADME properties of small molecules — for example, asking to analyze biologics, perform docking, interpret clinical PK data, or write a drug discovery report — do not proceed. Instead respond:
> "ADME Property Predictor is designed for computational ADME prediction of small molecules from SMILES input. Your request appears to be outside this scope. Please provide a valid SMILES string or compound library file, or use a more appropriate tool."

---

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## Workflow

1. Confirm the SMILES input (single compound or batch file), target properties, and output format.
2. Validate that the request matches the documented scope — small molecules only; stop if the task requires unsupported assumptions.
3. Run the script or apply the documented reasoning path with only the inputs that are available.
4. Return a structured result separating assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

**Fallback:** If `--smiles` or `--input` is missing, respond: "Required input not provided. Please supply a SMILES string (`--smiles`) or an input file (`--input`). Do not proceed without a valid molecular structure."

---

## Core Capabilities

### 1. Absorption (A) Prediction

```python
from scripts.adme_predictor import ADMEPredictor
predictor = ADMEPredictor()
absorption = predictor.predict_absorption(
    smiles="CC(=O)Oc1ccccc1C(=O)O",  # Aspirin
    properties=["all"]
)
print(absorption.summary())
```

| Property | Units | Interpretation |
|----------|-------|----------------|
| **HIA** | % | Human intestinal absorption; >80% good |
| **Caco-2** | 10⁻⁶ cm/s | Permeability; >70 high, <25 low |
| **Solubility** | mg/mL | >0.1 mg/mL acceptable |
| **Lipinski Pass** | boolean | Passes all 5 rules |

### 2. Distribution (D) Prediction

| Property | Units | Interpretation |
|----------|-------|----------------|
| **Vd** | L/kg | Volume of distribution; 0.1–10 typical |
| **PPB** | % | Plasma protein binding; >90% high |
| **BBB** | LogBB | Brain penetration; >0.3 penetrant |

### 3. Metabolism (M) Prediction

| Property | Output | Interpretation |
|----------|--------|----------------|
| **CYP Inhibition** | IC50 or class | DDI risk; <1 μM high risk |
| **Stability** | T1/2 or class | Microsomal/hepatocyte stability |
| **Liability Sites** | Atom indices | Soft spots for metabolism |

### 4. Excretion (E) Prediction

| Property | Units | Interpretation |
|----------|-------|----------------|
| **CL** | mL/min/kg | Clearance; <5 low, >15 high |
| **T1/2** | hours | Half-life; 2–8h typical for oral drugs |
| **Route** | renal/biliary/mixed | Primary excretion pathway |

### 5. Drug-Likeness Scoring

| Method | Range | Good Score |
|--------|-------|------------|
| **QED** | 0–1 | >0.6 |
| **Muegge** | 0–6 | >4 |
| **MPO** | 0–10 | >6 |

---

## CLI Usage

```text
# Predict ADME for single compound
python scripts/main.py \
  --smiles "CC(=O)Oc1ccccc1C(=O)O" \
  --properties all \
  --output aspirin_adme.json

# Batch process compound library
python scripts/main.py \
  --input library.smi \
  --properties absorption,distribution \
  --format csv \
  --output library_adme.csv

# Filter and rank
python scripts/main.py \
  --input library_adme.csv \
  --filter "lipinski_pass=True,hia>80" \
  --rank-by qed \
  --top-n 100 \
  --output top_candidates.csv
```

---

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--smiles` | str | — | SMILES string of the molecule |
| `--properties` | str | all | Specific properties to calculate |
| `--format` | str | json | Output format (json/csv) |
| `--input` | str | — | Input CSV/SMI file with SMILES column |
| `--output` | str | — | Output file for results |

---

## Output Requirements

Every final response must make these explicit:

- Objective or requested deliverable
- Inputs used (SMILES, file) and assumptions introduced
- Workflow or decision path taken
- Core result: predicted properties with values and confidence
- Constraints, risks, caveats (predictions are NOT experimental data)
- Unresolved items and next-step checks (experimental validation needed)

---

## Error Handling

- If `--smiles` or `--input` is missing, state the missing field and request it. Do not proceed.
- If the task goes outside scope (biologics, clinical PK, docking), stop and redirect.
- If `scripts/main.py` fails, report the failure point, summarize what can still be completed, and provide a manual fallback.
- Do not fabricate predictions, citations, or execution outcomes.

---

## Limitations

- **Small Molecules Only**: MW 100–800 Da; unreliable for biologics or macrocycles
- **pH 7.4 Assumption**: Most models predict at physiological pH
- **Human-Specific**: Predictions for human PK; animal models may differ
- **Qualitative Only**: For Go/No-Go decisions; not precise quantitative predictions
- **No Toxicity**: ADME only; use separate tools for safety assessment

**Model Accuracy (Typical):**
- LogP: R² = 0.85–0.95 | Solubility: R² = 0.65–0.80 | HIA: 75–85% | BBB: 70–80%

> ⚠️ **CRITICAL DISCLAIMER**: These predictions are computational estimates for prioritization only. They do NOT replace experimental ADME studies required for regulatory submissions or clinical decision-making.

---

## References

→ Full details: [references/lipinski_rules.md](references/lipinski_rules.md)
→ Full details: [references/qsar_models.md](references/qsar_models.md)
→ Full details: [references/property_ranges.md](references/property_ranges.md)
→ Full details: [references/model_validation.md](references/model_validation.md)

## Scripts

- `main.py` — CLI interface
- `adme_predictor.py` — Core prediction engine
- `absorption.py`, `distribution.py`, `metabolism.py`, `excretion.py` — Property models
- `druglikeness.py` — QED, MPO scoring
- `batch_processor.py` — Library screening
- `validator.py` — Input validation and applicability domain
