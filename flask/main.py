from flask import Flask, jsonify, request
import datetime
from uuid import uuid4

app = Flask(__name__)
contact_list = []

@app.route("/")
def health():
    return jsonify({
        "success": True,
        "message": "API is healthy and running",
        "data": {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        }
    }), 200

@app.route("/contact")
def get_contacts():
    return jsonify({
        "success": True,
        "message": "List of contacts",
        "data": {
            "contacts": contact_list
        }
    }), 200

@app.route("/contact", methods=['POST'])
def create_contact():
    data = request.get_data()
    if not data:
        return jsonify({
            "success": False,
            "message": "Please send valid data!",
            "data": None
        }), 400
    data = request.get_json()

    allowed_keys = {'name', 'family'}

    filtered_data = {
        key: data[key]
        for key in allowed_keys
        if key in data
    }

    if "name" not in filtered_data or "family" not in filtered_data:
        return jsonify({
            "success": False,
            "message": "Please send name and family",
            "data": None
        }), 400


    new_contact = filtered_data
    new_contact["id"] = str(uuid4())

    contact_list.append(new_contact)

    return jsonify({
        "success": True,
        "message": "Contact created.",
        "data": new_contact
    }), 200

@app.route("/contact/<contact_id>")
def details(contact_id):
    print(contact_list)
    contact = next((item for item in contact_list if item["id"] == contact_id), None)

    if not contact:
        return jsonify({
            "success": False,
            "message": "Contact not found!"
        }), 404

    return jsonify({
        "success": True,
        "data": contact
    }), 200

@app.route("/contact/<contact_id>", methods=['PUT'])
def edit(contact_id):
    data = request.get_data()
    if not data:
        return jsonify({
            "success": False,
            "message": "Please send valid data!",
            "data": None
        }), 400

    index = next((i for i, item in enumerate(contact_list) if item["id"] == contact_id), -1)
    if index == -1:
        return jsonify({
            "success": False,
            "message": "Contact not found!"
        }), 404

    data = request.get_json()

    allowed_keys = {'name', 'family'}

    filtered_data = {
        key: data[key]
        for key in allowed_keys
        if key in data
    }

    updated = {**contact_list[index], **filtered_data}
    contact_list[index] = updated
    return jsonify({"status": True, "data": updated}), 200

@app.route("/contact/<contact_id>", methods=['DELETE'])
def delete(contact_id):
    global contact_list
    index = next((i for i, item in enumerate(contact_list) if item["id"] == contact_id), -1)
    if index == -1:
        return jsonify({
            "success": False,
            "message": "Contact not found!"
        }), 404

    contact_list.pop(index)
    return jsonify({
        "success": True,
        "message": "Contact deleted"
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)