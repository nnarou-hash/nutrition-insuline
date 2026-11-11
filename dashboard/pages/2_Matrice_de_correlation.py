from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path(__file__).parent.parent / "exports"
BANDES = ["18-29", "30-39", "40-49", "50-59", "60-69", "70+"]
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
        m, zmin=-1, zmax=1, color_continuous_scale=[[0, "#78b9e6"], [0.5, "#f4f8fc"], [1, "#0d4f82"]],
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