from flask import Blueprint, jsonify, request
from src.utils import Interfaces, log

world = Blueprint("world", __name__)

@world.route("/DayZServlet/world/add/", methods=["POST"])
def add():
    item = request.json

    Interfaces.world.insert(item)
    log("/world/add/", f"[{item['type']}] added to world.")

    return jsonify({'status': 'success'}), 200

@world.route("/DayZServlet/world/save_obj/", methods=["POST"])
def save_obj():
    uid = request.args.get('objuid', None, str)
    Interfaces.database.update({'objuid': uid}, {
        '$set': request.json
    })

    log("/world/save_obj", f"[{objuid}] Saved object.")
    return jsonify({'status': 'success'}), 200

@world.route("/DayZServlet/world/remove/", methods=["POST"])
def remove():
    item = request.json

    query = Interfaces.world.delete(item)
    if query.deleted_count:
        log("/world/remove/", f"[{item['type']}] removed from world.")
    else:
        # log("/world/remove/", f"[{item['type']}] does not exist in world.")
        pass

    return jsonify({'status': 'success'}), 200

@world.route("/DayZServlet/world/count/", methods=["POST", "GET"])
def count():
    items = Interfaces.world.find()

    log("/world/count/", "served count.")

    return jsonify({'count': len(items)}), 200

@world.route("/DayZServlet/world/get/", methods=["POST", "GET"])
def get():
    item_id = request.json['item']

    items = Interfaces.world.find()
    
    item = items[item_id]

    log("/world/get/", f"[{item_id}] [{item['type']}] served object.")
    
    del item['_id'];
    return item
