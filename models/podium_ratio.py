from db.mongo import DATABASE

def model(id, season=None):
    constructor_id = int(id)

    # 1. Récupérer les courses (optionnellement filtrées par saison)
    race_query = {}
    if season:
        race_query["year"] = int(season)

    races = list(DATABASE["races"].find(race_query, {"raceId": 1}))
    race_ids = [r["raceId"] for r in races] if races else []

    # 2. Requête sur les résultats pour ce constructeur
    result_query = {"constructorId": constructor_id}
    if race_ids:
        result_query["raceId"] = {"$in": race_ids}

    results = list(DATABASE["results"].find(result_query, {
        "raceId": 1,
        "positionOrder": 1
    }))

    if not results:
        return {"error": "No results found"}, 404

    # 3. Analyser les podiums
    total_races = len(set(r["raceId"] for r in results))
    podiums = len([r for r in results if 1 <= r.get("positionOrder", 0) <= 3])

    if total_races == 0:
        return {"podiumRatio": 0, "podiums": 0, "races": 0}

    ratio = (podiums / total_races) * 100

    return {
        "podiumRatio": round(ratio, 2),
        "podiums": podiums,
        "races": total_races
    }, 200
