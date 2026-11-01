from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path(__file__).parent.parent / "exports"

st.title("HOMA-IR et mesures de laboratoire")
st.warning(
    "Projet de qualité de données. Résultats descriptifs sur cet échantillon, "
    "sans lien de cause, sans conclusion clinique et sans conseil de santé."
)
st.info(
    "Contrôle de cohérence de l'indicateur : on compare le HOMA-IR médian entre "
    "quartiles de chaque mesure, séparément chez les hommes et les femmes. Aucun "
    "seuil médical n'est utilisé. L'hémoglobine glyquée et le HOMA-IR reposent "
    "tous deux sur la glycémie : leur lien est en partie attendu."
)

labo = pd.read_csv(DATA / "homa_par_mesures_labo.csv")
mesure = st.selectbox("Mesure", sorted(labo["mesure"].unique()))
d = labo[labo["mesure"] == mesure].copy()
d["quartile"] = "Q" + d["quartile"].astype(str)
fig = px.bar(
    d, x="quartile", y="homa_mediane", color="groupe_sexe",
    barmode="group", text="n",
    hover_data=["valeur_min", "valeur_max"],
)
fig.update_layout(xaxis_title=None, yaxis_title="HOMA-IR (médiane)")
st.plotly_chart(fig)
st.caption("Le nombre de participants est affiché sur chaque barre.")
st.dataframe(
    d[["groupe_sexe", "quartile", "n", "valeur_min", "valeur_max", "homa_mediane"]],
    hide_index=True,
)

st.subheader("Robustesse des règles de qualité")
st.caption(
    "HOMA-IR médian selon la durée de jeûne minimale exigée (0 h = aucun minimum, "
    "toujours moins de 24 h). Les médianes changent peu ; les effectifs changent beaucoup."
)
sens = pd.read_csv(DATA / "sensibilite_jeune.csv")
sens["jeune_minimum"] = sens["jeune_minimum_heures"].astype(str) + " h"
fig2 = px.bar(
    sens, x="groupe_imc", y="homa_mediane", color="jeune_minimum",
    barmode="group", text="n",
)
fig2.update_layout(xaxis_title=None, yaxis_title="HOMA-IR (médiane)")
st.plotly_chart(fig2)