from flask import Blueprint, jsonify, request
from src.utils import Interfaces, log

objects = Blueprint("objects", __name__)

@objects.route("/DayZServlet/objects/save_obj/", methods=["POST"])
def save_obj():
    oid = request.args.get('oid', None, str)
    if not oid:
        log("OID incorrect")
        return jsonify({'status': 'error', 'message': 'Missing object ID'}), 400
    
    data = request.json
    items = data.get('items', [])
    item_data = {
        'model': data.get('model', ''),
        'items': items,
        'state': data.get('state', {})
    }

    document = {
        "oid": oid,
        "item_data": item_data
    }
    
    # Check if document with given oid exists in the database
    existing_doc = Interfaces.objects.find_one({'oid': oid})
    if existing_doc:
        # Update the existing document with the new data
        Interfaces.objects.update({'oid': oid}, {'$set': {'item_data': item_data}})
    else:
        # Create a new document with the given oid and data
        Interfaces.objects.insert(document)

    log("/objects/save_obj", f"[{oid}] Saved object.")
    return jsonify({'status': 'success'}), 200

@objects.route("/DayZServlet/objects/load_obj/", methods=["POST", "GET"])
def load_obj():
    oid = request.args.get('oid', None, str)
    obj = collection.find_one({'uid': oid})
    if obj is None:
        return ""
    
    res_arr = {}
    res_arr['model'] = obj['model']
    res_arr['servid'] = obj['servid']
    res_arr['items'] = obj['items']
    res_arr['state'] = obj['state']
    res_arr['pos'] = [round(obj['x'], 3), round(obj['y'], 3), round(obj['z'], 3)]
    res_arr['dir'] = [round(obj['dir_x'], 3), round(obj['dir_y'], 3), round(obj['dir_z'], 3)]
    res_arr['up'] = [round(obj['up_0'], 3), round(obj['up_1'], 3), round(obj['up_2'], 3)]
    
    log("/objects/load_obj/", f"[{obj}] [{oid['type']}] served object.")
    return jsonify(res_arr)

@objects.route("/DayZServlet/objects/kill_obj/", methods=["POST"])
def kill_obj():
    item = request.json

    query = Interfaces.objects.delete(item)
    if query.deleted_count:
        log("/objects/remove/", f"[{item['type']}] removed from world.")
    else:
        # log("/world/remove/", f"[{item['type']}] does not exist in world.")
        pass

    return jsonify({'status': 'success'}), 200

@objects.route("/DayZServlet/objects/count_obj/", methods=["POST", "GET"])
def count_obj():
    items = Interfaces.objects.find()

    log("/objects/count_obj/", "served count.")

    return jsonify({'count': len(items)}), 200