from flask import Flask, request, jsonify, json, Blueprint, render_template, redirect
from procedures.visits import *
from procedures.doctors import get_all_doctors
from procedures.diagnoses import get_all_diagnoses

app = Blueprint('visits', __name__)


@app.route("/get_all_visits", methods=["GET"])
def get_all_visits_route():
    visits = get_all_visits()
    return json.dumps(visits, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))

@app.route("/visit/<int:visit_id>", methods=["GET"])
def get_visits_route(visit_id):
    visit = get_visit_by_id(visit_id)[0]
    doctors = get_all_doctors()
    for d in doctors:
        if visit['doctor_id'] == d['doctor_id']:
            visit['doctor_name'] = f"{d['first_name']} {d['last_name']} {d['middle_name']}"
    if visit['diagnos'] == "":
        visit['diagnos'] = "Не поставлен"
    diagnosis = get_all_diagnoses()
    return render_template("visit.html", visit=visit, diagnosis=diagnosis)


@app.route("/update_visit", methods=["POST"])
def update_visit_route():
    f_diagnosis_id = request.form['diagnos_id']
    f_visit_id = request.form['visit_id']

    visit_id = set_diagnos_by_visit_id(visit_id=f_visit_id, diagnos_id=f_diagnosis_id)
    if visit_id:
        return redirect("/get_visits")
    else:
        return redirect(f"/visit/{f_visit_id}")


@app.route("/delete_visit/<int:visit_id>", methods=["DELETE"])
def delete_visit_route(visit_id):
    result = delete_visit(visit_id)
    if result:
        return jsonify({"message": "Запись о визите удалена успешно."}, status_code=200)
    else:
        return jsonify({"error": "Не удалось удалить запись о визите."}, status_code=500)