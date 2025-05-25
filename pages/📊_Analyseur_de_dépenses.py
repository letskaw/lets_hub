import streamlit as st
from scripts.stats_bancaires.side_bar import sidebar_stats_bq
from scripts.stats_bancaires.stats1 import stats1
from scripts.stats_bancaires.stats2 import stats2

st.set_page_config(
    page_title="Analyseur de dépenses",     # Titre de l'onglet navigateur
    page_icon="📊",                         # Icône de l'onglet
    layout="wide",                          # Le contenu rempli la page
)

sidebar_stats_bq()

if ("file" in st.session_state) and ("data" in st.session_state):

    list_tab= ["Données globale", "Comparatif entre enseignes"]#, "Editeur"
    data = st.session_state.data


    st.header("📊 Analyseur de dépenses")
    display_type = st.segmented_control("", list_tab, default="Données globale")

    #cols = st.columns(2)

    if display_type == "Données globale":
        stats1()

    elif display_type == "Comparatif entre enseignes":
        stats2()
        
    #elif display_type == "Data editor":
        #st.data_editor(data, num_rows="dynamic", use_container_width=True)
else:
    st.header("📊 Analyseur de dépenses")
    st.text("📄Chargez un fichier .csv\n\n Banques disponibles :\n- Revolut")
