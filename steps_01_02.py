import tkinter as tk
from tkinter import ttk, messagebox

class Steps01_02:
    """
    Étapes 1 & 2 du wizard :
      1. step_keys / validate_keys
      2. step_type_livraison / validate_type_livraison
    """

    def step_keys(self):
        content = ttk.Frame(self.main_frame)
        # expand=True sans fill → le frame est centré horizontalement et verticalement
        content.pack(expand=True, padx=60, pady=20)

        # Titre
        ttk.Label(
            content,
            text="Veuillez saisir le code client de l'établissement",
            font=('Helvetica', 16, 'bold')
        ).pack(pady=(10, 20))

        # Champ de saisie unique
        self.entry_key = ttk.Entry(content, width=40, justify='center')
        self.entry_key.pack(pady=(0, 15))
        # Restaurer si déjà saisi
        if self.data.get("clefs"):
            self.entry_key.insert(0, self.data["clefs"][0])

        # Navigation
        nav = ttk.Frame(content)
        nav.pack(pady=12, anchor="center")
        ttk.Button(nav, text="Suivant", command=self.validate_keys).pack(side="left", padx=6)

    def validate_keys(self):
        key = self.entry_key.get().strip()
        if not key:
            messagebox.showerror("Erreur", "Merci de saisir la clef unique.")
            return
        # stocke sous forme de liste pour compatibilité
        self.data["clefs"] = [key]
        self.next_step()

    def step_type_livraison(self):
        content = ttk.Frame(self.main_frame)
        content.pack(expand=True, padx=60, pady=20)

        ttk.Label(
            content,
            text="Sélectionnez le type de livraison :",
            font=('Helvetica', 14, 'bold')
        ).grid(row=0, column=0, pady=(0,10))
        content.columnconfigure(0, weight=1)

        options = [
            "Complète",
            "Prise de vue en binôme (je livre une partie de l'établissement)",
            "Un reliquat"
        ]
        val = self.data.get("type_livraison", options[0])
        self.var_livraison = tk.StringVar(value=val)

        for i, opt in enumerate(options, start=1):
            ttk.Radiobutton(
                content,
                text=opt,
                variable=self.var_livraison,
                value=opt
            ).grid(row=i, column=0, sticky="w", pady=4)

        nav = ttk.Frame(content)
        nav.grid(row=len(options)+1, column=0, pady=(20,0))
        ttk.Button(nav, text="Précédent", command=self.prev_step).pack(side="left", padx=6)
        ttk.Button(nav, text="Suivant", command=self.validate_type_livraison).pack(side="left", padx=6)

    def validate_type_livraison(self):
        selected = self.var_livraison.get()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner une option.")
            return
        self.data["type_livraison"] = selected
        self.next_step()