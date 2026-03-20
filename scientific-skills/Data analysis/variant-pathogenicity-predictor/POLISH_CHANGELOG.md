SKILL POLISH CHANGELOG
══════════════════════════════════════════════════════════
Skill           : variant-pathogenicity-predictor
Original Score  : 77 / 100  (Limited Release)
Estimated Score : 90 / 100  (Production Ready)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT — strengthened with verbatim refusal requirement; added "no speculative variant interpretation in refusal responses"
  [QS-2] Progressive Disclosure        : No split needed (138 → 155 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P1: No PII warning for VCF files with patient genomic data — added Data Safety Check to Input Validation section; elevated Data Exposure risk to High in Risk Assessment table with de-identification recommendation
  [MAJOR] F-02 — P1: Conflicting tool predictions not consistently flagged — added explicit CONFLICTING_EVIDENCE flag definition to Returns section: "When ≥2 tools disagree on pathogenicity direction, emit CONFLICTING_EVIDENCE flag listing disagreeing tools"
  [MINOR] F-03 — P2: No clinical genetics review recommendation for conflicting VUS — added to Output Requirements: "when classification is VUS with conflicting evidence, include clinical genetics review recommendation"

Fixes Skipped:
  None

Output saved to: variant-pathogenicity-predictor/SKILL.md
══════════════════════════════════════════════════════════
