from db.mongo import DATABASE


def model(team_id, season=None):
    """
    Retrieve the performance evolution of a team over a season or all seasons if null.
    :param team_id: ID de l'écurie (string)
    :param season: année de la saison (int ou string), ou None pour tout
    :return: Liste des courses avec nom, date, points marqués
    """
    races_collection = DATABASE['races']
    results_collection = DATABASE['results']

    # Filtrer les courses selon la saison si fournie
    race_filter = {}
    if season:
        race_filter["year"] = int(season)

    # Récupérer les courses concernées
    races = list(races_collection.find(race_filter, {"_id": 1, "name": 1, "date": 1}).sort("date", 1))
    race_ids = [race["_id"] for race in races]

    # Récupérer les résultats correspondant à l'écurie et aux courses
    results = results_collection.find({
        "constructorId": team_id,
        "raceId": {"$in": race_ids}
    }, {"raceId": 1, "points": 1})

    # Indexer les points par raceId
    points_by_race = {}
    for res in results:
        race_id = res["raceId"]
        points = res.get("points", 0)
        points_by_race[race_id] = points_by_race.get(race_id, 0) + points  # au cas où plusieurs entrées

    # Construire le résultat final
    performance = []
    for race in races:
        race_id = race["_id"]
        performance.append({
            "raceName": race["name"],
            "date": race["date"],
            "points": points_by_race.get(race_id, 0)
        })

    return performance, 200 if performance else {"error": "No performance data found for the specified team"}, 404
