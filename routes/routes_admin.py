from flask import Flask, request, jsonify, json, Blueprint, render_template, redirect, url_for, session
from procedures.visits import *
from procedures.doctors import *
from procedures.patients import *
from procedures.diagnoses import get_all_diagnoses
from procedures.doctor_specialties import get_all_doctor_specialties
from procedures.admin import *
from procedures.auth import *
from datetime import date, timedelta, datetime

app = Blueprint('admin', __name__)


@app.route('/admin/update_doctor/<int:doctor_id>', methods=["GET", "POST"])
def update_doctor_admin(doctor_id):
    if request.method == "POST":
        data = request.form
        print(data)

        update_doctor(doctor_id, data["first_name"], data["last_name"], data["middle_name"], data["experience"],
                        data["specialty_id"])

        return redirect("/statistics")
    else:
        print(doctor_id)
        d_doctors = get_all_doctors()
        doctor = None
        for d in d_doctors:
            print(d)
            if int(d["doctor_id"]) == doctor_id:
                doctor = d
        print(doctor)
        return render_template("doctor_update.html", doctor=doctor, specialties=get_all_doctor_specialties())



@app.route('/admin/delete_doctor/<int:doctor_id>', methods=["GET", "POST"])
def delete_doctor_admin(doctor_id):
    if request.method == "POST":
        data = request.form
        print(data)

        delete_doctor(doctor_id)

        return redirect("/statistics")
    else:
        return render_template("confirm_doctor_delete.html")




@app.route('/admin/update_patient/<int:patient_id>', methods=["GET", "POST"])
def update_patient_admin(patient_id):
    if request.method == "POST":
        data = request.form
        print(data)

        update_patient(patient_id, data["first_name"], data["last_name"], data["middle_name"], data["birth_date"],
                        data["adress"].replace("\"", ""))

        return redirect("/get_patient_card")
    else:
        print(patient_id)
        d_patients = get_all_patients()
        patient = None
        for d in d_patients:
            print(d)
            if int(d["patient_id"]) == patient_id:
                patient = d
        print(patient)
        return render_template("patient_update.html", patient=patient)


@app.route('/admin/delete_patient/<int:patient_id>', methods=["GET", "POST"])
def delete_patient_admin(patient_id):
    if request.method == "POST":
        data = request.form
        print(data)

        delete_patient(patient_id)

        return redirect("/get_patient_card")
    else:
        return render_template("confirm_patient_delete.html")


