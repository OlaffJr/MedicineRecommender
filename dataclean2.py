import re
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['cleaned_medicine_database']
original_collection = db['cleaned_medicines']  # Assuming this is where cleaned data is stored

# New database and collection for transformed data
new_db = client['newmedicinedatabase']
cleaned_collection = new_db['new_medicines']

# Regular expressions for matching sections
INTRO_RE = re.compile(r'^INTRODUCTION ABOUT', re.IGNORECASE)
DIRECTIONS_RE = re.compile(r'^DIRECTIONS FOR USE', re.IGNORECASE)
SIDE_EFFECTS_RE = re.compile(r'^SIDE EFFECTS OF', re.IGNORECASE)

# Function to clean and transform data
def clean_and_transform(data):
    medicine_name = data['medicine_name']
    disease_name = re.sub(r'\(\d+\)', '', data['disease_name']).strip()  # Remove numbers and parentheses

    description = data.get('introduction', '')
    if INTRO_RE.match(description):
        description = f"INTRODUCTION ABOUT {medicine_name}:{description[19:].strip()}"

    directions = data.get('directions', '')
    if DIRECTIONS_RE.match(directions):
        directions = f"DIRECTIONS FOR USE:{directions[18:].strip()}"

    side_effects = data.get('side_effects', '')
    side_effects = re.sub(r'^(COMMON|UNCOMMON|RARE)', r'\n\1', side_effects, flags=re.IGNORECASE).strip()

    # Construct cleaned data
    cleaned_data = {
        "_id": data['_id'],
        "medicine_name": medicine_name,
        "price": data.get('price', 'Price not available'),
        "disease_name": disease_name,
        "description": description,
        "directions": directions,
        "side_effects": side_effects
    }
    return cleaned_data

# Process each document in the original collection
for document in original_collection.find():
    cleaned_data = clean_and_transform(document)
    cleaned_collection.insert_one(cleaned_data)

print("Data transformation and storage complete.")
