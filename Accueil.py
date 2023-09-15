import folium
import streamlit as st
import pandas as pd
from lib.database_functions import *
from lib.database_faker import *
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
import plotly.express as px

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
with open('css/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

st.header("Bienvenue dans l'application de l'association ToKoole")
# footer_content = """
# <style>
# .footer {
#     text-align: center;
#     background-color: #f0f0f0;
#     padding: 10px;
#     font-size: 14px;
# }
# </style>

# <div class="footer">
#     <p><a href="Mentions_légales">Mentions légales</a></p>
#     <p>"Créé par ToKool - © 2023</p>
# </div>
# """

# # Affichez le footer personnalisé
# st.markdown(footer_content, unsafe_allow_html=True)

create_table()

left_column, right_column = st.columns(2)

with left_column:
    st.write(f"Il y a actuellement  <span style='font-size: xx-large;'><b>{get_nombre_inscrits()}</b></span>   adhérent(s) à ToKoole. <br> L'age moyen des adhérents est de <span style='font-size: xx-large;'><b>{get_moyenne_age()}</b></span> ans.",
     unsafe_allow_html=True)
    st.subheader("Position des adhérent(s)")
    def geocode_address(address):
        try:
            geolocator = Nominatim(user_agent="geoapiExercises", timeout=5)
            location = geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except Exception as e:
            print(f"Erreur de géocodage : {str(e)}")
            return None, None
    adresses = get_adherent_adresse()
    adresses_df = pd.DataFrame(adresses, columns=['Nom', 'Prénom', 'Adresse'])
    coordinates = []
    for address in adresses:
        latitude, longitude = geocode_address(address[2])
        if latitude and longitude:
            coordinates.append((latitude, longitude))
    df = pd.DataFrame(coordinates, columns=['LATITUDE', 'LONGITUDE'])  
    m = folium.Map(location=[df['LATITUDE'].values.mean(), df['LONGITUDE'].values.mean()], zoom_start=8)
    for index, row in df.iterrows():
        arow = adresses_df.iloc[index]
        popup = folium.Popup(f"Adherent: {arow['Nom']} {arow['Prénom']} <br> Adresse: {arow['Adresse']}", max_width=300)
        folium.Marker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            popup=popup
        ).add_to(m)
    st_folium(folium.Figure(width=300, height=100).add_child(m))

    with right_column:
        st.subheader("Répartition par genre")
        repartitions = get_repartition_inscrits()
        repartitions = [
            {"Genre": repartitions[0][0], "Nombre": repartitions[0][1]},
            {"Genre": repartitions[1][0], "Nombre": repartitions[1][1]}
        ]
        df_repartitions = pd.DataFrame(repartitions)
        color_discrete_map = {'Homme': '#3471eb', 'Femme': '#eb34ab'}
        fig = px.pie(df_repartitions, names='Genre', values='Nombre',
                    color='Genre', color_discrete_map=color_discrete_map)
        fig.update_traces(hoverinfo='label+percent+value+name',
                        hovertemplate='%{label} : %{value} <extra></extra>')
        st.plotly_chart(fig)

        unpaid_members = get_unpaid_members()
        st.subheader("Cotisation impayée")
        st.write(f"Nombre de personnes dont la cotisation n'a pas été réglée : {len(unpaid_members)}")
        df = pd.DataFrame(unpaid_members, columns=['Nom', 'Prenom', 'Mail'])
        st.write(df)
        if st.button("Exporter au format CSV"):
            df.to_csv("cotisation_impayee.csv", index=False)
            st.success("Données exportées au format CSV avec succès.")