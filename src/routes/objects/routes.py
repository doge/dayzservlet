from flask import Blueprint, jsonify, request
from src.utils import Interfaces, log

objects = Blueprint("objects", __name__)

@objects.route("/DayZServlet/objects/save_obj/", methods=["POST"])
def save_obj():
    try:
        data = request.get_json()  # Get the JSON data from the request

        # Assuming the 'oid' parameter is part of the URL
        oid = request.args.get("oid")

        # Extract the model and state data from the incoming JSON
        model = data.get("model")
        state = data.get("state")

        # # Assuming 'items' array is present in the incoming JSON
        # items = data.get("items", [])

        # Log the received data for debugging purposes
        log("/objects/save_obj", f"[{oid}] Received object with model: {model}")
        log("/objects/save_obj", f"[{oid}] Received object with state: {state}")

        # Return a success response
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        # In case of an error, return an error response
        return jsonify({'status': 'error', 'message': str(e)}), 500

@objects.route("/DayZServlet/objects/load_obj/", methods=["POST", "GET"])
def load_obj():
    oid = request.args.get('oid', None, str)
    if not oid:
        return jsonify({'status': 'error', 'message': 'Missing object ID'}), 400

    obj = Interfaces.objects.find_one({'oid': oid})

    if obj is None:
        return jsonify({'status': 'error', 'message': 'Object not found'}), 404

    item_data = obj['item_data']

    response_data = {
        'model': item_data['model'],
        'items': item_data['items'],
        'state': item_data['state']
    }

    log("/objects/load_obj/", f"[{obj}] [{oid}] served object.")
    return jsonify(response_data)

@objects.route("/DayZServlet/objects/kill_obj/", methods=["POST", "GET"])
def kill_obj():
    oid = request.args.get('obj', None, str)
    if not oid:
        return jsonify({'status': 'error', 'message': 'Missing object ID'}), 400

    obj = Interfaces.objects.find_one({'oid': oid})

    if obj is None:
        return jsonify({'status': 'error', 'message': 'Object not found'}), 404

    query = Interfaces.objects.delete({'oid': oid})
    if query.deleted_count:
        log("/objects/remove/", f"[{oid}] removed from world.")
    else:
        # log("/world/remove/", f"[{item['type']}] does not exist in world.")
        pass

    return jsonify({'status': 'success'}), 200


@objects.route("/DayZServlet/objects/count/", methods=["GET"])
def count_objects():
    objects = Interfaces.objects.find({}, {"oid": 0})
    count = objects.count(True)
    ids = [obj["oid"] for obj in objects]

    response_data = {
        "ids": ids
    }

    return jsonify(response_data)