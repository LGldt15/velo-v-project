import csv
import math
import unicodedata
from collections import defaultdict
from pathlib import Path
VELOV = Path(__file__).parent / "data" / "velov.csv"
POLYTECH = (45.779189, 4.867286) # latitude, longitude du bâtiment Polytech


def distance_km(lat1, lng1, lat2, lng2):
    """Distance approchée en kilomètres entre deux points proches.
    """
    dx = (lng2 - lng1) * 111.32 * math.cos(math.radians((lat1 + lat2) / 2))
    dy = (lat2 - lat1) * 110.57
    return math.hypot(dx, dy)

def premieres_lignes(chemin, n=3):
    """Renvoie la liste des n premieres lignes du fichier
    sans leur saut de ligne"""
    with open(chemin,encoding="utf-8") as f:
        return [f.readline().rstrip() for _ in range(n)]

def compter_lignes(chemin):
    """Renvoie le nombre de lignes du fichier, sans le charger en mémoire."""
    nb = 0
    with open(chemin,encoding="utf-8") as f:
        for _ in f:
            nb += 1
    return nb

def colonnes(chemin):
    """Renvoie la liste des noms de colonnes lus sur la premiere ligne"""
    return premieres_lignes(chemin, 1)[0].split(",")


if __name__ == "__main__":
    print(premieres_lignes(VELOV, 3))
    print(compter_lignes(VELOV))
    print(colonnes(VELOV))

   