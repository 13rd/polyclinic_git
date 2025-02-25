from flask import Flask, request, jsonify, json, Blueprint
from procedures.diagnoses import *

app = Blueprint('diagnosis', __name__)

# Маршруты для работы с таблицей diagnoses
@app.route('/create_diagnosis', methods=['POST'])
def create_diagnosis_route():
    data = request.get_json()
    result = create_diagnosis(data['name'], data['mkb_code'])
    if result:
        return jsonify({'message': 'Diagnosis created successfully.'}), 201
    else:
        return jsonify({'error': 'Failed to create diagnosis.'}), 500

@app.route('/get_all_diagnoses')
def get_all_diagnoses_route():
    diagnoses = get_all_diagnoses()
    return json.dumps(diagnoses, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))

@app.route('/update_diagnosis/<int:diagnosis_id>', methods=['PUT'])
def update_diagnosis_route(diagnosis_id):
    data = request.get_json()
    result = update_diagnosis(diagnosis_id, data['name'], data['mkb_code'])
    if result:
        return jsonify({'message': 'Diagnosis updated successfully.'}), 200
    else:
        return jsonify({'error': 'Failed to update diagnosis.'}), 400

@app.route('/delete_diagnosis/<int:diagnosis_id>', methods=['DELETE'])
def delete_diagnosis_route(diagnosis_id):
    result = delete_diagnosis(diagnosis_id)
    if result:
        return jsonify({'message': 'Diagnosis deleted successfully.'}), 200
    else:
        return jsonify({'error': 'Failed to delete diagnosis.'}), 400

