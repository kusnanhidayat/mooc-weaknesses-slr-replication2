# Replication Package — Weaknesses of MOOCs from the Participants' Perspective: A Systematic Literature Review

Kusnan Hidayat, Mita Septiani, Uwes Anis Chaeruman, Imam Fitri Rahmadi
Universitas Negeri Jakarta, Indonesia
Corresponding author: Kusnan Hidayat — kusnan_1110824029@mhs.unj.ac.id

This repository contains all data, coding decisions, and code needed to reproduce the
study selection (PRISMA 2020 flow), the thematic counts, the critical/non-critical
classification, Figure 1, Figure 2, and Tables 2–3 of the article.

## Contents

```
.
├── README.md
├── CITATION.cff
├── LICENSE                       CC BY 4.0 (data, docs) + MIT (code)
├── requirements.txt
├── data/
│   ├── raw/
│   │   └── Appendix_A_MOOC_Weaknesses.xlsx   Appendix A as submitted (26 records)
│   └── processed/
│       ├── appendix_A_records.csv            tidy CSV of Appendix A (generated)
│       ├── extracted_findings.csv            46 extracted findings (Tables 2–3)
│       ├── study_theme_matrix.csv            10 studies × 8 themes, 0/1 (generated)
│       ├── theme_summary.csv                 studies, findings, classification (generated)
│       ├── prisma_counts.csv                 counts for each PRISMA box (generated)
│       └── gagne_mapping.csv                 theme → Gagné's Nine Events (Discussion)
├── docs/
│   ├── search_strategy.md                    Scopus query, filters, date, results
│   ├── eligibility_criteria.md               Table 1 inclusion/exclusion criteria
│   └── codebook.md                           theme definitions and decision rules
├── scripts/
│   └── reproduce.py                          rebuilds every number and figure
└── outputs/
    ├── figure1_prisma_flow.png
    └── figure2_studies_findings.png
```

## How to reproduce

Requires Python 3.9+.

```bash
pip install -r requirements.txt
python scripts/reproduce.py
```

The script reads `data/raw/Appendix_A_MOOC_Weaknesses.xlsx` and
`data/processed/extracted_findings.csv`, regenerates all files marked *generated*
above, and checks every count against the values reported in the manuscript.
It exits with an error if any count differs.

Expected output:

| PRISMA 2020 stage | n |
|---|---|
| Records identified (Scopus) | 26 |
| Duplicates removed | 0 |
| Records screened / excluded | 26 / 0 |
| Reports sought / not retrieved | 26 / 2 |
| Reports assessed for eligibility | 24 |
| Excluded: review, conceptual, SWOT, no participant data | 7 |
| Excluded: no participant-perspective weaknesses | 6 |
| Excluded: retracted | 1 |
| **Studies included** | **10** |

| Theme | Studies | Findings | Classification |
|---|---|---|---|
| Lack of interaction | 7 | 13 | critical |
| Technical barriers | 6 | 6 | critical |
| Inadequate media format | 4 | 9 | critical |
| Content too complex | 4 | 7 | critical |
| Evaluation weaknesses | 4 | 5 | critical |
| Difficult platform navigation | 3 | 3 | non-critical |
| Self-directed learning difficulties | 2 | 2 | non-critical |
| Language barriers | 1 | 1 | non-critical |

A theme is **critical** when reported by ≥ 4 of the 10 included studies
(number of independent studies, not number of findings).

## Re-running the search

The exact Scopus query, filters, and search date (4 May 2026) are in
[`docs/search_strategy.md`](docs/search_strategy.md). Scopus is a subscription
database and its index changes over time, so a re-run may return a different
number of records; the 26 records screened in this review are listed in full in
Appendix A.

## Notes on the data

- All data are bibliographic metadata and summaries of published articles. No
  personal data from human participants were collected for this review.
- Full texts of the included articles are not redistributed because of
  publisher copyright; they can be obtained from the publishers via the
  journal details in Appendix A.

## License

Data and documentation: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Code (`scripts/`): MIT. See `LICENSE`.

## How to cite

Please cite the article and this repository (see `CITATION.cff`).
