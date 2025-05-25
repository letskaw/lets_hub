import streamlit as st

st.set_page_config(
    page_title="Let's Hub",      # Titre de l'onglet navigateur
    page_icon=":material/home:",                    # Icône de l'onglet
    layout="wide",
)

st.header(":material/home: Home")

col,_ , _=st.columns([1,1,1])

with col:
    h_rule = ":material/horizontal_rule:"
    suite_geom = ":material/hexagon::material/square::material/circle::material/rectangle::material/pentagon:"
    st.subheader("Bienvenue sur Let\'s Hub !\n Un espace entierement codé en python pour centraliser mes projets")
    
    st.subheader(f"{suite_geom+suite_geom}")
    st.text("")

    st.text("Pour commencer, selectionner une autre fenetre dans le volet de gauche.\n\n En vous souhaitant une bonne visite 😺")
    st.text("")
    @st.dialog("Formulaire de contact")
    def contact():

        name = st.text_input("Nom")
        email = st.text_input("Email")
        text = st.text_area("Message")

        if st.button("Submit"):
            st.session_state.message = {"Nom": name, "email": email, "message":text}
            st.rerun()

    if "message" not in st.session_state:
        if st.button("Contactez-moi"):
            contact()
    else:
        st.success(":material/check_circle: Message envoyé ")