# Codebook

## Extraction rule

A finding was extracted as a **MOOC weakness** only when it described a problem
encountered by learners (e.g., unstable connectivity, unresponsive forums,
quizzes giving little diagnostic feedback). Limitations that the primary
authors attributed to their own research design (small samples, low response
rates, too few test items for statistical analysis) were recorded separately
and not counted, unless the same issue was also a problem for learners.

The first author extracted and coded all ten studies; the second author
independently re-extracted and re-coded them; discrepancies were resolved by
discussion, with the third author consulted when needed.

## Themes (generated inductively, Braun & Clarke, 2006)

| Theme | Definition |
|---|---|
| Content too complex | Content depth, length, or disciplinary register exceeds participants' prior knowledge or stated prerequisites, or fails to match their professional needs |
| Lack of interaction | Insufficient, slow, or monologic interaction among participants and with instructors/experts; isolation; limited feedback dialogue |
| Technical barriers | Connectivity, hardware, electricity, or implementation problems that impede access |
| Inadequate media format | Media type, length, or production quality unsuited to the content or to participants' context of use |
| Evaluation weaknesses | Assessments too few, misaligned, "tricky", or surface-level, providing little diagnostic feedback |
| Difficult platform navigation | Interface or forum structure that is hard to navigate or to monitor progress in |
| Language barriers | Language of instruction not the participants' own |
| Self-directed learning difficulties | Participants struggle to self-regulate (time management, self-evaluation) without scaffolding |

## Counting and classification

- `n_studies`: number of included studies coded with the theme (column
  `themes_coded` in Appendix A).
- `n_findings`: number of individual findings in `extracted_findings.csv`
  assigned to the theme (one study may contribute several findings).
- **Critical** = reported by ≥ 4 independent studies; **non-critical** = ≤ 3.
  Studies, not findings, are the criterion so that one detailed study cannot
  inflate a theme.
- Evidence from studies outside a theme's source set that is cited in the
  narrative for context is **not** counted toward the theme.

## Gagné mapping

After inductive theme generation, each theme was mapped deductively onto the
event(s) of Gagné's Nine Events of Instruction whose function it most directly
compromises (`data/processed/gagne_mapping.csv`). Mapping by the first author,
reviewed by the third author, finalized by consensus. It is an interpretive
layer, not part of the primary synthesis.
