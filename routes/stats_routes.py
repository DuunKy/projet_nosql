from flask import Blueprint, request, jsonify
from controllers import *
from controllers import team_performance_controller, constructors_standings_controller, top_drivers_controller, \
    lap_times_controller, retirements_controller

stats_api = Blueprint('stats_api', __name__, url_prefix='/api/v1')

# 1. Evolution des performances d'une écurie sur une saison
@stats_api.route('/teams/<int:constructorId>/performance', methods=['GET'])
def get_team_performance(constructorId):
    season = request.args.get('season')
    return team_performance_controller.get_team_performance(constructorId, season)

# 2. Classement général des écuries pour une saison
@stats_api.route('/seasons/<int:year>/constructors/standings', methods=['GET'])
def get_constructors_standings(year):
    return constructors_standings_controller.get_constructors_standings(year)

# 3. Meilleurs pilotes d'une écurie donnée
@stats_api.route('/constructors/<int:id>/top-drivers', methods=['GET'])
def get_top_drivers(id):
    season = request.args.get('season')
    return top_drivers_controller.get_top_drivers(id, season)

# 4. Temps moyen au tour par circuit
@stats_api.route('/constructors/<int:id>/lap-times', methods=['GET'])
def get_lap_times(id):
    season = request.args.get('season')
    return lap_times_controller.get_lap_times(id, season)

# 5. Nombre d'abandons par saison
@stats_api.route('/constructors/<int:id>/retirements', methods=['GET'])
def get_retirements(id):
    season = request.args.get('season')
    return retirements_controller.get_retirements(id, season)

# 6. Comparaison qualifs vs résultats en course
@stats_api.route('/constructors/<int:id>/qualif-vs-race', methods=['GET'])
def get_qualif_vs_race(id):
    return jsonify({'message': f'Qualif vs Race for constructor {id}'}), 200

# 7. Performances dans les arrêts au stand
@stats_api.route('/constructors/<int:id>/pitstops', methods=['GET'])
def get_pitstops(id):
    return jsonify({'message': f'Pitstops performance for constructor {id}'}), 200

# 8. Comparaison avec les autres écuries
@stats_api.route('/constructors/compare', methods=['GET'])
def compare_constructors():
    ids = request.args.getlist('ids[]')
    season = request.args.get('season')
    return jsonify({'message': f'Compare constructors {ids} season {season}'}), 200

# 9. Répartition des circuits où l’écurie performe le mieux
@stats_api.route('/constructors/<int:id>/top-circuits', methods=['GET'])
def get_top_circuits(id):
    return jsonify({'message': f'Top circuits for constructor {id}'}), 200

# 10. Moyenne de points par pilote et par course
@stats_api.route('/constructors/<int:id>/driver-averages', methods=['GET'])
def get_driver_averages(id):
    return jsonify({'message': f'Driver averages for constructor {id}'}), 200

# 11. Position moyenne sur la grille de départ
@stats_api.route('/constructors/<int:id>/grid-stats', methods=['GET'])
def get_grid_stats(id):
    return jsonify({'message': f'Grid stats for constructor {id}'}), 200

# 12. Ratio de podiums par rapport aux courses courues
@stats_api.route('/constructors/<int:id>/podium-ratio', methods=['GET'])
def get_podium_ratio(id):
    return jsonify({'message': f'Podium ratio for constructor {id}'}), 200

# 13. Temps moyen au tour dans les sprints
@stats_api.route('/constructors/<int:id>/sprint-laps', methods=['GET'])
def get_sprint_laps(id):
    return jsonify({'message': f'Sprint laps average for constructor {id}'}), 200

# 14. Evolution du classement par course
@stats_api.route('/constructors/<int:id>/standing-evolution', methods=['GET'])
def get_standing_evolution(id):
    season = request.args.get('season')
    return jsonify({'message': f'Standing evolution for constructor {id} season {season}'}), 200

# 15. Comparaison performances qualif vs sprint vs course
@stats_api.route('/constructors/<int:id>/full-comparison', methods=['GET'])
def get_full_comparison(id):
    season = request.args.get('season')
    return jsonify({'message': f'Full comparison for constructor {id} season {season}'}), 200
