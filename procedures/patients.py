from database import execute_procedure

def create_patient(first_name, last_name, middle_name, birth_date, address):
    params = f"'{first_name}', '{last_name}', '{middle_name}', '{birth_date}', '{address}'"
    result = execute_procedure("create_patient", params)
    return result

def get_all_patients():
    result = execute_procedure("get_all_patients")
    rows = result.fetchall()
    result = []
    for i in rows:
        print(list(i)[0].replace(")", "").replace("(", "").split(","))
        result.append(list(i)[0].replace(")", "").replace("(", "").split(","))
    columns = ['patient_id', 'first_name', 'last_name', 'middle_name', 'birth_date', 'address', 'user_id']
    return [dict(zip(columns, row)) for row in result]

def update_patient(patient_id, first_name, last_name, middle_name, birth_date, address):
    params = f"{patient_id}, '{first_name}', '{last_name}', '{middle_name}', '{birth_date}', '{address}'"
    result = execute_procedure("update_patient", params)
    return result

def delete_patient(patient_id):
    params = f"{patient_id}"
    result = execute_procedure("delete_patient", params)
    return result