from flask import Flask, request, jsonify
from config import Config
from database import Database
from datetime import datetime, timedelta
import moment

database = Database(Config.credentials, 'players')


def log(uid, message):
    print("[%s] [%s] %s" % (f"{datetime.now():%Y-%m-%d %H:%M:%S}", uid, message))


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.secret_key
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    log("DayZServlet", "Servlet started!")

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

            log(uid, "[/lud0/find/] Found player!")

            return jsonify(player)

        log(uid, "[/lud0/find/] Player not found.")
        return jsonify({'status': 'player not found'}), 200

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

            log(uid, "[/lud0/load/] Loaded player.")

            return jsonify(player)

        log(uid, "[/lud0/load/] Couldn't load player!")
        return jsonify({'status': 'error'}), 200

    @app.route('/DayZServlet/lud0/create/', methods=['POST'])
    def create():
        uid = request.args.get('uid', None, str)
        if not database.find_one({'uid': uid}):
            try:
                database.insert({
                    'uid': uid
                })
                log(uid, "[/lud0/create/] Creating player..")
            except Exception as e:
                log(uid, "[/lud0/create/] Error creating player.")
                log("[Exception]", e)

            return jsonify({'status': 'success'}), 200

        log(uid, "[/lud0/create/] Player already exists.")
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

        log(uid, "[/lud0/save/] Saved player.")
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
                log(uid, "[/lud0/queue/] Set queue time.")
            except Exception as e:
                log(uid, "[/lud0/queue/] Error setting queue time.")
                log("[Exception]", e)

        return jsonify({'status': 'success'}), 200

    @app.route('/DayZServlet/lud0/kill/', methods=['POST'])
    def kill():
        uid = request.args.get('uid', None, str)
        if database.find_one({'uid': uid}):
            try:
                database.delete({'uid': uid})
                log(uid, "[/lud0/kill/] Successfully killed player.")
            except Exception as e:
                log(uid, "[/lud0/kill/] Error killing player!")
                log("[Exception", e)

            log(uid, "[/lud0/kill/] couldn't kill player!")
        return jsonify({'status': 'success'}), 200

    return app


if __name__ == '__main__':
    create_app().run()
