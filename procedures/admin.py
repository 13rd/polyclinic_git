from database import execute_procedure, execute, get_table_from_raw


def get_doctors_with_specialties():
    # params = f"{user_id}"
    result = execute_procedure("get_all_doctor_specialties")
    cursor = result.fetchall()
    table = get_table_from_raw(cursor, columns=["specialties_id", "specialties_name"])
    return table


def count_visits_per_doctor_in_period(start_date, end_date):
    params = f"'{start_date}', '{end_date}'"
    result = execute_procedure("count_visits_per_doctor", params)
    cursor = result.fetchall()
    table = get_table_from_raw(cursor, columns=["doctor_id", "doctor_fullname", "visits_count"])
    return table


def count_visits_per_doctor():
    # params = f"{user_id}"
    result = execute_procedure("count_visits_per_doctor")
    cursor = result.fetchall()
    table = get_table_from_raw(cursor, columns=["doctor_id", "doctor_fullname", "visits_count"])
    return table


def count_diagnos_in_period(start_date, end_date):
    params = f"'{start_date}', '{end_date}'"
    result = execute_procedure("count_visits_per_doctor", params)
    cursor = result.fetchall()
    table = get_table_from_raw(cursor, columns=["doctor_id", "doctor_fullname", "visits_count"])
    return table


def count_diagnos():
    # params = f"{user_id}"
    result = execute_procedure("count_cases_per_diagnosis")
    cursor = result.fetchall()
    table = get_table_from_raw(cursor, columns=["diagnos_id", "diagnos_name", "diagnos_count"])
    return table
