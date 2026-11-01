from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path(__file__).parent / "exports"

st.set_page_config(page_title="NHANES : qualité des données", layout="wide")
st.title("NHANES 2021-2023 : qualité des données et HOMA-IR")
st.warning(
    "Projet de qualité de données. Résultats descriptifs sur cet échantillon, "
    "sans lien de cause, sans conclusion clinique et sans conseil de santé."
)

motifs = pd.read_csv(DATA / "motifs_exclusion.csv")
manquants = pd.read_csv(DATA / "valeurs_manquantes.csv")
homa = pd.read_csv(DATA / "homa_par_activite.csv")
resume = pd.read_csv(DATA / "resume.csv")

tab1, tab2 = st.tabs(["Qualité des données", "Association descriptive"])

with tab1:
    total = int(motifs["n"].sum())
    retenus = int(motifs.loc[motifs["motif"] == "Retenus pour le HOMA-IR", "n"].sum())
    c1, c2, c3 = st.columns(3)
    c1.metric("Participants examinés", f"{total:,}".replace(",", " "))
    c2.metric("Retenus pour le HOMA-IR", f"{retenus:,}".replace(",", " "))
    c3.metric("Part retenue", f"{100 * retenus / total:.1f} %")

    st.subheader("Pourquoi des participants sont écartés")
    st.caption("Chaque participant n'est compté que dans le premier motif qui le concerne.")
    fig = px.bar(motifs, x="n", y="motif", orientation="h", text="n")
    fig.update_layout(yaxis_title=None, xaxis_title="Participants")
    st.plotly_chart(fig)

    st.subheader("Valeurs manquantes parmi les adultes retenus")
    fig2 = px.bar(manquants, x="variable", y="pct_manquants", text="pct_manquants")
    fig2.update_layout(xaxis_title=None, yaxis_title="% de valeurs manquantes")
    st.plotly_chart(fig2)
    st.dataframe(manquants, hide_index=True)

with tab2:
    adultes = int(resume["adultes_retenus"].iloc[0])
    inconnue = int(resume["activite_inconnue"].iloc[0])
    c1, c2 = st.columns(2)
    c1.metric("Adultes retenus", adultes)
    c2.metric("Activité physique inconnue", inconnue)

    st.subheader("HOMA-IR par niveau d'activité de loisir déclaré")
    st.caption(
        "Activité = modérée + intense, en minutes par semaine, ramenée depuis "
        "l'unité déclarée. Barres : médiane. Traits : 1er et 3e quartiles."
    )
    homa["haut"] = homa["homa_q3"] - homa["homa_mediane"]
    homa["bas"] = homa["homa_mediane"] - homa["homa_q1"]
    fig3 = px.bar(
        homa, x="groupe_activite", y="homa_mediane",
        error_y="haut", error_y_minus="bas", text="n",
    )
    fig3.update_layout(xaxis_title=None, yaxis_title="HOMA-IR (médiane)")
    st.plotly_chart(fig3)
    st.dataframe(
        homa[["groupe_activite", "n", "homa_q1", "homa_mediane", "homa_q3"]],
        hide_index=True,
    )
    st.info(
        "Une association dans cet échantillon n'est ni une cause ni un conseil. "
        "Les valeurs décrivent ces participants, pas la population américaine."
    )