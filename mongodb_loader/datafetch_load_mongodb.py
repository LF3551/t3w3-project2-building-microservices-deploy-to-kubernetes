import pymongo
import requests

def fetch_json_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error requesting data from {url}: {e}")
        return None

def save_to_mongodb(collection, data):
    if data and isinstance(data, list):
        try:
            #collection.insert_many(data)
            for doc in data:
                filter_query = {'id': doc['id']}  # Assuming 'id' is the unique identifier
                update_doc = {'$set': doc}  # Using $set to update the entire document
                collection.update_one(filter_query, update_doc, upsert=True)
            print(f"Data successfully saved to the {collection.name} collection.")
        except Exception as e:
            print(f"Error saving data to {collection.name}: {e}")
    else:
        print(f"No data to save to the {collection.name} collection.")

connection_string = "mongodb://mongodb-service:27017/hogwarts"
client = pymongo.MongoClient(connection_string)

try:
    client.admin.command('ismaster')
    print("MongoDB connection successful")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)

db = client["hogwarts"]
characters = db["Characters"]
spells = db["Spells"]

spells_url = "https://hp-api.onrender.com/api/spells"
staff_url = "https://hp-api.onrender.com/api/characters/staff"

list_staff = fetch_json_data(staff_url)
list_spells = fetch_json_data(spells_url)
spells.create_index([('id', 1)], unique=True)
characters.create_index([('id', 1)], unique=True)
try:
    save_to_mongodb(characters, list_staff)
    save_to_mongodb(spells, list_spells)
except pymongo.errors.DuplicateKeyError as e:
    print(f"Duplicate key error: {e}")

client.close()
