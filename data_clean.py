import re
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['medicine_database']
original_collection = db['medicines']

# New database and collection for cleaned data
cleaned_db = client['cleaned_medicine_database']
cleaned_collection = cleaned_db['cleaned_medicines']

# Regular expressions for matching sections
INTRO_RE = re.compile(r'^INTRODUCTION', re.IGNORECASE)
DIRECTIONS_RE = re.compile(r'^DIRECTIONS FOR USE', re.IGNORECASE)
SIDE_EFFECTS_RE = re.compile(r'^SIDE EFFECTS OF', re.IGNORECASE)

# Helper function to clean description text
def clean_description(description):
    intro = None
    directions = None
    side_effects = None

    for paragraph in description:
        paragraph = paragraph.strip()  # Remove leading/trailing whitespace
        if INTRO_RE.match(paragraph):
            intro = paragraph
        elif DIRECTIONS_RE.match(paragraph):
            directions = paragraph
        elif SIDE_EFFECTS_RE.match(paragraph):
            side_effects = paragraph

    return intro, directions, side_effects

# Default values for missing fields
DEFAULTS = {
    "medicine_name": "Unknown medicine",
    "price": "Price not available",
    "disease_name": "Unknown disease",
    "introduction": "Introduction not available",
    "directions": "Directions not available",
    "side_effects": "Side effects not available"
}

# Iterate through each document in the original collection
for document in original_collection.find():
    # Extract and clean description
    description = document.get('description', [])
    intro, directions, side_effects = clean_description(description)

    # Extract other fields and handle missing values
    medicine_name = document.get('medicine_name', DEFAULTS["medicine_name"])
    price = document.get('price', DEFAULTS["price"])
    disease_name = document.get('disease_name', DEFAULTS["disease_name"])

    # Ensure all fields are present
    cleaned_data = {
        "medicine_name": medicine_name,
        "price": price,
        "disease_name": disease_name,
        "introduction": intro if intro else DEFAULTS["introduction"],
        "directions": directions if directions else DEFAULTS["directions"],
        "side_effects": side_effects if side_effects else DEFAULTS["side_effects"]
    }

    # Insert cleaned document into the new collection
    cleaned_collection.insert_one(cleaned_data)

print("Data cleaning and migration complete.")
