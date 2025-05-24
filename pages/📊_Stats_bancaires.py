import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    page_title="Analyseur de dépenses Revolut",      # Titre de l'onglet navigateur
    page_icon="📊",                    # Icône de l'onglet
)

from scripts.stats_bancaires.side_bar import sidebar_stats_bq
from scripts.stats_bancaires.stats1 import stats1
from scripts.stats_bancaires.stats2 import stats2


sidebar_stats_bq()

if ("file" in st.session_state) and ("data" in st.session_state):

    list_tab= ["Données globale", "Comparatif entre enseignes"]#, "Editeur"
    data = st.session_state.data


    st.header("Analyseur de dépenses")
    display_type = st.segmented_control("Display type", list_tab, default="Données globale")

    #cols = st.columns(3)

    event = None

    if display_type == "Données globale":
        event = stats1()
    elif display_type == "Comparatif entre enseignes":
        event = stats2()
        
    #elif display_type == "Data editor":
        #st.data_editor(data, num_rows="dynamic", use_container_width=True)
else:
    st.title("📊 Analyseur de dépenses")
    st.text("📄Chargez un fichier .csv\n\n\n\n Banques disponibles :\n\n- Revolut\n- ")
