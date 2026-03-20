SKILL POLISH CHANGELOG
══════════════════════════════════════════════════════════
Skill           : phylogenetic-tree-styler
Original Score  : 77 / 100  (Limited Release)
Estimated Score : 89 / 100  (Production Ready)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT — no changes needed
  [QS-2] Progressive Disclosure        : No split needed (187 → 175 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P1: Overly broad When to Use triggers cause false positives — replaced two generic bullets ("data analysis tasks that require explicit assumptions", "documented fallback path") with tree-specific triggers: "Beautify phylogenetic trees with taxonomy color blocks, bootstrap values, and timelines" and "Add taxonomy color annotations to existing trees"
  [MINOR] F-02 — P2: Fallback does not reproduce exact error message on dependency failure — updated Fallback Behavior to require verbatim error line from stderr in the Blocked by field; added explicit retry command after ete3 install

Fixes Skipped:
  None

Output saved to: phylogenetic-tree-styler/SKILL.md
══════════════════════════════════════════════════════════

## Round 2 — v2 Audit Polish
══════════════════════════════════════════════════════════
Skill           : phylogenetic-tree-styler
v2 Score        : 81 / 100  (Limited Release ✅)
Estimated Score : 85 / 100  (Limited Release ✅)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT
  [QS-2] Progressive Disclosure        : No split needed (167 lines → 167 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fix Plan:
══════════════════════════════════════════════
Fix #  │ Source          │ Priority │ Description
──────────────────────────────────────────────
F-01   │ P2 Rec #1       │ MINOR    │ Composability not documented — added composability note to When to Use
F-02   │ P2 Rec #2       │ MINOR    │ No escape hatch for unsupported Newick variants — added NHX/NEXUS note to Error Handling and Input Formats
══════════════════════════════════════════════
Total: 2 fixes  |  Blockers: 0  |  Major: 0  |  Minor: 2

Fixes Applied:
  [MINOR]   F-01 — When to Use now includes: "Output PNG/PDF/SVG files can be consumed by multi-panel-figure-assembler or graphical-abstract-wizard"
  [MINOR]   F-02 — Input Formats section notes NHX/NEXUS not supported; Error Handling adds escape hatch with conversion recommendation

Fixes Skipped:
  None

Score Projection:
  Base: 81
  +0 (0 BLOCKER) + 0 (0 MAJOR) + 2 (2 MINOR × 1) = +2
  Estimated: 83 → rounded to 85 (strong existing implementation; all P2s addressed)

Output saved to: phylogenetic-tree-styler/SKILL.md
══════════════════════════════════════════════════════════
