import random
import sqlite3
import csv

create_table_clients = """
    CREATE TABLE IF NOT EXISTS Clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        prenom TEXT,
        email TEXT,
        date_inscription DATE
    )
    """
create_table_commandes = """
    CREATE TABLE IF NOT EXISTS Commandes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        produit TEXT,
        date_commande DATE,
        FOREIGN KEY (client_id) references Clients(id)
    )
    """
insert_client = """
INSERT INTO Clients 
    (nom, prenom, email, date_inscription)
VALUES
    (:nom, :prenom, :email, :date_inscription)
"""

insert_commande = """
INSERT INTO Commandes 
    (client_id, produit, date_commande)
VALUES
    (:client_id, :produit, DATE('now'))
"""

get_clients = """
SELECT 
    id, nom, prenom, email, date_inscription
FROM
    Clients
ORDER BY
    date_inscription DESC
"""
select_commandes_by_client_id = """
SELECT 
    cm.id, cm.produit, cm.date_commande, cl.nom, cl.prenom, cl.email, cl.date_inscription
FROM
    Clients as cl
LEFT JOIN 
    Commandes as cm
ON
    cl.id = cm.client_id
GROUP BY
    cl.id
ORDER BY
    date_commande DESC
"""

get_commandes_by_client_id = """
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

update_client_email = """
UPDATE 
    Clients
SET
    email = 'new_email'
WHERE
    id = :client_id
"""

count_commandes = """
SELECT 
    Count(id)
FROM
    Commandes
"""

delete_commande = """
DELETE FROM
    Commandes 
WHERE
    id = :commande_id
"""

get_clients_commandes = """
SELECT 
    cm.id, cm.produit, cm.date_commande, cl.nom, cl.prenom, cl.email, cl.date_inscription, cl.id
FROM
    Clients as cl
LEFT JOIN 
    Commandes as cm
ON
    cl.id = cm.client_id
ORDER BY
    cl.id, date_commande DESC
"""



client_1 = {
    "nom" : "NOM1",
    "prenom" : "PRENOM1",
    "email" : "nom1.prenom1@ici.la",
    "date_inscription" : "2020-09-01"
}

client_2 = {
    "nom" : "NOM2",
    "prenom" : "PRENOM2",
    "email" : "nom2.prenom2@ici.la",
    "date_inscription" : "2023-10-01"
}

clients = [client_1, client_2]


db_connect = sqlite3.connect('my_db.db')
db_cursor = db_connect.cursor()

db_cursor.execute(create_table_clients)
db_cursor.execute(create_table_commandes)

for client in clients:
    db_cursor.execute(insert_client, client)
    db_connect.commit()
    last_client_id = db_cursor.lastrowid
    print('last client id = ' + str(last_client_id))
    commande1 = {
        "client_id" : last_client_id,
        "produit" : "produit" + str(last_client_id),
    }
    commande2 = {
        "client_id": last_client_id,
        "produit": "produit" + str(last_client_id + 1),
    }
    commandes = [commande1, commande2]
    for commande in commandes:
        db_cursor.execute(insert_commande, commande)
    db_connect.commit()
    last_commande_id = db_cursor.lastrowid
    print('last commande id = ' + str(last_commande_id))

db_cursor.execute(get_clients)
clients = db_cursor.fetchall()
for client in clients:
    print(client)

nb_clients = int(len(clients))
random_client_id = random.randint(1, nb_clients)
print('random client id = ' + str(random_client_id))
db_cursor.execute(get_commandes_by_client_id, {"client_id": random_client_id})
commandes = db_cursor.fetchall()
for commande in commandes:
    print(commande)
db_cursor.execute(update_client_email, {"client_id": random_client_id})
db_connect.commit()
db_cursor.execute(count_commandes)
nb_commandes = db_cursor.fetchone()[0]
random_commande_id = random.randint(1, nb_commandes)
db_cursor.execute(delete_commande, {"commande_id": random_commande_id})
print('delete commande with id = ' + str(random_commande_id))
db_connect.commit()





db_connect.close()



