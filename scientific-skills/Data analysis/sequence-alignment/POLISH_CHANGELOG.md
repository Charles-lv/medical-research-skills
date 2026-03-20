# SKILL POLISH CHANGELOG
══════════════════════════════════════════════════════════
Skill           : sequence-alignment
Original Score  : 80 / 100  (Limited Release)
Estimated Score : 88 / 100  (Production Ready)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT (strengthened with MSA tool redirect)
  [QS-2] Progressive Disclosure        : No split needed (154 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P1: Scope check fires after partial analysis on MSA requests — Moved Input Validation to Step 1 of Workflow; added explicit pre-flight check before any processing
  [MAJOR] F-02 — P1: Type annotation issues in XML parsing (str|None) — Documented None guard pattern in Input Validation note; fix guidance added for int(hit_len.text or 0) pattern
  [MINOR] F-03 — P2: No specific alternative tool suggested on MSA refusal — Added MUSCLE, CLUSTALW, MAFFT to the out-of-scope response template

Fixes Skipped:
  None

Output saved to: sequence-alignment/SKILL.md
══════════════════════════════════════════════════════════

## Round 2 — v2 Audit Polish
══════════════════════════════════════════════════════════
Skill           : sequence-alignment
v2 Score        : 84 / 100  (Limited Release)
Estimated Score : 87 / 100  (Limited Release)

Quality Standards Applied:
  [QS-1] Instruction Pollution Defense : ALREADY PRESENT
  [QS-2] Progressive Disclosure        : No split needed (154 lines)
  [QS-3] Canonical YAML Frontmatter   : ALREADY CORRECT

Fixes Applied:
  [MAJOR] F-01 — P1: XML None guards documented but not yet applied in script code — Reinforced Input Validation note that None guards must be applied in parse_blast_xml (int(hit_len.text or 0), float(bit_score.text or 0) pattern)
  [MINOR] F-02 — P2: No explicit escape hatch for phylogenetic tree requests — Added phylogenetic tree redirect to out-of-scope response: "For phylogenetic tree construction, consider phylogenetic-tree-styler or IQ-TREE"

Fixes Skipped:
  None

Output saved to: sequence-alignment/SKILL.md (overwritten in place)
══════════════════════════════════════════════════════════

## Round 3 — Script Fix

══════════════════════════════════════════════════════════
Skill           : sequence-alignment
v3 Score        : 84 / 100  (Limited Release)
Estimated Score : 87 / 100  (Limited Release)

Script fixes applied to scripts/main.py:
  [P0] Added None guards to ALL XML text extractions in parse_blast_xml():
       - hit_len: int(hit_len.text or "0")
       - bit_score: float(bit_score.text or "0.0")
       - score, identity, positive, gaps, align_len: int(x.text or "0")
       - evalue: float(evalue.text or "0.0")
       - query_from, query_to, hit_from, hit_to: int(x.text or "0")
  No other logic changed.

Output saved to: sequence-alignment/scripts/main.py (overwritten in place)
══════════════════════════════════════════════════════════
