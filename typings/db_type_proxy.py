import flask_sqlalchemy
import sqlalchemy.orm


class Model(flask_sqlalchemy.Model):
    query: flask_sqlalchemy.BaseQuery


class SQLAlchemy():
    Query = flask_sqlalchemy.BaseQuery
    Model = Model
    session: sqlalchemy.orm.scoped_session
