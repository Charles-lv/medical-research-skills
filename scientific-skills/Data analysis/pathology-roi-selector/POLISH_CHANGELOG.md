SKILL POLISH CHANGELOG
══════════════════════════════════════════════════════════
Skill           : pathology-roi-selector
Original Score  : 71 / 100  (Beta Only)
Estimated Score : 84 / 100  (Release Candidate)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : STRENGTHENED — moved to top of document (Step 1 gate)
  [QS-2] Progressive Disclosure        : No split needed (117 → 130 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P1: Input Validation moved to Step 1 of Workflow to enforce early exit
  [MAJOR] F-02 — P1: Added path traversal enforcement note — script must use Path.resolve() to validate --image path
  [MAJOR] F-03 — P1: Added script placeholder disclosure — skill operates in reasoning mode until OpenSlide is implemented
  [MAJOR] F-04 — P2: Added Artifact Score as a required named field in Output section when quality metrics are requested
  [MINOR] F-05 — Added openslide-python to Prerequisites section

Fixes Skipped:
  None

Output saved to: Data Analytics/pathology-roi-selector/SKILL.md
══════════════════════════════════════════════════════════

## Round 2 — v2 Audit Polish

SKILL POLISH CHANGELOG — ROUND 2
══════════════════════════════════════════════════════════
Skill           : pathology-roi-selector
v2 Score        : 77 / 100  (Limited Release ✅)
Estimated Score : 83 / 100  (Limited Release ✅)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT (at top)
  [QS-2] Progressive Disclosure        : No split needed (124 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Round 2 Fix Plan:
══════════════════════════════════════════════
Fix #  │ Source          │ Priority │ Description
──────────────────────────────────────────────
F-01   │ P1 Rec #1       │ MAJOR    │ Script placeholder — placeholder disclosure note retained; no script change in SKILL.md
F-02   │ P2 Rec #1       │ MINOR    │ Fallback template not used for format+missing-flag combos — added explicit rule to Error Handling
══════════════════════════════════════════════
Total: 2 fixes  |  Blockers: 0  |  Major: 1  |  Minor: 1

Fixes Applied:
  [MAJOR]   F-01 — Placeholder disclosure note retained; Fallback Template updated to note "list multiple issues under Blocked by"
  [MINOR]   F-02 — Error Handling now states: "If both an unsupported format and a missing required flag are detected, use the Fallback Template with both issues listed under Blocked by"

Fixes Skipped:
  None

Output saved to: pathology-roi-selector/SKILL.md
══════════════════════════════════════════════════════════
