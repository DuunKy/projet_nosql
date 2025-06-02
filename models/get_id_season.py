from db.mongo import DATABASE

def model(collection_name, id, season):
    if id :
        query = {"id": id}
    else:
        query = {}
    if season:
        query["season"] = season
    collection = DATABASE[collection_name]

    results = list(collection.find(query, {"_id": 0 }))
    if not results:
        return {"error": "No data found"}, 404
    return {"data": results}, 200
