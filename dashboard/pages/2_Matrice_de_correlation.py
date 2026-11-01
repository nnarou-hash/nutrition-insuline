from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path(__file__).parent.parent / "exports"
BANDES = ["18-29", "30-39", "40-49", "50-59", "60-69", "70+"]

st.title("Matrice de corrélation")
st.warning(
    "Projet de qualité de données. Résultats descriptifs sur cet échantillon, "
    "sans lien de cause, sans conclusion clinique et sans conseil de santé."
)
st.info(
    "Corrélation de rangs (de -1 à +1) entre chaque paire de mesures. Proche de 0 : "
    "pas de lien net dans cet échantillon. La diagonale vaut toujours 1. "
    "L'hémoglobine glyquée et le HOMA-IR reposent tous deux sur la glycémie : leur "
    "lien est en partie attendu. Les cases vides ont moins de 30 participants "
    "avec les deux mesures."
)

mat = pd.read_csv(DATA / "matrice_correlation.csv")

debut, fin = st.select_slider(
    "Tranches d'âge retenues (valable pour les deux matrices)",
    options=BANDES,
    value=(BANDES[0], BANDES[-1]),
)
st.caption(
    "Le filtre agit par tranches de 10 ans (la dernière regroupe les 70 ans et plus, "
    "dont les 80 ans et plus). Les matrices sont précalculées : aucune donnée "
    "individuelle n'est publiée."
)


def bloc(sexe, titre):
    d = mat[
        (mat["sexe"] == sexe)
        & (mat["bande_debut"] == debut)
        & (mat["bande_fin"] == fin)
    ]
    st.header(titre)
    if d.empty:
        st.write("Aucune donnée pour cette plage.")
        return
    ordre = d["variable_x"].drop_duplicates().tolist()
    m = d.pivot(index="variable_x", columns="variable_y", values="correlation")
    m = m.reindex(index=ordre, columns=ordre)
    st.caption(f"{int(d['n_groupe'].iloc[0])} participants dans cette plage.")
    fig = px.imshow(
        m, zmin=-1, zmax=1, color_continuous_scale="RdBu_r",
        text_auto=".2f", aspect="auto",
    )
    fig.update_layout(height=650, xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig)
    with st.expander("Effectif de chaque paire"):
        n_pairs = d.pivot(index="variable_x", columns="variable_y", values="n")
        st.dataframe(n_pairs.reindex(index=ordre, columns=ordre))


bloc("Femme", "Femmes")
st.divider()
bloc("Homme", "Hommes")