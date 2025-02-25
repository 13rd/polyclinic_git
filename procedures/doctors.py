from database import execute_procedure

# def create_doctor(first_name, last_name, middle_name, experience, specialty_id):
#     params = f"'{first_name}', '{last_name}', '{middle_name}', {experience}, {specialty_id}"
#     result = execute_procedure("create_doctor", params)
#     return result

def get_doctor_by_user_id(user_id):
    params = f"{user_id}"
    result = execute_procedure("get_doctor_by_user_id", params)
    return result


def add_visit(doctor_id, patient_id, visit_date, diagnosis_id):
    params = f"{patient_id}, {doctor_id}, '{visit_date}', {diagnosis_id}"
    result = execute_procedure("create_visit", params)
    return result


def get_all_doctors():
    result = execute_procedure("get_all_doctors")
    rows = result.fetchall()
    result = []
    for i in rows:
        print(list(i)[0].replace(")", "").replace("(", "").split(","))
        result.append(list(i)[0].replace(")", "").replace("(", "").split(","))
    columns = ['doctor_id', 'first_name', 'last_name', 'middle_name', 'experience', 'specialty_id', 'user_id']
    return [dict(zip(columns, row)) for row in result]

def update_doctor(doctor_id, first_name, last_name, middle_name, experience, specialty_id):
    params = f"{doctor_id}, '{first_name}', '{last_name}', '{middle_name}', {experience}, {specialty_id}"
    result = execute_procedure("update_doctor", params)
    return result

def delete_doctor(doctor_id):
    params = f"{doctor_id}"
    result = execute_procedure("delete_doctor", params)
    return result