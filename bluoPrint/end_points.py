from flask import  Blueprint, jsonify, request
from datetime import datetime
from database.db import crashes, client
from repository.cras_ripository import init_crash_chicago, read_csv

crashes_bp = Blueprint('crashes_bp', __name__)

#הכנסת כל הנתונים לדאטאבייס
@crashes_bp.route('/init', methods=["POST"])
def add_database():
    init_crash_chicago()
    return jsonify({"Database successfully added"}), 201

#הצגת כל התאונות
@crashes_bp.route('/get_all_crashes', methods=['GET'])
def get_all_crashes():
    all_crashes = list(crashes.find({}, {'_id':0}))
    all_crashes = all_crashes[:100]
    return jsonify(all_crashes), 200

#הצגת התאונות לפי איזור
@crashes_bp.route('/get_count_crashes/<int:beat>', methods=['GET'])
def get_count_crashes(beat):
    count_of_crashes = crashes.count_documents({"BEAT_OF_OCCURRENCE": str(beat)})
    return jsonify({"count_of_crashes_for_beat": count_of_crashes}), 200

#הצגת התאונות לפי איזור ותאריך
@crashes_bp.route('/get_count_crashes_for_time/<int:beat>', methods=['GET'])
def get_count_crashes_for_time(beat):
    try:
        type_of_time = request.args.get('type_of_time')
        time = request.args.get('time')
        if not type_of_time or not time:
            return jsonify({"error": "Missing 'time' or 'type_of_time' parameter"}), 400

        if type_of_time == 'year':
            start_date = datetime(int(time), 1, 1)
            end_date = datetime(int(time) + 1, 1, 1)

        elif type_of_time == 'month':
            year, month = map(int, time.split('/'))
            start_date = datetime(year, month, 1)
            end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

        elif type_of_time == 'day':
            year, month, day = map(int, time.split('/'))
            start_date = datetime(year, month, day)
            end_date = datetime(year,   month, 1 + 1)

        else:
            return jsonify({"error": "Invalid 'type_of_time'. Use 'year', 'month', or 'day'."}), 400

        query = {
            "BEAT_OF_OCCURRENCE": str(beat),
            "CRASH_DATE": {"$gte": start_date, "$lt": end_date}
        }

        count_of_crashes = crashes.count_documents(query)
        return jsonify({"count_of_crashes_for_beat_and_time": count_of_crashes}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#הצגת הפרמטרים של התאונה לפי הסיבה
@crashes_bp.route('/get_params_of_cause_crashes/<int:beat>', methods=['GET'])
def get_params_of_cause_crashes(beat):
    try:
        query = [
            {'$match': {
                'BEAT_OF_OCCURRENCE': str(beat)
            }},
            {'$group': {
                '_id': '$PRIM_CONTRIBUTORY_CAUSE',
                'count': {'$sum': 1},
                'accidents': {'$push': {
                    'INJURIES_TOTAL': '$INJURIES_TOTAL',
                    'MOST_SEVERE_INJURY': '$MOST_SEVERE_INJURY',
                    'INJURIES_FATAL': '$INJURIES_FATAL',
                    'INJURIES_INCAPACITATING': '$INJURIES_INCAPACITATING',
                    'INJURIES_NON_INCAPACITATING': '$INJURIES_NON_INCAPACITATING',
                    'INJURIES_REPORTED_NOT_EVIDENT': '$INJURIES_REPORTED_NOT_EVIDENT',
                    'INJURIES_NO_INDICATION': '$INJURIES_NO_INDICATION',
                    'INJURIES_UNKNOWN': '$INJURIES_UNKNOWN'
                }}
            }},
        ]
        result = list(crashes.aggregate(query))
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@crashes_bp.route('/get_statistics_on_accidents/<int:beat>', methods=['GET'])
def get_injuries_statistics(beat):
    all_crashes = crashes.find({'BEAT_OF_OCCURRENCE': str(beat)})
    count_total = 0
    count_fatal = 0
    for i in list(all_crashes):
        count_total += int(i['INJURIES_TOTAL'])
        count_fatal += int(i['INJURIES_FATAL'])

    events = list(
        crashes.find({'BEAT_OF_OCCURRENCE': str(beat)}, {'_id': 0, 'CRASH_RECORD_ID': 1, 'CRASH_DATE': 1, 'BEAT_OF_OCCURRENCE': 1}))

    response = {
        'total_injuries': count_total,
        'fatal_injuries': count_fatal,
        'non_fatal_injuries': count_total - count_fatal,
        'events': events
    }

    return jsonify(response)

