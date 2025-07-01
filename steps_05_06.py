# steps_05_06.py

import tkinter as tk
from tkinter import ttk, messagebox

class Steps05_06:
    """
    Étapes 5 & 6 du wizard :
      5. step_commentaires / validate_commentaires
      6. step_retour_experience / validate_retour_experience
    """

    def step_commentaires(self):
        """
        Affiche l'étape de saisie des commentaires de la livraison,
        centré horizontalement et verticalement.
        """
        content = ttk.Frame(self.main_frame)
        content.pack(expand=True, padx=60, pady=20)

        # Titre
        ttk.Label(
            content,
            text="Commentaire infos",
            font=('Helvetica', 14, 'bold')
        ).grid(row=0, column=0, pady=(0, 10))
        content.columnconfigure(0, weight=1)

        # Sous-titre / instruction
        ttk.Label(
            content,
            text="Donne-nous des informations sur ta livraison, les photos, des infos pour la production ?"
        ).grid(row=1, column=0, pady=(0, 10))

        # Zone de texte
        self.text_commentaires = tk.Text(content, width=62, height=4, font=('Helvetica', 10))
        self.text_commentaires.grid(row=2, column=0, pady=(0, 20))
        if self.data.get("commentaires"):
            self.text_commentaires.insert("1.0", self.data["commentaires"])

        # Navigation
        nav = ttk.Frame(content)
        nav.grid(row=3, column=0)
        ttk.Button(nav, text="Précédent", command=self.prev_step).pack(side="left", padx=6)
        ttk.Button(nav, text="Suivant",   command=self.validate_commentaires).pack(side="left", padx=6)

    def validate_commentaires(self):
        """
        Valide et stocke les commentaires saisis.
        """
        text = self.text_commentaires.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Erreur", "Merci de renseigner ce champ.")
            return
        self.data["commentaires"] = text
        self.next_step()

    def step_retour_experience(self):
        """
        Affiche l'étape de retour d'expérience du photographe,
        centré horizontalement et verticalement.
        """
        content = ttk.Frame(self.main_frame)
        content.pack(expand=True, padx=60, pady=20)

        # Titre
        ttk.Label(
            content,
            text="Retour d'expérience",
            font=('Helvetica', 14, 'bold')
        ).grid(row=0, column=0, pady=(0, 10))
        content.columnconfigure(0, weight=1)

        # Instruction
        ttk.Label(
            content,
            text="Fais-nous un retour sur ton expérience du jour..."
        ).grid(row=1, column=0, pady=(0, 10))

        # Zone de texte
        self.text_retour = tk.Text(content, width=62, height=4, font=('Helvetica', 10))
        self.text_retour.grid(row=2, column=0, pady=(0, 20))
        if self.data.get("retour_experience"):
            self.text_retour.insert("1.0", self.data["retour_experience"])

        # Navigation
        nav = ttk.Frame(content)
        nav.grid(row=3, column=0)
        ttk.Button(nav, text="Précédent", command=self.prev_step).pack(side="left", padx=6)
        ttk.Button(nav, text="Suivant",   command=self.validate_retour_experience).pack(side="left", padx=6)

    def validate_retour_experience(self):
        """
        Valide et stocke le retour d'expérience saisi.
        """
        text = self.text_retour.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Erreur", "Merci de renseigner ce champ.")
            return
        self.data["retour_experience"] = text
        self.next_step()