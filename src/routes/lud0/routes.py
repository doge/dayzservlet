from flask import Blueprint, jsonify, request
from src.utils import Interfaces, log
from datetime import datetime, timedelta
import moment

lud0 = Blueprint("lud0", __name__)

@lud0.route('/DayZServlet/lud0/find/', methods=['POST', 'GET'])
def find():
    uid = request.args.get('uid', None, str)
    player = Interfaces.database.find_one({'uid': uid})

    if player:
        try:
            # calculate queue seconds
            moment_time = moment.date(player['queue'])
            formatted_seconds = round(-moment_time.diff(moment.now(), 'seconds').total_seconds())
            player['queue'] = formatted_seconds
        except KeyError:
            player['queue'] = 0
            log("/lud0/find/", f"[{uid}] Queue time not found. Skipping...")

        log("/lud0/find/", f"[{uid}] Found player!")

        del player['_id']
        return jsonify(player)

    log("/lud0/find/", f"[{uid}] Player not found.")
    return jsonify({'status': 'player not found'}), 200

@lud0.route('/DayZServlet/lud0/load/', methods=['POST', 'GET'])
def load():
    uid = request.args.get('uid', None, str)
    player = Interfaces.database.find_one({'uid': uid})

    if player:
        try:
            # calculate queue seconds
            moment_time = moment.date(player['queue'])
            formatted_seconds = round(-moment_time.diff(moment.now(), 'seconds').total_seconds())
            player['queue'] = formatted_seconds
        except KeyError:
            player['queue'] = 0
            log("/lud0/load/", f"[{uid}] Queue time not found. Skipping...")

        log("/lud0/load/", f"[{uid}] Loaded player.")

        del player['_id']
        return jsonify(player)

    log("/lud0/load/", f"[{uid}] Couldn't load player!")
    return jsonify({'status': 'error'}), 200

@lud0.route('/DayZServlet/lud0/create/', methods=['POST'])
def create():
    uid = request.args.get('uid', None, str)
    if not Interfaces.database.find_one({'uid': uid}):
        try:
            Interfaces.database.insert({
                'uid': uid
            })
            log("/lud0/create/", f"[{uid}] Creating player..")
        except Exception as e:
            log("/lud0/create/", f"[{uid}] Error creating player.")
            log("[Exception]", e)

        return jsonify({'status': 'success'}), 200

    log("/lud0/create/", f"[{uid}] Player already exists.")
    return jsonify({
        'status': 'error',
        'message': 'player already exists'
    }), 200

@lud0.route('/DayZServlet/lud0/save/', methods=['POST'])
def save():
    uid = request.args.get('uid', None, str)
    Interfaces.database.update({'uid': uid}, {
        '$set': request.json
    })

    log("/lud0/save/", f"[{uid}] Saved player.")
    return jsonify({'status': 'success'}), 200

@lud0.route('/DayZServlet/lud0/queue/', methods=['POST'])
def queue():
    uid = request.args.get('uid', None, str)
    player = Interfaces.database.find_one({'uid': uid})

    if player:
        add_queue_time = datetime.now() + timedelta(seconds=request.json['queue'])
        player['queue'] = add_queue_time
        try:
            Interfaces.database.update({'uid': uid}, {
                '$set': player
            })
            log("/lud0/queue/", f"[{uid}] Set queue time.")
        except Exception as e:
            log("/lud0/queue/", f"[{uid}] Error setting queue time.")
            log("[Exception]", e)

    return jsonify({'status': 'success'}), 200

@lud0.route('/DayZServlet/lud0/kill/', methods=['POST'])
def kill():
    uid = request.args.get('uid', None, str)
    if Interfaces.database.find_one({'uid': uid}):
        try:
            Interfaces.database.delete({'uid': uid})
            log("/lud0/kill/", f"[{uid}] Successfully killed player.")
        except Exception as e:
            log("/lud0/kill/", f"[{uid}] Error killing player!")
            log("[Exception", e)

        log("/lud0/kill/", f"[{uid}] couldn't kill player!")
    return jsonify({'status': 'success'}), 200
