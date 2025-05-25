# sidebar.py
import streamlit as st
from scripts.bank_analyst.script import get_list, load_data

def sidebar_stats_bq():
    
    with st.sidebar:
        st.header(":material/database: Données")

        if "file" in st.session_state:
            st.subheader(f":material/description: {st.session_state.file}")
            if st.button(":material/cancel:  Changer de fichier"):
                for key in ["file", "data", "data_origins", "year", "month", "day"]:
                    st.session_state.pop(key, None)
                st.rerun()

        else:
            file_uploaded = st.file_uploader(":material/description: Choisir un fichier CSV", type="csv", key="file_uploader")
            if file_uploaded:
                st.session_state.file = file_uploaded.name
                data = load_data(file_uploaded)
                st.session_state.data = data.copy()
                st.session_state.data_origins = data
                st.rerun()

        if "data" in st.session_state:
            st.session_state.data = st.session_state.data_origins

            st.session_state.list_year = get_list( st.session_state.data, 'year')
            st.session_state.list_month = []
            st.session_state.list_day = []
            st.session_state.label_picked = ""

            st.markdown("---")
            st.subheader(":material/filter_alt: Tri des données")


            ### Menu déroulant - year ###
            st.session_state.year = st.selectbox("Années", st.session_state.list_year, index=0)
            if st.session_state.year:
                st.session_state.data = st.session_state.data[st.session_state.data['year'] == st.session_state.year]

                ### Menu déroulant - month ###
                st.session_state.list_month  = get_list(st.session_state.data, 'month')
                st.session_state.month = st.selectbox("Mois", st.session_state.list_month, index=0)
                if st.session_state.month:
                    st.session_state.data = st.session_state.data[st.session_state.data['month'] == st.session_state.month]
            
                    ### Menu déroulant - day ###
                    st.session_state.list_day= get_list(st.session_state.data, 'day')
                    st.session_state.day = st.selectbox("Jour", st.session_state.list_day, index=0)
                    if st.session_state.day:
                        st.session_state.data = st.session_state.data[st.session_state.data['day'] == st.session_state.day]