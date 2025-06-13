#!/usr/bin/env python
'''
Usuario DB manager
---------------------------
Autor: Ing.Jesús Matías González
Version: 1.1

Descripcion:
Programa creado para administrar la base de datos de registro
de usuarios
'''

__author__ = "Ing.Jesús Matías González"
__email__ = "ingjesusmrgonzalez@gmail.com"
__version__ = "2.0"

import os
from datetime import datetime, timedelta

# pip3 install Flask-Login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    db.drop_all()

    # Crear las tablas
    db.create_all()


def insert(name, email, password):
    # Verificar si ya existe el usuario
    user = User.query.filter_by(name=name).first()

    # Si el usuario existe no puedo crearlo
    if user:
        return None

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return new_user

def get_user(name):
    return User.query.filter_by(name=name).first()

def check_password(name, password):
    user = User.query.filter_by(name=name).first()

    # Verificamos si el usuario existe
    if not user:
        return False

    # Verificamos la password
    if check_password_hash(user.password, password):
        return True
    else:
        return False


