"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body), 200


@app.route("/add", methods=['POST'])
def add_member():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    if "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    member = {
        "id": jackson_family._generate_id(),
        "first_name": data["first_name"],
        "last_name": jackson_family.last_name,
        "age": data["age"],
        "lucky_numbers": data["lucky_numbers"]
    }
    jackson_family.add_member(member)
    return jsonify({"message": "Member added successfully"}), 201

@app.route("/delete/<int:member_id>", methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.get_member(member_id )
    if not member:
        return jsonify({"error": "Member not found"}), 404
    jackson_family.delete_member(member_id)
    return jsonify({"message": "Member deleted successfully"}), 200

@app.route("/member/<int:member_id>", methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200
# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
