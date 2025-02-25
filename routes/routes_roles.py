from flask import Flask, request, jsonify, json, Blueprint
from procedures.roles import *

app = Blueprint('roles', __name__)


@app.route("/get_all_roles", methods=["GET"])
def get_all_roles_route():
    roles = get_all_roles()
    return json.dumps(roles, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))

@app.route("/create_role", methods=["POST"])
def create_role_route():
    data = request.json
    role_id = create_role(data["role_name"])
    if role_id:
        return jsonify({"message": "Роль создана успешно."}, status_code=201)
    else:
        return jsonify({"error": "Не удалось создать роль."}, status_code=500)

@app.route("/update_role/<int:role_id>", methods=["PUT"])
def update_role_route(role_id):
    data = request.json
    result = update_role(role_id, data["role_name"])
    if result:
        return jsonify({"message": "Роль обновлена успешно."}, status_code=200)
    else:
        return jsonify({"error": "Не удалось обновить роль."}, status_code=400)

@app.route("/delete_role/<int:role_id>", methods=["DELETE"])
def delete_role_route(role_id):
    result = delete_role(role_id)
    if result:
        return jsonify({"message": "Роль удалена успешно."}, status_code=200)
    else:
        return jsonify({"error": "Не удалось удалить роль."}, status_code=500)

