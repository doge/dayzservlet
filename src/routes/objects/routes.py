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
    state = data.get('state', [])
    model = data.get('model', [])

    document = {
        "oid": oid,
        "items": items,
        "state": state,
        "model": model,
    }
    
    # Check if document with given oid exists in the database
    existing_doc = Interfaces.objects.find_one({'oid': oid})
    if existing_doc:
        # Update the existing document with the new data
        Interfaces.objects.update({'oid': oid}, {'$set': {'state': state}})
    else:
        # Create a new document with the given oid and data
        Interfaces.objects.insert(document)

    log("/objects/save_obj", f"[{oid}] Saved object.")
    return jsonify({'status': 'success'}), 200
    
@objects.route("/DayZServlet/objects/load_obj/", methods=["POST", "GET"])
def load_obj():
    oid = request.args.get('oid', None, str)
    if not oid:
        return jsonify({'status': 'error', 'message': 'Missing object ID'}), 400

    obj = Interfaces.objects.find_one({'oid': oid})

    if obj is None:
        return jsonify({'status': 'error', 'message': 'Object not found'}), 404


    response_data = {
        'model': obj['model'],
        'items': obj['items'],
        'state': obj['state']
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


@objects.route("/DayZServlet/objects/count_obj/", methods=["GET"])
def count_obj():
        # Fetch all documents from the database
        all_documents = Interfaces.objects.find()

        # Initialize a list to store the OIDs
        oids = []

        # Collect OIDs from the documents
        for doc in all_documents:
            oid = doc.get("oid")
            if oid:
                oids.append(oid)

        # Return the list of OIDs as a JSON array
        return jsonify({'count': oids}), 200