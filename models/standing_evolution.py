from db.mongo import DATABASE

def model(id, season):
    constructor_id = int(id)
    season = int(season)

    # 1. Récupérer les courses de la saison, triées par ordre chronologique (par 'round')
    races = list(DATABASE["races"].find(
        {"year": season},
        {"raceId": 1, "round": 1}
    ).sort("round", 1))

    if not races:
        return {"error": "No races found for this season"}, 404

    race_id_by_round = {race["raceId"]: race["round"] for race in races}

    # 2. Récupérer le classement constructeur par course
    standings = list(DATABASE["constructor_standings"].find(
        {
            "raceId": {"$in": list(race_id_by_round.keys())},
            "constructorId": constructor_id
        },
        {"raceId": 1, "position": 1}
    ))

    if not standings:
        return {"error": "No standings found for this constructor"}, 404

    # 3. Mapper les standings à leur round pour avoir un classement par course
    evolution = []
    for s in standings:
        round_number = race_id_by_round.get(s["raceId"])
        if round_number is not None:
            evolution.append({
                "round": round_number,
                "position": s["position"]
            })

    # 4. Trier le résultat par round
    evolution.sort(key=lambda x: x["round"])

    return {
        "constructorId": constructor_id,
        "season": season,
        "evolution": evolution
    }, 200
