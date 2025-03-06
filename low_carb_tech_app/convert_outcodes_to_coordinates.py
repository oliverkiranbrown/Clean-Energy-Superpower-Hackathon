import pgeocode
import json

with open("./data/outcodes.txt", "r") as f:
    outcodes = f.read().splitlines()
locations = {}
for outcode in outcodes:
    nomi = pgeocode.Nominatim("gb")
    location = nomi.query_postal_code(outcode)
    locations[outcode] = [location.latitude, location.longitude]

json.dump(locations, open("./data/outcode_coordinates.json", "w"))