#!/usr/bin/env python3
"""
Poller pour détecter et traiter en continu tous les dossiers clients sous /Volumes/FTP/Saison_2025_2026.
Chaque dossier client contenant un contenu.txt est :
 1. Signalé par la création de <CODE>_Attente.txt dans Temp.
 2. Traité jusqu'à ce que tous les fichiers attendus soient copiés (detected.txt et missing.txt mis à jour en boucle).
 3. Une fois complet, le signal d'attente est supprimé et la Google Sheet est mise à jour (colonne F = "Réceptionné").

Le poller tourne en continu, lance chaque traitement dans un thread séparé et affiche un log à chaque scan.
"""
import os
import time
import logging
import threading
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# --- Configuration ---
BASE_DIR    = '/Volumes/FTP/Saison_2025_2026'
TEMP_DIR    = os.path.join(BASE_DIR, 'Temp')
POLL_INTERVAL = 10    # secondes entre chaque vérification dans un dossier client
GLOBAL_POLL   = 10    # secondes entre scans de nouveaux dossiers

# Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '/Users/JvA_Production_Script/Pyhton Explorer/MY-BOOT-ASANA-PYTHON/production-labhd-2025-a112358dfc53.json'
SPREADSHEET_ID       = '1oVdRMvHO-UWWJrqZQBL5rY03NMnvs-HycdDxoQZOI-U'
SHEET_NAME           = 'LIVRAISON'

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Sets pour suivre l'état des dossiers
processed = set()    # dossiers déjà traités
processing = set()   # dossiers en cours de traitement
lock = threading.Lock()


def find_client_dirs():
    """Retourne les chemins relatifs des dossiers contenant contenu.txt."""
    dirs = set()
    for root, _, files in os.walk(BASE_DIR):
        if os.path.commonpath([root, TEMP_DIR]) == TEMP_DIR:
            continue
        if 'contenu.txt' in files:
            dirs.add(os.path.relpath(root, BASE_DIR))
    return dirs


def parse_contenu(path):
    expected = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '|' not in line or line.lower().startswith('liste des fichiers'):
                continue
            expected.append(line.split('|', 1)[0].strip())
    return expected


def list_actual(path):
    found = []
    for root, _, files in os.walk(path):
        for fn in files:
            found.append(os.path.relpath(os.path.join(root, fn), path))
    return found


def update_sheet(code):
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    # Lecture A->F
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f"{SHEET_NAME}!A:F").execute()
    rows = result.get('values', [])
    for idx, row in enumerate(rows, start=1):
        if row and row[0].startswith(code):
            body = {'values': [['Réceptionné']]}
            sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                  range=f"{SHEET_NAME}!F{idx}",
                                  valueInputOption='RAW', body=body).execute()
            logging.info(f"Feuille mise à jour: code {code} à la ligne {idx}.")
            return
    logging.warning(f"Code client {code} non trouvé dans la feuille.")


def process_folder(rel_path):
    abs_path = os.path.join(BASE_DIR, rel_path)
    code = os.path.basename(abs_path)[:5]
    os.makedirs(TEMP_DIR, exist_ok=True)

    # Création du signal d'attente
    attente = os.path.join(TEMP_DIR, f"{code}_Attente.txt")
    open(attente, 'w', encoding='utf-8').close()
    logging.info(f"Début traitement {rel_path}, signalé par {attente}")

    expected = parse_contenu(os.path.join(abs_path, 'contenu.txt'))
    logging.info(f"{len(expected)} fichiers attendus pour {rel_path}")

    # Boucle de collecte
    while True:
        detected = list_actual(abs_path)
        # Mise à jour detected.txt
        with open(os.path.join(abs_path, 'detected.txt'), 'w', encoding='utf-8') as f:
            f.write("\n".join(detected))
        # Mise à jour missing.txt
        missing = sorted(set(expected) - set(detected))
        with open(os.path.join(abs_path, 'missing.txt'), 'w', encoding='utf-8') as f:
            f.write("\n".join(missing))
        logging.info(f"{len(detected)} trouvés, {len(missing)} manquants pour {rel_path}")

        if not missing:
            logging.info(f"Tous fichiers copiés pour {rel_path}. Fin traitement.")
            try:
                os.remove(attente)
                logging.info(f"Signal d'attente supprimé: {attente}")
            except OSError:
                pass
            update_sheet(code)
            break

        time.sleep(POLL_INTERVAL)

    # Marquer comme traité
    with lock:
        processing.discard(rel_path)
        processed.add(rel_path)


def worker(rel_path):
    try:
        process_folder(rel_path)
    except Exception as e:
        logging.error(f"Erreur sur {rel_path}: {e}")
        with lock:
            processing.discard(rel_path)
            processed.add(rel_path)


def main():
    # Initialisation
    with lock:
        processed.update(find_client_dirs())
    logging.info(f"Poller démarré, {len(processed)} dossiers existants ignorés.")

    try:
        while True:
            time.sleep(GLOBAL_POLL)
            current = find_client_dirs()
            to_start = current - processed - processing
            if to_start:
                for d in to_start:
                    with lock:
                        processing.add(d)
                    threading.Thread(target=worker, args=(d,), daemon=True).start()
                    logging.info(f"Démarrage traitement asynchrone pour {d}")
            else:
                logging.debug(f"Aucun nouveau dossier. Prochain scan dans {GLOBAL_POLL}s.")

    except KeyboardInterrupt:
        logging.info("Poller arrêté par l'utilisateur.")


if __name__ == '__main__':
    main()
