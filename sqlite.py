import sqlite3


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
    last_client_id = db_cursor.lastrowid
    print('last client id = ' + str(last_client_id))
    commande = {
        "client_id" : last_client_id,
        "produit" : "produit" + str(last_client_id),
    }
    db_cursor.execute(insert_commande, commande)
    last_commande_id = db_cursor.lastrowid
    print('last commande id = ' + str(last_commande_id))



db_connect.close()



