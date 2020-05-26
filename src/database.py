import os
import csv

import pymongo
from dotenv import load_dotenv

load_dotenv()
if os.getenv('MONGO_URL') is None:
    try:
        url = open('db_url.txt', 'r').read().replace('\n', '')
    except FileNotFoundError as e:
        url = "localhost:27017"
    os.environ["MONGO_URL"] = url


def get_collection():
    client = pymongo.MongoClient(os.getenv('MONGO_URL'))
    db = client['air_quality_db']

    collection_name = 'air_quality_data'
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)

    return db[collection_name]


def backup(filepath):
    if not filepath.endswith('.csv'):
        filepath = filepath + '.csv'

    client = pymongo.MongoClient(os.getenv('MONGO_URL'))
    data = client['air_quality_db']['air_quality_data'].find()
    with open(filepath, 'w+') as file:
        writer = csv.DictWriter(file, fieldnames=['temp', 'humidity', 'wind_speed', 'pressure', 'aqi', 'country',
                                                  'city1', 'city2', 'date'])
        writer.writeheader()
        for item in data:
            del item['_id']
            del item['origin_url']
            writer.writerow(item)


def restore(filepath):
    client = pymongo.MongoClient(os.getenv('MONGO_URL'))
    collection = client['air_quality_db']['air_quality_data']
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            collection.insert(row)
