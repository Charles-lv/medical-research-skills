# Neoantigen Predictor References

## Core Algorithm Papers

### NetMHCpan 4.1
- **Title**: NetMHCpan-4.1 and NetMHCIIpan-4.0: improved predictions of MHC antigen presentation by concurrent motif deconvolution and integration of MS MHC eluted ligand data
- **Authors**: Reynisson et al.
- **Journal**: Nucleic Acids Research
- **Year**: 2020
- **Link**: https://doi.org/10.1093/nar/gkaa379

### Neoantigen Prediction Review
- **Title**: Neoantigen prediction: perspectives on the present and future
- **Authors**: Wells et al.
- **Journal**: Nature Cancer
- **Year**: 2022
- **Abstract**: Systematic evaluation of computational methods and experimental validation strategies for neoantigen prediction

### Immunopeptidomics
- **Title**: The immunopeptidomics landscape of cancer: implications for immunotherapy
- **Authors**: Abelin et al.
- **Journal**: Immunity
- **Year**: 2019

## HLA Binding Motif References

### MHC-I Binding Motif Database
- **Source**: IEDB (Immune Epitope Database)
- **URL**: http://www.iedb.org/
- **Content**: Validated HLA-peptide binding data

### HLA Frequency Database
- **Source**: Allele Frequency Net Database
- **URL**: http://www.allelefrequencies.net/
- **Purpose**: Population HLA allele frequency data

## Tumor Immunotherapy Clinical Guidelines

### Neoantigen Vaccine Clinical Trial Design
- **Document**: NCI Neoantigen Guidance
- **Content**: Design principles and endpoint metrics for neoantigen vaccine clinical trials

### Immunotherapy Biomarkers
- **Title**: Biomarkers for Immunotherapy in Cancer
- **Organization**: FDA Guidance Document

## Related Databases

| Database | Purpose | Link |
|----------|---------|------|
| **Ensembl** | Genome annotation | https://www.ensembl.org/ |
| **UniProt** | Protein sequences | https://www.uniprot.org/ |
| **ClinVar** | Clinical variants | https://www.ncbi.nlm.nih.gov/clinvar/ |
| **COSMIC** | Tumor mutations | https://cancer.sanger.ac.uk/ |
| **TCGA** | Tumor genomics | https://portal.gdc.cancer.gov/ |
| **IMGT/HLA** | HLA sequences | https://www.ebi.ac.uk/ipd/imgt/hla/ |

## Amino Acid Properties Table

### Hydrophobicity Scale (Kyte-Doolittle)

| Amino Acid | Single Letter | Hydrophobicity Value |
|------------|---------------|----------------------|
| Isoleucine | I | 4.5 |
| Valine | V | 4.2 |
| Leucine | L | 3.8 |
| Phenylalanine | F | 2.8 |
| Cysteine | C | 2.5 |
| Methionine | M | 1.9 |
| Alanine | A | 1.8 |
| Glycine | G | -0.4 |
| Threonine | T | -0.7 |
| Serine | S | -0.8 |
| Tryptophan | W | -0.9 |
| Tyrosine | Y | -1.3 |
| Proline | P | -1.6 |
| Histidine | H | -3.2 |
| Glutamic Acid | E | -3.5 |
| Glutamine | Q | -3.5 |
| Aspartic Acid | D | -3.5 |
| Asparagine | N | -3.5 |
| Lysine | K | -3.9 |
| Arginine | R | -4.5 |

### Amino Acid Molecular Weight

| Amino Acid | Single Letter | Molecular Weight (Da) |
|------------|---------------|-----------------------|
| Alanine | A | 89.09 |
| Arginine | R | 174.20 |
| Asparagine | N | 132.12 |
| Aspartic Acid | D | 133.10 |
| Cysteine | C | 121.16 |
| Glutamic Acid | E | 147.13 |
| Glutamine | Q | 146.15 |
| Glycine | G | 75.07 |
| Histidine | H | 155.16 |
| Isoleucine | I | 131.17 |
| Leucine | L | 131.17 |
| Lysine | K | 146.19 |
| Methionine | M | 149.21 |
| Phenylalanine | F | 165.19 |
| Proline | P | 115.13 |
| Serine | S | 105.09 |
| Threonine | T | 119.12 |
| Tryptophan | W | 204.23 |
| Tyrosine | Y | 181.19 |
| Valine | V | 117.15 |

## Neoantigen Prediction Best Practices

### Quality Control Standards

1. **MHC Binding Affinity**
   - Strong binder: Rank < 0.5% or IC50 < 50 nM
   - Weak binder: Rank 0.5-2% or IC50 50-500 nM
   - Non-binder: Rank > 2% or IC50 > 500 nM

2. **Immunogenicity Assessment**
   - Foreignness score > 0.5
   - Anchor position mutations preferred
   - Hydrophobicity change |ΔH| > 0.3

3. **Clinical Relevance**
   - VAF > 5% (variant allele frequency)
   - Expression level: FPKM > 1
   - Clonal variants preferred

### Experimental Validation Workflow

1. **In Vitro Validation**
   - Peptide synthesis (variant peptide and wildtype control)
   - MHC binding assay (competitive binding assay)
   - T cell activation assay (ELISPOT)

2. **In Vivo Validation**
   - Humanized mouse model
   - TCR recognition validation
   - Cytotoxicity assay

3. **Clinical Application**
   - Personalized neoantigen vaccine design
   - TCR-T cell therapy target selection
   - Immunotherapy response prediction

## Tools and Software

### MHC Prediction Tools
- **NetMHCpan 4.1**: https://services.healthtech.dtu.dk/services/NetMHCpan-4.1/
- **MHCflurry**: https://github.com/openvax/mhcflurry
- **MixMHCpred**: http://mixmhcpred.deeplife/recipes/MixMHCpred

### Sequence Analysis Tools
- **Biopython**: https://biopython.org/
- **pysam**: https://pysam.readthedocs.io/
- **pyvcf**: https://pyvcf.readthedocs.io/

### Visualization Tools
- **matplotlib**: Python plotting library
- **seaborn**: Statistical data visualization
- **logomaker**: Sequence logo generation

## Glossary

| Term | Definition |
|------|-----------|
| Neoantigen | Antigen generated by tumor-specific mutations |
| HLA | Human Leukocyte Antigen, i.e. MHC molecule |
| MHC | Major Histocompatibility Complex |
| VAF | Variant Allele Frequency |
| TCR | T Cell Receptor |
| IC50 | Half-maximal inhibitory concentration |
| VUS | Variant of Uncertain Significance |
| VCF | Variant Call Format |
| FPKM | Fragments Per Kilobase Million |
