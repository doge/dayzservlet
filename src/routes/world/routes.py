from flask import Blueprint, jsonify, request
from src.utils import Interfaces, log

world = Blueprint("world", __name__)

@world.route("/DayZServlet/world/add/", methods=["POST"])
def add():
    item = request.json

    Interfaces.world.insert(item)
    log("/world/add/", f"[{item['type']}] added to world.")

    return jsonify({'status': 'success'}), 200

@world.route("/DayZServlet/world/remove/", methods=["POST"])
def remove():
    item = request.json

    Interfaces.world.delete(item)
    log("/world/remove/", f"[{item['type']}] removed from world.")

    return jsonify({'status': 'success'}), 200

@world.route("/DayZServlet/world/count/", methods=["POST"])
def count():
    items = Interfaces.world.find()
    log("/world/count/", "Count requested.")

    return jsonify({'count': len(items)}), 200
