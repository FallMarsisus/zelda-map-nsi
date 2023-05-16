from tkinter import *
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


coordonnees = {
    "Hyrule Castle": (455, 337),
    "Rito Village": (188, 232),
    "Tarrey Town": (777, 250),
    "Goron City": (605, 190),
    "Korok Forest": (509, 215),
    "Zora's Domain" : (728, 354),
    "Lurelin Village": (707, 654),
    "Hateno Village":(748, 547),
    "Kakariko Village": (615, 460),
    "Gerudo Town":(174, 610)
}

def test_and_run():
    global cities, distances, coordonnees, villes_passage

    start_button.pack_forget()

    canvas.delete("all")
    
    canvas.create_image((0, 0), image=bg, anchor=NW)

    # assertions : si une des villes citées n'existent pas dans notre tableau, on envoie une erreur !
    for i in range(len(villes_passage)):
        assert villes_passage[i] in cities, f"Une/Des ville(s) n'existe(nt) pas : {villes_passage[i]}"

    ville_depart = villes_passage[0]
    villes_passage.pop(0)

    ville_arrivee = villes_passage[-1]
    villes_passage.pop()
    
    choix(ville_depart, villes_passage, ville_arrivee, cities, data, coordonnees, 0)

def choix(ville_depart:str, villes_passage:list, ville_arrivee:str, villes:dict, distances:list, coordonnees:dict, count:int):
    """Choisit parmi une liste de villes le chemin le plus court pour aller
    d'un point A à un point B en passant par un nombre illimité de points C"""

    index_ville_depart = villes[ville_depart]
    distance_minimum = (9999, "")
    for ville, index in villes.items():
        if ville_depart == ville:
            continue
        if ville in villes_passage:
            distance = distances[index_ville_depart][index]
            if int(distance) < int(distance_minimum[0]):
                distance_minimum = (distance, ville)
    
    if distance_minimum == (9999, ""):
        distance_minimum = (distances[index_ville_depart][villes[ville_arrivee]], ville_arrivee)
    
    canvas.create_line(coordonnees[ville_depart][0], coordonnees[ville_depart][1], coordonnees[distance_minimum[1]][0], coordonnees[distance_minimum[1]][1], width=3, fill="blue")
    canvas.create_text(coordonnees[ville_depart], text=count + 1, font=("Calibri Bold", 15), anchor=CENTER, fill="white")

    print(f"Ville passage : {distance_minimum[1]} à {distance_minimum[0]} km")
    villes.pop(ville_depart)
    newVilles = villes

    if distance_minimum[1] == ville_arrivee:
        canvas.create_text(coordonnees[distance_minimum[1]], text="🛖", font="Calibri 15", anchor=CENTER, fill='white')
        return "Found"

    if len(villes) <= 1: 
        return "Not Found"
    
    choix(ville_depart=distance_minimum[1], villes=newVilles, distances=distances, ville_arrivee=ville_arrivee, villes_passage=villes_passage, coordonnees=coordonnees, count=count+1)

def addPlaces(e):
    global coordonnees, villes_passage
    x, y = e.x, e.y

    for key, value in coordonnees.items():
        if x - 10 < value[0] < x + 10 and y - 10 < value[1] < y + 10:
            if not key in villes_passage:
                villes_passage.append(key)
                canvas.create_text(value, text=f"{len(villes_passage)}: {key}", fill="white", anchor=CENTER, font=("Calibri Bold", 15))
                return  

window = Tk()
window.title("Hyrule Distance Mapper")

villes_passage = list()

window.geometry("912x767")

bg = PhotoImage(file="map.png")

canvas = Canvas(window, height=bg.height(), width=bg.width())
canvas.place(x=0, y=0)


canvas.create_image((0, 0), image=bg, anchor=NW)

start_button = Button(window, text="Start Calculating", font=("Calibri Bold", 15), command=test_and_run)
start_button.pack()

"""for i in coordonnees.values():
    canvas.create_text(i, text="1", fill="white", font=("Calibri Bold", 15), anchor=CENTER)
"""

window.bind('<ButtonPress-1>', addPlaces)

window.mainloop()