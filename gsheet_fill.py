# gsheet_fill.py

import os
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tkinter as tk
from tkinter import messagebox

def get_gs_client(keyfile_path: str):
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(keyfile_path, scopes)
    return gspread.authorize(creds)

def get_next_row(ws, start_row=4, col='A') -> int:
    col_idx = ord(col.upper()) - ord('A') + 1
    vals = ws.col_values(col_idx)
    while len(vals) < start_row - 1:
        vals.append('')
    for i in range(start_row - 1, len(vals)):
        if not vals[i].strip():
            return i + 1
    return len(vals) + 1

def fill_delivery(
    keyfile_path: str,
    spreadsheet_id: str,
    worksheet_name: str,
    *,
    clef_unique: str,
    code_client: str,
    id_photographe: str,
    type_livraison: str,
    photos_livrees: list[str],
    photo_etablissement: bool,
    retour_experience: str,
    commentaires: str
):
    # 1) Connexion
    client = get_gs_client(keyfile_path)
    sh     = client.open_by_key(spreadsheet_id)
    ws     = sh.worksheet(worksheet_name)

    # 2) Ligne cible
    row = get_next_row(ws, start_row=4, col='A')
    date_j  = datetime.now().strftime("%d/%m/%Y")
    heure_j = datetime.now().strftime("%H:%M")

    # 3) Comptages R,S,T
    base = os.path.expanduser("~/Desktop/ECOLE_A_LIVRER")
    # R: nombre de classes sans EQUIPE/ETABLISSEMENT
    n_classes = 0
    for client_dir in os.listdir(base):
        path_client = os.path.join(base, client_dir)
        if not os.path.isdir(path_client):
            continue
        for entry in os.listdir(path_client):
            if entry.upper().endswith("_GROUPE_BRUT"):
                groupe_dir = os.path.join(path_client, entry)
                for cl in os.listdir(groupe_dir):
                    if cl.upper() not in ("EQUIPE","ETABLISSEMENT"):
                        if os.path.isdir(os.path.join(groupe_dir, cl)):
                            n_classes += 1
                break

    # S,T: à partir des HAUTES_RESOLUTIONS
    total_eleves = 0
    total_fratrie = 0
    for client_dir in os.listdir(base):
        path_client = os.path.join(base, client_dir)
        if not os.path.isdir(path_client):
            continue
        for entry in os.listdir(path_client):
            if "HAUTES" in entry.upper() and "RESOLUTION" in entry.upper():
                haute_dir = os.path.join(path_client, entry)
                for cl in os.listdir(haute_dir):
                    cp = os.path.join(haute_dir, cl)
                    if not os.path.isdir(cp): continue
                    count = sum(1 for f in os.listdir(cp) if os.path.isfile(os.path.join(cp,f)))
                    if cl.upper() == "FRERES_ET_SOEURS":
                        total_fratrie += count
                    elif cl.upper() != "ENSEIGNANTS":
                        total_eleves += count
                break

    # 4) Préparation des mises à jour
    updates_text = {
        'A': clef_unique,
        'D': date_j,
        'E': heure_j,
        'F': "En cours",
        'H': id_photographe,
        'J': type_livraison,
        'R': n_classes,
        'S': total_eleves,
        'T': total_fratrie,
        'U': retour_experience,
        'V': commentaires,
        'Q': photo_etablissement
    }

    print(f"[DEBUG]→ R,S,T calculés : {n_classes=}, {total_eleves=}, {total_fratrie=}")

    # 5) Écriture USER_ENTERED (texte + R,S,T + case Q)
    text_cols = list(updates_text.keys())
    body_text = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": f"{worksheet_name}!{col}{row}", "values": [[updates_text[col]]]}
            for col in text_cols
        ]
    }
    sh.values_batch_update(body_text)

        # 6) Cases à cocher K→P — correspondance avec mapped_photos
    photo_to_col = {
        "Groupes Classique":    "K",
        "Groupes Fun":          "L",
        "Groupe Equipe":        "M",
        "Photos Individuelles": "N",
        "Photos Fratries":      "O",
        "Portraits Profs":      "P",
    }
    bool_cols = ['K','L','M','N','O','P']
    desired = [False]*6
    for p in photos_livrees:
        c = photo_to_col.get(p)
        if c:
            idx = bool_cols.index(c)
            desired[idx] = True

    print(f"[DEBUG]→ Cases K→P attendues : {desired}")

    for attempt in range(1,4):
        sh.values_update(
            f"{worksheet_name}!K{row}:P{row}",
            params={"valueInputOption":"RAW"},
            body={"values":[desired]}
        )
        time.sleep(0.3)
        current = ws.get(f"K{row}:P{row}")[0]
        curr_bool = [str(v).upper()=='TRUE' for v in current]
        print(f"[DEBUG] tentative {attempt} lu {curr_bool}")
        if curr_bool == desired:
            print(f"[INFO] Cases K→P OK à la ligne {row}")
            break

    # 7) Fin
    return