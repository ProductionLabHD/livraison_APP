# main.py

import sys
import tkinter.messagebox as msg

from network_utils import check_internet
from wizard_core   import LivraisonWizard

def main():
    if not check_internet():
        msg.showerror(
            "Connexion Internet requise",
            "Impossible de démarrer l’application sans connexion Internet.\n"
            "Veuillez vous connecter et réessayer."
        )
        sys.exit(1)

    app = LivraisonWizard()
    app.mainloop()

if __name__ == "__main__":
    main()