from db.mongo import DATABASE
from collections import defaultdict

def model(id, season=None, driver=None, circuit=None):
    constructor_id = int(id)

    # Étape 1 : Construire la query pour filtrer les courses
    race_query = {}
    if season:
        race_query["year"] = int(season)
    if circuit:
        race_query["circuitId"] = int(circuit)

    races = list(DATABASE["races"].find(race_query, {"raceId": 1}))
    race_ids = [r["raceId"] for r in races] if races else []

    # Étape 2 : Requête sur les résultats
    query = {
        "constructorId": constructor_id
    }
    if race_ids:
        query["raceId"] = {"$in": race_ids}
    if driver:
        query["driverId"] = int(driver)

    results = list(DATABASE["results"].find(query, {
        "driverId": 1,
        "grid": 1
    }))

    if not results:
        return {"error": "No results found"}, 404

    # Étape 3 : Calcul de la position moyenne sur la grille par pilote
    driver_grid_stats = defaultdict(lambda: {"sum": 0, "count": 0})
    for res in results:
        driver_id = res["driverId"]
        grid = res.get("grid")
        if grid is not None and grid >= 0:
            driver_grid_stats[driver_id]["sum"] += grid
            driver_grid_stats[driver_id]["count"] += 1

    output = []
    for driver_id, data in driver_grid_stats.items():
        avg_grid = data["sum"] / data["count"] if data["count"] > 0 else None
        output.append({
            "driverId": driver_id,
            "averageGrid": round(avg_grid, 2) if avg_grid is not None else None,
            "starts": data["count"]
        })

    # Tri par grille moyenne croissante (meilleurs départs en premier)
    output.sort(key=lambda x: x["averageGrid"] if x["averageGrid"] is not None else 999)

    return output, 200
