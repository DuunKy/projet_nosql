from db.mongo import DATABASE
from bson import ObjectId

def serialize_obj_id(doc):
    for k, v in doc.items():
        if isinstance(v, ObjectId):
            doc[k] = str(v)
    return doc

def model(id, season=None, driver=None):
    pipeline = [
        {
            "$match": {
                "constructorId": int(id),
            }
        },
        {
            "$lookup": {
                "from": "races",
                "localField": "raceId",
                "foreignField": "raceId",
                "as": "race"
            }
        },
        { "$unwind": "$race" },
    ]

    if season:
        pipeline.append({
            "$match": {
                "race.year": int(season)
            }
        })

    if driver:
        pipeline.append({
            "$match": {
                "driverId": int(driver)
            }
        })

    pipeline += [
        {
            "$lookup": {
                "from": "qualifying",
                "let": { "raceId": "$raceId", "driverId": "$driverId" },
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    { "$eq": ["$raceId", "$$raceId"] },
                                    { "$eq": ["$driverId", "$$driverId"] }
                                ]
                            }
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "position": 1
                        }
                    }
                ],
                "as": "qualifying"
            }
        },
        { "$unwind": "$qualifying" },

        # Conversion avec gestion d'erreur si valeur non convertible
        {
            "$addFields": {
                "gridPosition": {
                    "$convert": {
                        "input": "$qualifying.position",
                        "to": "int",
                        "onError": None,
                        "onNull": None
                    }
                },
                "finishPosition": {
                    "$convert": {
                        "input": "$position",
                        "to": "int",
                        "onError": None,
                        "onNull": None
                    }
                }
            }
        },

        # Filtrer les documents où on a une position valide
        {
            "$match": {
                "gridPosition": { "$ne": None },
                "finishPosition": { "$ne": None }
            }
        },

        {
            "$project": {
                "driverId": 1,
                "raceId": 1,
                "grid": "$gridPosition",
                "finishPosition": "$finishPosition",
                "delta": { "$subtract": ["$gridPosition", "$finishPosition"] }
            }
        }
    ]

    results = list(DATABASE["results"].aggregate(pipeline))
    # Convert ObjectId en string pour JSON
    results = [serialize_obj_id(r) for r in results]
    return results
