from flask import jsonify

from models import team_performance, constructors_standings, top_drivers, lap_time, retirements, qualif_vs_race, \
    pitstop, compare_constructor, top_circuit, driver_averages_by_race, grid_stats, podium_ratio, sprint_laps, \
    standing_evolution, full_comparison


def get_team_performance(team_id, season=None):
    return team_performance.model(team_id, season)

def get_constructors_standings(year):
    return constructors_standings.model(year)

def get_top_drivers(team_id, season=None):
    return top_drivers.model(team_id, season)

def get_lap_times(id, cicuit, season, driver):
    if not driver or not season:
        return {"error": "Driver and season parameters are required"}, 400

    return lap_time.model(id, cicuit, season, driver)

def get_retirements(id, season):
    if not season:
        return {"error": "Season parameter is required"}, 400
    return retirements.model(id, season)


def get_qualif_vs_race(id, season, driver):
    return qualif_vs_race.model(id, season, driver)


def get_pitstops(id, season):
    return pitstop.model(id, season)


def compare_constructors(ids, season):
    return compare_constructor.model(ids, season)


def get_top_circuits(id, season, driver):
    return top_circuit.model(id, season, driver)


def get_driver_averages_by_race(id, season, circuit):
    return driver_averages_by_race.model(id, season, circuit)


def get_grid_stats(id, season, driver, circuit):
    return grid_stats.model(id, season, driver, circuit)


def get_podium_ratio(id, season):
    return podium_ratio.model(id, season)


def get_sprint_laps(id, season, driver, circuit):
    return sprint_laps.model(id, season, driver, circuit)


def get_standing_evolution(id, season):
    if not season:
        return {"error": "Season parameter is required"}, 400
    return standing_evolution.model(id, season)


def get_full_comparison(id, season, driver):
    return full_comparison.model(id, season, driver)