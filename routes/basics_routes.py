from flask import Blueprint, request

from controllers import basic_controller

basics_api = Blueprint('basics_api', __name__, url_prefix='/api/v1')

# 1. Get Season
@basics_api.route('/seasons', methods=['GET'])
def get_seasons():
    year = request.args.get('year')
    return basic_controller.get_seasons(year)

# 2. Get Circuits
@basics_api.route('/circuits', methods=['GET'])
def get_circuits():
    id = request.args.get('id')
    return basic_controller.get_circuits(id)

# 3. Get Races
@basics_api.route('/races', methods=['GET'])
def get_races():
    id = request.args.get('id')
    season = request.args.get('season')
    return basic_controller.get_races(id, season)

# 4. Get Drivers
@basics_api.route('/drivers', methods=['GET'])
def get_drivers():
    id = request.args.get('id')
    return basic_controller.get_drivers(id)

# 5. Get Constructors
@basics_api.route('/constructors', methods=['GET'])
def get_constructors():
    id = request.args.get('id')
    return basic_controller.get_constructors(id)

# 6. Get Results
@basics_api.route('/results', methods=['GET'])
def get_results():
    id = request.args.get('id')
    season = request.args.get('season')
    return basic_controller.get_results(id, season)

# 7. Get Qualifying
@basics_api.route('/qualifying', methods=['GET'])
def get_qualifying():
    id = request.args.get('id')
    season = request.args.get('season')
    return basic_controller.get_qualifying(id, season)

# 8. Get Pit Stops
@basics_api.route('/pitstops', methods=['GET'])
def get_pitstops():
    id = request.args.get('id')
    season = request.args.get('season')
    return basic_controller.get_pitstops(id, season)

# 9. Get Lap Times
@basics_api.route('/lap-times', methods=['GET'])
def get_lap_times():
    id = request.args.get('id')
    circuit = request.args.get('circuit')
    season = request.args.get('season')
    driver = request.args.get('driver')
    return basic_controller.get_lap_times(id, circuit, season, driver)

# 10. Get Retirements
@basics_api.route('/retirements', methods=['GET'])
def get_retirements():
    id = request.args.get('id')
    season = request.args.get('season')
    return basic_controller.get_retirements(id, season)

# 11. Get Driver Standings
@basics_api.route('/driver-standings', methods=['GET'])
def get_driver_standings():
    id = request.args.get('id')
    season = request.args.get('season')
    return basic_controller.get_driver_standings(id, season)

# 12. Get Constructor Standings
@basics_api.route('/constructor-standings', methods=['GET'])
def get_constructor_standings():
    id = request.args.get('id')
    season = request.args.get('season')
    return basic_controller.get_constructor_standings(id, season)

# 13. Get Constructor Results
@basics_api.route('/constructor-results', methods=['GET'])
def get_constructor_results():
    id = request.args.get('id')
    season = request.args.get('season')
    return basic_controller.get_constructor_results(id, season)

# 14. Get Sprint Results
@basics_api.route('/sprint-results', methods=['GET'])
def get_sprint_results():
    id = request.args.get('id')
    season = request.args.get('season')
    return basic_controller.get_sprint_results(id, season)
