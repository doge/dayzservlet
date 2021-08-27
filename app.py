from flask import Flask, request, jsonify
from config import Config
from database import Database
from datetime import datetime, timedelta
import moment

database = Database(Config.credentials, 'players')

app = Flask(__name__)


@app.route('/DayZServlet/lud0/find/', methods=['POST', 'GET'])
def find():
    uid = request.args.get('uid', None, str)
    player = database.find_one({'uid': uid})

    if player:
        player['_id'] = str(player['_id'])

        # calculate queue seconds
        moment_time = moment.date(player['queue'])
        formatted_seconds = round(-moment_time.diff(moment.now(), 'seconds').total_seconds())
        player['queue'] = formatted_seconds

        return player

    return jsonify({'status': 'success'}), 200


@app.route('/DayZServlet/lud0/load/', methods=['POST', 'GET'])
def load():
    uid = request.args.get('uid', None, str)
    player = database.find_one({'uid': uid})
    if player:
        player['_id'] = str(player['_id'])

        # calculate queue seconds
        moment_time = moment.date(player['queue'])
        formatted_seconds = round(-moment_time.diff(moment.now(), 'seconds').total_seconds())
        player['queue'] = formatted_seconds

        return player

    return jsonify({'status': 'success'}), 200


@app.route('/DayZServlet/lud0/create/', methods=['POST'])
def create():
    uid = request.args.get('uid', None, str)

    if not database.find_one({'uid': uid}):
        database.insert({
            'uid': uid
        })
        return jsonify({'status': 'success'}), 200

    return jsonify({
        'status': 'error',
        'message': 'player already exists'
    }), 200


@app.route('/DayZServlet/lud0/save/', methods=['POST'])
def save():
    uid = request.args.get('uid', None, str)
    database.update({'uid': uid}, {
        '$set': request.json
    })

    return jsonify({'status': 'success'}), 200


@app.route('/DayZServlet/lud0/queue/', methods=['POST'])
def queue():
    uid = request.args.get('uid', None, str)
    player = database.find_one({'uid': uid})

    if player:
        add_queue_time = datetime.now() + timedelta(seconds=request.json['queue'])
        player['queue'] = add_queue_time
        database.update({'uid': uid}, {
            '$set': player
        })

    return jsonify({'status': 'success'}), 200


@app.route('/DayZServlet/lud0/kill/', methods=['POST'])
def kill():
    uid = request.args.get('uid', None, str)
    if database.find_one({'uid': uid}):
        database.delete({'uid': uid})

    return jsonify({'status': 'success'}), 200
