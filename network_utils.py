# network_utils.py

import socket

def check_internet(host: str = "8.8.8.8", port: int = 53, timeout: int = 2) -> bool:
    """
    Vérifie la disponibilité d'une connexion Internet en essayant de se connecter
    à un serveur DNS (par défaut 8.8.8.8:53).

    :param host: hôte à contacter (IP ou nom de domaine)
    :param port: port TCP
    :param timeout: délai en secondes avant abandon
    :return: True si la connexion a réussi, False sinon
    """
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False