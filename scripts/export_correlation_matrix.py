"""Matrices de corrélation de rangs (Spearman) par sexe et plage de tranches d'âge.

Seuls des résultats agrégés sont écrits : aucune ligne individuelle.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from google.cloud import bigquery

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dashboard" / "exports" / "matrice_correlation.csv"
SEUIL_N = 30

BANDES = [
    ("18-29", 18, 29),
    ("30-39", 30, 39),
    ("40-49", 40, 49),
    ("50-59", 50, 59),
    ("60-69", 60, 69),
    ("70+", 70, 200),
]

VARIABLES = {
    "homa_ir": "HOMA-IR",
    "imc": "IMC",
    "tour_taille_cm": "Tour de taille",
    "sedentaire_minutes": "Temps assis",
    "hdl": "HDL",
    "triglycerides": "Triglycérides",
    "ldl": "LDL",
    "cholesterol_total": "Cholestérol total",
    "hba1c": "Hémoglobine glyquée",
    "hemoglobine": "Hémoglobine",
    "ferritine": "Ferritine",
}

SQL = """
select
    b.sexe_code,
    m.age_annees,
    b.homa_ir,
    b.imc,
    m.tour_taille_cm,
    m.sedentaire_minutes,
    b.hdl,
    b.triglycerides,
    b.ldl,
    b.cholesterol_total,
    b.hba1c,
    b.hemoglobine,
    b.ferritine
from `nutrition-homa-nn.nhanes_marts.mart_participants_bilans` as b
inner join `nutrition-homa-nn.nhanes_marts.mart_participants` as m
    on b.participant_id = m.participant_id
where b.motif_exclusion is null
  and b.homa_ir is not null
"""

client = bigquery.Client(project="nutrition-homa-nn", location="EU")
df = client.query(SQL).to_dataframe().rename(columns=VARIABLES)
cols = list(VARIABLES.values())

rows = []
for sexe_code, sexe in [(1, "Homme"), (2, "Femme")]:
    for i, (lab_debut, age_debut, _) in enumerate(BANDES):
        for j in range(i, len(BANDES)):
            lab_fin, _, age_fin = BANDES[j]
            sub = df[
                (df["sexe_code"] == sexe_code)
                & (df["age_annees"] >= age_debut)
                & (df["age_annees"] <= age_fin)
            ][cols].astype(float)
            corr = sub.corr(method="spearman")
            notna = sub.notna().astype(int)
            n_paires = notna.T.dot(notna)
            for x in cols:
                for y in cols:
                    n = int(n_paires.loc[x, y])
                    c = corr.loc[x, y]
                    rows.append(
                        {
                            "sexe": sexe,
                            "bande_debut": lab_debut,
                            "bande_fin": lab_fin,
                            "n_groupe": len(sub),
                            "variable_x": x,
                            "variable_y": y,
                            "correlation": round(float(c), 2) if n >= SEUIL_N and pd.notna(c) else np.nan,
                            "n": n,
                        }
                    )

out = pd.DataFrame(rows)
assert "participant_id" not in out.columns
out.to_csv(OUT, index=False)
print(f"OK {OUT.name} : {len(out)} lignes")