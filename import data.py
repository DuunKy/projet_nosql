import pandas as pd
import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient

# Charger les variables d’environnement
load_dotenv()

# Récupérer les variables d’environnement
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
DATA_PATH = os.getenv("DATA_PATH")

def importer_csv_vers_mongo(csv_path, db_name, collection_name):
    client = MongoClient(MONGO_URI)
    db = client[db_name]
    collection = db[collection_name]

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"[ERREUR] Lecture du fichier {csv_path} : {e}")
        return

    data = df.to_dict(orient="records")
    if data:
        result = collection.insert_many(data)
        print(f"[OK] {len(result.inserted_ids)} documents insérés depuis {csv_path}")
    else:
        print(f"[INFO] Aucun enregistrement dans {csv_path}")

if __name__ == "__main__":
    if not os.path.isdir(DATA_PATH):
        print(f"[ERREUR] Dossier '{DATA_PATH}' introuvable.")
        sys.exit(1)

    # Liste tous les fichiers .csv dans le dossier
    fichiers_csv = [f for f in os.listdir(DATA_PATH) if f.endswith(".csv")]

    if not fichiers_csv:
        print(f"[INFO] Aucun fichier CSV trouvé dans '{DATA_PATH}'.")
        sys.exit(0)

    for fichier in fichiers_csv:
        chemin_complet = os.path.join(DATA_PATH, fichier)
        importer_csv_vers_mongo(chemin_complet, DB_NAME, COLLECTION_NAME)
