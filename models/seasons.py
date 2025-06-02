from db.mongo import DATABASE


def model(year):
    if year:
        seasons = DATABASE['seasons'].find({'year': int(year)})
    else:
        seasons = DATABASE['seasons'].find()
    seasons_list = [season for season in seasons]
    return seasons_list, 200