import csv

# On ouvre le fichier des distances
with open("DistanceCities.csv") as file:
    data = list(csv.reader(file, delimiter=";"))

# ... on le traite
cities = {}
for i in range(len(data[0][1:])):
    cities[data[0][i+1]] = i

data.pop(0)
for i in range(len(data)):
    data[i].pop(0)

def test_and_run(ville_depart:str, villes_passage:list, ville_arrivee:str):
    global cities, distances

    # assertions : si une des villes citées n'existent pas dans notre tableau, on envoie une erreur !
    assert ville_depart in cities, "La ville de départ n'existe pas !"
    assert ville_arrivee in cities, "La ville d'arrivée n'existe pas !"
    for i in range(len(villes_passage)):
        assert villes_passage[i] in cities, f"Une/Des ville(s) de passage n'existe(nt) pas : {villes_passage[i]}"

    # test préliminaire : si il n'y a pas déjà la ville d'arrivée dans les villes de passage :
    if not ville_arrivee in villes_passage:
        villes_passage.append(ville_arrivee)

    choix(ville_depart, villes_passage, ville_arrivee, cities, data)


def choix(ville_depart:str, villes_passage:list, ville_arrivee:str, villes:dict, distances:list,):
    """Choisit parmi une liste de villes le chemin le plus court pour aller
    d'un point A à un point B en passant par un nombre illimité de points C"""

    index_ville_depart = villes[ville_depart]
    distance_minimum = (9999, "")
    for ville, index in villes.items():
        if ville_depart == ville:
            continue
        if not ville in villes_passage:
            continue
        distance = distances[index_ville_depart][index]
        if int(distance) < int(distance_minimum[0]):
            distance_minimum = (distance, ville)
            
    print(f"Ville passage : {distance_minimum[1]} à {distance_minimum[0]} km")
    villes.pop(ville_depart)
    newVilles = villes

    if distance_minimum[1] == ville_arrivee:
        return "Found"

    if len(villes) <= 1: 
        return "Not Found"
    
    choix(ville_depart=distance_minimum[1], villes=newVilles, distances=distances, ville_arrivee=ville_arrivee, villes_passage=villes_passage)

test_and_run(ville_depart="Hyrule Castle", villes_passage=["Goron City", "Korok Forest"], ville_arrivee="Lurelin Village")
        
