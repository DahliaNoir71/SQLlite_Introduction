import random
import sqlite3

# Constantes pour les requêtes SQL
CREATE_TABLE_CLIENTS = """
    CREATE TABLE IF NOT EXISTS Clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        prenom TEXT,
        email TEXT,
        date_inscription DATE
    )
"""

CREATE_TABLE_COMMANDES = """
    CREATE TABLE IF NOT EXISTS Commandes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        produit TEXT,
        date_commande DATE,
        FOREIGN KEY (client_id) references Clients(id)
    )
"""

INSERT_CLIENT = """
INSERT INTO Clients 
    (nom, prenom, email, date_inscription)
VALUES
    (:nom, :prenom, :email, :date_inscription)
"""

INSERT_COMMANDE = """
INSERT INTO Commandes 
    (client_id, produit, date_commande)
VALUES
    (:client_id, :produit, DATE('now'))
"""

GET_CLIENTS = """
SELECT 
    id, nom, prenom, email, date_inscription
FROM
    Clients
ORDER BY
    date_inscription DESC
"""

GET_COMMANDES_BY_CLIENT_ID = """
SELECT 
    cm.id, cm.produit, cm.date_commande, cl.nom, cl.prenom, cl.email, cl.date_inscription, cl.id
FROM
    Clients as cl
LEFT JOIN 
    Commandes as cm
ON
    cl.id = cm.client_id
WHERE
    cl.id = :client_id
ORDER BY
    cm.date_commande DESC
"""

UPDATE_CLIENT_EMAIL = """
UPDATE 
    Clients
SET
    email = 'new_email'
WHERE
    id = :client_id
"""

COUNT_COMMANDES = """
SELECT 
    Count(id)
FROM
    Commandes
"""

DELETE_COMMANDE = """
DELETE FROM
    Commandes 
WHERE
    id = :commande_id
"""


def create_tables(cursor):
    cursor.execute(CREATE_TABLE_CLIENTS)
    cursor.execute(CREATE_TABLE_COMMANDES)


def insert_client(cursor, client_data):
    cursor.execute(INSERT_CLIENT, client_data)
    return cursor.lastrowid


def insert_commandes(cursor, client_id, produits):
    for produit in produits:
        commande_data = {"client_id": client_id, "produit": produit}
        cursor.execute(INSERT_COMMANDE, commande_data)
    return cursor.lastrowid


def fetch_all_clients(cursor):
    cursor.execute(GET_CLIENTS)
    return cursor.fetchall()


def fetch_commandes_by_client_id(cursor, client_id):
    cursor.execute(GET_COMMANDES_BY_CLIENT_ID, {"client_id": client_id})
    return cursor.fetchall()


def update_email(cursor, client_id):
    cursor.execute(UPDATE_CLIENT_EMAIL, {"client_id": client_id})


def fetch_commandes_count(cursor):
    cursor.execute(COUNT_COMMANDES)
    return cursor.fetchone()[0]


def delete_commande(cursor, commande_id):
    cursor.execute(DELETE_COMMANDE, {"commande_id": commande_id})


# Initialisation de la base de données
db_connect = sqlite3.connect('my_db.db')
db_cursor = db_connect.cursor()

# Création des tables
create_tables(db_cursor)

clients_data = [
    {"nom": "NOM1", "prenom": "PRENOM1", "email": "nom1.prenom1@ici.la", "date_inscription": "2020-09-01"},
    {"nom": "NOM2", "prenom": "PRENOM2", "email": "nom2.prenom2@ici.la", "date_inscription": "2023-10-01"}
]

# Insertion de clients et commandes
for client in clients_data:
    last_client_id = insert_client(db_cursor, client)
    produits = [f"produit{last_client_id}", f"produit{last_client_id + 1}"]
    last_commande_id = insert_commandes(db_cursor, last_client_id, produits)
    db_connect.commit()

# Affichage des clients
clients = fetch_all_clients(db_cursor)
for client in clients:
    print(client)

# Sélection et mise à jour d'un client aléatoire
nb_clients = len(clients)
random_client_id = random.randint(1, nb_clients)
print('random client id = ' + str(random_client_id))
commandes = fetch_commandes_by_client_id(db_cursor, random_client_id)
for commande in commandes:
    print(commande)

update_email(db_cursor, random_client_id)
db_connect.commit()

# Suppression d'une commande aléatoire
nb_commandes = fetch_commandes_count(db_cursor)
random_commande_id = random.randint(1, nb_commandes)
delete_commande(db_cursor, random_commande_id)
print('delete commande with id = ' + str(random_commande_id))

db_connect.commit()
db_connect.close()
