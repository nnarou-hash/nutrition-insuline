from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path(__file__).parent / "exports"
SEUIL_PETIT_EFFECTIF = 50

st.set_page_config(page_title="HOMA-IR · NHANES 2021–2023", layout="wide")
px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = ["#0d5b95", "#78b9e6", "#2d83bd", "#add6ef"]
px.defaults.color_continuous_scale = [[0, "#78b9e6"], [0.5, "#f4f8fc"], [1, "#0d4f82"]]
st.markdown("""<style>
.stApp{background:#f4f8fc;color:#18334f}
h1,h2,h3{color:#123b65}
[data-testid="stMetricValue"]{color:#0d5b95}
[data-testid="stMetricLabel"]{color:#58718b}
[data-testid="stPlotlyChart"]{background:#fff;border:1px solid #d7e5f1;border-radius:14px;padding:6px}
.stTabs [data-baseweb="tab"][aria-selected="true"]{color:#0d5b95}
.stTabs [data-baseweb="tab-highlight"]{background:#0d5b95}
</style>
<div style="display:flex;align-items:center;gap:14px;margin:0 0 1rem 0">
 <div style="width:66px;height:66px;flex:0 0 66px;border-radius:50%;background:#fff;border:1px solid #d7e5f1;display:grid;place-items:center">
  <svg viewBox="0 0 100 100" width="52" height="52" aria-hidden="true"><circle cx="50" cy="50" r="37" fill="none" stroke="#087fc1" stroke-width="11"/></svg>
 </div>
 <div>
  <div style="font-size:11px;letter-spacing:.14em;font-weight:850;color:#0d568d">NN / DATA PORTFOLIO</div>
  <div style="font-size:10px;letter-spacing:.08em;color:#60768e">CERCLE BLEU · SYMBOLE MONDIAL DE SENSIBILISATION AU DIABÈTE</div>
 </div>
</div>""", unsafe_allow_html=True)
st.title("NHANES 2021–2023 : qualité des données et HOMA-IR")
st.caption("Le HOMA-IR est un indicateur indirect d’insulinorésistance calculé à partir de la glycémie et de l’insuline à jeun ; il ne permet pas, à lui seul, de diagnostiquer un diabète.")
st.warning(
    "Projet de qualité de données. Résultats descriptifs sur cet échantillon, "
    "sans lien de cause, sans conclusion clinique et sans conseil de santé."
)

st.info(
    "**Sources :** données publiques NHANES du CDC, cycle août 2021–août 2023 "
    "(démographie, mesures corporelles, insuline et glycémie à jeun, activité physique, "
    "jeûne, lipides, hémoglobine glyquée, hémoglobine et ferritine). "
    "Les fichiers sources sont préparés dans BigQuery et transformés avec dbt ; "
    "l’application exploite les exports analytiques agrégés du projet."
)
st.caption(
    "Onglets : règles de qualité et sélection des participants · facteurs descriptivement associés au HOMA-IR · limites et précautions d’interprétation."
)


def charger(nom):
    return pd.read_csv(DATA / f"{nom}.csv")


def barres_homa(df, x, titre, couleur=None):
    d = df.copy()
    d["haut"] = d["homa_q3"] - d["homa_mediane"]
    d["bas"] = d["homa_mediane"] - d["homa_q1"]
    fig = px.bar(
        d, x=x, y="homa_mediane", color=couleur, barmode="group",
        error_y="haut", error_y_minus="bas", text="n", title=titre,
    )
    fig.update_layout(xaxis_title=None, yaxis_title="HOMA-IR (médiane)")
    st.plotly_chart(fig)
    if (d["n"] < SEUIL_PETIT_EFFECTIF).any():
        st.caption(
            f"Attention : au moins un groupe a moins de {SEUIL_PETIT_EFFECTIF} "
            "participants (le nombre est affiché sur chaque barre) : lecture fragile."
        )
    with st.expander("Voir le tableau"):
        st.dataframe(d.drop(columns=["haut", "bas"]), hide_index=True)


tab1, tab2, tab3 = st.tabs(["Qualité des données", "Facteurs associés", "Limites"])

with tab1:
    motifs = charger("motifs_exclusion")
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
    manquants = charger("valeurs_manquantes")
    fig2 = px.bar(manquants, x="variable", y="pct_manquants", text="pct_manquants")
    fig2.update_layout(xaxis_title=None, yaxis_title="% de valeurs manquantes")
    st.plotly_chart(fig2)

    st.subheader("Part d'adultes retenus selon l'âge et le sexe")
    qualite = charger("qualite_retenus_par_groupe")
    fig3 = px.bar(
        qualite, x="groupe_age", y="pct_retenus", color="groupe_sexe",
        barmode="group", text="pct_retenus",
    )
    fig3.update_layout(xaxis_title=None, yaxis_title="% retenus parmi les adultes examinés")
    st.plotly_chart(fig3)
    st.caption("La tranche 70 ans et plus inclut les 80 ans et plus (âge plafonné à 80).")

with tab2:
    st.info(
        "Chaque barre montre la médiane du HOMA-IR du groupe, avec les 1er et 3e "
        "quartiles en traits. Ce sont des associations dans cet échantillon : "
        "les facteurs sont liés entre eux et rien ici ne montre une cause."
    )
    barres_homa(charger("homa_par_imc"), "groupe_imc", "Par catégorie d'IMC")

    tt = charger("homa_par_tour_taille")
    tt["quartile_tour_taille"] = "Quartile " + tt["quartile_tour_taille"].astype(str)
    barres_homa(tt, "quartile_tour_taille", "Par quartile de tour de taille, selon le sexe", "groupe_sexe")

    barres_homa(charger("homa_par_age_sexe"), "groupe_age", "Par tranche d'âge, selon le sexe", "groupe_sexe")
    barres_homa(charger("homa_sexe_par_imc"), "groupe_imc", "Par catégorie d'IMC, selon le sexe", "groupe_sexe")
    barres_homa(charger("homa_par_activite"), "groupe_activite", "Par niveau d'activité physique de loisir déclarée")
    barres_homa(charger("homa_par_intensite"), "groupe_intensite", "Par intensité de l'activité de loisir")
    barres_homa(charger("homa_par_sedentarite"), "groupe_sedentarite", "Par temps passé assis")
    barres_homa(
        charger("homa_activite_par_imc"), "groupe_imc",
        "Activité de loisir à IMC comparable", "groupe_activite",
    )

with tab3:
    resume = charger("resume")
    st.metric("Adultes retenus", int(resume["adultes_retenus"].iloc[0]))
    st.markdown(
        """
- Les chiffres décrivent cet échantillon, pas la population américaine.
- Les poids de sondage sont conservés dans la table mais ne sont pas utilisés.
- Ces données ne suivent pas les mêmes personnes dans le temps : elles ne peuvent pas montrer ce qui fait varier le HOMA-IR.
- L'activité physique est celle de loisir, déclarée.
- Les seuils de catégories (IMC, temps assis, quartiles) sont des choix du projet, pas des normes.
- L'approximation du HOMA-IR utilisée date de 1985 et n'est pas recalibrée pour les dosages actuels.
- Référence : Matthews DR et al., Diabetologia 1985;28(7):412-419, https://doi.org/10.1007/BF00280883
        """
    )