from datetime import timedelta
from typing import TYPE_CHECKING

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

if TYPE_CHECKING:
    import db_type_proxy
    db: db_type_proxy.SQLAlchemy

NOME_PROJETO = 'imboliahria'

app = Flask(NOME_PROJETO)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{NOME_PROJETO}.db'
app.config['JWT_SECRET_KEY'] = 'b25aeed15e1a4f3e9837125d8a815b86-casanapraia-2c040adb0beb40cebf4af3276028acee'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1, minutes=30)

db = SQLAlchemy(app)
jwt = JWTManager(app)
