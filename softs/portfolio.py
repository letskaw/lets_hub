import streamlit.components.v1 as components
import streamlit as st
st.set_page_config(
    page_title="Let's Hub",         # Titre de l'onglet navigateur
    page_icon=":material/person:",  # Icône de l'onglet
    layout="wide",
)

### TITLLE ###
col1, col2 = st.columns([1,1], border=False, vertical_alignment="bottom",)#"top", "center", or "bottom"
with col1:
    st.header(":material/person: Portfolio")
with col2:
    _, col3 =  st.columns([1,1], border=False, vertical_alignment="bottom")
    with col3:
        st.link_button("Ouvrir dans le navigateur", "http://www.letskaw.com/portfolio", type="primary", icon=":material/open_in_new:")

### INTEGRATION WEB ###
html_code = """
<style>
iframe { width: 100%; height: 600px; border: none;6 }
</style>
<div class="container-iframe">
    <iframe src="https://letskaw.com"></iframe>
</div>
"""
components.html(html_code, height=620, scrolling=True)
