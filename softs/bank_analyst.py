import streamlit as st
from scripts.bank_analyst.script import get_pdf

#from scripts.bank_analyst.script import get_pdf

st.set_page_config(
    page_title="Let's Hub",              # Titre de l'onglet navigateur
    page_icon=":material/monitoring:",                         # Icône de l'onglet
    layout="wide",                          # Le contenu rempli la page
)

# Lance la sidebar personalisé 
from scripts.bank_analyst.sidebar import sidebar
sidebar()

# Mise en place du titre
st.header(":material/monitoring: Bank analyst")

# Mise en place des onglets
tab1, tab2, tab3 = "Données globale", "Comparatif entre enseignes",":material/calendar_clock: Coming soon"
list_tab= [tab1, tab2, tab3]
st.session_state.list_tab = list_tab

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

    # Chargement des scripts de stats
    from scripts.bank_analyst.script import get_df1, get_fig1,get_df2, get_fig2, get_df1_title, get_df2_title #, show_metrics


    select_tab = st.segmented_control("---", list_tab, default="Données globale")

    data = st.session_state.data.copy()
    col1, col2 = st.columns(2)

    # Lance l'onglet sur lequel on a cliqué
    if select_tab in list_tab:

        st.session_state.segmented_picked = select_tab

        # Premier onglet
        if select_tab == tab1:

            with col1:
                get_df1_title()
                st.dataframe(get_df1())
            with col2:
                st.markdown("")
                st.pyplot(get_fig1())

            #show_metrics()

        # Deuxieme onglet
        elif select_tab == tab2:
            if st.session_state.label_picked:
                st.toast(":material/warning: Le choix d'enseigne n'a aucun impact ici", icon=None)

            if "data_without_label" in st.session_state:
                            
                with col1:
                    get_df2_title()
                    st.dataframe(get_df2())
                with col2:
                    st.markdown("")
                    st.pyplot(get_fig2())


            
    # Sinon affiche un message invitant a cliquer sur un onglet
    else:
        st.subheader(':material/arrow_upward: Veuillez cliquer sur un onglet :material/arrow_upward:')





