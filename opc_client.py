# opc_client.py
import random
import math
import time
from datetime import datetime

try:
    from opcua import Client
    OPCUA_AVAILABLE = True
except ImportError:
    OPCUA_AVAILABLE = False

from config import OPC_SERVER_URL


class OPCClient:
    """
    Client OPC UA simulé ou réel.
    - Si le serveur OPC UA est accessible → lecture réelle
    - Sinon → simulation avec données aléatoires réalistes
    """

    def __init__(self, server_url=OPC_SERVER_URL):
        self.server_url = server_url
        self.client = None
        self.simulation_mode = False
        self.t0 = time.time()

    def connect(self):
        if OPCUA_AVAILABLE:
            try:
                self.client = Client(self.server_url)
                self.client.connect()
                print(f"✅ Connecté au serveur OPC UA : {self.server_url}")
                self.simulation_mode = False
                return
            except Exception as e:
                print(f"⚠️ Impossible de se connecter au serveur OPC UA ({e}), passage en mode simulation.")
        else:
            print("⚠️ Bibliothèque opcua non installée → passage en mode simulation.")

        self.simulation_mode = True

    def disconnect(self):
        if self.client:
            try:
                self.client.disconnect()
                print("🔌 Déconnecté du serveur OPC UA")
            except Exception as e:
                print(f"Erreur lors de la déconnexion : {e}")

    def read_variable(self, adresse_opc, nom_variable, vtype="reel"):
        """
        Lit une variable OPC UA ou retourne une valeur simulée.
        """
        if self.simulation_mode or not self.client:
            return self._simulate_value(nom_variable, vtype)

        try:
            node = self.client.get_node(adresse_opc)
            value = node.get_value()
            return value
        except Exception as e:
            print(f"⚠️ Erreur de lecture sur {nom_variable} ({adresse_opc}): {e}")
            return self._simulate_value(nom_variable, vtype)

    def _simulate_value(self, nom_variable, vtype="reel"):
        """
        Génère une valeur simulée :
        - TempFour1 → sinus autour de 60°C
        - PressionBC2 → valeurs normales autour de 3.0
        - VibrationBK3 → valeurs faibles, pics parfois
        - Booléens → alternance aléatoire
        """
        elapsed = time.time() - self.t0

        if vtype == "bool":
            return random.choice([0, 1])

        if "TempFour" in nom_variable:
            return 60 + 10 * math.sin(elapsed / 10) + random.uniform(-2, 2)

        if "Pression" in nom_variable:
            return 3.0 + random.uniform(-0.5, 0.5)

        if "Vibration" in nom_variable:
            return random.choice([0.2, 0.3, 0.5, 1.1, 1.3])

        # Valeur générique pour tout autre cas
        return random.uniform(0, 10)


# -------- Test en exécution directe --------
if __name__ == "__main__":
    client = OPCClient()
    client.connect()

    for _ in range(5):
        print("TempFour1 =", client.read_variable("ns=2;s=Fours.Four1.Temp", "TempFour1", "reel"))
        print("PressionBC2 =", client.read_variable("ns=2;s=BC2.Pression", "PressionBC2", "reel"))
        print("VibrationBK3 =", client.read_variable("ns=2;s=BK3.Vibration", "VibrationBK3", "reel"))
        print("ContactUrgence =", client.read_variable("ns=2;s=Urgence.Contact", "ContactUrgence", "bool"))
        time.sleep(1)

    client.disconnect()
