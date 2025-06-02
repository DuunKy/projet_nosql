from db.mongo import DATABASE
from collections import defaultdict

def model(id, season=None, driver=None):
    query = {"constructorId": int(id)}

    if season:
        races = list(DATABASE["races"].find({"year": int(season)}, {"raceId": 1}))
        race_ids = [r["raceId"] for r in races]
        if not race_ids:
            return {"error": "No races for season"}, 404
        query["raceId"] = {"$in": race_ids}

    if driver:
        query["driverId"] = int(driver)

    # Récupération des résultats filtrés
    results = list(DATABASE["results"].find(query, {
        "raceId": 1, "points": 1, "positionOrder": 1
    }))

    if not results:
        return {"error": "No results"}, 404

    # Association avec les circuits
    race_ids = list(set([res["raceId"] for res in results]))
    races = DATABASE["races"].find({"raceId": {"$in": race_ids}}, {"raceId": 1, "circuitId": 1})
    race_to_circuit = {r["raceId"]: r["circuitId"] for r in races}

    # Regrouper par circuit
    circuits_stats = defaultdict(lambda: {"totalPoints": 0, "positions": [], "count": 0})

    for res in results:
        race_id = res["raceId"]
        circuit_id = race_to_circuit.get(race_id)
        if circuit_id is None:
            continue
        circuits_stats[circuit_id]["totalPoints"] += res.get("points", 0)
        circuits_stats[circuit_id]["positions"].append(res.get("positionOrder", 999))
        circuits_stats[circuit_id]["count"] += 1

    # Construction des stats finales
    output = []
    for circuit_id, stats in circuits_stats.items():
        avg_pos = sum(stats["positions"]) / len(stats["positions"]) if stats["positions"] else None
        output.append({
            "circuitId": circuit_id,
            "avgPosition": avg_pos,
            "totalPoints": stats["totalPoints"],
            "entries": stats["count"]
        })

    # Tri par performance moyenne (position croissante)
    output.sort(key=lambda x: x["avgPosition"])

    return output, 200
