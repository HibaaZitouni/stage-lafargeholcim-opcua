# ui.py
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import subprocess
import threading

from database import get_active_variables, init_db, ensure_example_data
from surveillance import Surveillance
from report import generate_daily_report


class SurveillanceUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🟢 Application de Surveillance Industrielle")
        self.root.geometry("1000x600")

        self.tree = ttk.Treeview(
            root,
            columns=("Nom", "Adresse OPC", "Valeur", "Seuil Min", "Seuil Max", "Alarme"),
            show="headings",
            height=20
        )
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Adresse OPC", text="Adresse OPC")
        self.tree.heading("Valeur", text="Valeur actuelle")
        self.tree.heading("Seuil Min", text="Min")
        self.tree.heading("Seuil Max", text="Max")
        self.tree.heading("Alarme", text="Alarme")

        self.tree.column("Nom", width=170)
        self.tree.column("Adresse OPC", width=220)
        self.tree.column("Valeur", width=120)
        self.tree.column("Seuil Min", width=90, anchor="center")
        self.tree.column("Seuil Max", width=90, anchor="center")
        self.tree.column("Alarme", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.surv = Surveillance(interval=5)

        self.menu_button = tk.Button(root, text="🔔", font=("Arial", 18), bg="lightblue", command=self.show_menu)
        self.menu_button.place(relx=1.0, rely=1.0, x=-60, y=-60, anchor="se", width=50, height=50)

        self.update_table()
        self.auto_refresh()

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        variables = get_active_variables()
        for var in variables:
            (
                var_id, nom_variable, adresse_opc, description,
                vtype, vmin, vmax, last_value, last_update,
                alarme_min, alarme_max
            ) = var

            valeur_txt = f"{last_value:.2f}" if last_value is not None else "-"
            alarme_txt = "ACTIVE" if (
                (last_value is not None and last_value < vmin) or
                (last_value is not None and last_value > vmax)
            ) else "OK"

            self.tree.insert("", "end", iid=var_id,
                             values=(nom_variable, adresse_opc, valeur_txt, vmin, vmax, alarme_txt))
            if alarme_txt == "ACTIVE":
                self.tree.item(var_id, tags=("alarme",))
        self.tree.tag_configure("alarme", background="red", foreground="white")

    def auto_refresh(self):
        self.update_table()
        self.root.after(3000, self.auto_refresh)

    def show_menu(self):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="▶️ Activer Surveillance", command=self.start_surveillance)
        menu.add_command(label="⏹ Désactiver Surveillance", command=self.stop_surveillance)
        menu.add_command(label="📑 Générer Rapport", command=self.show_report)
        menu.add_command(label="➕ Ajouter un Élément", command=self.add_variable)
        menu.add_command(label="🌐 Accéder Dashboard", command=self.open_dashboard)
        try:
            menu.tk_popup(self.menu_button.winfo_rootx(), self.menu_button.winfo_rooty() - 10)
        finally:
            menu.grab_release()

    def start_surveillance(self):
        self.surv.start()
        messagebox.showinfo("Surveillance", "✅ Surveillance activée")

    def stop_surveillance(self):
        self.surv.stop()
        messagebox.showinfo("Surveillance", "🛑 Surveillance arrêtée")

    def show_report(self):
        try:
            filename = generate_daily_report()
            messagebox.showinfo("Rapport", f"📑 Rapport généré : {filename}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de générer le rapport : {e}")

    def add_variable(self):
        """Ajout manuel d’une variable avec un petit formulaire."""
        form = tk.Toplevel(self.root)
        form.title("Ajouter une variable")

        labels = ["Nom", "Adresse OPC", "Description", "Type (reel/bool)", "Seuil Min", "Seuil Max", "Valeur initiale"]
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(form, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(form)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[label] = entry

        def valider():
            try:
                nom = entries["Nom"].get()
                adresse = entries["Adresse OPC"].get()
                desc = entries["Description"].get()
                vtype = entries["Type (reel/bool)"].get().strip().lower()
                vmin = float(entries["Seuil Min"].get())
                vmax = float(entries["Seuil Max"].get())
                val_init = float(entries["Valeur initiale"].get())

                from database import insert_variable
                insert_variable(nom, adresse, desc, vtype, vmin, vmax, val_init)

                self.update_table()
                messagebox.showinfo("Ajout", f"✅ Variable {nom} ajoutée avec succès")
                form.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d’ajouter la variable : {e}")

        tk.Button(form, text="Valider", command=valider).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def open_dashboard(self):
        cmd = ["python", "-m", "streamlit", "run", "dashboard.py"]
        threading.Thread(target=lambda: subprocess.run(cmd), daemon=True).start()


if __name__ == "__main__":
    init_db()
    ensure_example_data()
    root = tk.Tk()
    app = SurveillanceUI(root)
    root.mainloop()
