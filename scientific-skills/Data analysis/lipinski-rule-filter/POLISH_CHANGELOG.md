SKILL POLISH CHANGELOG
══════════════════════════════════════════════════════════
Skill           : lipinski-rule-filter
Original Score  : 77 / 100  (Limited Release)
Estimated Score : 89 / 100  (Production Ready)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT — strengthened with Ro5 limitations note and ADMET alternative tool suggestions
  [QS-2] Progressive Disclosure        : No split needed (117 → 130 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P1: UnicodeEncodeError on Python 3.6 for status symbols — added note to Error Handling: use ASCII equivalents [PASS]/[FAIL]/[INVALID]; added PYTHONIOENCODING=utf-8 workaround
  [MINOR] F-02 — P2: No contextual note that Ro5 is a guideline, not a complete ADMET predictor — added Limitations section with explicit Ro5 scope note and complementary ADMET tool recommendations (SwissADME, pkCSM, ADMETlab, Schrödinger QikProp)
  [MINOR] F-03 — P2: No example test cases — added aspirin SMILES test to Quick Check section

Fixes Skipped:
  [MINOR] F-04 — P2: No example compound library file — Skipped: adding a bundled examples/ directory is a script-level change outside SKILL.md scope

Output saved to: lipinski-rule-filter/SKILL.md
══════════════════════════════════════════════════════════

## Round 2 — v2 Audit Polish
══════════════════════════════════════════════════════════
Skill           : lipinski-rule-filter
v2 Score        : 81 / 100  (Limited Release ✅)
Estimated Score : 87 / 100  (Limited Release ✅)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : STRENGTHENED — added "Do not generate any output or property calculations before emitting this refusal. Validate scope first — this is the absolute first action before any other processing."
  [QS-2] Progressive Disclosure        : No split needed (129 lines → 129 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fix Plan:
══════════════════════════════════════════════
Fix #  │ Source          │ Priority │ Description
──────────────────────────────────────────────
F-01   │ P1 Rec #1       │ MAJOR    │ Partial ADMET context provided before declining — strengthened Input Validation with absolute-first-action instruction
F-02   │ P2 Rec #1       │ MINOR    │ No bundled example compound library — noted in Quick Check section
F-03   │ QS-1            │ MAJOR    │ Hard gate not fully enforced — reinforced in Workflow Step 1
══════════════════════════════════════════════
Total: 3 fixes  |  Blockers: 0  |  Major: 2  |  Minor: 1

Fixes Applied:
  [MAJOR]   F-01 — Input Validation now states "Do not generate any output or property calculations before emitting this refusal"
  [MINOR]   F-02 — Quick Check aspirin example retained; note added that example SMILES file can be added to examples/ directory
  [MAJOR]   F-03 — Workflow Step 1 added as explicit first step: validate input before any processing

Fixes Skipped:
  None

Score Projection:
  Base: 81
  +0 (0 BLOCKER) + 4 (2 MAJOR × 2) + 1 (1 MINOR × 1) + 1 (QS-1 strengthened) = +6
  Estimated: 87

Output saved to: lipinski-rule-filter/SKILL.md
══════════════════════════════════════════════════════════
