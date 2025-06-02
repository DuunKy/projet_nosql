from db.mongo import DATABASE
from collections import defaultdict

def model(id, season=None, driver=None):
    constructor_id = int(id)

    # 1. Récupérer les courses de la saison (ou toutes si aucune saison donnée)
    race_filter = {}
    if season:
        race_filter["year"] = int(season)

    races = list(DATABASE["races"].find(race_filter))
    race_ids = [r["raceId"] for r in races]

    if not race_ids:
        return {"error": "No races found"}, 404

    # 2. Récupérer les résultats pour le constructeur
    result_filter = {
        "constructorId": constructor_id,
        "raceId": {"$in": race_ids}
    }
    if driver:
        result_filter["driverId"] = int(driver)

    results = list(DATABASE["results"].find(result_filter, {
        "raceId": 1, "driverId": 1, "positionOrder": 1
    }))

    # 3. Récupérer les qualifications
    qualis = list(DATABASE["qualifying"].find({
        "raceId": {"$in": race_ids},
        "driverId": {"$in": [r["driverId"] for r in results]}
    }, {"raceId": 1, "driverId": 1, "position": 1}))

    # 4. Récupérer les sprints (on suppose une collection dédiée `sprint_results`)
    sprints = list(DATABASE["sprint_results"].find({
        "raceId": {"$in": race_ids},
        "driverId": {"$in": [r["driverId"] for r in results]}
    }, {"raceId": 1, "driverId": 1, "position": 1}))

    # 5. Organisation par pilote
    comparison = defaultdict(lambda: {"qualifying": [], "sprint": [], "race": []})

    for q in qualis:
        comparison[q["driverId"]]["qualifying"].append(q["position"])

    for s in sprints:
        comparison[s["driverId"]]["sprint"].append(s["position"])

    for r in results:
        comparison[r["driverId"]]["race"].append(r["positionOrder"])

    # 6. Calcul des moyennes
    def avg(lst):
        cleaned = [int(x) for x in lst if isinstance(x, (int, float)) or (isinstance(x, str) and x.isdigit())]
        return round(sum(cleaned) / len(cleaned), 2) if cleaned else None


    final_data = []
    for driver_id, data in comparison.items():
        final_data.append({
            "driverId": driver_id,
            "averageQualifying": avg(data["qualifying"]),
            "averageSprint": avg(data["sprint"]),
            "averageRace": avg(data["race"])
        })

    return final_data, 200
