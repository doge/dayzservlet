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
    model = data.get('model', [])
    state = data.get('state', {})
    # Ensure 'pos', 'dir', and 'up' are present in state_vars
    pos = data.get('pos')
    dir = data.get('dir')
    up = data.get('up')
    if not pos or not dir or not up:
        return jsonify({'status': 'error', 'message': 'Missing pos, dir, or up'}), 400
    
    # Extract 'items' and nested 'items' data properly
    extracted_items = []
    for item in items:
        item_data = {
            'slot': item.get('slot', ''),
            'type': item.get('type', ''),
            'state': item.get('state', {}),
            'items': []  # Initialize empty nested items array
        }

        nested_items = item.get('items', [])  # Extract nested items
        for nested_item in nested_items:
            nested_item_data = {
                'slot': nested_item.get('slot', ''),
                'type': nested_item.get('type', ''),
                'state': nested_item.get('state', {})
            }
            item_data['items'].append(nested_item_data)  # Append nested item

        extracted_items.append(item_data)
    
    document = {
        "oid": oid,
        "items": extracted_items,  # Use extracted_items here
        "state": state,
        "model": model,
        "pos": pos,
        "dir": dir,
        "up": up,
    }

    # Check if document with given oid exists in the database
    existing_doc = Interfaces.objects.find_one({'oid': oid})
    if existing_doc:
        # Update the existing document with the new data
        Interfaces.objects.update({'oid': oid}, {'$set': document})
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

    extracted_items = []
    for item in obj.get('items', []):
        item_data = {
            'slot': item.get('slot', ''),
            'type': item.get('type', ''),
            'state': item.get('state', {})
        }

        nested_items = item.get('items', [])  # Extract nested items
        nested_items_data = []  # Structure for nested items

        for nested_item in nested_items:
            nested_item_data = {
                'slot': nested_item.get('slot', ''),
                'type': nested_item.get('type', ''),
                'state': nested_item.get('state', {})
            }
            nested_items_data.append(nested_item_data)

        item_data['items'] = nested_items_data
        extracted_items.append(item_data)

    response_data = {
        'model': obj['model'],
        'items': extracted_items,  # Use extracted_items here
        'pos': obj.get('pos'),
        'dir': obj.get('dir'),
        'up': obj.get('up')
    }

    log("/objects/load_obj/", f"[{oid}] served object into world.")
    return jsonify(response_data)

@objects.route("/DayZServlet/objects/destroy_obj/", methods=["POST", "GET"])
def destroy_obj():
    oid = request.args.get('oid', None, str)
    if not oid:
        return jsonify({'status': 'error', 'message': 'Missing object ID'}), 400

    obj = Interfaces.objects.find_one({'oid': oid})

    if obj is None:
        return jsonify({'status': 'error', 'message': 'Object not found'}), 404

    query = Interfaces.objects.delete({'oid': oid})
    if query.deleted_count:
        log("/objects/destroy_obj/", f"[{oid}] removed from world.")
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

    # Return the count of OIDs as well as the list of OIDs as a JSON response
    return jsonify({'count': oids}), 200
