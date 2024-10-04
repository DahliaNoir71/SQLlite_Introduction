import random
import sqlite3

# Constantes pour les requêtes SQL
SQL_REQUESTS = {
    "create_clients_table": """
        CREATE TABLE IF NOT EXISTS Clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT,
            email TEXT,
            date_inscription DATE
        )
    """,
    "create_commandes_table": """
        CREATE TABLE IF NOT EXISTS Commandes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            produit TEXT,
            date_commande DATE,
            FOREIGN KEY (client_id) references Clients(id)
        )
    """,
    "insert_client": """
        INSERT INTO Clients 
            (nom, prenom, email, date_inscription)
        VALUES
            (:nom, :prenom, :email, :date_inscription)
    """,
    "insert_commande": """
        INSERT INTO Commandes 
            (client_id, produit, date_commande)
        VALUES
            (:client_id, :produit, DATE('now'))
    """,
    "get_clients": """
        SELECT 
            id, nom, prenom, email, date_inscription
        FROM
            Clients
        ORDER BY
            date_inscription DESC
    """,
    "get_commandes_by_client_id": """
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
    """,
    "update_client_email": """
        UPDATE 
            Clients
        SET
            email = 'new_email'
        WHERE
            id = :client_id
    """,
    "count_commandes": """
        SELECT 
            Count(id)
        FROM
            Commandes
    """,
    "delete_commande": """
        DELETE FROM
            Commandes 
        WHERE
            id = :commande_id
    """
}


def get_db_connection(db_name='my_db.db'):
    """
    :param db_name: Name of the database file to connect to. Defaults to 'my_db.db'.
    :return: A tuple containing the database connection and the cursor.
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    return connection, cursor


def create_tables(cursor):
    """
    :param cursor: The cursor used to interact with the database.
    :return: None
    """
    cursor.execute(SQL_REQUESTS["create_clients_table"])
    cursor.execute(SQL_REQUESTS["create_commandes_table"])


def insert_client(cursor, client_data):
    """
    :param cursor: Database cursor object to execute the SQL query.
    :param client_data: Dictionary containing the data of the client to be inserted.
    :return: The ID of the last row inserted into the database.
    """
    cursor.execute(SQL_REQUESTS["insert_client"], client_data)
    return cursor.lastrowid


def insert_commandes(cursor, client_id, produits):
    """
    :param cursor: Database cursor object to execute SQL queries.
    :param client_id: ID of the client placing the order.
    :param produits: List of products being ordered.
    :return: The ID of the last row inserted.
    """
    for produit in produits:
        commande_data = {"client_id": client_id, "produit": produit}
        cursor.execute(SQL_REQUESTS["insert_commande"], commande_data)
    return cursor.lastrowid


def fetch_all_clients(cursor):
    """
    :param cursor: Database cursor object used to execute SQL commands.
    :return: A list of all client records retrieved from the database.
    """
    cursor.execute(SQL_REQUESTS["get_clients"])
    return cursor.fetchall()


def fetch_commandes_by_client_id(cursor, client_id):
    """
    :param cursor: Database cursor object to interact with the database.
    :param client_id: The ID of the client whose order information is being fetched.
    :return: List of orders associated with the given client ID.
    """
    cursor.execute(SQL_REQUESTS["get_commandes_by_client_id"], {"client_id": client_id})
    return cursor.fetchall()


def update_email(cursor, client_id):
    """
    :param cursor: Database cursor for executing SQL commands.
    :param client_id: The unique identifier of the client whose email is to be updated.
    :return: None
    """
    cursor.execute(SQL_REQUESTS["update_client_email"], {"client_id": client_id})


def fetch_commandes_count(cursor):
    """
    :param cursor: Database cursor object used to execute SQL queries.
    :return: The total number of commandes fetched from the database.
    """
    cursor.execute(SQL_REQUESTS["count_commandes"])
    return cursor.fetchone()[0]


def delete_commande(cursor, commande_id):
    """
    :param cursor: The database cursor used to execute SQL commands.
    :param commande_id: The unique identifier of the command to be deleted.
    :return: None
    """
    cursor.execute(SQL_REQUESTS["delete_commande"], {"commande_id": commande_id})


def fetch_table_data(table_name):
    """
    :param table_name: The name of the table from which to fetch data.
    :return: A tuple containing the table header (list of column names) and rows of data (list of tuples).
    """
    connection, cursor = get_db_connection()
    cursor.execute(f'SELECT * FROM {table_name}')
    header = [row[0] for row in cursor.description]
    rows = cursor.fetchall()
    connection.close()
    return header, rows


def export_table_to_csv(table_name):
    """
    :param table_name: The name of the table to export from the database.
    :return: None
    """
    header, rows = fetch_table_data(table_name)
    with open(f'{table_name}.csv', 'w') as f:
        f.write(','.join(header) + '\n')
        for row in rows:
            f.write(','.join(str(r) for r in row) + '\n')
    print(f'{len(rows)} rows written successfully to {table_name}.csv')

def insert_clients_commandes():
    """
    Inserts client records into the database and assigns commandes (orders) to each client.

    :return: None
    """
    global client
    clients_data = [
        {"nom": "NOM1", "prenom": "PRENOM1", "email": "nom1.prenom1@ici.la", "date_inscription": "2020-09-01"},
        {"nom": "NOM2", "prenom": "PRENOM2", "email": "nom2.prenom2@ici.la", "date_inscription": "2023-10-01"}
    ]
    for client in clients_data:
        last_client_id = insert_client(db_cursor, client)
        produits = [f"produit{last_client_id}", f"produit{last_client_id + 1}"]
        insert_commandes(db_cursor, last_client_id, produits)
    db_connection.commit()

def print_clients():
    """
    Fetches all clients from the database and prints each client's details.

    :return: None
    :rtype: None
    """
    global clients, client
    clients = fetch_all_clients(db_cursor)
    for client in clients:
        print(client)

def update_email_client():
    """
    Updates the email address of a randomly selected client and commits the changes to the database.

    :return: None
    """
    nb_clients = len(clients)
    random_client_id = random.randint(1, nb_clients)
    print('random client id = ' + str(random_client_id))
    commandes = fetch_commandes_by_client_id(db_cursor, random_client_id)
    for commande in commandes:
        print(commande)
    update_email(db_cursor, random_client_id)
    db_connection.commit()

# Initialisation de la base de données et création des tables
db_connection, db_cursor = get_db_connection()
create_tables(db_cursor)

# Insertion de clients et commandes
insert_clients_commandes()

# Affichage des clients
print_clients()

# Sélection et mise à jour de l'email d'un client aléatoire
update_email_client()


def delete_random_commande():
    """
    delete_random_commande
    Deletes a randomly selected order from the database.

    :return: None
    """
    nb_commandes = fetch_commandes_count(db_cursor)
    random_commande_id = random.randint(1, nb_commandes)
    delete_commande(db_cursor, random_commande_id)
    print('delete commande with id = ' + str(random_commande_id))
    db_connection.commit()


# Suppression d'une commande aléatoire
delete_random_commande()

db_connection.close()

# Exportation des tables
export_table_to_csv('Clients')
export_table_to_csv('Commandes')
