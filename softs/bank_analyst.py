import streamlit as st
st.set_page_config(
    page_title="Let's Hub",              # Titre de l'onglet navigateur
    page_icon=":material/monitoring:",                         # Icône de l'onglet
    layout="wide",                          # Le contenu rempli la page
)
from scripts.bank_analyst.side_bar import sidebar_stats_bq


sidebar_stats_bq()
st.header(":material/monitoring: Bank analyst")

if "data" not in st.session_state:
    for _ in range(7):
        st.text("")
    st.subheader(":material/arrow_back: Chargez un fichier .csv")


    st.text("Banques disponibles :\n- Revolut")

else:
    from scripts.bank_analyst.stats1 import stats1
    from scripts.bank_analyst.stats2 import stats2
    list_tab= ["Données globale", "Comparatif entre enseignes", "Cooming soon :material/timer:"]
    data = st.session_state.data

    select_tab = st.segmented_control("", list_tab, default="Données globale")

    if select_tab == "Données globale":
        stats1()

    elif select_tab == "Comparatif entre enseignes":
        stats2()
