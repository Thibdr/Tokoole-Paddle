import sqlite3
import random
from faker import Faker
from datetime import date, timedelta

def fake_database():
    # Créer une base de données SQLite (ou ouvrir une existante)
    conn = sqlite3.connect('database/tokoole.db')
    cursor = conn.cursor()

    # Générateur de données factices
    fake = Faker('fr_FR')  # Utilise des données factices en français

    # Liste de prénoms masculins et féminins
    prenoms_masculins = [
        "Jean", "Paul", "Pierre", "Thomas", "François", "Nicolas", "David", "Eric", "Philippe", "Bruno",
        "Vincent", "Charles", "Antoine", "Mathieu", "Olivier", "Laurent", "Samuel", "Guillaume", "Alexandre",
        "Julien", "Christophe", "Xavier", "Michel", "Jérôme", "Grégoire", "Frédéric", "Thierry", "Sébastien",
        "Rémi", "Benoît", "Maxime", "Sébastien", "Romain", "Emmanuel", "Stéphane", "Lucas", "Quentin", "Cédric",
        "Yann", "Marc", "Lucas", "Thibault", "Jonathan", "Étienne", "Arnaud", "Nicolas", "Clément", "Damien",
        "Ludovic", "Fabien"
    ]

    prenoms_feminins = [
        "Marie", "Anne", "Sophie", "Catherine", "Isabelle", "Claire", "Émilie", "Élodie", "Sylvie", "Valérie",
        "Nathalie", "Patricia", "Sandrine", "Virginie", "Laura", "Caroline", "Véronique", "Laurence", "Aurélie",
        "Émilie", "Chloé", "Vanessa", "Isabelle", "Audrey", "Mélanie", "Alice", "Léa", "Céline", "Julie",
        "Amandine", "Stéphanie", "Sarah", "Charlotte", "Élise", "Clémence", "Manon", "Pauline", "Lucie",
        "Camille", "Marion", "Léna", "Océane", "Éva", "Lisa", "Roxane", "Anaïs", "Mélanie", "Margaux", "Marine",
        "Mathilde"
    ]

    # Créer la table "Adhérent"
    cursor.execute('''CREATE TABLE IF NOT EXISTS adherent (
        adherent_id INTEGER PRIMARY KEY AUTOINCREMENT,
        prenom TEXT NOT NULL,
        nom TEXT NOT NULL,
        date_naissance DATE,
        genre INTEGER,
        adresse TEXT NOT NULL CHECK(LENGTH(adresse) >= 5 AND LENGTH(adresse) <= 255),
        telephone TEXT,
        mail TEXT CHECK(LENGTH(mail) >= 5 AND LENGTH(mail) <= 255)
    )''')

    # Créer la table "inscription"
    cursor.execute('''CREATE TABLE IF NOT EXISTS inscription (
        inscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
        adherent_id INTEGER NOT NULL,
        date DATE,
        dossier_medical INTEGER DEFAULT 0 CHECK(dossier_medical IN (0, 1)),
        FOREIGN KEY (adherent_id) REFERENCES adherent (adherent_id)
    )''')

    # Créer la table "cotisation"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cotisation (
            cotisation_id INTEGER PRIMARY KEY,
            annee TEXT NOT NULL,
            statut INTEGER DEFAULT 0 CHECK(statut IN (0, 1)),
            description TEXT,
            prix REAL DEFAULT 0.0
    )''')

    # Création de la table de jointure 'adherent_cotisation'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS adherent_cotisation (
            adherent_id INTEGER,
            cotisation_id INTEGER,
            PRIMARY KEY (adherent_id, cotisation_id),
            FOREIGN KEY (adherent_id) REFERENCES adherent (adherent_id),
            FOREIGN KEY (cotisation_id) REFERENCES cotisation (cotisation_id)
    )''')

    # Générer 50 lignes d'insertion pour la table "Adhérent" avec de vraies adresses en France
    addresses = [
        "1 Rue de la République, 75001 Paris",
        "2 Avenue des Champs-Élysées, 75008 Paris",
        "32 rue Edouard Vaillant, 37000 Tours",
        "74 Rue de Charonne, 75020 Paris",
        "12 Place Gaston Pailloux, 37000 Tours",
        "Rue de la Vallée, 75000 Paris"
    ]

    # Générer 50 lignes d'insertion pour la table "adherent" 
    for _ in range(50):
        prenom = random.choice(prenoms_masculins + prenoms_feminins)
        nom = fake.last_name()
        date_naissance = fake.date_of_birth(minimum_age=7, maximum_age=70)
        genre = "homme" if prenom in prenoms_masculins else "femme"
        telephone = random.choice(["06" + str(fake.random_number(digits=8)), "07" + str(fake.random_number(digits=8))])  # Numéro de téléphone aléatoire
        adresse = random.choice(addresses)  # Adresse aléatoire en France
        mail = fake.email()
        cursor.execute("INSERT INTO adherent (prenom, nom, date_naissance, genre, adresse, telephone, mail) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (prenom, nom, date_naissance, genre, adresse, telephone, mail))

    # Générer 50 lignes d'insertion pour la table "inscription" avec des dates à partir du 1er juillet 2023
    start_date = date(2023, 7, 1)
    end_date = date.today()
    adherent_ids = list(range(1, 51))  # Liste des adhérents ID de 1 à 50
    for _ in range(50):
        adherent_id = random.choice(adherent_ids)  # Sélectionner un ID d'adhérent aléatoire
        adherent_ids.remove(adherent_id)  # Retirer cet ID de la liste pour qu'il soit unique
        date_inscription = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        dossier_medical = random.randint(0, 1)  # Statut de dossier médical aléatoire

        cursor.execute("INSERT INTO inscription (adherent_id, date_inscription, dossier_medical) VALUES (?, ?, ?)",
        (adherent_id, date_inscription, dossier_medical))

    # Générer 50 lignes d'insertion pour la table "cotisation" avec l'année 2023
    for _ in range(50):
        annee = "2023"
        description = random.choice(["Etudiant", "Demandeur d'emploi", "Ancien étudiant CEFIM", "Formateur CEFIM", "Enfant", "Adultes"])
        prix = 5 if description == "Etudiant" else \
            8 if description == "Demandeur d'emploi" else \
            9 if description == "Ancien étudiant CEFIM" else \
            0 if description == "Formateur CEFIM" else \
            10 if description == "Enfant" else 20  # Par défaut pour "Adultes"

        cursor.execute("INSERT INTO cotisation (annee, statut, description, prix) VALUES (?, ?, ?, ?)",
        (annee, random.randint(0, 1), description, prix))

    # Créez un ensemble pour stocker les ID d'adhérents et de cotisations déjà utilisés
    adherent_ids_utilises = set()
    cotisation_ids_utilises = set()

    # Générer 50 lignes d'insertion pour la table "adherent_cotisation" en associant aléatoirement des adhérents et des cotisations
    for _ in range(50):
        adherent_id = random.randint(1, 50)  # ID d'adhérent aléatoire entre 1 et 50 (selon le nombre d'adhérents)
        cotisation_id = random.randint(1, 50)  # ID de cotisation aléatoire entre 1 et 50 (selon le nombre de cotisations)

        # Assurez-vous que les ID sont uniques en vérifiant s'ils ont déjà été utilisés
        while adherent_id in adherent_ids_utilises:
            adherent_id = random.randint(1, 50)
        adherent_ids_utilises.add(adherent_id)

        while cotisation_id in cotisation_ids_utilises:
            cotisation_id = random.randint(1, 50)
        cotisation_ids_utilises.add(cotisation_id)

        cursor.execute("INSERT INTO adherent_cotisation (adherent_id, cotisation_id) VALUES (?, ?)",
        (adherent_id, cotisation_id, annee))

    # Valider les insertions et fermer la connexion à la base de données
    conn.commit()
    conn.close()