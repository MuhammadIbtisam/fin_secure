
import json
import csv
import os

DATA_DIR = 'data/'

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.isfile(path):
        return []
    with open(path, 'r') as json_file:
        return json.load(json_file)

def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.isfile(path):
        return []
    with open(path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)

def save_csv(filename, data, fieldnames):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


