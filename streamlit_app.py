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
    ),
    st.Page(
        "softs/random_stats.py",
        title="Random Stats",
        icon=":material/shuffle:"
    ),
    st.Page(
        "softs/sport_timer.py",
        title="Sport Timer",
        icon=":material/timer:"
    ),]
page = st.navigation(pages)
page.run()


full_logo = "assets/logo18.png"
st.logo(full_logo)