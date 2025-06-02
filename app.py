from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Charger les variables d’environnement
load_dotenv()

app = Flask(__name__)

# Connexion à MongoDB
client = os.getenv("MONGO_URI")
db = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Route 1 – Lister tous les circuits
@app.route("/circuits", methods=["GET"])
def get_all_circuits():
    circuits = list(COLLECTION_NAME.find({}, {"_id": 0}))
    return jsonify(circuits)

# Route 2 – Circuits par pays
@app.route("/circuits/by-country", methods=["GET"])
def get_circuits_by_country():
    country = request.args.get("country")
    circuits = list(COLLECTION_NAME.find({"country": country}, {"_id": 0}))
    return jsonify(circuits)

# Route 3 – Circuits en altitude (> 1000m)
@app.route("/circuits/high-altitude", methods=["GET"])
def high_altitude_circuits():
    circuits = list(COLLECTION_NAME.find({"alt": {"$gt": 1000}}, {"_id": 0}))
    return jsonify(circuits)

# Route 4 – Circuits triés par latitude (nord au sud)
@app.route("/circuits/by-latitude", methods=["GET"])
def circuits_by_latitude():
    circuits = list(COLLECTION_NAME.find({}, {"_id": 0}).sort("lat", -1))
    return jsonify(circuits)

if __name__ == "__main__":
    app.run(debug=True)
