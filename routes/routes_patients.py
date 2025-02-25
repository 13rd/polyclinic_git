from flask import Flask, request, jsonify, json, Blueprint
from procedures.patients import *

app = Blueprint('patients', __name__)

@app.route("/get_all_patients", methods=["GET"])
def get_all_patients_route():
    patients = get_all_patients()
    return json.dumps(patients, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))

# @app.route("/create_patient", methods=["POST"])
# def create_patient_route():
#     data = request.json
#     patient_id = create_patient(data["first_name"], data["last_name"], data["middle_name"], data["birth_date"], data["address"], data["user_id"])
#     if patient_id:
#         return jsonify({"message": "Пациент зарегистрирован успешно.", "code": 201})
#     else:
#         return jsonify({"error": "Не удалось зарегистрировать пациента."}, status_code=500)

@app.route("/update_patient/<int:patient_id>", methods=["PUT"])
def update_patient_route(patient_id):
    data = request.json
    result = update_patient(patient_id, data["first_name"], data["last_name"], data["middle_name"], data["birth_date"], data["address"], data["user_id"])
    if result:
        return jsonify({"message": "Информация о пациенте обновлена успешно."}, status_code=200)
    else:
        return jsonify({"error": "Не удалось обновить информацию о пациенте."}, status_code=400)

@app.route("/delete_patient/<int:patient_id>", methods=["DELETE"])
def delete_patient_route(patient_id):
    result = delete_patient(patient_id)
    if result:
        return jsonify({"message": "Пациент удален успешно."}, status_code=200)
    else:
        return jsonify({"error": "Не удалось удалить пациента."}, status_code=500)