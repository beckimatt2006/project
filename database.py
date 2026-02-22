import csv

def load_airports():
    airports = {}
    with open("backend/data/airports.csv", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            airports[row["Airports"]] = (float(row["latitude"]), float(row["longitude"]))
    return airports
