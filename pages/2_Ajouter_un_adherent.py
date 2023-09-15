import streamlit as st
from lib.database_functions import *

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

st.title("Page d'ajout d'adherent")

with st.form("Formulaire d'ajout d'adhérents", clear_on_submit=True):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    date_naissance = st.date_input("Âge", format="DD/MM/YYYY", min_value=date(1930, 1, 1))
    genre = st.selectbox("Genre", ("Homme", "Femme"))
    adresse = st.text_input("Adresse")
    telephone = st.text_input("Téléphone")
    mail = st.text_input("E-mail")
    inscription_dossier_medical = st.checkbox("Dossier médical fourni ?")
    cotisation_statut = st.checkbox("Cotisation réglée à l'avance ?")

    cotisation = {
        "Etudiant": "5",
        "Demandeur d'emploi": "8",
        "Ancien étudiant de CEFIM": "9",
        "Formateur à CEFIM": "0",
        "Enfant": "10",
        "Adulte": "20"
    }
    # Créez une liste d'options formatées
    options_formattees = [f"{cle} {valeur} €" for cle, valeur in cotisation.items()]

    # Créez une liste de clés uniquement
    options_cles = list(cotisation.keys())

    # Utilisez la liste des options formatées pour afficher le selectbox
    cotisation_description = st.selectbox("Tarif sélectionné", options_formattees)

    # Utilisez la liste des clés pour obtenir la valeur sélectionnée
    cotisation_cle = options_cles[options_formattees.index(cotisation_description)]
    cotisation_prix = cotisation_description.split()[1]

    if st.form_submit_button("Ajouter"):
        create_adherent(
            nom, prenom, date_naissance, genre, adresse, telephone, mail,
            inscription_dossier_medical, cotisation_statut,cotisation_description.split()[0], cotisation_prix
        )