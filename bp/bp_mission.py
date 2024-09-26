from flask import jsonify, Blueprint

from services.queries1 import *
from services.service_mission import *

bp_mission = Blueprint('mission', __name__)


@bp_mission.route('/<int:mission_id>', methods=['GET'])
def get_mission(mission_id):
    mission_data = get_mission_by_id(mission_id)

    if mission_data:
        return jsonify(mission_data), 200
    else:
        return jsonify({"error": "Mission not found"}), 404

@bp_mission.route('/all', methods=['GET'])
def get_all_missions():
    missions = get_all_missions_in_db()
    return jsonify(missions), 200

@bp_mission.route('/air-force-missions/<int:year>', methods=['GET'])
def air_force_missions_by_year(year):
    result = get_air_force_missions_by_city(year)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({"error": "Error retrieving data"}), 500

@bp_mission.route('/average-damage', methods=['GET'])
def average_damage_by_country():
    result = get_average_damage_by_country()
    if result is not None:
        return jsonify(result), 200
    else:
        return jsonify({"error": "Error retrieving data"}), 500