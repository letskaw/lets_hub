# sidebar.py
import streamlit as st
from scripts.bank_analyst.script import load_data, get_sort_menu, show_pdf_popup, lets_init_session_state

def sidebar():
    
    with st.sidebar:
        st.header(":material/database: Données")

        if "data" not in st.session_state:
            file_uploaded = st.file_uploader(":material/description: Choisir un fichier CSV", type="csv", key="file_uploader")
            if file_uploaded:
                st.session_state.file = file_uploaded.name
                data = load_data(file_uploaded)
                st.session_state.data = data.copy()
                st.session_state.data_origins = data
                st.rerun()

        else:
            st.subheader(f":material/description: {st.session_state.file}")
            if st.button(":material/cancel:  Changer de fichier", use_container_width=True):
                for key in ["file", "data", "data_origins", "year", "month", "day"]:
                    st.session_state.pop(key, None)
                st.rerun()

            if "init_session" not in st.session_state:
                lets_init_session_state()

            st.markdown("")
            with st.popover(":material/filter_alt: Tri des données", use_container_width=True):
                get_sort_menu()
            st.markdown("")
            if st.button(":material/file_save: Compte rendu PDF", use_container_width=True, type="primary"):
                show_pdf_popup(st.session_state.list_tab)








     


