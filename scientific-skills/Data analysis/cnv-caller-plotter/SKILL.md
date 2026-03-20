---
name: cnv-caller-plotter
description: Detect copy number variations from whole genome sequencing data and generate publication-quality genome-wide CNV plots. Supports CNV calling, segmentation, tumor-normal comparison, and BED format export for cancer genomics and rare disease analysis.
license: MIT
skill-author: AIPOCH
status: beta
---

# CNV Caller & Plotter

Detect copy number variations (CNVs) from whole genome sequencing (WGS) data and generate genome-wide visualization plots for cancer genomics, rare disease analysis, and population genetics studies.

> ⚠️ **PLACEHOLDER ALGORITHM — NOT FOR PRODUCTION USE**
> The current CNV calling logic returns hardcoded mock data and does not analyze real BAM files. Do not run on patient samples or use results for clinical or research decisions until a real algorithm (pysam + numpy read-depth calculation) is implemented.

**Key Capabilities:**
- **CNV Detection from WGS**: Identify copy number gains and losses from aligned BAM data
- **Genomic Segmentation**: Divide genome into bins/windows for copy number estimation
- **Flexible Input Support**: Process BAM and VCF standard genomics formats
- **Publication-Quality Plots**: Genome-wide CNV profiles in PNG, PDF, or SVG
- **Standard Output Formats**: Export CNV calls in BED format

---

## Input Validation

This skill accepts: aligned BAM files (with index .bai) and a reference genome FASTA file. Optional parameters include bin size, output directory, and plot format.

If the request does not involve detecting CNVs from WGS data or generating CNV plots — for example, asking to call SNVs, perform RNA-seq analysis, or interpret clinical genetic reports — do not proceed. Instead respond:
> "CNV Caller & Plotter is designed to detect copy number variations from WGS BAM files and generate genome-wide plots. Please provide a BAM file and reference genome. For other genomics tasks, use a more appropriate tool."

**PHI Warning:** This skill may process patient genomic data. Ensure HIPAA compliance and data use agreements are in place before running on patient samples. For research use, consider anonymizing patient identifiers before processing using tools like ARX or Amnesia for genomic data de-identification.

**HIPAA Enforcement:** Pass `--confirm-hipaa` when processing patient genomic data. Without this flag, the script will refuse to proceed: `"Patient genomic data detected. Confirm HIPAA compliance with --confirm-hipaa before proceeding."`

---

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## Workflow

1. Confirm the input BAM file, reference genome, output directory, and analysis parameters.
2. Validate that the request matches the documented scope; stop if the task requires unsupported assumptions.
3. Run the script or apply the documented analysis path with only the inputs available.
4. Return a structured result separating assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

**Fallback:** If `--input` or `--reference` is missing, respond: "Required parameters missing. Please provide `--input` (BAM file) and `--reference` (reference FASTA). Cannot call CNVs without both."

---

## Core Capabilities

### 1. CNV Detection

```python
from scripts.main import CNVCaller
caller = CNVCaller(bin_size=1000)
cnv_calls = caller.call_cnvs(input_file="sample.bam", reference="hg38.fa")
for cnv in cnv_calls:
    print(f"{cnv['chrom']}:{cnv['start']}-{cnv['end']} CN={cnv['cn']}")
```

**Bin Size Selection:**

| Bin Size | Resolution | Coverage Required |
|----------|------------|-------------------|
| 100 bp | High | >30x |
| 1000 bp | Standard | >15x |
| 10000 bp | Low | >5x |

### 2. Genome-Wide Visualization

```python
plot_file = caller.plot_genome_wide(cnv_calls=cnv_calls, output_path="./results", fmt="pdf")
```

| Format | Best For |
|--------|----------|
| **PNG** | Web, presentations |
| **PDF** | Publications, printing |
| **SVG** | Vector editing |

### 3. BED Format Export

```python
bed_file = caller.save_bed(cnv_calls, "./output")
# Format: chrom  start  end  CN=3  .  .
```

### 4. Tumor-Normal Comparison

**Note:** Tumor-normal differential calling is documented but not yet implemented in the placeholder. Until the real algorithm is in place, both tumor and normal inputs return the same placeholder calls. Do not use for somatic CNV identification.

| Category | Tumor CN | Normal CN |
|----------|----------|-----------|
| **Somatic Amplification** | >2 | 2 |
| **Somatic Deletion** | <2 | 2 |
| **Germline CNV** | ≠2 | ≠2 |

---

## CLI Usage

```text
# Call CNVs from BAM file
python scripts/main.py --input sample.bam --reference hg38.fa

# Custom output and bin size
python scripts/main.py --input sample.bam --reference hg38.fa --output ./results --bin-size 500

# Generate PDF plots
python scripts/main.py --input sample.bam --reference hg38.fa --plot-format pdf

# Patient data (requires HIPAA acknowledgment)
python scripts/main.py --input patient.bam --reference hg38.fa --confirm-hipaa
```

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--input`, `-i` | string | **Yes** | Input BAM/VCF file |
| `--reference`, `-r` | string | **Yes** | Reference genome FASTA |
| `--output`, `-o` | string | No | Output directory |
| `--bin-size` | int | No | Bin size for analysis (default 1000) |
| `--plot-format` | string | No | Plot format (png, pdf, svg) |
| `--confirm-hipaa` | flag | **Required for patient data** | Confirms HIPAA compliance before processing patient genomic data |

---

## Output Requirements

Every final response must make these explicit:

- Objective or requested deliverable
- Inputs used (BAM file, reference, parameters) and assumptions introduced
- Analysis path taken (bin size, filters applied)
- Core result: CNV call count, BED file path, plot file path
- Constraints and risks (minimum 15x coverage required; validate key findings; **placeholder algorithm — results are mock data**)
- Unresolved items and next-step checks (filter against population CNV databases)

---

## Error Handling

- If `--input` or `--reference` is missing, state the missing parameters and request them.
- If BAM file is not indexed (.bai missing), flag and request indexing: `samtools index sample.bam`
- If patient data is detected without `--confirm-hipaa`, refuse with: `"Patient genomic data detected. Confirm HIPAA compliance with --confirm-hipaa before proceeding."`
- If `scripts/main.py` fails, report the failure point and provide manual fallback guidance.
- Do not fabricate CNV calls, coordinates, or plot outputs.

---

## Common Pitfalls

- **Low coverage data**: Minimum 15–20x for reliable WGS CNV calling
- **Mismatched reference genomes**: Verify BAM uses same reference as CNV caller (hg19 vs hg38)
- **No matched normal for tumors**: Cannot distinguish somatic vs germline without normal
- **Not filtering common CNVs**: Filter against DGV, gnomAD to avoid reporting polymorphisms
- **Ignoring tumor purity**: Low purity samples have attenuated CNV signals

---

## Security Checklist

- [x] No hardcoded credentials or API keys
- [x] Input validation for file paths
- [x] Output directory restricted
- [x] **CRITICAL**: HIPAA compliance required for patient data; `--confirm-hipaa` flag enforced in script

---

## References

- Database of Genomic Variants (DGV): http://dgv.tcag.ca
- gnomAD Structural Variants: https://gnomad.broadinstitute.org
- ClinVar: https://www.ncbi.nlm.nih.gov/clinvar
- COSMIC: https://cancer.sanger.ac.uk
