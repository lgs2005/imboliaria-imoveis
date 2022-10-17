from datetime import datetime
from typing import TYPE_CHECKING, Callable

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import get_current_user
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped

if TYPE_CHECKING:
    import flask_sqlalchemy
    import sqlalchemy
    import sqlalchemy.orm
    from typing_extensions import Self

    class Model(flask_sqlalchemy.Model):
        query: 'flask_sqlalchemy.BaseQuery[Self]'

    class Database(flask_sqlalchemy.SQLAlchemy):
        Model: 'type[Model]'
        relationship: 'type[sqlalchemy.orm.relationship]'

    db: Database

db = SQLAlchemy()


def extrair_dados(*campos: str):
    return lambda self: { c: self.__getattribute__(c) for c in campos }


class Cliente(db.Model):
    '''Representa um cliente''' 
    id:             Mapped[int]             = Column(Integer, primary_key=True)

    nome:           Mapped[str]             = Column(String(255), nullable=False)
    email:          Mapped[str]             = Column(String(255), nullable=False, unique=True)
    cpf:            Mapped[str]             = Column(String(11), nullable=False, unique=True)
    telefone:       Mapped[str]             = Column(String(20), nullable=False, unique=True)
    senha:          Mapped[str]             = Column(String(60), nullable=False)

    admin:          Mapped[bool]            = Column(Boolean, default=False)

    dados = extrair_dados('nome', 'email', 'cpf', 'telefone')
    atual: 'Callable[[], Cliente]' = lambda: get_current_user()
    

class Imovel(db.Model):
    '''Representa os dados de um imóvel'''

    id:             Mapped[int]             = Column(Integer, primary_key=True)

    nome:           Mapped[str]             = Column(String(255), nullable=False)
    descricao:      Mapped[str]             = Column(String(1000), nullable=False)
    cidade:         Mapped[str]             = Column(String(255), nullable=False)
    bairro:         Mapped[str]             = Column(String(255), nullable=False)
    area:           Mapped[int]             = Column(Integer, nullable=False)
    quartos:        Mapped[int]             = Column(Integer, nullable=False)
    apartamento:    Mapped[bool]            = Column(Boolean, nullable=False)
    quintal:        Mapped[bool]            = Column(Boolean, nullable=False)

    venda:          Mapped['Venda']         = db.relationship('Venda', back_populates='imovel', uselist=False)
    imagens:        Mapped['list[Imagem]']  = db.relationship('Imagem', back_populates='imovel')


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

    data:           Mapped[datetime]        = Column(DateTime)


class VendaAlugel(Venda):
    '''Venda através de alugeis'''

    __mapper_args__ = {
        'polymorphic_identity': 'alugel'
    }

    alugado:        Mapped[bool]            = Column(Boolean)
    alugeis:        'Mapped[list[Alugel]]'  = db.relationship('Alugel', back_populates='venda')


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

    data_fim:       Mapped[datetime]        = Column(DateTime)
    apostas:        'Mapped[list[Aposta]]'  = db.relationship('Aposta', back_populates='leilao', foreign_keys='Aposta.leilao_id')

    vencedor_id:    Mapped[int]             = Column(ForeignKey('aposta.id'), nullable=True)
    vencedor:       Mapped['Aposta']        = db.relationship('Aposta', foreign_keys=vencedor_id)


class Aposta(db.Model):
    '''Aposta feita em um leilao'''

    id:             Mapped[int]             = Column(Integer, primary_key=True)

    cliente_id:     Mapped[int]             = Column(ForeignKey(Cliente.id))
    cliente:        Mapped[Cliente]         = db.relationship(Cliente)

    leilao_id:      Mapped[int]             = Column(ForeignKey(VendaLeilao.id))
    leilao:         Mapped[VendaLeilao]     = db.relationship(VendaLeilao, back_populates='apostas', foreign_keys=leilao_id)

    valor:          Mapped[int]             = Column(Integer, nullable=False)
    data:           Mapped[datetime]        = Column(DateTime, nullable=False)


class Imagem(db.Model):
    id: Mapped[int] = Column(Integer, primary_key=True)
    arquivo: Mapped[str] = Column(String(32), nullable=False, unique=True)

    imovel_id: Mapped[int] = Column(ForeignKey(Imovel.id))
    imovel = db.relationship(Imovel, back_populates='imagens')
