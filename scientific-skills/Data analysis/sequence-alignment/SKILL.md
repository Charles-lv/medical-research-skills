---
name: sequence-alignment
description: Perform sequence alignment via NCBI BLAST API supporting blastn, blastp, blastx, tblastn, and tblastx against major biological databases.
license: MIT
skill-author: AIPOCH
---
# Sequence Alignment

Perform nucleotide and protein sequence alignment using the NCBI BLAST API against major biological databases (nr, nt, swissprot, refseq, pdb).

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## When to Use

- DNA sequence similarity search (blastn vs nt/nr)
- Protein sequence alignment (blastp vs swissprot/refseq_protein)
- Translated DNA vs protein database (blastx)
- Protein vs translated nucleotide database (tblastn)
- Identify homologs, orthologs, or conserved domains

## Input Validation

This skill accepts: DNA or protein sequences with a specified BLAST program and target database for sequence similarity search via NCBI BLAST API.

If the request does not involve sequence alignment — for example, asking to perform multiple sequence alignment (MSA), phylogenetic tree construction, or genome assembly — do not proceed. Instead respond:

> "sequence-alignment is designed to perform pairwise sequence similarity search via NCBI BLAST. Your request appears to be outside this scope. Please provide a query sequence, BLAST program, and target database, or use a more appropriate tool for your task. For multiple sequence alignment, consider MUSCLE, CLUSTALW, or MAFFT. For phylogenetic tree construction, consider phylogenetic-tree-styler or IQ-TREE."

**Note on XML parsing:** The script uses None guards for XML element `.text` attributes (`int(hit_len.text or 0)`, `float(bit_score.text or 0)`) to prevent TypeErrors on malformed BLAST XML.

## Usage

```bash
python scripts/main.py \
  --sequence "ATGCGTACGTAGCTAGCTAG" \
  --program blastn \
  --database nt \
  --output results.txt
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--sequence` | Yes | — | Query sequence (DNA or protein) |
| `--program` | Yes | — | blastn, blastp, blastx, tblastn, tblastx |
| `--database` | Yes | — | nr, nt, swissprot, pdb, refseq_protein |
| `--output` | No | stdout | Output file path |
| `--format` | No | text | text, json, csv |
| `--max-hits` | No | 10 | Maximum hits to return |
| `--evalue` | No | 10 | E-value threshold |

## BLAST Program Reference

| Program | Query | Database | Use Case |
|---------|-------|----------|----------|
| blastn | Nucleotide | Nucleotide | DNA vs DNA |
| blastp | Protein | Protein | Protein vs Protein |
| blastx | Nucleotide (translated) | Protein | DNA vs Protein |
| tblastn | Protein | Nucleotide (translated) | Protein vs DNA |
| tblastx | Nucleotide (translated) | Nucleotide (translated) | Translated DNA vs DNA |

## Workflow

1. **Validate input first:** Confirm the request is within scope (pairwise BLAST alignment only). If MSA, phylogenetics, or genome assembly is requested, emit the scope refusal before any processing.
2. Confirm objective, required inputs, and constraints before proceeding.
3. Run `scripts/main.py` with available inputs, or use the documented reasoning path.
4. Return structured result separating assumptions, deliverables, risks, and unresolved items.
5. On execution failure or incomplete inputs, switch to fallback path and state exactly what blocked completion.

## Fallback Template

If `scripts/main.py` cannot run (network unavailable, missing inputs), respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective      : <stated goal>
Blocked by     : <exact missing input or error>
Partial result : <what can still be assessed manually>
Next step      : <minimum action to unblock>
───────────────────────────────────────
```

## Output Format

Results include:
- Query sequence info and search parameters
- Hit definitions and accession numbers
- Alignment scores (bit score, e-value)
- Percent identity and similarity
- Alignment visualization with match/mismatch highlighting

## Output Requirements

Every response must make these explicit when relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what can still be completed safely, and provide the manual fallback above.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Response Template

Use this fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

For simple requests, compress the structure but keep assumptions and limits explicit when they affect correctness.

## Risk Assessment

| Risk Indicator | Assessment | Level |
|----------------|------------|-------|
| Code Execution | Python scripts with NCBI API calls | High |
| Network Access | External NCBI BLAST API (HTTPS only) | High |
| File System Access | Read sequence input, write results | Medium |
| Data Exposure | Results saved to workspace | Medium |

## Security Notes

- All API requests use HTTPS only
- Input sequences validated against allowed character patterns
- API timeout and retry mechanisms implemented
- No internal service architecture exposed in error messages

## References

- [BLAST Documentation](references/blast_docs.md)
- [NCBI BLAST API Guide](references/ncbi_api_guide.md)

## Prerequisites

No additional Python packages required beyond standard library.
