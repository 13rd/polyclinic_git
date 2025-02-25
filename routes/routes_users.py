from flask import Flask, request, jsonify, json, Blueprint
from procedures.users import *

app = Blueprint('users', __name__)


@app.route("/get_all_users", methods=["GET"])
def get_all_users_route():
    users = get_all_users()
    return json.dumps(users, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))

# @app.route("/register", methods=["POST"])
# def register_user_route():
#     data = request.json
#     user_id = create_user(data["username"], data["password"], data["role_id"])
#     if user_id:
#         return jsonify({"message": "Пользователь зарегистрирован успешно."}, status_code=201)
#     else:
#         return jsonify({"error": "Регистрация не прошла."}, status_code=500)

@app.route("/update_user/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):
    data = request.json
    result = update_user(user_id, data["username"], data["passwordhash"], data["role_id"])
    if result:
        return jsonify({"message": "Информация о пользователе обновлена успешно."}, status_code=200)
    else:
        return jsonify({"error": "Не удалось обновить информацию о пользователе."}, status_code=400)

@app.route("/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    result = delete_user(user_id)
    if result:
        return jsonify({"message": "Пользователь удален успешно."}, status_code=200)
    else:
        return jsonify({"error": "Не удалось удалить пользователя."}, status_code=500)