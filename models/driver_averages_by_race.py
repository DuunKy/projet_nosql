from db.mongo import DATABASE
from collections import defaultdict

def model(id, season=None, circuit=None):
    constructor_id = int(id)

    # Étape 1 : Récupérer les courseIds selon saison et circuit
    race_query = {}
    if season:
        race_query["year"] = int(season)
    if circuit:
        race_query["circuitId"] = int(circuit)

    races = list(DATABASE["races"].find(race_query, {"raceId": 1}))
    race_ids = [r["raceId"] for r in races]

    # Étape 2 : Requête sur les résultats
    query = {"constructorId": constructor_id}
    if race_ids:
        query["raceId"] = {"$in": race_ids}

    results = list(DATABASE["results"].find(query, {
        "driverId": 1,
        "points": 1
    }))

    if not results:
        return {"error": "No results"}, 404

    # Étape 3 : Calcul de la moyenne par pilote
    driver_stats = defaultdict(lambda: {"points": 0, "races": 0})
    for res in results:
        driver_id = res["driverId"]
        driver_stats[driver_id]["points"] += res.get("points", 0)
        driver_stats[driver_id]["races"] += 1

    output = []
    for driver_id, stats in driver_stats.items():
        avg = stats["points"] / stats["races"] if stats["races"] > 0 else 0
        output.append({
            "driverId": driver_id,
            "averagePoints": round(avg, 2),
            "totalPoints": stats["points"],
            "races": stats["races"]
        })

    # Tri par moyenne décroissante
    output.sort(key=lambda x: x["averagePoints"], reverse=True)

    return output, 200
