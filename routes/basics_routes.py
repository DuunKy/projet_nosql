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

    return basic_controller.get_results(id)

# 7. Get Qualifying
@basics_api.route('/qualifying', methods=['GET'])
def get_qualifying():
    id = request.args.get('id')

    return basic_controller.get_qualifying(id)

# 8. Get Pit Stops
@basics_api.route('/pitstops', methods=['GET'])
def get_pitstops():
    raceid = request.args.get('raceid')

    stop = request.args.get('stop')
    return basic_controller.get_pitstops(raceid, stop)

# 9. Get Lap Times
@basics_api.route('/lap-times', methods=['GET'])
def get_lap_times():
    raceid = request.args.get('raceid')

    driver = request.args.get('driver')
    lap = request.args.get('lap')
    return basic_controller.get_lap_times(raceid, driver, lap)

# 10. Get Driver Standings
@basics_api.route('/driver-standings', methods=['GET'])
def get_driver_standings():
    id = request.args.get('id')

    return basic_controller.get_driver_standings(id)

# 11. Get Constructor Standings
@basics_api.route('/constructor-standings', methods=['GET'])
def get_constructor_standings():
    id = request.args.get('id')

    return basic_controller.get_constructor_standings(id)

# 12. Get Constructor Results
@basics_api.route('/constructor-results', methods=['GET'])
def get_constructor_results():
    id = request.args.get('id')

    return basic_controller.get_constructor_results(id)

# 13. Get Sprint Results
@basics_api.route('/sprint-results', methods=['GET'])
def get_sprint_results():
    id = request.args.get('id')

    return basic_controller.get_sprint_results(id)
