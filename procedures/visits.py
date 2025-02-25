from database import execute_procedure, get_table_from_raw

def create_visit(patient_id, doctor_id, visit_date, diagnosis_id):
    params = f"{patient_id}, {doctor_id}, '{visit_date}', {diagnosis_id}"
    result = execute_procedure("create_visit", params)
    return result

def get_all_visits():
    result = execute_procedure("get_all_visits")
    rows = result.fetchall()
    result = []
    for i in rows:
        print(list(i)[0].replace(")", "").replace("(", "").split(","))
        result.append(list(i)[0].replace(")", "").replace("(", "").split(","))
    columns = ['visit_id', 'patient_id', 'doctor_id', 'visit_date', 'diagnosis_id']
    return [dict(zip(columns, row)) for row in result]

def update_visit(visit_id, patient_id, doctor_id, visit_date, diagnosis_id):
    params = f"{visit_id}, {patient_id}, {doctor_id}, '{visit_date}', {diagnosis_id}"
    result = execute_procedure("update_visit", params)
    return result

def delete_visit(visit_id):
    params = f"{visit_id}"
    result = execute_procedure("delete_visit", params)
    return result

def get_all_visits_by_doctor(doctor_id: int):
    params = f"{doctor_id}"
    result = execute_procedure("get_all_visits_by_doctor", params)
    print(result)
    cursor = result.fetchall()
    print(cursor)
    table = get_table_from_raw(cursor, columns=["visit_id", "datetime", "full_name", "diagnos"])
    return table

def get_all_visits_by_patient(patient_id: int):
    params = f"{patient_id}"
    result = execute_procedure("get_all_visits_by_patient", params)
    print(result)
    cursor = result.fetchall()
    print(cursor)
    table = get_table_from_raw(cursor, columns=["visit_id", "doctor_name", "datetime", "full_name", "diagnos"])
    return table


def get_visit_by_id(visit_id):
    params = f"{visit_id}"
    result = execute_procedure("get_visit_by_id", params)
    print(result)
    cursor = result.fetchall()
    print(cursor)
    table = get_table_from_raw(cursor, columns=["visit_id", "datetime", "full_name", "diagnos", "doctor_id"])
    return table

def set_diagnos_by_visit_id(visit_id, diagnos_id):
    params = f"{visit_id}, {diagnos_id}"
    result = execute_procedure("set_diagnos_to_visit", params)
    return result

def count_visits_by_doctor_in_period(doctor_id, start_date, end_date):
    params = f"{doctor_id}, '{start_date}', '{end_date}'"
    result = execute_procedure("count_visits_by_doctor_in_period", params)
    return result