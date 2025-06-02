from db.mongo import DATABASE

def model(year):
    """
    Retrieve the constructors standings for a given season.

    Args:
        year (int): The year of the season for which to retrieve standings.

    Returns:
        tuple: (list of constructors standings, HTTP status code)
    """
    try:
        races = list(DATABASE["races"].find(
            {"year": int(year)}, {"raceId": 1}
        ).sort("date", 1))

        print("DEBUG: races trouvées =", races)

        if not races:
            return [], 404

        latest_race_id = races[-1]["raceId"]  # ici, on récupère le champ entier raceId
        print("DEBUG: latest_race_id =", latest_race_id)

        standings = list(DATABASE["constructor_standings"].find(
            {"raceId": latest_race_id},
            {"_id": 0, "constructorId": 1, "points": 1, "position": 1}
        ))

        print("DEBUG: standings =", standings)

        return standings, 200

    except Exception as e:
        return {"message": f"Erreur interne : {str(e)}"}, 500
