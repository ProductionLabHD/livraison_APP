# steps_03_04.py

import tkinter as tk
from tkinter import ttk, messagebox

class Steps03_04:
    """
    Étapes 3 & 4 du wizard :
      3. step_photos_etablissement / validate_photos_etablissement
      4. step_photos_livrees / validate_photos_livrees
    """

    def step_photos_etablissement(self):
        # 1) Frame de contenu centrée dans la fenêtre
        content = ttk.Frame(self.main_frame)
        content.pack(expand=True, padx=60, pady=20)  # centré verticalement & horizontalement

        # 2) Titre centré en haut du content
        lbl = ttk.Label(
            content,
            text="Photos établissements",
            font=('Helvetica', 14, 'bold')
        )
        lbl.grid(row=0, column=0, pady=(0, 10))

        # 3) Configuration de la grille pour centrer la colonne 0
        content.columnconfigure(0, weight=1)

        # 4) Les options en Radiobutton (même colonne, alignées)
        options = [
            "J'ai bien pris en photos les bâtiments",
            "J'ai oublié de prendre en photos les bâtiments",
            "Les photos établissements sont livrées par un autre photographe (binôme)"
        ]
        val = self.data.get("photos_etablissement", options[0])
        self.var_photos_etab = tk.StringVar(value=val)

        for i, opt in enumerate(options, start=1):
            rb = ttk.Radiobutton(
                content,
                text=opt,
                variable=self.var_photos_etab,
                value=opt
            )
            rb.grid(row=i, column=0, sticky="w", pady=4)

        # 5) Barre de navigation centrée
        nav = ttk.Frame(content)
        nav.grid(row=len(options) + 1, column=0, pady=(20, 0))
        ttk.Button(nav, text="Précédent", command=self.prev_step).pack(side="left", padx=6)
        ttk.Button(nav, text="Suivant",   command=self.validate_photos_etablissement).pack(side="left", padx=6)

    def validate_photos_etablissement(self):
        """
        Valide et stocke le choix des photos d'établissement.
        """
        self.data["photos_etablissement"] = self.var_photos_etab.get()
        self.next_step()

    def step_photos_livrees(self):
        content = ttk.Frame(self.main_frame)
        content.pack(expand=True, padx=60, pady=20)

        ttk.Label(
            content,
            text="Sélectionnez les types de photos livrées :",
            font=('Helvetica', 14, 'bold')
        ).grid(row=0, column=0, pady=(0,10))
        content.columnconfigure(0, weight=1)

        options = [
            "Les photos de groupes Classique",
            "Les photos de groupe Fun",
            "Les photos individuelles",
            "Les photos de Fratries",
            "Portraits de professeur",
            "Photos d'équipes de professeur"
        ]
        selected = set(self.data.get("photos_livrees", []))
        self.vars_photos_livrees = []

        for i, opt in enumerate(options, start=1):
            var = tk.BooleanVar(value=(opt in selected))
            cb = ttk.Checkbutton(content, text=opt, variable=var)
            cb.grid(row=i, column=0, sticky="w", pady=4)
            self.vars_photos_livrees.append((opt, var))

        nav = ttk.Frame(content)
        nav.grid(row=len(options)+1, column=0, pady=(20,0))
        ttk.Button(nav, text="Précédent", command=self.prev_step).pack(side="left", padx=6)
        ttk.Button(nav, text="Suivant",   command=self.validate_photos_livrees).pack(side="left", padx=6)

    def validate_photos_livrees(self):
        """
        Valide et stocke la sélection des photos livrées.
        """
        selected = [opt for opt, var in self.vars_photos_livrees if var.get()]
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner au moins une option.")
            return
        # ←––––––––– AJOUT DEBUG
        print("[DEBUG] photos_livrees saisies :", selected)
        # ––––––––––––––––––––––––––––––––––––––––
        self.data["photos_livrees"] = selected
        self.next_step()