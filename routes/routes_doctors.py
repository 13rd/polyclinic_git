from flask import Flask, request, jsonify, json, Blueprint, render_template, redirect, url_for, session
from procedures.doctors import *
from procedures.patients import get_all_patients
from procedures.visits import *
from procedures.doctor_specialties import get_all_doctor_specialties
from datetime import date, timedelta, datetime


app = Blueprint('doctors', __name__)

@app.route("/doctors", methods=["GET"])
def get_all_doctors_route():
    doctors = get_all_doctors()
    return render_template("doctors.html", doctors=doctors) # json.dumps(doctors, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))

# @app.route("/create_doctor", methods=["GET", "POST"])
# def create_doctor_route():
#     if request.method == "POST":
#         data = request.json
#         doctor_id = create_doctor(data["first_name"], data["last_name"], data["middle_name"], data["experience"], data["specialty_id"], data["user_id"])
#         if doctor_id:
#             return jsonify({"message": "Врач создан успешно.", "code": 201})
#         else:
#             return jsonify({"error": "Не удалось создать врача."}, status_code=500)
#     else:
#         return render_template("create_doctor.html", specialties=get_all_doctor_specialties())

# @app.route("/update_doctor/<int:doctor_id>", methods=["PUT"])
# def update_doctor_route(doctor_id):
#     data = request.json
#     result = update_doctor(doctor_id, data["first_name"], data["last_name"], data["middle_name"], data["experience"], data["specialty_id"], data["user_id"])
#     if result:
#         return jsonify({"message": "Информация о враче обновлена успешно."}, status_code=200)
#     else:
#         return jsonify({"error": "Не удалось обновить информацию о враче."}, status_code=400)

# @app.route("/delete_doctor/<int:doctor_id>", methods=["DELETE"])
# def delete_doctor_route(doctor_id):
#     result = delete_doctor(doctor_id)
#     if result:
#         return jsonify({"message": "Врач удален успешно."}, status_code=200)
#     else:
#         return jsonify({"error": "Не удалось удалить врача."}, status_code=500)


@app.route("/create_visit", methods=["POST", "GET"])
def create_visit_route():
    if request.method == "GET":
        if session["user"]["role"] == "doctor":
            d_patients = get_all_patients()
            return render_template("create_visit_doctor.html", patients=d_patients)
        else:
            d_patients = get_all_patients()
            d_doctors = get_all_doctors()
            return render_template("create_visit_admin.html", patients=d_patients, doctors=d_doctors)
    else:
        f_patient_id = request.form['patient_id']
        f_user_id = request.form.get("user_id", None)
        f_doctor_id = get_doctor_by_user_id(f_user_id)
        if not f_doctor_id:
            doctors = get_all_doctors()
            for i in doctors:
                print(i)
                if i["user_id"] == request.form["doctor_id"]:
                    f_doctor_id = i["doctor_id"]
        f_visit_date = request.form['visit_date']
        f_diagnosis_id = "null"

        visit_id = add_visit(doctor_id=f_doctor_id, patient_id=f_patient_id, visit_date=f_visit_date, diagnosis_id=f_diagnosis_id)
        if visit_id:
            return redirect("/")
        else:
            return redirect("/create_visit")


@app.route("/get_visits", methods=["GET"])
def get_visits_route():
    if session["user"]["role"] == "doctor":
        d_doctors = get_all_doctors()
        for d in d_doctors:
            print(d)
            print(d['user_id'], session['user']['user_id'], type(int(d['doctor_id'])))
            if d['user_id'] == session['user']['user_id']:
                d_visits = get_all_visits_by_doctor(int(d['doctor_id']))
                print(d_visits)
                table_visits = []
                for v in d_visits:
                    if v['diagnos'] == "":
                        v['diagnos'] = "Не поставлен"
                    v['date'] = v['datetime'].split()[0]
                    v['time'] = v['datetime'].split()[1]
                    table_visits.append(v)
                today = date.today().strftime("%Y-%m-%d")
                start_date = request.args.get("start_date", "")
                end_date = request.args.get("end_date", "")
                today_only = request.args.get("today", False)

                filtered_visits = table_visits.copy()
                if start_date and end_date:
                    start_date = date.fromisoformat(start_date)
                    end_date = date.fromisoformat(end_date)
                    filtered_visits = [v for v in filtered_visits if
                    start_date <= date.fromisoformat(v["date"]) <= end_date]
                if today_only:
                    filtered_visits = [v for v in filtered_visits if v["date"] == today]

                return render_template("visits.html", visits=filtered_visits)
    else:
        d_doctors = get_all_doctors()

        today = date.today().strftime("%Y-%m-%d")
        doctor_id = request.args.get("doctor_id", "0")
        patient_id = request.args.get("patient_id", "0")
        start_date = request.args.get("start_date", "")
        end_date = request.args.get("end_date", "")
        today_only = request.args.get("today", False)

        doctor_name = ""
        for d in d_doctors:
            if d["doctor_id"] == doctor_id:
                doctor_name = d["first_name"] + " " + d["last_name"] + " " + d["middle_name"]

        d_visits = get_all_visits_by_doctor(doctor_id)
        print(d_visits)
        table_visits = []
        for v in d_visits:
            if v['diagnos'] == "":
                v['diagnos'] = "Не поставлен"
            v['date'] = v['datetime'].split()[0]
            v['time'] = v['datetime'].split()[1]
            table_visits.append(v)

        filtered_visits = table_visits.copy()
        if start_date and end_date:
            start_date = date.fromisoformat(start_date)
            end_date = date.fromisoformat(end_date)
            filtered_visits = [v for v in filtered_visits if
                               start_date <= date.fromisoformat(v["date"]) <= end_date]
        if today_only:
            filtered_visits = [v for v in filtered_visits if v["date"] == today]

        return render_template("visits_admin.html", visits=filtered_visits, doctors=d_doctors, doctor_name=doctor_name)



@app.route('/doctor-statistics')
def doctor_statistics():
    two_weeks_ago = datetime.now() - timedelta(days=14)
    print(two_weeks_ago)
    doctor_id = get_doctor_by_user_id(session['user']['user_id'])
    print(doctor_id)
    cursor = doctor_id.fetchall()
    d_visits = count_visits_by_doctor_in_period(cursor[0][0], two_weeks_ago, datetime.now()+timedelta(days=14))
    print(d_visits)
    cursor = d_visits.fetchall()
    table = get_table_from_raw(cursor, ["count", "date"])
    print(table)
    labels = []
    data = []
    for i in table:
        labels.append(i['date'])
        data.append(i['count'])
    print(labels)
    print(data)

    return render_template('doctor_statistics.html', labels=labels, data=data)


# # Фильтрация по начальной и конечной дате
# if start_date and end_date:
#     start_date = date.fromisoformat(start_date)
#     end_date = date.fromisoformat(end_date)
#     filtered_visits = [v for v in filtered_visits if start_date <= date.fromisoformat(v["date"]) <= end_date]
#
# # Фильтрация только сегодняшних визитов
# if today_only:
#     filtered_visits = [v for v in filtered_visits if v["date"] == today]
#
# return render_template('index.html', visits=filtered_visits, start_date=start_date, end_date=end_date)