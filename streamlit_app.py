import streamlit as st
pages = [
    st.Page(
        "softs/home.py",
        title="Home",
        icon=":material/home:"
    ),
    st.Page(
        "softs/portfolio.py",
        title="Portfolio",
        icon=":material/person:"
    ),
    st.Page(
        "softs/bank_analyst.py",
        title="Bank Analyst",
        icon=":material/monitoring:"
    ),]
page = st.navigation(pages)
page.run()