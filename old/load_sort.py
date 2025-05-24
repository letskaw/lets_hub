import streamlit as st
from scripts.script import load_data_revolut, get_list

#~~~~~~~~ Upload d'un fichier CSV

uploaded_file = st.file_uploader("Choisir un fichier CSV", type="csv")

if uploaded_file:

    st.session_state.data_revolut_origins = load_data_revolut(uploaded_file)
    st.session_state.data_revolut = st.session_state.data_revolut_origins.copy()
    data_revolut =  st.session_state.data_revolut

    ########################################################################
    ########################
    ###   SORT ENTRIES   ###     Tri préalable pour visualisation prochaine

    st.subheader("Trier par date ")

    ### Menu déroulant - year ###
    data_revolut_year = get_list(data_revolut, 'year')
    st.session_state.year = st.selectbox("Années", data_revolut_year, index=0)

    if st.session_state.year:
        st.session_state.data_revolut = data_revolut[data_revolut['year'] == st.session_state.year]

        ### Menu déroulant - month ###
        data_revolut_month = get_list(data_revolut, 'month')
        st.session_state.month = st.selectbox("Mois", data_revolut_month, index=0)
        graph_month = False
        if st.session_state.month:
            st.session_state.data_revolutdata_revolut = data_revolut[data_revolut['month'] == st.session_state.month]
    

            ### Menu déroulant - day ###
            data_revolut_day = get_list(data_revolut, 'day')
            st.session_state.day = st.selectbox("Jour", data_revolut_day, index=0)
            if st.session_state.day:
                st.session_state.data_revolutdata_revolut = data_revolut[data_revolut['day'] == st.session_state.day]