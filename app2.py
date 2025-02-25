from flask import Flask, render_template, redirect, session
from config import Config
from models import db

from routes.routes_diagnoses import app as diagnoses_route
from routes.routes_doctors import app as doctor_route
from routes.routes_doctor_specialties import app as doctor_specialties_route
from routes.routes_patients import app as patients_route
from routes.routes_roles import app as roles_route
from routes.routes_users import app as users_route
from routes.routes_visits import app as visits_route
from routes.routes_auth import app as auth_route
from routes.routes_admin import app as admin_route

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(diagnoses_route)
app.register_blueprint(doctor_route)
app.register_blueprint(doctor_specialties_route)
app.register_blueprint(patients_route)
app.register_blueprint(roles_route)
app.register_blueprint(visits_route)
app.register_blueprint(users_route)
app.register_blueprint(auth_route)
app.register_blueprint(admin_route)

@app.route("/", methods=["GET"])
def home():
    if "user" in session:
        user = session['user']
        return render_template("index.html", user=user)
    else:
        return render_template("index.html", user=None)

if __name__ == '__main__':
    app.run(debug=True)


"""
Задание: В поликлинике ведется учет посещений больными врачей. Данные о каждом враче содержат Ф.И.О., специальность и стаж работы. 
Каждый врач может принимать множество пациентов, и каждый пациент может посещать нескольких врачей (в том числе в один и тот же день). 
В карточке пациента указываются его Ф.И.О., дата рождения и адрес места жительства. В результате визита врач ставит пациенту диагноз. 
Для удобства анализа заболеваемости диагнозы стандартизованы и подлежат единому учету.
В целях анализа результатов работы поликлиники необходимо иметь возможность автоматически генерировать следующие документы:
• перечень специалистов (список врачей по специальностям);
• количества визитов к врачам;
• количества случаев заболевания по каждому диагнозу.
Кроме того, необходимо иметь возможность просматривать для каждого из врачей список больных, которые посетили его за заданный период времени.

"""