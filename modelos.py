from init import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean


class Cliente(db.Model):
    '''Representa um cliente'''
    id = Column(Integer, primary_key=True)

    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    cpf = Column(String(11), nullable=False, unique=True)
    telefone = Column(String(20), nullable=False, unique=True)
    hash_senha = Column(String(60), nullable=False)


class Imovel(db.Model):
    '''Representa os dados de um imóvel'''
    id = Column(Integer, primary_key=True)

    nome = Column(String(255), nullable=False)
    descricao = Column(String(1000), nullable=False)
    local = Column(String(255), nullable=False)
    area = Column(Integer, nullable=False)

    venda = db.relationship('Venda', back_populates='imovel', uselist=False)


class Venda(db.Model):
    '''Representa a venda de um imóvel'''
    id = Column(ForeignKey(Imovel.id), primary_key=True)

    imovel = db.relationship(Imovel, back_populates='venda', uselist=False)
    preco = Column(Integer, nullable=False)

    tipo = Column(String(20))
    __mapper_args__ = {
        'polymorphic_on': tipo,
        'polymorphic_identity': 'venda'
    }


class VendaRealizada(Venda):
    '''Uma venda que foi realizada'''
    __mapper_args__ = {
        'polymorphic_identity': 'realizada'
    }

    data = Column(DateTime, nullable=False)

    cliente_id = Column(ForeignKey(Cliente.id))
    cliente = db.relationship(Cliente)


class VendaAlugel(Venda):
    '''Venda através de alugeis'''
    __mapper_args__ = {
        'polymorphic_identity': 'alugel'
    }

    alugado = Column(Boolean, nullable=False)
    alugeis = db.relationship('alugeis', back_populates='venda')


class Alugel(db.Model):
    '''Um alugel realizado'''
    id = Column(Integer, primary_key=True)

    venda_id = Column(ForeignKey(VendaAlugel.id))
    venda = db.relationship(VendaAlugel, back_populates='alugeis')

    cliente_id = Column(ForeignKey(Cliente.id))
    cliente = db.relationship(Cliente)

    data = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)


class VendaLeilao(Venda):
    '''Venda através de leilao'''
    __mapper_args__ = {
        'polymorphic_identity': 'leilao'
    }

    data_fim = Column(DateTime, nullable=False)
    apostas = db.relationship('Aposta', back_populates='venda')

    vencedor_id = Column(ForeignKey('aposta.id'), nullable=True)
    vencedor = db.relationship('Aposta')


class Aposta(db.Model):
    '''Aposta feita em um leilao'''
    id = Column(Integer, primary_key=True)

    cliente_id = Column(ForeignKey(Cliente.id))
    cliente = db.relationship(Cliente)

    leilao_id = Column(ForeignKey(VendaLeilao.id))
    leilao = db.relationship(VendaLeilao, back_populates='apostas')

    valor = Column(Integer, nullable=False)
