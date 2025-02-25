from database import execute_procedure

def create_diagnosis(name, mkb_code):
    params = f"'{name}', '{mkb_code}'"
    result = execute_procedure("create_diagnosis", params)
    return result

def get_all_diagnoses():
    result = execute_procedure("get_all_diagnoses")
    rows = result.fetchall()
    result = []
    for i in rows:
        # print(list(i)[0].replace(")", "").replace("(", "").split(","))
        result.append(list(i)[0].replace(")", "").replace("(", "").split(","))
    columns = ['diagnosis_id', 'name', 'mkb_code']
    return [dict(zip(columns, row)) for row in result]

def update_diagnosis(diagnosis_id, name, mkb_code):
    params = f"{diagnosis_id}, '{name}', '{mkb_code}'"
    result = execute_procedure("update_diagnosis", params)
    return result

def delete_diagnosis(diagnosis_id):
    params = f"{diagnosis_id}"
    result = execute_procedure("delete_diagnosis", params)
    return result