from flask import Flask, jsonify, request, send_from_directory
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['newmedicinedatabase']
collection = db['new_medicines']

app = Flask(__name__, static_folder='static')

# Endpoint to get all medicines
@app.route('/medicines', methods=['GET'])
def get_medicines():
    print("Fetching all medicines")  # Debug print statement
    medicines = list(collection.find({}, {'_id': 0}))
    print("Medicines fetched:", medicines)  # Debug print statement
    return jsonify(medicines)

# Endpoint to get medicines by disease name
@app.route('/medicines/<disease_name>', methods=['GET'])
def get_medicines_by_disease(disease_name):
    print(f"Fetching medicines for disease: {disease_name}")  # Debug print statement
    medicines = list(collection.find({'disease_name': disease_name}, {'_id': 0}))
    print("Medicines fetched:", medicines)  # Debug print statement
    return jsonify(medicines)

# Serve the static index.html file
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
