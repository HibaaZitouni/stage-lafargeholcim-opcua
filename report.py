# report.py
import sqlite3
from fpdf import FPDF
from datetime import datetime
from config import DB_FILE

def generate_daily_report():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("""
        SELECT e.date_heure, v.nom_variable, e.evenement, e.alarme
        FROM evenements e
        JOIN variables v ON e.variable_id = v.id
        WHERE date_heure LIKE ?
    """, (today + "%",))
    rows = c.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Rapport Journalier - {today}", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, "Liste des événements :", ln=True)

    if rows:
        for row in rows:
            date, variable, evenement, alarme = row
            statut = "🚨 ALARME" if alarme == 1 else "OK"
            texte = f"[{date}] {variable} - {evenement} - {statut}"
            pdf.multi_cell(0, 10, texte)  # ✅ utilise multi_cell pour gérer le retour à la ligne
    else:
        pdf.cell(0, 10, "Aucun événement aujourd’hui.", ln=True)

    filename = f"rapport_{today}.pdf"
    pdf.output(filename)
    return filename
