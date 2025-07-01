# file_utils.py

import os
from datetime import datetime
from tkinter import messagebox

def create_content_file(output_dir: str = None) -> bool:
    """
    Crée un fichier 'contenu.txt' listant tous les fichiers du répertoire donné
    (ou cwd si output_dir=None), avec leur taille et date de création.

    :param output_dir: chemin du dossier dans lequel créer le contenu.txt
    :return: True si la création a réussi, False sinon
    """
    try:
        base = output_dir or os.getcwd()
        sortie = os.path.join(base, "contenu.txt")
        with open(sortie, "w", encoding="utf-8") as f:
            f.write(f"Liste des fichiers dans : {base}\n")
            f.write("=" * 80 + "\n\n")
            for root, dirs, files in os.walk(base):
                if '.git' in dirs:
                    dirs.remove('.git')
                for file in files:
                    path = os.path.join(root, file)
                    stats = os.stat(path)
                    size = stats.st_size
                    created = datetime.fromtimestamp(stats.st_ctime)
                    if size < 1024 * 1024:
                        size_str = f"{size/1024:.1f} KB"
                    else:
                        size_str = f"{size/(1024*1024):.1f} MB"
                    rel = os.path.relpath(path, base)
                    f.write(f"{rel} | {size_str} | {created:%Y-%m-%d %H:%M:%S}\n")
        return True
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la création de contenu.txt : {e}")
        return False

def get_folder_file_counts() -> dict:
    """
    Parcourt tous les sous-dossiers de '~/Desktop/ECOLE_A_LIVRER' et renvoie un dict
    {dossier_relatif: nombre_de_fichiers}.

    :return: dictionnaire des comptes
    """
    base = os.path.expanduser("~/Desktop/ECOLE_A_LIVRER")
    counts = {}

    # Fichiers à la racine
    root_files = [
        f for f in os.listdir(base)
        if os.path.isfile(os.path.join(base, f))
    ]
    counts["."] = len(root_files)

    # Chaque sous-dossier
    for root, dirs, files in os.walk(base):
        if root == base:
            continue
        rel = os.path.relpath(root, base)
        visible_files = [f for f in files if not f.startswith('.')]
        counts[rel] = len(visible_files)

    return counts