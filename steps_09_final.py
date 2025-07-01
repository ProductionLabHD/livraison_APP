# steps_09_final.py

import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from file_utils import create_content_file
from gsheet_fill import fill_delivery

class Steps09_Final:
    """
    Étape 9 du wizard : génère le .txt, crée contenu.txt,
    trouve le code client et exporte vers Google Sheets
    (y compris colonnes R/S/T via fill_delivery).
    """

    def step_final(self):
        # 1) Recherche du code_client ET du dossier client_dir
        base_parent = os.path.expanduser("~/Desktop/ECOLE_A_LIVRER")
        code_client = None
        client_dir = None

        for client in os.listdir(base_parent):
            path_client = os.path.join(base_parent, client)
            if not os.path.isdir(path_client):
                continue
            for entry in os.listdir(path_client):
                if entry.upper().endswith("_GROUPE_BRUT"):
                    code_client = entry.split('_')[0]
                    client_dir  = path_client
                    break
            if code_client:
                break

        if not code_client or not client_dir:
            messagebox.showwarning(
                "Code client introuvable",
                "Aucun dossier *_GROUPE_BRUT* trouvé sous ECOLE_A_LIVRER."
            )
            return

        # 2) Génération du fichier de livraison local DANS client_dir
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"livraison_{timestamp}.txt"
        heure_finale = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        livraison_path = os.path.join(client_dir, filename)

        lines = [
            "Informations de livraison :",
            "",
            f"Heure de finalisation : {heure_finale}",
            "",
            "1. Clefs uniques :"
        ]
        for i, k in enumerate(self.data.get("clefs", []), start=1):
            lines.append(f"- Clef {i}: {k}")

        lines += [
            "",
            "2. Type de livraison :",
            f"- {self.data.get('type_livraison','')}",
            "",
            "3. Photos établissements :",
            f"- {self.data.get('photos_etablissement','')}",
            "",
            "4. Photos livrées :"
        ]
        for p in self.data.get("photos_livrees", []):
            lines.append(f"- {p}")

        lines += [
            "",
            "5. Commentaires :",
            self.data.get("commentaires",""),
            "",
            "6. Retour d'expérience :",
            self.data.get("retour_experience",""),
            "",
            f"7. Identifiant photographe : {self.data.get('id_photographe','')}"
        ]

        with open(livraison_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        # 3) Création de contenu.txt DANS client_dir
        create_content_file(output_dir=client_dir)

        # 4) Mapping pour Google Sheets
        livraison_map = {
            "Complète": "Livraison Complète",
            "Un reliquat": "Reliquat",
            "Prise de vue en binôme (je livre une partie de l'établissement)": "Prise de vue en binôme"
        }
        mapped_type = livraison_map.get(self.data["type_livraison"], "")

        photos_map = {
            "Les photos de groupes Classique": "Groupes Classique",
            "Les photos de groupe Fun":        "Groupes Fun",
            "Les photos individuelles":        "Photos Individuelles",
            "Les photos de Fratries":          "Photos Fratries",
            "Portraits de professeur":         "Portraits Profs",
            "Photos d'équipes de professeur":   "Groupe Equipe"
        }
        mapped_photos = [photos_map[p] for p in self.data.get("photos_livrees", [])]

        photo_etab_ok = (self.data["photos_etablissement"] == "J'ai bien pris en photos les bâtiments")

        # 5) Appel de fill_delivery (écrit également R, S, T)
        for clef in self.data.get("clefs", []):
            fill_delivery(
                keyfile_path="/Users/JvA_Production_Script/Pyhton Explorer/MY-BOOT-ASANA-PYTHON/production-labhd-2025-a112358dfc53.json",
                spreadsheet_id="1oVdRMvHO-UWWJrqZQBL5rY03NMnvs-HycdDxoQZOI-U",
                worksheet_name="LIVRAISON",
                clef_unique=clef,
                code_client=code_client,
                id_photographe=self.data["id_photographe"],
                type_livraison=mapped_type,
                photos_livrees=mapped_photos,
                photo_etablissement=photo_etab_ok,
                retour_experience=self.data["retour_experience"],
                commentaires=self.data["commentaires"]
            )

        # 6) Message de fin centré
        content = ttk.Frame(self.main_frame)
        content.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Label(
            content,
            text="Merci pour ta livraison et pour ton travail,\nbon courage à toi !",
            font=('Helvetica', 14),
            wraplength=400,
            justify="center"
        ).pack(pady=(0,20))
        ttk.Button(content, text="Fermer", command=self.quit).pack()
