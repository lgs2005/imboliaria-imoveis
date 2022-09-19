from init import app, db, jwt


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(254), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    senha_hash = db.Column(db.String(254), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    def json(self):
        return {

        }


class Imovel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(254), nullable=False)
    descricao = db.Column(db.String(800), nullable=False)
    localizacao = db.Column(db.String(254), nullable=False)
    preco = db.Column(db.Integer, nullable=False)

    aluguel = db.Column(db.Boolean, nullable=False)
    mobiliado = db.Column(db.Boolean, nullable=False)
    area = db.Column(db.Integer, nullable=False)

    venda = db.relationship('Venda')

    def json(self):
        return {

        }


# class Casa(Imovel):
#     pass


# class Apartamento(Imovel):
#     pass


class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    comprador_id = db.Column(db.Integer)
    comprador = db.relationship('Usuario')

    imovel_id = db.Column(db.Integer)
    imovel = db.relationship(Imovel)

    def json(self):
        return {

        }
