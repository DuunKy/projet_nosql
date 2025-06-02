from db.mongo import DATABASE
from collections import defaultdict

def model(id, season=None, driver=None, circuit=None):
    constructor_id = int(id)

    # 1. Récupérer les courses avec une sprint race
    race_query = {"sprint_time": {"$ne": "\\N"}}
    if season:
        race_query["year"] = int(season)
    if circuit:
        race_query["circuitId"] = int(circuit)

    races = list(DATABASE["races"].find(race_query, {"raceId": 1}))
    race_ids = [r["raceId"] for r in races]
    if not race_ids:
        return {"error": "No sprint races found"}, 404

    # 2. Récupérer les résultats de l'écurie dans ces courses
    result_query = {"constructorId": constructor_id, "raceId": {"$in": race_ids}}
    if driver:
        result_query["driverId"] = int(driver)

    results = list(DATABASE["results"].find(result_query, {"driverId": 1, "raceId": 1}))
    if not results:
        return {"error": "No drivers found for this constructor in sprint races"}, 404

    # 3. Identifier les pilotes de l’écurie sur ces courses
    race_driver_map = defaultdict(set)
    for res in results:
        race_driver_map[res["raceId"]].add(res["driverId"])

    # 4. Récupérer tous les temps au tour des courses sprint
    laps = list(DATABASE["lap_times"].find({
        "raceId": {"$in": race_ids}
    }, {"raceId": 1, "driverId": 1, "milliseconds": 1}))

    # 5. Filtrer ceux appartenant aux pilotes de l’écurie
    filtered_laps = [
        l for l in laps
        if l["driverId"] in race_driver_map.get(l["raceId"], set())
    ]
    if not filtered_laps:
        return {"average": 0, "perSprint": []}

    # 6. Calcul du temps moyen global
    all_times = [l["milliseconds"] for l in filtered_laps if "milliseconds" in l]
    global_avg = sum(all_times) / len(all_times) if all_times else 0

    # 7. Moyenne par course sprint
    per_race = defaultdict(list)
    for l in filtered_laps:
        per_race[l["raceId"]].append(l["milliseconds"])

    per_sprint = []
    for race_id, times in per_race.items():
        avg = sum(times) / len(times)
        per_sprint.append({
            "raceId": race_id,
            "average": avg
        })

    return {
        "average": round(global_avg, 2),
        "perSprint": per_sprint
    }, 200
