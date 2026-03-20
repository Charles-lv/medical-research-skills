SKILL POLISH CHANGELOG
══════════════════════════════════════════════════════════
Skill           : metagenomic-krona-chart
Original Score  : 77 / 100  (Limited Release)
Estimated Score : 89 / 100  (Production Ready)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT — strengthened with verbatim redirect message requirement; added "no partial processing" instruction; added Kraken2/Bracken suggestion
  [QS-2] Progressive Disclosure        : No split needed (160 → 155 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P1: Out-of-scope redirect not consistently applied — added "Do not attempt any partial taxonomy lookup or processing before emitting this refusal" instruction; added verbatim redirect message requirement; added Kraken2/Bracken first-step suggestion; moved validation to Step 1 of workflow
  [MINOR] F-02 — P2: Input file path not validated against path traversal — added path traversal check to Workflow (Step 3) and Error Handling section
  [MINOR] F-03 — P2: No multi-sample comparison mode documented — added Limitations note about single-sample scope

Fixes Skipped:
  None

Output saved to: metagenomic-krona-chart/SKILL.md
══════════════════════════════════════════════════════════

## Round 2 — v2 Audit Polish
══════════════════════════════════════════════════════════
Skill           : metagenomic-krona-chart
v2 Score        : 83 / 100  (Limited Release)
Estimated Score : 86 / 100  (Limited Release)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : STRENGTHENED — upgraded "Do not attempt" to absolute-first-action mandate with explicit no-output-before-refusal instruction
  [QS-2] Progressive Disclosure        : No split needed (143 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P1: Minor processing still occurs before out-of-scope refusal — Upgraded Input Validation to state refusal must fire as absolute first action before any taxonomy lookup, context processing, or partial analysis
  [MINOR] F-02 — P2: Path traversal check documented but not verified in script — Reinforced Error Handling note that script must reject ../ paths before opening input file

Fixes Skipped:
  None

Output saved to: metagenomic-krona-chart/SKILL.md (overwritten in place)
══════════════════════════════════════════════════════════
