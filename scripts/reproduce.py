"""
Reproduce every count reported in:
  Hidayat, K., Septiani, M., Chaeruman, U. A., & Rahmadi, I. F.
  "Weaknesses of Massive Open Online Courses from the Participants'
   Perspective: A Systematic Literature Review"

Inputs
  data/raw/Appendix_A_MOOC_Weaknesses.xlsx     (screening + coding of 26 records)
  data/processed/extracted_findings.csv         (46 findings, Tables 2-3)

Outputs (written to data/processed/ and outputs/)
  appendix_A_records.csv     tidy version of Appendix A (26 rows)
  study_theme_matrix.csv     10 included studies x 8 themes (0/1)
  theme_summary.csv          studies / findings / classification per theme
  prisma_counts.csv          numbers for every box of the PRISMA 2020 flow
  figure2_studies_findings.png
  figure1_prisma_flow.png

Run:  python scripts/reproduce.py
The script stops with an error if any number differs from the manuscript.
"""
from pathlib import Path
import sys

import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "Appendix_A_MOOC_Weaknesses.xlsx"
PROC = ROOT / "data" / "processed"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

CRITICAL_THRESHOLD = 4  # a theme is critical if reported by >= 4 independent studies

THEMES = [
    "Lack of interaction",
    "Technical barriers",
    "Inadequate media format",
    "Content too complex",
    "Evaluation weaknesses",
    "Difficult platform navigation",
    "Self-directed learning difficulties",
    "Language barriers",
]

# Values reported in the manuscript (Results section, Figure 1, Figure 2, Tables 2-3)
EXPECTED_THEMES = {
    "Lack of interaction": (7, 13),
    "Technical barriers": (6, 6),
    "Inadequate media format": (4, 9),
    "Content too complex": (4, 7),
    "Evaluation weaknesses": (4, 5),
    "Difficult platform navigation": (3, 3),
    "Self-directed learning difficulties": (2, 2),
    "Language barriers": (1, 1),
}
EXPECTED_PRISMA = {
    "records_identified_scopus": 26,
    "duplicates_removed": 0,
    "records_screened": 26,
    "records_excluded_at_screening": 0,
    "reports_sought_for_retrieval": 26,
    "reports_not_retrieved": 2,
    "reports_assessed_for_eligibility": 24,
    "excluded_review_conceptual_swot": 7,
    "excluded_no_participant_weakness": 6,
    "excluded_retracted": 1,
    "studies_included": 10,
}

# ---------------------------------------------------------------- 1. load
raw = pd.read_excel(RAW, header=3)  # header row is row 4 in the sheet
raw = raw.dropna(subset=["No"]).copy()
raw.columns = [
    "record_no", "author_year", "title", "journal", "research_focus",
    "research_method", "results", "decision", "exclusion_reason", "themes_coded",
]
raw["record_no"] = raw["record_no"].astype(int)
for c in raw.columns[1:]:
    raw[c] = raw[c].astype(str).str.strip()
raw.to_csv(PROC / "appendix_A_records.csv", index=False, encoding="utf-8")


# ---------------------------------------------------------------- 2. PRISMA
def n_reason(key):
    return int(raw["exclusion_reason"].str.contains(key, case=False, regex=False).sum())


not_retrieved = int((raw["decision"] == "Not retrieved").sum())
prisma = {
    "records_identified_scopus": len(raw),
    "duplicates_removed": len(raw) - raw["title"].str.lower().nunique(),
    "records_screened": len(raw),
    "records_excluded_at_screening": 0,
    "reports_sought_for_retrieval": len(raw),
    "reports_not_retrieved": not_retrieved,
    "reports_assessed_for_eligibility": len(raw) - not_retrieved,
    "excluded_review_conceptual_swot": n_reason("Review, meta-analysis"),
    "excluded_no_participant_weakness": n_reason("does not report MOOC weaknesses"),
    "excluded_retracted": n_reason("retracted by the publisher"),
    "studies_included": int((raw["decision"] == "Include").sum()),
}
pd.Series(prisma, name="n").rename_axis("prisma_box").to_csv(PROC / "prisma_counts.csv")

# ---------------------------------------------------------------- 3. themes
inc = raw[raw["decision"] == "Include"].copy()
matrix = pd.DataFrame(0, index=inc["author_year"], columns=THEMES)
for _, row in inc.iterrows():
    for t in [x.strip() for x in row["themes_coded"].split(";")]:
        if t not in THEMES:
            sys.exit(f"Unknown theme '{t}' for {row['author_year']}")
        matrix.loc[row["author_year"], t] = 1
matrix.index.name = "study"
matrix.to_csv(PROC / "study_theme_matrix.csv")

findings = pd.read_csv(PROC / "extracted_findings.csv")
summary = pd.DataFrame({
    "theme": THEMES,
    "n_studies": [int(matrix[t].sum()) for t in THEMES],
    "n_findings": [int((findings["theme"] == t).sum()) for t in THEMES],
})
summary["classification"] = summary["n_studies"].apply(
    lambda n: "critical" if n >= CRITICAL_THRESHOLD else "non-critical")
