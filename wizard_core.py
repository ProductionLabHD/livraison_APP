# wizard_core.py

import os
import sys
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from network_utils    import check_internet
from steps_01_02      import Steps01_02
from steps_03_04      import Steps03_04
from steps_05_06      import Steps05_06
from steps_07_08      import Steps07_08
from steps_09_final   import Steps09_Final

BASE_DIR = os.path.expanduser("~/Desktop/ECOLE_A_TRAITER")

class LivraisonWizard(
    tk.Tk,
    Steps01_02,
    Steps03_04,
    Steps05_06,
    Steps07_08,
    Steps09_Final
):
    """
    Classe principale de la wizard : hérite des mixins StepsXX,  
    gère l'affichage, la navigation, et l'affichage du logo.
    """

    def __init__(self):
        super().__init__()

        # —————— DÉCLARATION DE LA POLICE PAR DÉFAUT ——————
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="Lexend", size=11)
        bold_font = tkfont.Font(family="Lexend", size=16, weight="bold")

        # Applique Lexend partout
        self.option_add("*TLabel.Font",    default_font)
        self.option_add("*TButton.Font",   default_font)
        self.option_add("*TEntry.Font",    default_font)
        self.option_add("*TRadiobutton.Font", default_font)
        self.option_add("*TCheckbutton.Font", default_font)
        # Pour les titres de section
        self.option_add("*Label.Font", bold_font)
        # ————————————————————————————————————————————————

        self.title("Livraison Photo - LAB HD")
        self.geometry("1500x900")
        self.resizable(False, False)

        # --- Chargement et redimensionnement du logo sans déformation ---
        base = os.path.expanduser("~/Desktop/ECOLE_A_LIVRER")
        logo_path = os.path.join(base, "logo.png")
        self.logo_img = None

        if os.path.exists(logo_path):
            try:
                pil_img = Image.open(logo_path)
                max_w, max_h = 300, 200
                ratio = min(max_w / pil_img.width, max_h / pil_img.height)
                new_size = (int(pil_img.width * ratio), int(pil_img.height * ratio))
                pil_img = pil_img.resize(new_size, Image.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(pil_img)
            except Exception as e:
                messagebox.showwarning("Erreur logo", f"Échec chargement/logo : {e}")

        # Affichage du logo centré en haut
        if self.logo_img:
            logo_frame = ttk.Frame(self)
            logo_frame.pack(fill="x", pady=(30,10))
            ttk.Label(logo_frame, image=self.logo_img).pack(anchor="center")

        # Container pour les étapes
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.data = {}
        self.steps = [
            self.step_keys,
            self.step_type_livraison,
            self.step_photos_etablissement,
            self.step_photos_livrees,
            self.step_commentaires,
            self.step_retour_experience,
            self.step_id_photographe,
            self.step_recap,
            self.step_final,
        ]
        self.current_step = 0

        self.show_step()

    def clear_frame(self):
        """Détruit tous les widgets du main_frame."""
        for w in self.main_frame.winfo_children():
            w.destroy()

    def show_step(self):
        """Affiche l'étape courante."""
        self.clear_frame()
        self.steps[self.current_step]()

    def next_step(self):
        """Passe à l'étape suivante si possible."""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_step()

    def prev_step(self):
        """Retourne à l'étape précédente si possible."""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step()


def main():
    # Vérifie la connexion avant de lancer l'UI
    if not check_internet():
        messagebox.showerror(
            "Connexion Internet requise",
            "Impossible de démarrer l’application sans connexion Internet.\n"
            "Veuillez vous connecter et réessayer."
        )
        sys.exit(1)

    app = LivraisonWizard()
    app.mainloop()


if __name__ == "__main__":
    main()