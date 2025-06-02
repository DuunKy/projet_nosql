from db.mongo import DATABASE
from collections import defaultdict

def model(constructor_id, season=None):
    # 1. Récupérer les courses de la saison si saison donnée
    if season is not None:
        season = int(season)
        races = list(DATABASE["races"].find({"year": season}, {"raceId": 1}))
        race_ids = [race["raceId"] for race in races]
        if not race_ids:
            return {"error": "no race ids"}, 404
    else:
        race_ids = None  # pas de filtre raceId

    # 2. Récupérer résultats du constructeur (filtrer sur raceId si existant)
    query_results = {"constructorId": constructor_id}
    if race_ids is not None:
        query_results["raceId"] = {"$in": race_ids}

    results = list(DATABASE["results"].find(query_results, {"raceId": 1, "driverId": 1}))

    # Map raceId -> set(driverId)
    race_drivers = defaultdict(set)
    for res in results:
        race_drivers[res["raceId"]].add(res["driverId"])

    # 3. Récupérer pit stops du constructeur
    query_pit = {}
    if race_ids is not None:
        query_pit["raceId"] = {"$in": race_ids}
    pitstops = list(DATABASE["pit_stops"].find(query_pit, {"raceId": 1, "driverId": 1, "milliseconds": 1}))

    # 4. Filtrer pit stops par driverId du constructeur dans la course
    filtered_pitstops = [p for p in pitstops if p["driverId"] in race_drivers.get(p["raceId"], set())]

    if not filtered_pitstops:
        return {"globalAvg": 0, "globalMax": 0, "globalMin": 0, "perRace": []}

    durations = [p["milliseconds"] for p in filtered_pitstops]
    global_avg = sum(durations) / len(durations)
    global_max = max(durations)
    global_min = min(durations)

    per_race_durations = defaultdict(list)
    for p in filtered_pitstops:
        per_race_durations[p["raceId"]].append(p["milliseconds"])

    per_race_stats = []
    for race_id, times in per_race_durations.items():
        avg = sum(times) / len(times)
        mx = max(times)
        mn = min(times)
        per_race_stats.append({
            "raceId": race_id,
            "avg": avg,
            "max": mx,
            "min": mn
        })

    return {
        "globalAvg": global_avg,
        "globalMax": global_max,
        "globalMin": global_min,
        "perRace": per_race_stats
    }, 200
