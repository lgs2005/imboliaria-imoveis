from datetime import timedelta
from flask import Flask


from modelo import db
import blueprints.cliente
import blueprints.pages
import blueprints.imagem
import blueprints.venda
import blueprints.imovel
import blueprints.alugel
import blueprints.busca

DATABASE_FILE = 'database.db'


def create_app():
    app = Flask(__name__)

    app.config['MAX_CONTENT_LENGHT'] = 2 * 1024 * 1024

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_FILE}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['JWT_SECRET_KEY'] = 'b25aeed15e1a4f3e9837125d8a815b86-casanapraia-2c040adb0beb40cebf4af3276028acee'
    #app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

    db.init_app(app)

    with app.app_context():
        db.session.execute('PRAGMA FOREIGN_KEYS=ON')

    blueprints.cliente.jwt.init_app(app)

    app.register_blueprint(blueprints.cliente.bp)
    app.register_blueprint(blueprints.pages.bp)
    app.register_blueprint(blueprints.imagem.bp)

    app.register_blueprint(blueprints.venda.bp)
    app.register_blueprint(blueprints.imovel.bp)
    app.register_blueprint(blueprints.alugel.bp)
    app.register_blueprint(blueprints.busca.bp)

    return app
