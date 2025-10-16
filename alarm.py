# alarm.py
import threading
import tkinter as tk
from tkinter import messagebox
import pyttsx3

# On importe ici pour pouvoir acquitter juste après le clic "OK"
from database import acquit_alarme


class AlarmManager:
    def __init__(self):
        # Init TTS (hors thread UI)
        self.engine = pyttsx3.init()
        # Petit réglage de voix/volume si tu veux
        try:
            self.engine.setProperty("rate", 180)
            self.engine.setProperty("volume", 1.0)
        except Exception:
            pass

    def _speak(self, text: str):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            # On n'échoue pas la logique si la synthèse vocale a un souci
            pass

    def trigger_alarm(self, message: str, variable_id: int | None = None):
        """
        Affiche un pop-up bloquant (warning) et lance la synthèse vocale en parallèle.
        Si l'utilisateur clique OK et que variable_id est fourni, on acquitte en DB.
        """
        # Voix en arrière-plan
        threading.Thread(target=self._speak, args=(message,), daemon=True).start()

        # Pop-up bloquant depuis un mini root isolé
        root = tk.Tk()
        root.withdraw()
        response = messagebox.showwarning("ALERTE CRITIQUE", message, parent=root)
        root.destroy()

        # Après clic OK → acquittement automatique
        if response == "ok" and variable_id is not None:
            try:
                acquit_alarme(variable_id)
            except Exception:
                pass
