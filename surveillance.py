# surveillance.py
import threading
import time
import random
from database import get_active_variables, update_variable, log_event, acquit_alarme
from alarm import AlarmManager


class Surveillance:
    def __init__(self, interval=10):
        self.interval = interval
        self.running = False
        self.thread = None
        self.alarm_manager = AlarmManager()

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def run(self):
        while self.running:
            variables = get_active_variables()
            for var in variables:
                (
                    var_id, nom_variable, adresse_opc, description,
                    vtype, vmin, vmax, last_value, last_update,
                    alarme_min, alarme_max
                ) = var

                # --- GÉNÉRATION DE VALEUR ---
                new_value = self.simulate_value(vmin, vmax)

                # --- MISE À JOUR DB ---
                update_variable(var_id, new_value)

                # --- CONTRÔLE DE SEUILS ---
                if new_value < vmin:
                    log_event(var_id, "min", 1)
                    self.alarm_manager.trigger_alarm(
                        f"Alerte : {nom_variable} sous le seuil ({new_value:.2f} < {vmin}) !",
                        variable_id=var_id
                    )
                elif new_value > vmax:
                    log_event(var_id, "max", 1)
                    self.alarm_manager.trigger_alarm(
                        f"Alerte : {nom_variable} au-dessus du seuil ({new_value:.2f} > {vmax}) !",
                        variable_id=var_id
                    )
                else:
                    # Revenu normal → acquittement
                    acquit_alarme(var_id)

            time.sleep(self.interval)

    def simulate_value(self, vmin, vmax):
        """
        Simulation :
        - la plupart du temps entre 0.9*vmin et 1.1*vmax,
        - mais ~60% du temps, on force une sortie de seuil (alarme fréquente).
        """
        if random.random() < 0.6:
            if random.random() < 0.5:
                return vmin * random.uniform(0.6, 0.85)  # sous le min
            else:
                return vmax * random.uniform(1.15, 1.35)  # au-dessus du max
        return random.uniform(max(vmin * 0.9, vmin - 1), min(vmax * 1.1, vmax + 1))
