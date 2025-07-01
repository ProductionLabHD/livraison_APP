# run_all.py

import sys
import tkinter.messagebox as msg

# On importe tous vos modules, pour s'assurer qu'ils sont chargés
import network_utils
import file_utils
import wizard_core
import steps_01_02
import steps_03_04
import steps_05_06
import steps_07_08
import steps_09_final

# On prend les fonctions/classes principales
from network_utils import check_internet
from wizard_core import LivraisonWizard

def main():
    # 1) Vérification Internet
    if not check_internet():
        msg.showerror(
            "Connexion Internet requise",
            "Impossible de démarrer l’application sans connexion Internet.\n"
            "Veuillez vous connecter et réessayer."
        )
        sys.exit(1)
    # 2) Démarrage du wizard
    app = LivraisonWizard()
    app.mainloop()

if __name__ == "__main__":
    main()