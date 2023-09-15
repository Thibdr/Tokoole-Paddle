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

st.title("Liste des adhérents")

df = pd.DataFrame(get_adherent_with_relations(), columns=
    [
        "Adherent_id", "Nom", "Prenom", "Date_naissance", "Genre", "Adresse", "Telephone", "Mail", 
        "Date_inscription", "Dossier_medical", "Annee", "Statut", "Description", "Prix"
    ],
)

if "Adherent_id" in df.columns:
    df = df.drop(columns=["Adherent_id"])

st.dataframe(df)