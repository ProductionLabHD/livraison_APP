# steps_07_08.py

import os
import tkinter as tk
from tkinter import ttk, messagebox

from file_utils import create_content_file, get_folder_file_counts

class Steps07_08:
    """
    Étapes 7 & 8 du wizard :
      7. step_id_photographe / validate_id_photographe
      8. step_recap
    """

    def step_id_photographe(self):
        """
        Affiche l'étape de saisie de l'identifiant photographe (2 chiffres),
        centré horizontalement et verticalement.
        """
        content = ttk.Frame(self.main_frame)
        content.pack(expand=True, padx=60, pady=20)

        # Titre
        ttk.Label(
            content,
            text="Mon identifiant photographe",
            font=('Helvetica', 14, 'bold')
        ).grid(row=0, column=0, pady=(0,10))
        content.columnconfigure(0, weight=1)

        # Instruction
        ttk.Label(
            content,
            text="Je tape les 2 chiffres"
        ).grid(row=1, column=0, pady=(0,10))

        # Champ de saisie
        self.entry_id = ttk.Entry(content, width=6, font=('Helvetica', 16), justify='center')
        self.entry_id.grid(row=2, column=0, pady=(0,20))
        if self.data.get("id_photographe"):
            self.entry_id.insert(0, self.data["id_photographe"])

        # Validation de la saisie (0 à 2 chiffres)
        def validate_num(P):
            return len(P) <= 2 and (P.isdigit() or P == "")
        vcmd = (self.register(validate_num), '%P')
        self.entry_id.config(validate="key", validatecommand=vcmd)

        # Navigation
        nav = ttk.Frame(content)
        nav.grid(row=3, column=0)
        ttk.Button(nav, text="Précédent", command=self.prev_step).pack(side="left", padx=6)
        ttk.Button(nav, text="Suivant",   command=self.validate_id_photographe).pack(side="left", padx=6)

    def validate_id_photographe(self):
        """
        Valide que l'identifiant contient exactement 2 chiffres et poursuit.
        """
        val = self.entry_id.get().strip()
        if not (val.isdigit() and len(val) == 2):
            messagebox.showerror("Erreur", "Merci de saisir 2 chiffres.")
            return
        self.data["id_photographe"] = val
        self.next_step()
    
    def step_recap(self):
        """
        Affiche le récapitulatif de la livraison au centre de la fenêtre,
        avec scroll si nécessaire.
        """
        # 1) Frame principal du récapitulatif, centré et dimensionné
        outer = ttk.Frame(self.main_frame)
        outer.place(
            relx=0.5, rely=0.5, anchor="center",
            relwidth=0.9, relheight=0.8
        )

        # 2) Canvas scrollable à l’intérieur de outer
        canvas = tk.Canvas(outer, borderwidth=0, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        vscroll = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        vscroll.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=vscroll.set)

        content = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=content, anchor="nw")
        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # 3) Titre
        ttk.Label(
            content,
            text="Récapitulatif de la livraison",
            font=('Helvetica', 16, 'bold')
        ).pack(pady=10)

        # 4) Tableau général
        tree_general = ttk.Treeview(
            content,
            columns=("champ", "valeur"),
            show='headings',
            height=7
        )
        tree_general.heading("champ", text="Champ")
        tree_general.heading("valeur", text="Informations")
        tree_general.column("champ", width=200, anchor='e')
        tree_general.column("valeur", width=800, anchor='w')
        for champ, valeur in [
            ("Clés uniques",            ", ".join(self.data.get("clefs", []))),
            ("Type de livraison",       self.data.get("type_livraison", "")),
            ("Photos établissements",   self.data.get("photos_etablissement", "")),
            ("Photos livrées",          ", ".join(self.data.get("photos_livrees", []))),
            ("Commentaires",            self.data.get("commentaires", "")),
            ("Retour d'expérience",     self.data.get("retour_experience", "")),
            ("Identifiant photographe", self.data.get("id_photographe", ""))
        ]:
            tree_general.insert('', 'end', values=(champ, valeur))
        tree_general.pack(fill='x', pady=(0, 20))

        # 5) Détails des Groupes (pour chaque client)
        ttk.Label(
            content,
            text="Détails des Groupes",
            font=('Helvetica', 14, 'bold')
        ).pack(pady=(0, 6), anchor='w')

        tree_gb = ttk.Treeview(
            content,
            columns=("classe", "total", "GRCL", "GRFU"),
            show='headings',
            height=8
        )
        for col, txt, w in [
            ("classe", "Classe", 200),
            ("total", "Total fichiers", 120),
            ("GRCL", "GRCL", 100),
            ("GRFU", "GRFU", 100)
        ]:
            tree_gb.heading(col, text=txt, anchor='center')
            tree_gb.column(col, width=w, anchor='center')

        # nouveau : parcours de tous les dossiers clients
        base_parent = os.path.expanduser("~/Desktop/ECOLE_A_LIVRER")
        client_dirs = [
            os.path.join(base_parent, d)
            for d in os.listdir(base_parent)
            if os.path.isdir(os.path.join(base_parent, d))
        ]

        # recherche des sous-dossiers *_GROUPE_BRUT*
        group_dirs = []
        for client in client_dirs:
            for entry in os.listdir(client):
                if entry.upper().endswith("_GROUPE_BRUT"):
                    group_dirs.append(os.path.join(client, entry))

        # insertion dans le Treeview
        for groupe_dir in group_dirs:
            for classe in sorted(os.listdir(groupe_dir)):
                class_path = os.path.join(groupe_dir, classe)
                if not os.path.isdir(class_path):
                    continue

                total = sum(len(files) for _, _, files in os.walk(class_path))
                grcl = len(os.listdir(os.path.join(class_path, 'GRCL'))) \
                    if os.path.isdir(os.path.join(class_path, 'GRCL')) else 0
                grfu = len(os.listdir(os.path.join(class_path, 'GRFU'))) \
                    if os.path.isdir(os.path.join(class_path, 'GRFU')) else 0

                tag = 'zero' if total == 0 else ''
                tree_gb.insert(
                    '', 'end',
                    values=(classe, total, grcl, grfu),
                    tags=(tag,)
                )

        tree_gb.tag_configure('zero', foreground='red')
        tree_gb.pack(fill='x', pady=(0, 20))

        # 6) Détails des Individuelles (pour chaque client)
        ttk.Label(
            content,
            text="Détails des Individuelles",
            font=('Helvetica', 14, 'bold')
        ).pack(pady=(0, 6), anchor='w')

        tree_indiv = ttk.Treeview(
            content,
            columns=("classe", "nb_eleves"),
            show='headings',
            height=6
        )
        tree_indiv.heading("classe", text="Classe", anchor='center')
        tree_indiv.column("classe", width=300, anchor='center')
        tree_indiv.heading("nb_eleves", text="Nombre d'élèves", anchor='center')
        tree_indiv.column("nb_eleves", width=120, anchor='center')

        # recherche des sous-dossiers *_HAUTES_RESOLUTIONS*
        indiv_dirs = []
        for client in client_dirs:
            for entry in os.listdir(client):
                if entry.upper().endswith("_HAUTES_RESOLUTIONS"):
                    indiv_dirs.append(os.path.join(client, entry))

        # insertion dans le Treeview
        for haute_dir in indiv_dirs:
            for classe in sorted(os.listdir(haute_dir)):
                class_path = os.path.join(haute_dir, classe)
                if not os.path.isdir(class_path):
                    continue
                nb = len([
                    f for f in os.listdir(class_path)
                    if os.path.isfile(os.path.join(class_path, f))
                ])
                tree_indiv.insert('', 'end', values=(classe, nb))

        tree_indiv.pack(fill='x', pady=(0, 20))


        # --- Détails du master ---
        ttk.Label(
            content,
            text="Détails du master",
            font=('Helvetica', 14, 'bold')
        ).pack(pady=(0, 6), anchor='w')

        tree_master = ttk.Treeview(
            content,
            columns=("client", "nb_files"),
            show='headings',
            height=6
        )
        # Colonne de gauche : nom du dossier client (appelé "Master")
        tree_master.heading("client", text="Master", anchor='w')
        tree_master.column("client", width=300, anchor='w')
        # Colonne de droite : nombre de fichiers
        tree_master.heading("nb_files", text="Nombre de Fichiers", anchor='center')
        tree_master.column("nb_files", width=120, anchor='center')

                # Parcours de tous les dossiers-client sous ECOLE_A_LIVRER
        base_parent = os.path.expanduser("~/Desktop/ECOLE_A_LIVRER")
        for client in sorted(os.listdir(base_parent)):
            client_dir = os.path.join(base_parent, client)
            if not os.path.isdir(client_dir):
                continue

            # 1) On cherche le dossier *_LABORATOIRE*
            labo_name = next(
                (d for d in os.listdir(client_dir)
                 if os.path.isdir(os.path.join(client_dir, d))
                    and d.upper().endswith("_LABORATOIRE")),
                None
            )
            if not labo_name:
                continue
            labo_dir = os.path.join(client_dir, labo_name)

            # 2) À l’intérieur de XXX_LABORATOIRE, on prend son sous-dossier 'master'
            master_dir = os.path.join(labo_dir, "master")
            if not os.path.isdir(master_dir):
                continue

            # 3) Comptage des fichiers dans master/
            nb = sum(
                1 for f in os.listdir(master_dir)
                if os.path.isfile(os.path.join(master_dir, f))
            )

            # 4) On insère le nom du client et ce compte
            tree_master.insert('', 'end', values=(client, nb))

        tree_master.pack(fill='x', pady=(0, 20))

                # 7) Navigation
        nav = ttk.Frame(content)
        nav.pack(pady=18)
        ttk.Button(nav, text="Précédent", command=self.prev_step).pack(side="left", padx=6)
        ttk.Button(nav, text="Valider et envoyer", command=self.next_step).pack(side="left", padx=6)