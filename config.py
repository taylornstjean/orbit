from string import ascii_uppercase
import json


CHAR_MAP = {}
for i in range(10, 32):
    CHAR_MAP[ascii_uppercase[i - 10]] = i

with open("./data/planets.json", "r") as f:
    PLANETS = json.load(f)
