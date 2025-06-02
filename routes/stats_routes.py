from flask import Blueprint, request

from controllers import controller
from controllers.controller import *

stats_api = Blueprint('stats_api', __name__, url_prefix='/api/v1')

# 1. Evolution des performances d'une écurie sur une saison
@stats_api.route('/teams/<int:constructorId>/performance', methods=['GET'])
def get_team_performance(constructorId):
    season = request.args.get('season')
    return controller.get_team_performance(constructorId, season)

# 2. Classement général des écuries pour une saison
@stats_api.route('/seasons/<int:year>/constructors/standings', methods=['GET'])
def get_constructors_standings(year):
    return controller.get_constructors_standings(year)

# 3. Meilleurs pilotes d'une écurie donnée
@stats_api.route('/constructors/<int:id>/top-drivers', methods=['GET'])
def get_top_drivers(id):
    season = request.args.get('season')
    return controller.get_top_drivers(id, season)

# 4. Temps moyen au tour par circuit
@stats_api.route('/constructors/<int:id>/<int:cicuit>/lap-times', methods=['GET'])
def get_lap_times(id, cicuit):
    season = request.args.get('season')
    driver = request.args.get('driver')
    return controller.get_lap_times(id, cicuit, season, driver)

# 5. Nombre d'abandons par saison
@stats_api.route('/constructors/<int:id>/retirements', methods=['GET'])
def get_retirements(id):
    season = request.args.get('season')
    return controller.get_retirements(id, season)

# 6. Comparaison qualifs vs résultats en course
@stats_api.route('/constructors/<int:id>/qualif-vs-race', methods=['GET'])
def get_qualif_vs_race(id):
    season = request.args.get('season')
    driver = request.args.get('driver')
    return controller.get_qualif_vs_race(id, season, driver)

# 7. Performances dans les arrêts au stand
@stats_api.route('/constructors/<int:id>/pitstops', methods=['GET'])
def get_pitstops(id):
    season = request.args.get('season')
    return controller.get_pitstops(id, season)

# 8. Comparaison avec les autres écuries
@stats_api.route('/constructors/compare', methods=['GET'])
def compare_constructors():
    ids = request.args.getlist('ids[]')
    season = request.args.get('season')
    return controller.compare_constructors(ids, season)

# 9. Répartition des circuits où l’écurie performe le mieux
@stats_api.route('/constructors/<int:id>/top-circuits', methods=['GET'])
def get_top_circuits(id):
    season = request.args.get('season')
    driver = request.args.get('driver')
    return controller.get_top_circuits(id, season, driver)

# 10. Moyenne de points par pilote et par course
@stats_api.route('/constructors/<int:id>/driver-averages', methods=['GET'])
def get_driver_averages(id):
    season = request.args.get('season')
    circuit = request.args.get('circuit')
    return controller.get_driver_averages_by_race(id, season, circuit)

# 11. Position moyenne sur la grille de départ
@stats_api.route('/constructors/<int:id>/grid-stats', methods=['GET'])
def get_grid_stats(id):
    season = request.args.get('season')
    driver = request.args.get('driver')
    circuit = request.args.get('circuit')
    return controller.get_grid_stats(id, season, driver, circuit)

# 12. Ratio de podiums par rapport aux courses courues
@stats_api.route('/constructors/<int:id>/podium-ratio', methods=['GET'])
def get_podium_ratio(id):
    season = request.args.get('season')
    return controller.get_podium_ratio(id, season)

# 13. Temps moyen au tour dans les sprints
@stats_api.route('/constructors/<int:id>/sprint-laps', methods=['GET'])
def get_sprint_laps(id):
    season = request.args.get('season')
    driver = request.args.get('driver')
    circuit = request.args.get('circuit')
    return controller.get_sprint_laps(id, season, driver, circuit)

# 14. Evolution du classement par course
@stats_api.route('/constructors/<int:id>/standing-evolution', methods=['GET'])
def get_standing_evolution(id):
    season = request.args.get('season')
    return controller.get_standing_evolution(id, season)

# 15. Comparaison performances qualif vs sprint vs course
@stats_api.route('/constructors/<int:id>/full-comparison', methods=['GET'])
def get_full_comparison(id):
    season = request.args.get('season')
    driver = request.args.get('driver')
    return controller.get_full_comparison(id, season, driver)
