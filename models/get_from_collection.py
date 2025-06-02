from db.mongo import DATABASE
from flask import Response
from bson import json_util

def model(collection_name, id=None, season=None, driver=None, race_id=None, stop=None, qualifyId=None, lap=None, driver_standings_id=None, constructor_standings_id=None, constructor_results_id=None, sprint_results_id=None):

    query = {}
    if id:
        print(collection_name[:-1]+"Id")
        query[collection_name[:-1]+"Id"] = int(id)
    if qualifyId:
        query["qualifyId"] = int(qualifyId)
    if season:
        query["year"] = int(season)
    if driver:
        query["driverId"] = int(driver)
    if race_id:
        query["raceId"] = int(race_id)
    if stop:
        query["stop"] = int(stop)
    if lap:
        query["lap"] = int(lap)
    if driver_standings_id:
        query["driverStandingsId"] = int(driver_standings_id)
    if constructor_standings_id:
        query["constructorStandingsId"] = int(constructor_standings_id)
    if constructor_results_id:
        query["constructorResultsId"] = int(constructor_results_id)
    if sprint_results_id:
        query["resultId"] = int(sprint_results_id)

    collection = DATABASE[collection_name]

    results = list(collection.find(query, {"_id": 0}))  # tu excludes déjà _id

    if not results:
        return {"error": "No data found"}, 404

    # Sérialisation via bson.json_util pour gérer les types MongoDB spécifiques
    return Response(json_util.dumps({"data": results}), mimetype="application/json"), 200
