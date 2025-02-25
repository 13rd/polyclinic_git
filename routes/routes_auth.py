from flask import Flask, request, jsonify, json, Blueprint, session, redirect, url_for, render_template
from procedures.auth import *
from models import User

app = Blueprint('auth', __name__, url_prefix="/auth")


# @app.route("/get_auth", methods=["GET"])
# def get_auth_test_route():
#     user = session['user']
#     print(user)
#     return {"user": user}

@app.route("/register_doctor", methods=["POST"])
def register_doctor_route():
    data = request.json
    user_id = register_doctor(data["first_name"], data["last_name"], data["middle_name"], data["experience"],
                          data["specialty_id"], data["username"], data["password"])
    if user_id:
        return {"message": "Пользователь зарегистрирован успешно."}
    else:
        return {"error": "Регистрация не прошла."}

@app.route("/register", methods=["POST", "GET"])
def register_user_route():
    if request.method == "POST":
        f_username = request.form['username']
        f_password = request.form['password']
        f_role = request.form['role']
        user_id = register_user(f_username, f_password, f_role)
        if user_id:
            return redirect("/")
        else:
            return redirect("/auth/register")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET"])
def login_route():
    print(session)
    if 'user' in session:
        return redirect("/")
    else:
        return render_template('login.html')


@app.route("/auth", methods=["POST"])
def auth_user_route():
    f_username = request.form['username']
    f_password = request.form['password']

    username = authenticate_user(f_username, f_password)
    if username:
        user = get_user_by_username(username)[0]
        print(user, type(user))
        user = User(**user)
        # user = User(user_id=user['user_id'], username=user['username'], role=user['user_role'])
        print(user)
        session['user'] = user.__dict__
        return redirect("/")
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)  # Удалить пользователя из сессии
    return redirect("/")
