from database import execute_procedure, get_table_from_raw, execute_func
import hashlib
# from hashlib import sha256


def register_user(username, password, role_name):
    password_hash = hashlib.new('sha256')
    password_hash.update(password.encode())
    print(password_hash.hexdigest())

    params = f"'{username}', '{password_hash.hexdigest()}', '{role_name}'"
    result = execute_func("register_user", params)
    return result


def register_doctor(first_name, last_name, middle_name, experience, specialty_id, username, password):
    password_hash = hashlib.new('sha256')
    password_hash.update(password.encode())
    print(password_hash.hexdigest())

    params = f"'{first_name}', '{last_name}', '{middle_name}', {experience}, {specialty_id}, '{username}', " \
             f"'{password_hash.hexdigest()}'"
    result = execute_procedure("create_doctor", params)
    return result


def register_patient(first_name, last_name, middle_name, birth_date, adress):
    params = f"'{first_name}', '{last_name}', '{middle_name}', '{birth_date}', '{adress}'"
    result = execute_procedure("create_patient", params)
    return result


def get_user_by_username(username):
    params = f"'{username}'"
    d_user = execute_procedure("get_user_by_username", params)
    cursor = d_user.fetchall()
    table = get_table_from_raw(cursor, columns=["user_id", "username", "role"])
    # print(type(table))
    return table


def authenticate_user(username, password):
    try:
        params = f"'{username}', '{password}'"
        result = execute_procedure("authenticate_user", params)
        cursor = result.fetchall()

        if cursor is None:
            return False
        # print(cursor)

        stored_password_hash = cursor[0][0]
        # print(stored_password_hash)

        password_hash = hashlib.new('sha256')
        password_hash.update(password.encode())
        # p_password = password_hash.hexdigest()
        # print(f"user password: {password_hash.hexdigest()}\npassword hash: {stored_password_hash}")

        # Проверяем введённый пароль с хранимым хешем
        if password_hash.hexdigest() == stored_password_hash:
            print("user auth")
            return username
        else:
            print("user NO auth")
            return None

    except Exception as error:
        print("Error while authenticating user", error)


"""
admin: a
qq: qq
anton: anton
"""