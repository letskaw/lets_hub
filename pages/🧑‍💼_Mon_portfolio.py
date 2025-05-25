import streamlit.components.v1 as components
import streamlit as st


st.set_page_config(
    page_title="Portfolio",      # Titre de l'onglet navigateur
    page_icon="🧑‍💼",                    # Icône de l'onglet
    layout="wide",
    #menu_items=None,
    #initial_sidebar_state="collapsed"
)

st.header("🧑‍💼 Mon portfolio")

html_code = """
<style>
/* Enlève les marges latérales imposées par Streamlit */
.main > div {
    padding-left: 0rem;
    padding-right: 0rem;
}

/* Conteneur étendu */
.container-iframe {
    width: 100vw;
    max-width: 100%;
    margin-left: auto;
    margin-right: auto;
}

/* iFrame responsive */
iframe {
    width: 100%;
    height: 700px;
    border: none;
}
</style>

<div class="container-iframe">
    <iframe src="https://letskaw.com"></iframe>
</div>
"""



components.html(html_code, height=750, scrolling=True)
