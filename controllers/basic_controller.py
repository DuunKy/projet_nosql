from models import seasons, get_id, get_id_season, lap_times


def get_seasons(year):
    return seasons.model(year)


def get_circuits(id):
    return get_id.model("circuits", id)


def get_races(id, season):
    return get_id_season.model("races",id, season)


def get_drivers(id):
    return get_id.model("drivers", id)


def get_constructors(id):
    return get_id.model("constructors", id)


def get_results(id, season):
    return get_id_season.model("results", id, season)


def get_qualifying(id, season):
    return get_id_season.model("qualifying", id, season)


def get_pitstops(id, season):
    return get_id_season.model("pitstops", id, season)


def get_lap_times(id, circuit, season, driver):
    return lap_times.model(id, circuit, season, driver)


def get_retirements(id, season):
    return get_id_season.model("retirements", id, season)


def get_driver_standings(id, season):
    return get_id_season.model( "driver_standings", id, season)


def get_constructor_standings(id, season):
    return get_id_season.model("constructor_standings", id, season)


def get_constructor_results(id, season):
    return get_id_season.model("constructor_results", id, season)


def get_sprint_results(id, season):
    return get_id_season.model("sprint_results", id, season)