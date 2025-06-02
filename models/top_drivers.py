from db.mongo import DATABASE


def model(team_id, season=None):
    """
    Récupère les pilotes ayant rapporté le plus de points à une écurie donnée (optionnellement pour une saison).

    Args:
        team_id (int): ID de l’écurie (constructorId).
        season (int, optional): Saison à filtrer (ex: 2021).

    Returns:
        list: Liste des pilotes avec points totaux et position moyenne.
        int: Status HTTP
    """

    # Étape 1 : filtrer les résultats (results) pour la bonne écurie, éventuellement par saison
    match_stage = {"constructorId": int(team_id)}

    if season:
        # Trouver les raceId de cette saison
        races = list(DATABASE["races"].find({"year": int(season)}, {"raceId": 1}))
        race_ids = [r["raceId"] for r in races]
        match_stage["raceId"] = {"$in": race_ids}

    # Étape 2 : agrégation
    pipeline = [
        {
            "$match": {
                "constructorId": team_id,
                **({"season": season} if season else {})
            }
        },
        {
            "$match": {
                "position": { "$nin": ["\\N", "R", "DNF", None, ""] }
            }
        },
        {
            "$addFields": {
                "positionInt": {
                    "$convert": {
                        "input": "$position",
                        "to": "int",
                        "onError": None,
                        "onNull": None
                    }
                }
            }
        },
        {
            "$group": {
                "_id": "$driverId",
                "totalPoints": {"$sum": "$points"},
                "avgPosition": {"$avg": "$positionInt"}
            }
        },
        {
            "$lookup": {
                "from": "drivers",
                "localField": "_id",
                "foreignField": "driverId",
                "as": "driver"
            }
        },
        {"$unwind": "$driver"},
        {
            "$project": {
                "_id": 0,
                "driverId": "$_id",
                "totalPoints": 1,
                "avgPosition": {"$round": ["$avgPosition", 2]},
                "driverName": {"$concat": ["$driver.forename", " ", "$driver.surname"]}
            }
        },
        {"$sort": {"totalPoints": -1}}
    ]

    results = list(DATABASE["results"].aggregate(pipeline))
    return results, 200 if results else 404
