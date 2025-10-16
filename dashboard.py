# dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from config import DB_FILE

# Connexion DB
def get_data(query):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ---------------- Interface Streamlit ----------------
st.set_page_config(page_title="Dashboard Surveillance", layout="wide")

st.title("📊 Tableau de Bord - Application de Surveillance Industrielle")

# Onglets
tab1, tab2, tab3 = st.tabs(["📜 Historique", "📌 Variables", "📈 Statistiques"])

with tab1:
    st.subheader("Historique des événements")
    df = get_data("SELECT * FROM evenements ORDER BY date_heure DESC LIMIT 50")
    st.dataframe(df)

with tab2:
    st.subheader("Liste des variables surveillées")
    df = get_data("SELECT * FROM variables")
    st.dataframe(df)

with tab3:
    st.subheader("Statistiques sur les alarmes")

    alarms = get_data("SELECT * FROM evenements WHERE alarme=1")

    if alarms.empty:
        st.warning("⚠️ Aucune alarme détectée pour l’instant.")
    else:
        alarms["date_heure"] = pd.to_datetime(alarms["date_heure"])
        alarms["hour"] = alarms["date_heure"].dt.hour

        alarms_by_hour = alarms.groupby("hour").size()
        alarms_by_variable = alarms.groupby("variable_id").size()

        # ➡️ Organisation côte à côte
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📌 Alarmes par heure (Barres)")
            fig1, ax1 = plt.subplots(figsize=(4,3))
            alarms_by_hour.plot(kind="bar", ax=ax1)
            ax1.set_xlabel("Heure")
            ax1.set_ylabel("Nombre d'alarmes")
            st.pyplot(fig1)

        with col2:
            st.markdown("### ⚙️ Alarmes par variable (Camembert)")
            fig2, ax2 = plt.subplots(figsize=(4,3))
            alarms_by_variable.plot(kind="pie", ax=ax2, autopct="%1.1f%%")
            ax2.set_ylabel("")  # enlève le label inutile sur l’axe Y
            st.pyplot(fig2)
