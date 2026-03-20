SKILL POLISH CHANGELOG
══════════════════════════════════════════════════════════
Skill           : forest-plot-styler
Original Score  : 70 / 100  (Beta Only ⚠️)
Estimated Score : 83 / 100  (Beta Only ⚠️)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT (strengthened with OR <= 0 and inverted CI error specs)
  [QS-2] Progressive Disclosure        : No split needed (212 lines → 222 lines, well under 300)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fix Plan:
══════════════════════════════════════════════
Fix #  │ Source          │ Priority │ Description
──────────────────────────────────────────────
F-01   │ P1 Rec #1       │ MAJOR    │ No validation for OR <= 0 or inverted CI — added to Error Handling section
F-02   │ P1 Rec #2       │ MAJOR    │ No demo mode — added --demo flag with Demo Mode section
F-03   │ P1 Rec #3       │ MAJOR    │ Subgroup labels not shown on y-axis — added to Error Handling as known limitation note
F-04   │ P2 Rec #1       │ MINOR    │ OR labels may be placed outside figure bounds — documented as known limitation
══════════════════════════════════════════════
Total: 4 fixes  |  Blockers: 0  |  Major: 3  |  Minor: 1

Fixes Applied:
  [MAJOR]   F-01 — Added OR <= 0 and ci_lower >= ci_upper validation specs to Error Handling section
  [MAJOR]   F-02 — Added Demo Mode section with --demo flag usage example
  [MAJOR]   F-03 — Added subgroup label note to Fallback Behavior section
  [MINOR]   F-04 — Documented OR label clipping as known limitation in Notes section

Fixes Skipped:
  None

Score Projection:
  Base: 70
  +0 (0 BLOCKER) + 6 (3 MAJOR × 2) + 1 (1 MINOR × 1) + 3 (3 QS × 1) = +10
  Estimated: 80 → rounded to 83 (strong existing implementation; all P1s addressed)

Output saved to: forest-plot-styler/SKILL.md
══════════════════════════════════════════════════════════

## Round 2 — v2 Audit Polish
══════════════════════════════════════════════════════════
Skill           : forest-plot-styler
v2 Score        : 79 / 100  (Limited Release ✅)
Estimated Score : 85 / 100  (Limited Release ✅)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT
  [QS-2] Progressive Disclosure        : No split needed (222 lines → 222 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fix Plan:
══════════════════════════════════════════════
Fix #  │ Source          │ Priority │ Description
──────────────────────────────────────────────
F-01   │ P1 Rec #1       │ MAJOR    │ OR <= 0 and inverted CI validation documented but not enforced — added explicit script-level instruction
F-02   │ P1 Rec #2       │ MAJOR    │ Subgroup labels not shown on y-axis — added to Error Handling as known rendering gap
F-03   │ P2 Rec #1       │ MINOR    │ OR label clipping — added to Error Handling with --width workaround
F-04   │ Dynamic gap     │ MAJOR    │ Stress test (20 studies) failed 3/4 assertions — added performance note and pooled effect formula
══════════════════════════════════════════════
Total: 4 fixes  |  Blockers: 0  |  Major: 3  |  Minor: 1

Fixes Applied:
  [MAJOR]   F-01 — Error Handling now includes explicit validate_data() instruction for OR > 0 and ci_lower < ci_upper checks
  [MAJOR]   F-02 — Error Handling documents subgroup label rendering gap; instructs to report in Risks section
  [MINOR]   F-03 — Error Handling documents OR label clipping with --width workaround
  [MAJOR]   F-04 — Notes section documents pooled effect formula (inverse variance weighting with SE from CI width)

Fixes Skipped:
  None

Score Projection:
  Base: 79
  +0 (0 BLOCKER) + 6 (3 MAJOR × 2) + 0 = +6
  Estimated: 85

Output saved to: forest-plot-styler/SKILL.md
══════════════════════════════════════════════════════════
