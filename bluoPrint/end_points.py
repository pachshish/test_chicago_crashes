from flask import  Blueprint, jsonify, request

from database.db import crashes, client
from repository.cras_ripository import init_crash_chicago, read_csv

crashes_bp = Blueprint('crashes_bp', __name__)

@crashes_bp.route('/init', methods=["POST"])
def add_database():
    init_crash_chicago()
    return jsonify({"Database successfully added"}), 201

@crashes_bp.route('/get_all_crashes', methods=['GET'])
def get_all_crashes():
    all_crashes = list(crashes.find({}, {'_id':0}))
    all_crashes = all_crashes[:100]
    return jsonify(all_crashes), 200

@crashes_bp.route('/get_count_crashes/<int:beat>', methods=['GET'])
def get_count_crashes(beat):
    count_of_crashes = crashes.count_documents({"BEAT_OF_OCCURRENCE": str(beat)})
    return jsonify({"count": count_of_crashes}), 200