@app.route('/create_patient', methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        data = request.form
        print(data)

        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        middle_name = data.get("middle_name", "").strip()
        birth_date = data.get("birth_date", "").strip()
        adress = data.get("adress", "").strip()


        if not first_name or not last_name or not adress or not birth_date:
            return render_template("create_patient.html", error="Заполните все обязательные поля")

        patient_id = register_patient(first_name, last_name, middle_name, birth_date, adress)
        if patient_id:
            return redirect("/")
        else:
            return render_template("create_patient.html", error="Ошибка при создании пациента")
    else:
        return render_template("create_patient.html")


@app.route('/create_doctor', methods=["GET", "POST"])
def add_doctor():
    if request.method == "POST":
        data = request.form
        print(data)
        doctor_id = register_doctor(data["first_name"], data["last_name"], data["middle_name"], data["experience"],
                                  data["specialty_id"], data["username"], data["password"])
        if doctor_id:
            return redirect("/")
        else:
            return render_template("create_doctor.html", specialties=get_all_doctor_specialties())
    else:
        return render_template("create_doctor.html", specialties=get_all_doctor_specialties())


@app.route('/statistics')
def statistics():
    if session["user"]["role"] == "doctor":
        doctor_id = get_doctor_by_user_id(session['user']['user_id'])
        print(doctor_id)
        cursor = doctor_id.fetchall()

        start_date = request.args.get("start_date_visits", "")
        end_date = request.args.get("end_date_visits", "")
        if start_date and end_date:
            start_date = datetime.fromisoformat(start_date)
            print("start: ", start_date)
            end_date = datetime.fromisoformat(end_date)
            d_visits = count_visits_by_doctor_in_period(cursor[0][0], start_date, end_date)
        else:
            d_visits = count_visits_by_doctor_in_period(cursor[0][0], datetime(2020, 1, 1, 0, 0, 0), datetime.now())

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
    #===

        # start_date = request.args.get("start_date_visits", "")
        # end_date = request.args.get("end_date_visits", "")
        # if start_date and end_date:
        #     start_date = date.fromisoformat(start_date)
        #     end_date = date.fromisoformat(end_date)
        #     table = count_visits_per_doctor_in_period(start_date, end_date)
        # else:
        #     table = count_visits_per_doctor()
        #
        # labels_visits = []
        # data_visits = []
        # print("table")
        # print(table)
        # for i in table:
        #     data_visits.append(i.get('visits_count'))
        #     labels_visits.append(i.get('doctor_fullname'))


        return render_template('doctor_statistics.html', labels=labels, data=data)
    else:
        d_doctors = get_all_doctors()
        d_specialties = get_doctors_with_specialties()
        print(d_doctors)
        print(d_specialties)
        for d in d_doctors:
            for s in d_specialties:
                if d.get("specialty_id") == s.get("specialties_id"):
                    d["specialty"] = s.get("specialties_name")

        specialty = request.args.get("specialties_id", None)
        print(specialty)

        filtered_doctors = d_doctors.copy()
        if specialty and specialty != "None":
            filtered_doctors = [v for v in filtered_visits if v["specialty_id"] == specialty]
        print(filtered_doctors)

        # visits count
        start_date = request.args.get("start_date_visits", "")
        end_date = request.args.get("end_date_visits", "")
        if start_date and end_date:
            start_date = date.fromisoformat(start_date)
            end_date = date.fromisoformat(end_date)
            table = count_visits_per_doctor_in_period(start_date, end_date)
        else:
            table = count_visits_per_doctor()

        labels_visits = []
        data_visits = []
        print(table)
        for i in table:
            data_visits.append(i.get('visits_count'))
            labels_visits.append(i.get('doctor_fullname'))

        # diagnos count
        start_date = request.args.get("start_date_diagnos", "")
        end_date = request.args.get("end_date_diagnos", "")
        if start_date and end_date:
            start_date = date.fromisoformat(start_date)
            end_date = date.fromisoformat(end_date)
            table = count_diagnos_in_period(start_date, end_date)
        else:
            table = count_diagnos()
        print(table)

        labels_diagnos = []
        data_diagnos = []
        print(table)
        for i in table:
            data_diagnos.append(i.get('diagnos_count'))
            labels_diagnos.append(i.get('diagnos_name'))


        return render_template('admin_statistics.html', specialties=d_specialties, doctors=filtered_doctors, labels_visits=labels_visits, data_visits=data_visits, labels_diagnos=labels_diagnos, data_diagnos=data_diagnos)


@app.route("/get_patient_card", methods=["GET"])
def get_patient_card_route():
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
        d_doctors = get_all_patients()

        today = date.today().strftime("%Y-%m-%d")
        patient_id = request.args.get("patient_id", "0")
        start_date = request.args.get("start_date", "")
        end_date = request.args.get("end_date", "")
        today_only = request.args.get("today", False)

        patient_name = ""
        patient_db = None
        for d in d_doctors:
            if d["patient_id"] == patient_id:
                patient_name = d["first_name"] + " " + d["last_name"] + " " + d["middle_name"]
                patient_db = d

        d_visits = get_all_visits_by_patient(patient_id)
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

        return render_template("patient_visits.html", visits=filtered_visits, patients=d_doctors, patient_name=patient_name, patient_db=patient_db)



@app.route('/create_admin', methods=["GET", "POST"])
def add_admin():
    if request.method == "POST":
        data = request.form
        print(data)
        doctor_id = register_user(data["username"], data["password"], "admin")
        if doctor_id:
            return redirect("/")
        else:
            return render_template("create_admin.html")
    else:
        return render_template("create_admin.html")


'''
• перечень специалистов (список врачей по специальностям); done
• количества визитов к врачам; done
• количества случаев заболевания по каждому диагнозу.
'''