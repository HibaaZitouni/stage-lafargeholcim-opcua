# database.py
import sqlite3
from datetime import datetime, timedelta
from config import DB_FILE

# -------- Connexion --------
def get_connection():
    return sqlite3.connect(DB_FILE)

# -------- Initialisation des tables --------
def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS variables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_variable TEXT,
        adresse_opc TEXT,
        description TEXT,
        type TEXT,
        min REAL,
        max REAL,
        last_value REAL,
        last_update TEXT,
        alarme_min INTEGER DEFAULT 0,
        alarme_max INTEGER DEFAULT 0
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS etats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        designation TEXT,
        activation INTEGER
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS evenements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_heure TEXT,
        variable_id INTEGER,
        evenement TEXT,
        alarme INTEGER,
        FOREIGN KEY(variable_id) REFERENCES variables(id)
    )
    """)
    conn.commit()
    conn.close()

# -------- Données d’exemple --------
def ensure_example_data():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM variables")
    c.execute("DELETE FROM etats")
    c.execute("DELETE FROM evenements")

    exemples = [
        ("TempFour1", "ns=2;s=Fours.Four1.Temp", "Température palier Four 1", "reel", 40.0, 85.5, 95.0, 0, 1),
        ("EtatConvoyeur1", "ns=2;s=Convoyeur1.Run", "État de marche du Convoyeur 1", "bool", 1, 1, 0, 1, 0)
    ]

    now = datetime.now()
    for i, (nom, adresse, desc_, vtype, vmin, vmax, val, a_min, a_max) in enumerate(exemples):
        c.execute("""
            INSERT INTO variables
            (nom_variable, adresse_opc, description, type, min, max, last_value, last_update, alarme_min, alarme_max)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), ?, ?)
        """, (nom, adresse, desc_, vtype, vmin, vmax, val, a_min, a_max))
        var_id = c.lastrowid
        if val < vmin or val > vmax:
            event_time = (now - timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S")
            c.execute("""
                INSERT INTO evenements (date_heure, variable_id, evenement, alarme)
                VALUES (?, ?, 'Alarme simulée', 1)
            """, (event_time, var_id))

    etats = [("SurveillanceGlobale", 1), ("Four1", 1), ("BC2", 1), ("BK3", 1)]
    for designation, activation in etats:
        c.execute("INSERT INTO etats (designation, activation) VALUES (?, ?)", (designation, activation))

    conn.commit()
    conn.close()

# -------- Fonctions utilitaires --------
def get_active_variables():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM variables")
    rows = c.fetchall()
    conn.close()
    return rows

def update_variable(var_id, value):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE variables
        SET last_value=?, last_update=?
        WHERE id=?
    """, (value, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), var_id))
    conn.commit()
    conn.close()

def log_event(var_id, evenement, alarme):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO evenements (date_heure, variable_id, evenement, alarme)
        VALUES (?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), var_id, evenement, alarme))
    conn.commit()
    conn.close()

def reset_alarm(event_id: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE evenements SET alarme = 0 WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

def acquit_alarme(var_id: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE variables SET alarme_min = 0, alarme_max = 0 WHERE id = ?", (var_id,))
    c.execute("""
        UPDATE evenements
        SET alarme = 0, evenement = 'Alarme acquittée'
        WHERE variable_id = ? AND alarme = 1
    """, (var_id,))
    conn.commit()
    conn.close()

# -------- Nouvelle fonction --------
def insert_variable(nom, adresse, description, vtype, vmin, vmax, valeur_init, a_min=0, a_max=0):
    """Ajoute une nouvelle variable dans la base et retourne son id."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO variables
        (nom_variable, adresse_opc, description, type, min, max, last_value, last_update, alarme_min, alarme_max)
        VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), ?, ?)
    """, (nom, adresse, description, vtype, vmin, vmax, valeur_init, a_min, a_max))
    conn.commit()
    var_id = c.lastrowid
    conn.close()
    return var_id

# -------- Exécution directe --------
if __name__ == "__main__":
    init_db()
    ensure_example_data()
    print("✅ Base de données initialisée + exemples forcés avec alarmes")
