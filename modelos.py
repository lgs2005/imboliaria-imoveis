from datetime import datetime
from typing import TYPE_CHECKING

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped

from init import NOME_PROJETO, app

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{NOME_PROJETO}.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

db = SQLAlchemy(app)
db.session.execute('PRAGMA FOREIGN_KEYS=ON')


class Cliente(db.Model):
    '''Representa um cliente''' 
    id:             Mapped[int]             = Column(Integer, primary_key=True)

    nome:           Mapped[str]             = Column(String(255), nullable=False)
    email:          Mapped[str]             = Column(String(255), nullable=False, unique=True)
    cpf:            Mapped[str]             = Column(String(11), nullable=False, unique=True)
    telefone:       Mapped[str]             = Column(String(20), nullable=False, unique=True)
    hash_senha:     Mapped[str]             = Column(String(60), nullable=False)


class Imovel(db.Model):
    '''Representa os dados de um imóvel'''

    id:             Mapped[int]             = Column(Integer, primary_key=True)

    nome:           Mapped[str]             = Column(String(255), nullable=False)
    descricao:      Mapped[str]             = Column(String(1000), nullable=False)
    local:          Mapped[str]             = Column(String(255), nullable=False)
    area:           Mapped[int]             = Column(Integer, nullable=False)

    venda:          Mapped['Venda']         = db.relationship('Venda', back_populates='imovel', uselist=False)


class Venda(db.Model):
    '''Representa a venda de um imóvel'''

    id:             Mapped[int]             = Column(ForeignKey(Imovel.id), primary_key=True)
    imovel:         Mapped[Imovel]          = db.relationship(Imovel, back_populates='venda', uselist=False)

    preco:          Mapped[int]             = Column(Integer, nullable=False)
    tipo:           Mapped[str]             = Column(String(20))
    
    __mapper_args__ = {
        'polymorphic_on': tipo,
        'polymorphic_identity': 'venda'
    }


class VendaRealizada(Venda):
    '''Uma venda que foi realizada'''

    __mapper_args__ = {
        'polymorphic_identity': 'realizada'
    }

    cliente_id:     Mapped[int]             = Column(ForeignKey(Cliente.id))
    cliente:        Mapped[Cliente]         = db.relationship(Cliente)

    data:           Mapped[datetime]        = Column(DateTime, nullable=False)


class VendaAlugel(Venda):
    '''Venda através de alugeis'''

    __mapper_args__ = {
        'polymorphic_identity': 'alugel'
    }

    alugado:        Mapped[bool]            = Column(Boolean, nullable=False)
    alugeis:        Mapped[list['Alugel']]  = db.relationship('alugeis', back_populates='venda')


class Alugel(db.Model):
    '''Um alugel realizado'''

    id:             Mapped[int]             = Column(Integer, primary_key=True)

    venda_id:       Mapped[int]             = Column(ForeignKey(VendaAlugel.id))
    venda:          Mapped[VendaAlugel]     = db.relationship(VendaAlugel, back_populates='alugeis')

    cliente_id:     Mapped[int]             = Column(ForeignKey(Cliente.id))
    cliente:        Mapped[Cliente]         = db.relationship(Cliente)

    data:           Mapped[datetime]        = Column(DateTime, nullable=False)
    data_fim:       Mapped[datetime]        = Column(DateTime, nullable=False)


class VendaLeilao(Venda):
    '''Venda através de leilao'''

    __mapper_args__ = {
        'polymorphic_identity': 'leilao'
    }

    data_fim:       Mapped[datetime]        = Column(DateTime, nullable=False)
    apostas:        Mapped[list['Aposta']]  = db.relationship('Aposta', back_populates='venda')

    vencedor_id:    Mapped[int]             = Column(ForeignKey('aposta.id'), nullable=True)
    vencedor:       Mapped['Aposta']        = db.relationship('Aposta')


class Aposta(db.Model):
    '''Aposta feita em um leilao'''

    id:             Mapped[int]             = Column(Integer, primary_key=True)

    cliente_id:     Mapped[int]             = Column(ForeignKey(Cliente.id))
    cliente:        Mapped[Cliente]         = db.relationship(Cliente)

    leilao_id:      Mapped[int]             = Column(ForeignKey(VendaLeilao.id))
    leilao:         Mapped[VendaLeilao]     = db.relationship(VendaLeilao, back_populates='apostas')

    valor:          Mapped[int]             = Column(Integer, nullable=False)
    data:           Mapped[datetime]        = Column(DateTime, nullable=False)
