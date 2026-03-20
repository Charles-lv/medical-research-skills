---
SKILL POLISH CHANGELOG
══════════════════════════════════════════════════════════
Skill           : pseudotime-trajectory-viz
Original Score  : 80.6 / 100  (Limited Release)
Estimated Score : 91 / 100  (Production Ready)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : STRENGTHENED — refusal template now names specific out-of-scope examples (bulk RNA-seq, differential expression, non-AnnData inputs)
  [QS-2] Progressive Disclosure        : SPLIT — original was 347 lines (exceeds 300-line limit); removed bulky boilerplate sections; polished version is 178 lines. Retained all scientifically essential content (methods, limitations, safety practices).
  [QS-3] Canonical YAML Frontmatter   : NORMALIZED — description rewritten to be specific and ≤280 chars

Fixes Applied:
  [MAJOR] F-01 — P1: Stabilize executable path and fallback behavior — Added explicit Fallback Template section with structured FALLBACK REPORT block including assumptions, constraints, risks, and unresolved items
  [MAJOR] F-02 — P2: Improve stress-case output rigor — Fallback Template mandates assumptions, constraints, risks, and unresolved items sections for complex requests
  [MAJOR] F-03 — Static gap: human_usability score 6/13 — Simplified parameter table (removed rarely-used params); added clear input format specification; improved output file tree
  [MAJOR] F-04 — Audit-Ready Commands contained invalid --format flag — Removed `--format json` from audit commands (script does not support this flag per returncode=2 in input #4); corrected to valid commands only
  [MAJOR] F-05 — When to Use contained self-referential boilerplate — Replaced with concrete domain-specific use-case bullets
  [MINOR] F-06 — Input Validation refusal template was too vague — Strengthened with named out-of-scope examples
  [MINOR] F-07 — Security: path traversal not explicitly called out — Added `../` rejection note in Error Handling
  [MINOR] F-08 — Error handling: missing AnnData obs keys not addressed — Added explicit stop condition for missing leiden/cell_type keys
  [MINOR] F-09 — Removed bulky boilerplate sections (347→178 lines): Lifecycle Status, Evaluation Criteria, Security Checklist, Version block, full Methods subsections, Example Workflow code block, References list — content preserved in spirit via Limitations and Safety sections

Fixes Skipped:
  [MINOR] Slingshot/Palantir method details — Reason: removed to meet QS-2 line limit; core methods (diffusion, paga) retained in parameters table

Output saved to: pseudotime-trajectory-viz_polished/SKILL.md
══════════════════════════════════════════════════════════

## Round 2 — v2 Audit Polish
══════════════════════════════════════════════════════════
Skill           : pseudotime-trajectory-viz
v2 Score        : 83 / 100  (Limited Release)
Estimated Score : 87 / 100  (Limited Release)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT
  [QS-2] Progressive Disclosure        : No split needed (159 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P1: PAGA pseudotime adds random noise without fixed seed in script — Added explicit note to Limitations that script must call np.random.seed(args.seed) before noise addition; seed recorded in analysis_report.json
  [MINOR] F-02 — P2: Corrected safe path guidance not provided on traversal rejection — Updated Error Handling to provide explicit corrected safe path example (/workspace/data/sample.h5ad)

Fixes Skipped:
  None

Output saved to: pseudotime-trajectory-viz/SKILL.md (overwritten in place)
══════════════════════════════════════════════════════════
