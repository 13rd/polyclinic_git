from flask_sqlalchemy import SQLAlchemy
from config import Config
from dataclasses import dataclass

db = SQLAlchemy()

class Diagnoses(db.Model):
    __tablename__ = 'diagnoses'
    diagnosis_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    mkb_code = db.Column(db.String(8))

class DoctorSpecialties(db.Model):
    __tablename__ = 'doctor_specialties'
    id = db.Column(db.Integer, primary_key=True)
    specialty = db.Column(db.String(100))

class Doctors(db.Model):
    __tablename__ = 'doctors'
    doctor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    experience = db.Column(db.Integer)
    specialty_id = db.Column(db.Integer, db.ForeignKey('doctor_specialties.id'))
    user_id = db.Column(db.Integer)

class Patients(db.Model):
    __tablename__ = 'patients'
    patient_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    address = db.Column(db.Text)
    user_id = db.Column(db.Integer)

class Roles(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50))

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    passwordhash = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))

class Visits(db.Model):
    __tablename__ = 'visits'
    visit_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    visit_date = db.Column(db.DateTime(timezone=True))
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnoses.diagnosis_id'))


@dataclass
class User():
    user_id: int
    username: str
    role: str

    # def __init__(self, user_id, username, role):
    #     self.user_id = user_id
    #     self.username = username
    #     self.role = role
    #
    # def to_dict(self):
    #     return {"user_id": self.user_id, "username": self.username, "role": self.role}
