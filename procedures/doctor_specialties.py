from database import execute_procedure

def create_doctor_specialty(specialty):
    params = f"'{specialty}'"
    result = execute_procedure("create_doctor_specialty", params)
    return result

def get_all_doctor_specialties():
    result = execute_procedure("get_all_doctor_specialties")
    rows = result.fetchall()
    result = []
    for i in rows:
        print(list(i)[0].replace(")", "").replace("(", "").split(","))
        result.append(list(i)[0].replace(")", "").replace("(", "").split(","))
    columns = ['id', 'specialty']
    return [dict(zip(columns, row)) for row in result]

def update_doctor_specialty(id, specialty):
    params = f"{id}, '{specialty}'"
    result = execute_procedure("update_doctor_specialty", params)
    return result

def delete_doctor_specialty(id):
    params = f"{id}"
    result = execute_procedure("delete_doctor_specialty", params)
    return result