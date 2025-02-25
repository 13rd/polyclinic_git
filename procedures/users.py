from database import execute_procedure

def create_user(username, passwordhash, role_id):
    params = f"'{username}', '{passwordhash}', {role_id}"
    result = execute_procedure("create_user", params)
    return result

def get_all_users():
    result = execute_procedure("get_all_users")
    rows = result.fetchall()
    result = []
    for i in rows:
        print(list(i)[0].replace(")", "").replace("(", "").split(","))
        result.append(list(i)[0].replace(")", "").replace("(", "").split(","))
    columns = ['user_id', 'username', 'passwordhash', 'role_id']
    return [dict(zip(columns, row)) for row in result]

def update_user(user_id, username, passwordhash, role_id):
    params = f"{user_id}, '{username}', '{passwordhash}', {role_id}"
    result = execute_procedure("update_user", params)
    return result

def delete_user(user_id):
    params = f"{user_id}"
    result = execute_procedure("delete_user", params)
    return result