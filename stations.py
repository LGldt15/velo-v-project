import csv
import math
import unicodedata
from collections import defaultdict
from pathlib import Path
VELOV = Path(__file__).parent / "data" / "velov.csv"
POLYTECH = (45.779189, 4.867286) # latitude, longitude du bâtiment Polytech

#exercice 1

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


#exercice 2

def compter_stations(chemin):
    """ Renvoie le nombre de sations """
    n=0
    with open(chemin, encoding="utf-8") as f:
        for _ in csv.DictReader(f):
            n+=1
        return n
            


def lire_stations(chemin):
    """ Renvoie une liste de stations ou chaque station est un dico """
    stations=[]
    with open(chemin, encoding="utf-8") as f:
        for l in csv.DictReader(f):
            stations.append({
                "numero": int(l["number"]),
                "nom": l["name"],
                "commune": l["commune"],
                "places": int(l["bike_stands"]),
                "velos": int(l["available_bikes"]),
                "bornes_libres": int(l["available_bike_stands"]),
                "ouverte": l["status"] == "OPEN",
                "lat": float(l["lat"]),
                "lng": float(l["lng"]),
            })
    return stations


def stations_vides(stations):
    """renvoit les stations ouvertes sans aucun vélo"""
    stat_vide=[]
    for s in stations:
        if s["ouverte"] and s["velos"]==0:
            stat_vide.append(s)

    return stat_vide


def stations_pleines(stations):
    """Renvoit les stations pleines"""
    stat_pleines=[]
    for s in stations:
        if s["ouverte"] and s["bornes_libres"]==0:
            stat_pleines.append(s)
    return stat_pleines


def velos_par_commune(stations):
    total = defaultdict(int)
    for s in stations:
        if s["ouverte"]:
            total[s["commune"]] += s["velos"]
    return total

def classement_communes(stations, k=5):
    chaque_commune=velos_par_commune(stations)
    classement = sorted(chaque_commune.items(), key=lambda cv: (-cv[1], cv[0]))
    return classement[:k]


def plus_proches(stations, lat, lng, k=5):
    potentiels_plus_proches = [
        (distance_km(lat, lng, s["lat"], s["lng"]), s)
        for s in stations
        if s["ouverte"] and s["velos"] > 0
    ]
    potentiels_plus_proches.sort(key=lambda ds: ds[0])
    return [(s["nom"], s["velos"], round(d, 2)) for d, s in potentiels_plus_proches[:k]]


#exercice 3

def ecrire_bilan(stations,chemin):
    chemin = Path(chemin)
    par_commune = {}
    for s in stations:
        if s["ouverte"]:
            ligne = par_commune.setdefault(
                s["commune"],
                {"commune": s["commune"], "stations": 0, "velos": 0, "places": 0},
            )
            ligne["stations"] += 1
            ligne["velos"] += s["velos"]
            ligne["places"] += s["places"]

    lignes = sorted(par_commune.values(), key=lambda l: (-l["velos"], l["commune"]))

    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["commune", "stations", "velos", "places"])
        writer.writeheader()
        writer.writerows(lignes)
    return len(lignes)


if __name__ == "__main__":


    print(premieres_lignes(VELOV, 3))
    print(compter_lignes(VELOV))
    print(colonnes(VELOV))


    stations = lire_stations(VELOV)
    print(compter_stations(VELOV), "stations pour", compter_lignes(VELOV), "lignes")
    print("lecture cohérente :", compter_stations(VELOV) == len(stations))
    print(stations[0])
    print(len(stations_vides(stations)), "stations vides")
    print(len(stations_pleines(stations)), "stations pleines")
    print(velos_par_commune(stations))
    total = sum(s["velos"] for s in stations if s["ouverte"])
    print(total, "vélos disponibles dans les stations ouvertes")
    for commune, velos in classement_communes(stations, 5):
        print(f"{commune} : {velos} vélos")
    proches = plus_proches(stations, *POLYTECH, k=5)
    for nom, velos, distance in proches:
        print(f"{nom} : {velos} vélos à {distance} km")

   #exemple exo 3
    bilan = Path(__file__).parent / "sorties" / "bilan_communes.csv"
    print(ecrire_bilan(stations, bilan),"communes écrites")
    with open(bilan, encoding="utf-8", newline="") as f:lignes = list(csv.DictReader(f))
    print(lignes[0])
    velos = [int(l["velos"]) for l in lignes]
    print("classement décroissant :", velos == sorted(velos, reverse=True))
    print(bilan.read_text(encoding="utf-8")[:200])