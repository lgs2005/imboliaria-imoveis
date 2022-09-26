from datetime import timedelta
from typing import TYPE_CHECKING

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

if TYPE_CHECKING:
    import flask_sqlalchemy
    import sqlalchemy.orm

    class Model(flask_sqlalchemy.Model):
        query: flask_sqlalchemy.BaseQuery

    class Database(SQLAlchemy):
        Query = flask_sqlalchemy.BaseQuery
        Model = Model
        session: sqlalchemy.orm.scoped_session

    db: Database

NOME_PROJETO = 'imboliahria'

app = Flask(NOME_PROJETO)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{NOME_PROJETO}.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.session.execute('PRAGMA FOREIGN_KEYS=ON')

app.config['JWT_SECRET_KEY'] = 'b25aeed15e1a4f3e9837125d8a815b86-casanapraia-2c040adb0beb40cebf4af3276028acee'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1, minutes=30)

jwt = JWTManager(app)
