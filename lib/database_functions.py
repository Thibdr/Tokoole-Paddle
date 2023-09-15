import sqlite3 as sqli
from datetime import date, datetime

# Création des tables nécessaires au fonctionnement de l'application
def create_table():
    connection = sqli.connect("./database/tokoole.db")
    cursor = connection.cursor()

    # Création de la table 'adherent'
    cursor.execute('''CREATE TABLE IF NOT EXISTS adherent (
        adherent_id INTEGER PRIMARY KEY AUTOINCREMENT,
        prenom TEXT NOT NULL,
        nom TEXT NOT NULL,
        date_naissance DATE,
        genre INTEGER,
        adresse TEXT NOT NULL CHECK(LENGTH(adresse) >= 5 AND LENGTH(adresse) <= 255),
        telephone TEXT CHECK(LENGTH(telephone) >= 10 AND LENGTH(telephone) <= 20),
        mail TEXT CHECK(LENGTH(mail) >= 5 AND LENGTH(mail) <= 255)
    )''')
    # Création de la table 'inscription'
    cursor.execute('''CREATE TABLE IF NOT EXISTS inscription (
        inscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
        adherent_id INTEGER NOT NULL,
        date DATE,
        dossier_medical INTEGER DEFAULT 0 CHECK(dossier_medical IN (0, 1)),
        FOREIGN KEY (adherent_id) REFERENCES adherent (adherent_id)
    )''')
    # Création de la table 'cotisation'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cotisation (
            cotisation_id INTEGER PRIMARY KEY,
            annee TEXT NOT NULL,
            statut INTEGER DEFAULT 0 CHECK(statut IN (0, 1)),
            description TEXT,
            prix REAL DEFAULT 0.0
        )
    ''')
    # Création de la table de jointure 'adherent_cotisation'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS adherent_cotisation (
            adherent_id INTEGER,
            cotisation_id INTEGER,
            PRIMARY KEY (adherent_id, cotisation_id),
            FOREIGN KEY (adherent_id) REFERENCES adherent (adherent_id),
            FOREIGN KEY (cotisation_id) REFERENCES cotisation (cotisation_id)
        )
    ''')

    connection.commit()
    connection.close()

# Création d'un adherent
def create_adherent(nom, prenom, date_naissance, genre, adresse, telephone, mail, dossier_medical, statut, description, prix):
    connection = sqli.connect("./database/tokoole.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO adherent (nom, prenom, date_naissance, genre, adresse, telephone, mail) VALUES (?, ?, ?, ?, ?, ?, ?)", 
        (nom, prenom, date_naissance, genre, adresse, telephone, mail)
    )
    adherent_id = cursor.lastrowid
    cursor.execute("INSERT INTO inscription (adherent_id, date, dossier_medical) VALUES (?, ?, ?)", 
        (adherent_id, date.today(), dossier_medical)
    )
    cursor.execute("INSERT INTO cotisation (annee, statut, description, prix) VALUES (?, ?, ?, ?)", 
        (date.today().year, statut, description, prix)
    )
    cotisation_id = cursor.lastrowid
    cursor.execute("INSERT INTO adherent_cotisation (adherent_id, cotisation_id) VALUES (?, ?)", 
        (adherent_id, cotisation_id)
    )
    connection.commit()
    connection.close()

# Récupère la liste des adhérents
def get_adherent():
    connection = sqli.connect("./database/tokoole.db")
    cursor = connection.cursor()
    cursor.execute("SELECT nom, prenom, date_naissance, genre, adresse, telephone, mail FROM adherent")
    resultats = cursor.fetchall()
    connection.commit()
    connection.close()
    return resultats

#  Mise à jour d'un adherent 
def update_adherent(adherent_id, nom, prenom, date_naissance, genre, adresse, telephone, mail, inscription_dossier_medical, cotisation_statut):
    connection = sqli.connect("./database/tokoole.db")
    cursor = connection.cursor()
    
    cursor.execute("""
    UPDATE adherent
    SET nom = ?,
    prenom = ?,
    date_naissance = ?,
    genre = ?,
    adresse = ?,
    telephone = ?,
    mail = ?
    WHERE adherent_id = ?
    """, (nom, prenom, date_naissance, genre, adresse, telephone, mail, adherent_id))

    cursor.execute("""
    UPDATE inscription
        SET dossier_medical = ?
    WHERE adherent_id = (
        SELECT adherent_id
        FROM adherent
        WHERE adherent_id = ?
    )
    """, (inscription_dossier_medical, adherent_id))

    cursor.execute("""
    UPDATE cotisation
    SET statut = ?
    WHERE cotisation_id IN (
        SELECT ac.cotisation_id
        FROM adherent_cotisation AS ac
        WHERE ac.adherent_id = ?
    )
    """, (cotisation_statut, adherent_id))

    connection.commit()
    connection.close()

#  Suppression d'un adherent 
def delete_adherent(mail, nom):
    connection = sqli.connect("./database/tokoole.db")
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM adherent
    WHERE mail = ? AND nom = ?
    """, (mail, nom))

    connection.commit()
    connection.close()

# Récupère la liste des adhérents
def get_adherent_with_relations():
    connection = sqli.connect("./database/tokoole.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT a.adherent_id, a.nom, a.prenom, a.date_naissance, a.genre, a.adresse, a.telephone, a.mail,
            i.date AS date_inscription, i.dossier_medical,
            c.annee, c.statut, c.description, c.prix
        FROM adherent AS a
        LEFT JOIN inscription AS i ON a.adherent_id = i.adherent_id
        LEFT JOIN adherent_cotisation AS ac ON a.adherent_id = ac.adherent_id
        LEFT JOIN cotisation AS c ON ac.cotisation_id = c.cotisation_id
    """)
    resultats = cursor.fetchall()
    connection.close()
    return resultats

def get_adherent_adresse():
    connection = sqli.connect("./database/tokoole.db")
    cursor = connection.cursor()
    cursor.execute("SELECT nom, prenom, adresse FROM Adherent")
    resultats = cursor.fetchall()
    connection.close()
    return resultats

def get_nombre_inscrits():
    conn = sqli.connect('database/tokoole.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM adherent")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_repartition_inscrits():
    conn = sqli.connect('database/tokoole.db')
    cursor = conn.cursor()
    cursor.execute("SELECT genre, COUNT(*) AS nombre_adherents FROM Adherent GROUP BY genre")
    resultats = cursor.fetchall()
    conn.close()
    return resultats

def get_unpaid_members():
    conn = sqli.connect('database/tokoole.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT a.nom, a.prenom, a.mail
    FROM adherent AS a
    LEFT JOIN adherent_cotisation AS ac ON a.adherent_id = ac.adherent_id
    LEFT JOIN cotisation AS c ON ac.cotisation_id = c.cotisation_id
    WHERE c.statut = 0;
    """)
    resultats = cursor.fetchall()
    conn.close()
    return resultats



def get_moyenne_age():
    conn = sqli.connect('database/tokoole.db')
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(strftime('%Y', 'now') - strftime('%Y', date_naissance)) AS age_moyen FROM Adherent")
    result = cursor.fetchone()
    conn.close()
    age_moyen = result[0]
    return int(age_moyen)
