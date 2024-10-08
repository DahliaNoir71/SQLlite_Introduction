# Introduction to SQLite with Python

Ce projet contient un script Python `sqlite.py` qui démontre l'utilisation de SQLite pour la gestion d'une base de données simple. Le script inclut des exemples de création de tables, insertion de données, récupération de données, mise à jour et suppression de données.

## Prérequis

- Python 3.12.7
- SQLite3 (inclus avec la plupart des distributions Python)

## Installation

1. Clonez ce dépôt :
    ```sh
    git clone <URL_DU_DEPOT>
    cd introductionSQLite
    ```

2. Assurez-vous d'avoir `sqlite3` installé. Vous pouvez vérifier cela avec la commande suivante :
    ```sh
    python -m sqlite3
    ```

## Utilisation

Le script `sqlite.py` inclut les fonctions suivantes :

- **Connexion à la base de données :**
    ```python
    def get_db_connection()
    ```
  
- **Création des tables :**
    ```python
    def create_tables()
    ```

- **Insertion de données dans la table clients :**
    ```python
    def insert_client()
    ```
  
- **Insertion de données dans la table commandes :**
    ```python
    def insert_commandes()
    ```

- **Récupération de tous les clients :**
    ```python
    def fetch_all_clients()
    ```

- **Récupération des commandes par identifiant client :**
    ```python
    def fetch_commandes_by_client_id(client_id)
    ```

- **Mise à jour de l'email d'un client :**
    ```python
    def update_email(client_id, new_email)
    ```
  
- **Récupération du nombre de commandes :**
    ```python
    def fetch_commandes_count()
    ```

- **Suppression d'une commande :**
    ```python
    def delete_commande(commande_id)
    ```

- **Récupération des données d'une table spécifique :**
    ```python
    def fetch_table_data(table_name)
    ```

- **Exportation des données d'une table en CSV :**
    ```python
    def export_table_to_csv(table_name)
    ```

- **Insertion de clients aléatoires :**
    ```python
    def insert_random_clients(n)
    ```

- **Génération d'une date/heure aléatoire :**
    ```python
    def gen_datetime()
    ```

- **Récupération de clients aléatoires :**
    ```python
    def get_random_clients(n)
    ```

- **Mise à jour de l'email d'un client aléatoire :**
    ```python
    def update_email_client(client_id)
    ```

- **Suppression d'une commande aléatoire :**
    ```python
    def delete_random_commande(commande_id)
    ```

- **Exportation de toutes les tables en CSV :**
    ```python
    def export_tables_to_csv()
    ```

## Comment exécuter le script

Pour exécuter le script, lancez la commande suivante dans votre terminal :
```sh
python sqlite.py
```

## Auteurs

- [Votre Nom](https://github.com/votrenom)

## License

Ce projet est sous licence MIT - voir le fichier [LICENSE](./LICENSE) pour plus de détails.