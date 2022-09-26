from init import db


def extract_fields(*fields: 'str'):
    return lambda self: {field: self.__getattribute__(field) for field in fields}


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(254), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    senha_hash = db.Column(db.String(254), nullable=False)

    dados = extract_fields('id', 'nome', 'email', 'cpf', 'telefone')


class Imovel(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(254), nullable=False)
    descricao = db.Column(db.String(800), nullable=False)
    localizacao = db.Column(db.String(254), nullable=False)
    preco = db.Column(db.Integer, nullable=False)

    aluguel = db.Column(db.Boolean, nullable=False)
    mobiliado = db.Column(db.Boolean, nullable=False)
    area = db.Column(db.Integer, nullable=False)

    dados = extract_fields('id', 'nome', 'descricao', 'localizacao',
                           'preco', 'aluguel', 'mobilizado', 'area')


class Compra(db.Model):
    imovel_id = db.Column(db.Integer, db.ForeignKey(
        Imovel.id), primary_key=True)
    imovel = db.relationship('Imovel')

    comprador_id = db.Column(db.Integer, db.ForeignKey(Usuario.id))
    comprador = db.relationship('Usuario')

    dados = extract_fields('imovel_id', 'comprador_id')
