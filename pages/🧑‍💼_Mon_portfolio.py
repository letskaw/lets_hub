import streamlit.components.v1 as components

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
