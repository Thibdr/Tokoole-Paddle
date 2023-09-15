from datetime import datetime
import streamlit as st
import pandas as pd
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

st.title("Supprimer un adhérent")

df = pd.DataFrame(get_adherent_with_relations(), columns=
    [
        "Adherent_id", "Nom", "Prenom", "Date_naissance", "Genre", "Adresse", "Telephone", "Mail", 
        "Date_inscription", "Dossier_medical", "Annee", "Statut", "Description", "Prix"
    ],
)
selected_option = st.selectbox("Sélectionnez un adhérent à modifier :", df["Adherent_id"], format_func=lambda x: df[df["Adherent_id"] == x]["Prenom"].values[0])
record = df.query("Adherent_id == @selected_option")

if record["Nom"].str != 0:
    with st.form("Formulaire d'ajout d'adhérents", clear_on_submit=True):
        nom = st.text_input("Nom", value=record['Nom'].values[0])
        prenom = st.text_input("Prenom", value=record['Prenom'].values[0])
        date_naissance = st.date_input("Date de naissance", format="DD/MM/YYYY", value=datetime.strptime(record['Date_naissance'].values[0], "%Y-%m-%d"))
        options = ("Homme", "Femme")
        genre = st.selectbox("Genre", options, options.index(record['Genre'].values[0]))
        adresse = st.text_input("Adresse", record['Adresse'].values[0])
        telephone = st.text_input("Téléphone", record['Telephone'].values[0])
        mail = st.text_input("E-mail", record['Mail'].values[0])

        if st.form_submit_button("Supprimer l'adhérent"):
            delete_adherent(mail, nom)
            st.success("L'adhérent est correctement supprimé.")
        
else:
    st.warning("Aucune valeur sélectionnée. Veuillez sélectionner un adhérent à supprimer.")