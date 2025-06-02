from models import get_from_collection


def get_seasons(year):
    return get_from_collection.model("seasons", season=year)


def get_circuits(id):
    return get_from_collection.model("circuits", id)


def get_races(id, season):
    return get_from_collection.model("races",id, season=season)


def get_drivers(id):
    return get_from_collection.model("drivers", id)


def get_constructors(id):
    return get_from_collection.model("constructors", id)


def get_results(id):
    return get_from_collection.model("results", id)


def get_qualifying(id):
    return get_from_collection.model("qualifying", qualifyId=id)


def get_pitstops(race_id, stop):
    return get_from_collection.model("pit_stops", race_id=race_id, stop=stop)


def get_lap_times(race_id, driver, lap):
    return get_from_collection.model("lap_times", race_id=race_id, lap=lap, driver=driver)


def get_driver_standings(id):
    return get_from_collection.model( "driver_standings", driver_standings_id=id)


def get_constructor_standings(id):
    return get_from_collection.model("constructor_standings", constructor_standings_id=id)


def get_constructor_results(id):
    return get_from_collection.model("constructor_results", constructor_results_id=id)


def get_sprint_results(id):
    return get_from_collection.model("sprint_results", sprint_results_id=id)