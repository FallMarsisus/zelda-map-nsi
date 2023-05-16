import csv

with open("DistanceCities.csv") as file:
    data = list(csv.reader(file, delimiter=";"))

cities = {}
for i in range(len(data[0][1:])):
    cities[data[0][i+1]] = i

print(cities)

data.pop(0)
for i in range(len(data)):
    data[i].pop(0)

print(data)