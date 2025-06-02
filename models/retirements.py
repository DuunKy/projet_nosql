from db.mongo import DATABASE

def model(id, season):
    pipeline = [
        # Étape 1 : joindre avec les courses pour filtrer par saison
        {
            "$lookup": {
                "from": "races",
                "localField": "raceId",
                "foreignField": "raceId",
                "as": "race"
            }
        },
        { "$unwind": "$race" },

        # Étape 2 : filtrer les résultats de l’écurie et de la saison
        {
            "$match": {
                "constructorId": int(id),
                "race.year": int(season),
                "statusId": { "$ne": 1 }  # Abandons seulement
            }
        },

        # Étape 3 : joindre avec les statuts pour obtenir la raison
        {
            "$lookup": {
                "from": "status",
                "localField": "statusId",
                "foreignField": "statusId",
                "as": "status"
            }
        },
        { "$unwind": "$status" },

        # Étape 4 : regrouper par pilote
        {
            "$group": {
                "_id": "$driverId",
                "retirementCount": { "$sum": 1 },
                "reasons": { "$addToSet": "$status.status" }
            }
        },
        {
            "$project": {
                "_id": 0,
                "driverId": "$_id",
                "retirementCount": 1,
                "reasons": 1
            }
        }
    ]

    return list(DATABASE["results"].aggregate(pipeline))
