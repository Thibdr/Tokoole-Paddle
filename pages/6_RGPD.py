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

st.title("RGPD : Politique de Confidentialité")

st.header("1. Politique de confidentialité et conformité au RGPD")
st.write("""
Votre association de Paddle est déterminée à respecter la vie privée de ses membres et à se conformer au Règlement Général sur la Protection des Données (RGPD) en vigueur en France. Cette politique de confidentialité explique comment nous collectons, utilisons et protégeons les données personnelles de nos membres via notre site web, en particulier dans le cadre de l'enregistrement des adhérents, de la modification des données et de la gestion des cotisations.
""")

st.header("2. Collecte de données personnelles")
st.write("""
Lorsque nous utilisons notre site web pour vous inscrire en tant qu'adhérent, mettre à jour vos informations ou supprimer votre profil, nous collectons des données personnelles telles que votre nom, votre adresse e-mail, votre numéro de téléphone, votre adresse postale, votre date de naissance, etc. Ces données sont nécessaires à la gestion de votre adhésion.
""")


st.header("3. Utilisation des données personnelles")
st.write("""
Nous utilisons les données personnelles collectées pour les finalités suivantes :
- Gérer et suivre les adhésions des membres.
- Effectuer des analyses de données, y compris le suivi de certains KPI (indicateurs de performance clés) pour améliorer nos activités.
- Assurer la conformité aux obligations légales et réglementaires.
""")


st.header("4. Conservation des données")
st.write("""
Nous ne conservons vos données personnelles que pendant la durée nécessaire aux finalités pour lesquelles elles ont été collectées. Cela inclut la durée de votre adhésion à l'association, ainsi que toute période de conservation nécessaire pour satisfaire à nos obligations légales.
""")


st.header("5. Sécurité des données")
st.write("""
Nous prenons des mesures techniques et organisationnelles appropriées pour protéger vos données personnelles contre la perte, l'accès non autorisé, la divulgation, l'altération ou la destruction, y compris la sécurisation de l'accès aux données des membres.
""")

st.header("6. Alerte pour les cotisations non payées")
st.write("""
Nous utilisons des outils et des procédures automatisés pour suivre les cotisations de nos membres. Si une cotisation n'est pas payée dans les délais convenus, notre système génère une alerte qui est traitée par nos administrateurs. Vous recevrez alors une notification vous rappelant de régler votre cotisation.
""")


st.header("7. Vos droits")
st.write("""
En vertu du RGPD, vous avez certains droits concernant vos données personnelles, notamment le droit d'accéder à vos données, de les rectifier, de les effacer, de vous opposer au traitement ou de demander la limitation du traitement. Vous pouvez exercer ces droits en nous contactant à tokoole@gmail.com.
""")


st.header("8. Contact")
st.write("""
Si vous avez des questions ou des préoccupations concernant notre politique de confidentialité ou notre traitement de vos données personnelles, veuillez nous contacter à tokoole@gmail.com.
""")


st.header("9. Modifications de la politique de confidentialité")
st.write("""
Nous nous réservons le droit de mettre à jour cette politique de confidentialité à tout moment pour refléter les changements dans nos pratiques de gestion des données ou les exigences légales. Toute modification sera publiée sur cette page, et la date de révision en haut de cette page sera mise à jour.
""")