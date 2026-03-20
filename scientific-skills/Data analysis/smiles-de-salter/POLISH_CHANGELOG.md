# SKILL POLISH CHANGELOG
══════════════════════════════════════════════════════════
Skill           : smiles-de-salter
Original Score  : 82 / 100  (Limited Release)
Estimated Score : 88 / 100  (Production Ready)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT (strengthened with ADMET redirect)
  [QS-2] Progressive Disclosure        : No split needed (155 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P2: No specific ADMET tool suggested on out-of-scope refusal — Added SwissADME, pkCSM, ADMETlab to the out-of-scope response template
  [MINOR] F-02 — P2: --keep-largest bool parsing fragile with string 'false' — Documented the argparse bool limitation in Notes section; added guidance to use True/False explicitly

Fixes Skipped:
  None

Output saved to: smiles-de-salter/SKILL.md
══════════════════════════════════════════════════════════
## Round 2 — v2 Audit Polish
══════════════════════════════════════════════════════════
Skill           : smiles-de-salter
v2 Score        : 84 / 100  (Limited Release)
Estimated Score : 87 / 100  (Limited Release)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT
  [QS-2] Progressive Disclosure        : No split needed (155 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P1: --keep-largest bool parsing fragile with string 'false' — Updated Notes to state script must use lambda x: x.lower() == 'true' as argparse type (not type=bool) to fix the non-empty-string-is-truthy bug
  [MINOR] F-02 — P2: No path traversal check for --input file path — Added path traversal rejection rule to Error Handling for the --input batch file path

Fixes Skipped:
  None

Output saved to: smiles-de-salter/SKILL.md (overwritten in place)
══════════════════════════════════════════════════════════
