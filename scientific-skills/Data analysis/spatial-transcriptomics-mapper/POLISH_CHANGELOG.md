# SKILL POLISH CHANGELOG
══════════════════════════════════════════════════════════
Skill           : spatial-transcriptomics-mapper
Original Score  : 81 / 100  (Limited Release)
Estimated Score : 89 / 100  (Production Ready)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT
  [QS-2] Progressive Disclosure        : No split needed (166 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P1: No platform detection guidance when --platform is missing — Added platform identification guidance to Fallback Template; documented Visium vs Xenium file structure differences
  [MINOR] F-02 — P2: Composability not documented — Added Composability note to Notes section documenting downstream integration points

Fixes Skipped:
  None

Output saved to: spatial-transcriptomics-mapper/SKILL.md
══════════════════════════════════════════════════════════

## Round 2 — v2 Audit Polish
══════════════════════════════════════════════════════════
Skill           : spatial-transcriptomics-mapper
v2 Score        : 84 / 100  (Limited Release)
Estimated Score : 87 / 100  (Limited Release)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : STRENGTHENED — added non-10x platform escape hatch to Input Validation
  [QS-2] Progressive Disclosure        : No split needed (166 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P1: Platform inference not implemented — Added auto-detection step to Workflow Step 2: check for filtered_feature_bc_matrix.h5+spatial/ (Visium) or transcripts.parquet (Xenium) and infer platform automatically
  [MINOR] F-02 — P2: No explicit escape hatch for non-10x spatial platforms — Added Slide-seq/MERFISH/seqFISH redirect to Input Validation section

Fixes Skipped:
  None

Output saved to: spatial-transcriptomics-mapper/SKILL.md (overwritten in place)
══════════════════════════════════════════════════════════
