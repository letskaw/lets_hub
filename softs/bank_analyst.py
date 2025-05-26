import streamlit as st
st.set_page_config(
    page_title="Let's Hub",              # Titre de l'onglet navigateur
    page_icon=":material/monitoring:",                         # Icône de l'onglet
    layout="wide",                          # Le contenu rempli la page
)

# Lance la sidebar personalisé 
from scripts.bank_analyst.side_bar import sidebar_stats_bq
sidebar_stats_bq()

st.header(":material/monitoring: Bank analyst")

#########################################
# Message indiquant de joindre un fichier
if "data" not in st.session_state:
    for _ in range(7):
        st.text("")
    st.subheader(":material/arrow_back: Chargez un fichier .csv")
    st.text("Banques disponibles :\n- Revolut")


#######################################################
# Quand un fichier est joint et que la data est importé
else:
    from scripts.bank_analyst.stats1 import stats1
    from scripts.bank_analyst.stats2 import stats2

    list_tab= ["Données globale", "Comparatif entre enseignes", "Cooming soon :material/timer:"]
    data = st.session_state.data
    col1, col2 = st.columns(2, vertical_alignment="bottom")

    # Selection de l'onglet de stats
    with col1:
        select_tab = st.segmented_control("", list_tab, default="Données globale")

    # Boutton d'export des données en csv
    with col2:
        _, col2b = st.columns(2, vertical_alignment="bottom")
        with col2b:
            st.download_button("Télécharger les données", st.session_state.data.to_csv(index=False), "resultat.csv", "text/csv", type="primary")


    # Lance l'onglet sur lequel on a cliqué
    if select_tab in list_tab:

        if select_tab == "Données globale":
            stats1()

        elif select_tab == "Comparatif entre enseignes":
            stats2()
            
    # Sinon affiche un message invitant a cliquer sur un onglet
    else:
        st.subheader(':material/arrow_upward: Veuillez cliquer sur un onglet :material/arrow_upward:')
