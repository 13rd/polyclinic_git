from flask import Flask, request, jsonify, json, Blueprint
from procedures.doctor_specialties import *

app = Blueprint('doctor_specialties', __name__)


@app.route("/get_all_doctor_specialties", methods=["GET"])
def get_all_doctor_specialties_route():
    specialties = get_all_doctor_specialties()
    return json.dumps(specialties, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))

@app.route("/create_doctor_specialty", methods=["POST"])
def create_doctor_specialty_route():
    data = request.json
    id = create_doctor_specialty(data["specialty"])
    if id:
        return jsonify({"message": "Специализация создана успешно."}, status_code=201)
    else:
        return jsonify({"error": "Не удалось создать специализацию."}, status_code=500)


@app.route("/update_doctor_specialty/<int:doctor_specialty_id>", methods=["PUT"])
def update_doctor_specialty_route(doctor_specialty_id):
    data = request.json
    result = update_doctor_specialty(doctor_specialty_id, data["specialty"])
    if result:
        return jsonify({"message": "Специализация обновлена успешно."}, status_code=200)
    else:
        return jsonify({"error": "Не удалось обновить специализацию."}, status_code=400)


@app.route("/delete_doctor_specialty/<int:doctor_specialty_id>", methods=["DELETE"])
def delete_doctor_specialty_route(doctor_specialty_id):
    result = delete_doctor_specialty(doctor_specialty_id)
    if result:
        return jsonify({"message": "Специализация удалена успешно."}, status_code=200)
    else:
        return jsonify({"error": "Не удалось удалить специализацию."}, status_code=500)