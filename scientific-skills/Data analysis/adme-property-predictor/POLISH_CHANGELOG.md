# SKILL POLISH CHANGELOG
══════════════════════════════════════════════════════════
Skill           : adme-property-predictor
Original Score  : 83 / 100  (Limited Release)
Estimated Score : 90 / 100  (Production Ready)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT
  [QS-2] Progressive Disclosure        : No split needed (194 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P1: References directory listed but absent from bundle — Added note to References section clarifying files are planned; added model accuracy benchmarks inline in Limitations section
  [MAJOR] F-02 — P1: Batch ranking not applied when property subset is requested — Added cross-validation note to Error Handling: if --rank-by specifies a property not in --properties, warn user and request clarification
  [MINOR] F-03 — P2: Adversarial refusal lacks educational explanation — Added explanation to Error Handling: when refusing clinical PK requests, briefly explain computational vs. experimental ADME distinction

Fixes Skipped:
  None

Output saved to: adme-property-predictor/SKILL.md
══════════════════════════════════════════════════════════