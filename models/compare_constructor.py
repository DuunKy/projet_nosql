from db.mongo import DATABASE
from collections import defaultdict

def model(ids, season=None):
    constructor_ids = [int(cid) for cid in ids]  # assure que ce sont des entiers

    # 1. Récupération des raceIds si saison filtrée
    race_ids = None
    if season is not None:
        season = int(season)
        races = list(DATABASE["races"].find({"year": season}, {"raceId": 1}))
        race_ids = [race["raceId"] for race in races]
        if not race_ids:
            return {"error": "no race ids for season"}, 404

    # 2. Construction de la requête pour récupérer les résultats
    query = {"constructorId": {"$in": constructor_ids}}
    if race_ids:
        query["raceId"] = {"$in": race_ids}

    results = list(DATABASE["results"].find(query, {
        "constructorId": 1,
        "positionOrder": 1,
        "points": 1
    }))

    # 3. Statistiques par écurie
    stats = defaultdict(lambda: {
        "constructorId": None,
        "totalPoints": 0,
        "podiums": 0,
        "avgPosition": 0,
        "entries": 0
    })

    for res in results:
        cid = res["constructorId"]
        stats[cid]["constructorId"] = cid
        stats[cid]["totalPoints"] += res.get("points", 0)
        pos = res.get("positionOrder")
        if pos:
            stats[cid]["entries"] += 1
            stats[cid]["avgPosition"] += pos
            if pos <= 3:
                stats[cid]["podiums"] += 1

    # 4. Moyenne des positions
    for s in stats.values():
        if s["entries"] > 0:
            s["avgPosition"] = round(s["avgPosition"] / s["entries"], 2)
        else:
            s["avgPosition"] = None  # ou float("nan") selon besoin

    return list(stats.values()), 200
