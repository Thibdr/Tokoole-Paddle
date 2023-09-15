import streamlit as st

st.set_page_config(
    page_title="ToKool Paddle",
    page_icon="images/icon_paddle.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a Bug': None,
        'About': None
    }
)

st.title("Mentions Légales")

st.header("1. Informations sur l'association")
st.write("""
Nom de l'association : ToKoole
Siège social : [Adresse du Siège Social]
Numéro SIREN de l'association : [Numéro SIREN de l'association]
""")


st.header("2. Contact")
st.write("""
Adresse e-mail de contact : [Adresse e-mail de contact]
Numéro de téléphone de contact : [Numéro de téléphone de contact]
""")

st.header("3. Directeur de la publication")
st.write("[Nom du Directeur de la Publication]")

st.header("4. Hébergement du site web")
st.write("""
Nom de l'hébergeur : Streamlit Cloud
Adresse de l'hébergeur : .streamlit.app
""")

st.header("5. Politique de confidentialité")
st.write("Voir la partie ci-dessous concernant le RGPD.")