summary["source_studies"] = [
    "; ".join(matrix.index[matrix[t] == 1]) for t in THEMES]
summary.to_csv(PROC / "theme_summary.csv", index=False)

# ---------------------------------------------------------------- 4. verify
errors = []
for k, v in EXPECTED_PRISMA.items():
    if prisma[k] != v:
        errors.append(f"PRISMA {k}: got {prisma[k]}, manuscript {v}")
for _, r in summary.iterrows():
    exp = EXPECTED_THEMES[r["theme"]]
    if (r["n_studies"], r["n_findings"]) != exp:
        errors.append(f"{r['theme']}: got {r['n_studies']}/{r['n_findings']}, manuscript {exp[0]}/{exp[1]}")

print("PRISMA 2020 counts")
for k, v in prisma.items():
    print(f"  {k:<36}{v:>4}")
print("\nTheme summary")
print(summary[["theme", "n_studies", "n_findings", "classification"]].to_string(index=False))

# ---------------------------------------------------------------- 5. Figure 2
fig, ax = plt.subplots(figsize=(9, 5))
y = range(len(summary))[::-1]
h = 0.38
ax.barh([i + h / 2 for i in y], summary["n_studies"], h, label="Independent studies", color="#2b6cb0")
ax.barh([i - h / 2 for i in y], summary["n_findings"], h, label="Extracted findings", color="#90cdf4")
for i, (s, f) in zip(y, zip(summary["n_studies"], summary["n_findings"])):
    ax.text(s + 0.15, i + h / 2, str(s), va="center", fontsize=9)
    ax.text(f + 0.15, i - h / 2, str(f), va="center", fontsize=9)
ax.set_yticks(list(y))
ax.set_yticklabels(summary["theme"])
ax.axvline(CRITICAL_THRESHOLD, ls="--", lw=1, color="#c53030")
ax.text(CRITICAL_THRESHOLD + 0.1, len(summary) - 0.4, "critical threshold (≥4 studies)",
        color="#c53030", fontsize=8)
ax.set_xlabel("Count")
ax.legend(loc="lower right", frameon=False)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(OUT / "figure2_studies_findings.png", dpi=300)
plt.close(fig)

# ---------------------------------------------------------------- 6. Figure 1
p = prisma
fig, ax = plt.subplots(figsize=(10, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")


def box(x, y, w, hgt, text):
    ax.add_patch(FancyBboxPatch((x, y), w, hgt, boxstyle="round,pad=0.02",
                                fc="white", ec="black", lw=1))
    ax.text(x + w / 2, y + hgt / 2, text, ha="center", va="center", fontsize=9, wrap=True)


def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", lw=1))


box(0.5, 8.4, 4.2, 1.1, f"Records identified from Scopus\n(n = {p['records_identified_scopus']})")
box(5.5, 8.4, 4.0, 1.1, f"Duplicate records removed\n(n = {p['duplicates_removed']})")
box(0.5, 6.6, 4.2, 1.0, f"Records screened\n(n = {p['records_screened']})")
box(5.5, 6.6, 4.0, 1.0, f"Records excluded\n(n = {p['records_excluded_at_screening']})")
box(0.5, 4.8, 4.2, 1.0, f"Reports sought for retrieval\n(n = {p['reports_sought_for_retrieval']})")
box(5.5, 4.8, 4.0, 1.0, f"Reports not retrieved\n(n = {p['reports_not_retrieved']})")
box(0.5, 2.8, 4.2, 1.0, f"Reports assessed for eligibility\n(n = {p['reports_assessed_for_eligibility']})")
box(5.5, 2.3, 4.0, 2.0,
    "Reports excluded (n = {}):\n• Review/conceptual/SWOT, no\n  participant data (n = {})\n"
    "• No participant-perspective\n  weaknesses (n = {})\n• Retracted (n = {})".format(
        p["excluded_review_conceptual_swot"] + p["excluded_no_participant_weakness"] + p["excluded_retracted"],
        p["excluded_review_conceptual_swot"], p["excluded_no_participant_weakness"], p["excluded_retracted"]))
box(0.5, 0.8, 4.2, 1.0, f"Studies included in review\n(n = {p['studies_included']})")
arrow(2.6, 8.4, 2.6, 7.6); arrow(2.6, 6.6, 2.6, 5.8); arrow(2.6, 4.8, 2.6, 3.8); arrow(2.6, 2.8, 2.6, 1.8)
arrow(4.7, 8.95, 5.5, 8.95); arrow(4.7, 7.1, 5.5, 7.1); arrow(4.7, 5.3, 5.5, 5.3); arrow(4.7, 3.3, 5.5, 3.3)
for yy, lab in ((8.95, "Identification"), (5.3, "Screening"), (1.3, "Included")):
    ax.text(0.15, yy, lab, rotation=90, ha="center", va="center", fontsize=9, fontweight="bold")
fig.savefig(OUT / "figure1_prisma_flow.png", dpi=300, bbox_inches="tight")
plt.close(fig)

if errors:
    print("\nMISMATCH WITH MANUSCRIPT:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("\nAll counts match the manuscript. Outputs written to data/processed/ and outputs/.")
