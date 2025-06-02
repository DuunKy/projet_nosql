from db.mongo import DATABASE

def model(id, circuit, season, driver):
    if id :
        query = {"id": id}
    else:
        query = {}

    if season:
        query["season"] = season
    if circuit:
        query["circuitId"] = circuit
    if driver:
        query["driverId"] = driver

    collection = DATABASE["lap_times"]

    results = list(collection.find(query, {"_id": 0 }))
    if not results:
        return {"error": "No data found"}, 404
    return {"data": results}, 200
