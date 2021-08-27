from flask import Flask, request, jsonify
from config import Config
from database import Database
from datetime import datetime, timedelta
import moment

database = Database(Config.credentials, 'players')


def log(uid, message):
    print("[%s] %s" % (uid, message))


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.secret_key
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

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

            log(uid, "[find] successfully found")

            return jsonify(player)

        log(uid, "[find] could not find")
        return jsonify({'status': 'error'}), 200

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

            log(uid, "[load] loaded player")

            return jsonify(player)

        log(uid, "[load] could not load")
        return jsonify({'status': 'error'}), 200

    @app.route('/DayZServlet/lud0/create/', methods=['POST'])
    def create():
        uid = request.args.get('uid', None, str)
        if not database.find_one({'uid': uid}):
            try:
                database.insert({
                    'uid': uid
                })
                log(uid, "[create] creating player..")
            except:
                log(uid, "[create] couldn't create player")
            return jsonify({'status': 'success'}), 200

        log(uid, "[create] player already exists")
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
        log(uid, "[save] saved player")
        return jsonify({'status': 'success'}), 200

    @app.route('/DayZServlet/lud0/queue/', methods=['POST'])
    def queue():
        uid = request.args.get('uid', None, str)
        player = database.find_one({'uid': uid})

        if player:
            add_queue_time = datetime.now() + timedelta(seconds=request.json['queue'])
            player['queue'] = add_queue_time
            try:
                database.update({'uid': uid}, {
                    '$set': player
                })
                log(uid, "[queue] set queue time")
            except:
                log(uid, "[queue] error setting queue time")

        return jsonify({'status': 'success'}), 200

    @app.route('/DayZServlet/lud0/kill/', methods=['POST'])
    def kill():
        uid = request.args.get('uid', None, str)
        if database.find_one({'uid': uid}):
            try:
                database.delete({'uid': uid})
                log(uid, "[kill] successfully killed player")
            except:
                log(uid, "[kill] couldn't kill player")

            log(uid, "[kill] couldn't kill player")
        return jsonify({'status': 'success'}), 200

    return app


if __name__ == '__main__':
    create_app().run()
