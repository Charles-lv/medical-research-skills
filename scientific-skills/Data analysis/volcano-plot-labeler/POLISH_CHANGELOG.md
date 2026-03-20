SKILL POLISH CHANGELOG
══════════════════════════════════════════════════════════
Skill           : volcano-plot-labeler
Original Score  : 78 / 100  (Limited Release)
Estimated Score : 84 / 100  (Limited Release)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT
  [QS-2] Progressive Disclosure        : No split needed (154 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — Insufficient significant genes for top-N not warned: Added explicit error handling rule: "If significant genes < top-N, emit a note: 'Only [k] genes meet significance thresholds; labeling [k] instead of requested [N].'"
  [MINOR] F-02 — No audit-ready commands with concrete DEG data: Added Audit-Ready Commands section with data-driven test command using deseq2_results.csv.
  [MINOR] F-03 — Parameter overrides not noted in assumptions block: Added requirement in Output Requirements and Response Template to always list all non-default parameter values applied in Assumptions section.

Fixes Skipped:
  None

Output saved to: volcano-plot-labeler/SKILL.md (overwritten in place)
══════════════════════════════════════════════════════════

## Round 2 — v2 Audit Polish
══════════════════════════════════════════════════════════
Skill           : volcano-plot-labeler
v2 Score        : 84 / 100  (Limited Release)
Estimated Score : 87 / 100  (Limited Release)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT
  [QS-2] Progressive Disclosure        : No split needed (154 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MINOR] F-01 — P2: CSV column name injection not addressed — Added column name validation rule to Error Handling: validate --log2fc-col, --pvalue-col, --gene-col contain only alphanumeric characters, underscores, and hyphens before passing to script
  [MINOR] F-02 — P2: No custom gene list labeling documented — Skipped (no --gene-list parameter exists in current script; adding it would require script changes outside SKILL.md scope)

Fixes Skipped:
  [MINOR] F-02 — P2: No custom gene list labeling documented — Reason: requires script implementation; SKILL.md cannot document a parameter that does not exist

Output saved to: volcano-plot-labeler/SKILL.md (overwritten in place)
══════════════════════════════════════════════════════════
