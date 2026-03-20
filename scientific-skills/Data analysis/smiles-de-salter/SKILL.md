---
name: smiles-de-salter
description: Batch process chemical SMILES strings to remove salt ions and retain the active pharmaceutical ingredient core using RDKit.
license: MIT
skill-author: AIPOCH
---

# SMILES De-salter

Batch process chemical structure strings, removing salt ion portions and retaining only the active core (API). Uses RDKit to identify and strip counterions from SMILES notation.

## Quick Check

```bash
python -m py_compile scripts/main.py
```

## Audit-Ready Commands

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py -s "CC(C)CN1C(=O)N(C)C(=O)C2=C1N=CN2C.[Na+]"
python scripts/main.py -i input.csv -o output.csv -c smiles
```

## When to Use

- Remove salt ions from SMILES strings before cheminformatics analysis
- Standardize compound libraries by stripping counterions
- Batch-process CSV/TSV files containing SMILES columns
- Prepare clean SMILES for downstream ADMET or docking workflows

## Workflow

1. Confirm input format (single SMILES string, CSV/TSV file, or pure SMILES file) and column name.
2. Validate that the request involves SMILES de-salting; stop early if not.
3. Run the appropriate command (single `-s` flag or batch `-i/-o` flags).
4. Return a structured result separating assumptions, deliverables, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the Fallback Template below.

## Fallback Template

If `scripts/main.py` fails or required fields are missing, respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective        : <de-salting goal>
Inputs Available : <list what was provided>
Missing Inputs   : <list exactly what is missing>
Partial Result   : <any SMILES that could be processed safely>
Blocked Steps    : <what could not be completed and why>
Next Steps       : <minimum info needed to complete>
───────────────────────────────────────
```

## Salt Ion Identification Rules

- Multiple components identified via `.` separator in SMILES
- Salt ions are typically smaller fragments (Na⁺, Cl⁻, K⁺, Br⁻, etc.)
- Default: retain the component with the most heavy atoms
- Supports common inorganic salts and organic acid salts

| Type | Examples |
|---|---|
| Inorganic salts | NaCl, KCl, HCl, H₂SO₄ |
| Organic acid salts | Citrate, Tartrate, Maleate |
| Quaternary ammonium | Various quaternary ammonium compounds |

## CLI Usage

```bash
# Single SMILES string
python scripts/main.py -s "CC(C)CN1C(=O)N(C)C(=O)C2=C1N=CN2C.[Na+]"
# Output: CC(C)CN1C(=O)N(C)C(=O)C2=C1N=CN2C

# Batch CSV processing
python scripts/main.py -i input.csv -o output.csv -c smiles_column

# Keep largest fragment (default: True)
python scripts/main.py -i input.csv -o output.csv -k True
```

## Parameters

| Parameter | Short | Description | Default |
|---|---|---|---|
| `--input` | `-i` | Input file path (CSV/TSV/SMILES) | Required for batch |
| `--output` | `-o` | Output file path | `desalted_output.csv` |
| `--column` | `-c` | SMILES column name | `smiles` |
| `--smiles` | `-s` | Single SMILES string | — |
| `--keep-largest` | `-k` | Keep largest component by atom count | `True` |

## Input / Output Format

**Input CSV:**
```csv
id,smiles,name
1,CCO.[Na+],ethanol_sodium
2,c1ccccc1.[Cl-],benzene_hcl
```

**Output CSV:**
```csv
id,smiles,name,desalted_smiles,status
1,CCO.[Na+],ethanol_sodium,CCO,success
2,c1ccccc1.[Cl-],benzene_hcl,c1ccccc1,success
```

## Examples

| Input SMILES | Output SMILES | Note |
|---|---|---|
| `CCO.[Na+]` | `CCO` | Simple inorganic salt |
| `CN1C=NC2=C1C(=O)N(C)C(=O)N2C.Cl` | `CN1C=NC2=C1C(=O)N(C)C(=O)N2C` | HCl salt |
| `CC(C)CN1C(=O)...C.C(C(=O)O)...O` | `CC(C)CN1C(=O)...C` | Complex organic salt |

## Input Validation

This skill accepts: SMILES strings (single via `-s`) or CSV/TSV/SMILES files (batch via `-i`) containing chemical structure data for salt removal.

If the request does not involve SMILES de-salting — for example, asking to predict toxicity, perform docking, or analyze non-chemical data — do not proceed. Instead respond:

> "`smiles-de-salter` is designed to remove salt ions from chemical SMILES strings. Your request appears to be outside this scope. Please provide a valid SMILES string or input file, or use a more appropriate tool."

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the `--input` path contains `../` or resolves outside the workspace, reject with a path traversal warning before opening the file.
- If the task goes outside documented scope, stop instead of guessing.
- If `scripts/main.py` fails (e.g., RDKit parse error, file not found), use the Fallback Template above.
- Do not fabricate SMILES outputs, file contents, or execution outcomes.

## Output Requirements

Every final response must include:

1. **Objective** — what was de-salted and why
2. **Inputs Received** — SMILES strings or file path and column used
3. **Assumptions** — any inferred column names or defaults applied
4. **Result** — cleaned SMILES or output file path
5. **Risks and Limits** — co-crystals or multi-component drugs may need manual review
6. **Next Checks** — recommend sampling and verifying results

## Notes

1. This tool assumes the core is the component with the most heavy atoms; co-crystals may need manual review.
2. Some hydrochloride salts may appear as `[Cl-]` or `Cl` — both are handled.
3. Recommend spot-checking a sample of results after batch processing.
4. **`--keep-largest` bool parsing:** argparse `type=bool` treats any non-empty string as `True`. Always pass `True` or `False` explicitly. The script should use `lambda x: x.lower() == 'true'` as the argparse type to fix this.

## Dependencies

- Python >= 3.8
- rdkit >= 2022.03.1
- pandas
