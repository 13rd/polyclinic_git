from database import execute_procedure

def create_role(role_name):
    params = f"'{role_name}'"
    result = execute_procedure("create_role", params)
    return result

def get_all_roles():
    result = execute_procedure("get_all_roles")
    rows = result.fetchall()
    result = []
    for i in rows:
        print(list(i)[0].replace(")", "").replace("(", "").split(","))
        result.append(list(i)[0].replace(")", "").replace("(", "").split(","))
    columns = ['role_id', 'role_name']
    return [dict(zip(columns, row)) for row in result]

def update_role(role_id, role_name):
    params = f"{role_id}, '{role_name}'"
    result = execute_procedure("update_role", params)
    return result

def delete_role(role_id):
    params = f"{role_id}"
    result = execute_procedure("delete_role", params)
    return result