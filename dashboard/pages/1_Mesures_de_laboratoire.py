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
    "Contrôle de cohérence de l'indicateur : on compare le HOMA-IR avec d'autres "
    "mesures, séparément chez les hommes et les femmes. Aucun seuil médical n'est "
    "utilisé. L'hémoglobine glyquée et le HOMA-IR reposent tous deux sur la "
    "glycémie : leur lien est en partie attendu."
)

st.subheader("Corrélation avec le HOMA-IR")
st.caption(
    "Corrélation de rangs (de -1 à +1). Proche de 0 : pas de lien net dans cet "
    "échantillon. Ce n'est ni une cause ni un test statistique. "
    "La ferritine n'est présente que chez les femmes de cet échantillon."
)
corr = pd.read_csv(DATA / "correlation_homa.csv")
fig_corr = px.bar(
    corr, x="correlation_spearman", y="mesure", color="groupe_sexe",
    orientation="h", barmode="group", hover_data=["n"],
)
fig_corr.update_layout(xaxis_title="Corrélation avec le HOMA-IR", yaxis_title=None)
fig_corr.update_xaxes(range=[-1, 1])
st.plotly_chart(fig_corr)

st.subheader("HOMA-IR médian par groupe de chaque mesure")
st.caption(
    "Les 4 groupes ont la même taille, du plus bas (1) au plus haut (4) niveau "
    "de la mesure. Le nombre de participants est affiché sur chaque barre."
)
labo = pd.read_csv(DATA / "homa_par_mesures_labo.csv")
mesure = st.selectbox("Mesure", sorted(labo["mesure"].unique()))
d = labo[labo["mesure"] == mesure].copy()
d["groupe"] = "Groupe " + d["quartile"].astype(str)
fig = px.bar(
    d, x="groupe", y="homa_mediane", color="groupe_sexe",
    barmode="group", text="n", hover_data=["valeur_min", "valeur_max"],
)
fig.update_layout(xaxis_title=None, yaxis_title="HOMA-IR (médiane)")
st.plotly_chart(fig)
st.dataframe(
    d[["groupe_sexe", "groupe", "n", "valeur_min", "valeur_max", "homa_mediane"]],
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