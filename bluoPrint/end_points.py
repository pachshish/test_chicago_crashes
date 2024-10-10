from flask import  Blueprint, jsonify, request

from database.db import crashes, client
from repository.cras_ripository import init_crash_chicago, read_csv

crashes_bp = Blueprint('crashes_bp', __name__, url_prefix='/crashes/')

@crashes_bp.route('/')
def add_database():
    init_crash_chicago()
    return jsonify({"Database successfully added"}), 201

@crashes_bp.route('/', methods=['GET'])
def get_all_crashes():
    all_crashes = list(crashes.find({}, {}))
    client.close()
    return jsonify(all_crashes), 200
