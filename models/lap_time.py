from db.mongo import DATABASE

def model(team_id, circuit, season, driver):
    pipeline = [
        # Étape 1 : jointure avec la collection "races" pour obtenir circuitId + saison
        {
            "$lookup": {
                "from": "races",
                "localField": "raceId",
                "foreignField": "raceId",
                "as": "race"
            }
        },
        { "$unwind": "$race" },

        # Étape 2 : filtrage sur circuitId, saison, driverId
        {
            "$match": {
                "race.circuitId": int(circuit),
                "race.year": int(season),
                "driverId": int(driver)
            }
        },

        # Étape 3 : jointure avec "results" pour valider que le pilote appartient bien à l'écurie
        {
            "$lookup": {
                "from": "results",
                "let": {
                    "race_id": "$raceId",
                    "driver_id": "$driverId"
                },
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    { "$eq": [ "$raceId", "$$race_id" ] },
                                    { "$eq": [ "$driverId", "$$driver_id" ] },
                                    { "$eq": [ "$constructorId", int(team_id) ] }
                                ]
                            }
                        }
                    }
                ],
                "as": "result"
            }
        },

        # Étape 4 : filtrer ceux qui n'ont pas matché l'écurie
        {
            "$match": {
                "result": { "$ne": [] }
            }
        },

        # Étape 5 : regrouper par circuit pour moyenne
        {
            "$group": {
                "_id": "$race.circuitId",
                "circuitName": { "$first": "$race.name" },
                "avgLapTimeMs": { "$avg": "$milliseconds" },
                "totalLaps": { "$sum": 1 }
            }
        },

        # Étape 6 : format final de sortie
        {
            "$project": {
                "_id": 0,
                "circuitId": "$_id",
                "circuitName": 1,
                "avgLapTimeMs": 1,
                "totalLaps": 1
            }
        }
    ]

    results = list(DATABASE["lap_times"].aggregate(pipeline))
    return results
