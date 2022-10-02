from datetime import timedelta
from typing import TYPE_CHECKING

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

if TYPE_CHECKING:
    import flask_sqlalchemy
    import sqlalchemy
    import sqlalchemy.orm

    from typing_extensions import Self

    class Model(flask_sqlalchemy.Model):
        query: flask_sqlalchemy.BaseQuery[Self]

    class Database(flask_sqlalchemy.SQLAlchemy):
        Model: type[Model]
        relationship: type[sqlalchemy.orm.relationship]

    db: Database

NOME_PROJETO = 'imboliahria'

app = Flask(NOME_PROJETO)
bcrypt = Bcrypt(app)

app.config['JWT_SECRET_KEY'] = 'b25aeed15e1a4f3e9837125d8a815b86-casanapraia-2c040adb0beb40cebf4af3276028acee'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1, minutes=30)

jwt = JWTManager(app)