SKILL POLISH CHANGELOG
══════════════════════════════════════════════════════════
Skill           : sanger-chromatogram-qa
Original Score  : 71 / 100  (Beta Only)
Estimated Score : 84 / 100  (Release Candidate)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : STRENGTHENED — moved to top of document (Step 1 gate)
  [QS-2] Progressive Disclosure        : No split needed (116 → 120 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P1: Input Validation moved to Step 1 of Workflow to enforce early exit before any processing
  [MAJOR] F-02 — P1: Added explicit note that scope check must fire before partial analysis
  [MAJOR] F-03 — P1: Added mixed-peak severity requirement — output must include quantitative estimate or disclose placeholder limitation
  [MINOR] F-04 — P2: Added alternative tool suggestion (FastQC, variant calling pipeline) to out-of-scope refusal message
  [MINOR] F-05 — Human usability: improved natural trigger language in description

Fixes Skipped:
  None

Output saved to: Data Analytics/sanger-chromatogram-qa/SKILL.md
══════════════════════════════════════════════════════════

## Round 2 — v2 Audit Polish

SKILL POLISH CHANGELOG — ROUND 2
══════════════════════════════════════════════════════════
Skill           : sanger-chromatogram-qa
v2 Score        : 76 / 100  (Limited Release ✅)
Estimated Score : 82 / 100  (Limited Release ✅)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT (at Step 1)
  [QS-2] Progressive Disclosure        : No split needed (118 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Round 2 Fix Plan:
══════════════════════════════════════════════
Fix #  │ Source          │ Priority │ Description
──────────────────────────────────────────────
F-01   │ P1 Rec #1       │ MAJOR    │ Mixed-peak detection is placeholder returning 0 — added BioPython implementation spec to Returns section
F-02   │ P2 Rec #1       │ MINOR    │ No path traversal check for --ab1 — added to Error Handling and Returns section
══════════════════════════════════════════════
Total: 2 fixes  |  Blockers: 0  |  Major: 1  |  Minor: 1

Fixes Applied:
  [MAJOR]   F-01 — Returns section now specifies: quantitative severity = secondary peak height / primary peak height (0-1 scale); BioPython implementation path documented (Bio.SeqIO.read 'abi' format, 25% threshold); placeholder disclosure retained
  [MINOR]   F-02 — Error Handling now includes: if --ab1 path contains ../ or resolves outside workspace, reject with path traversal warning and exit code 1

Fixes Skipped:
  None

Output saved to: sanger-chromatogram-qa/SKILL.md
══════════════════════════════════════════════════════════
