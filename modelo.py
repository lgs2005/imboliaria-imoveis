from datetime import datetime, timezone
from typing import TYPE_CHECKING, Callable

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import get_current_user
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped


db = SQLAlchemy()


def extrair_dados(*campos: str) -> 'Callable[[object], dict]':
    '''Gera uma função que retorna os campos especificados em um formato pronto para json'''
    def get_dado(o: object, c: str):
        v = o.__getattribute__(c)
        if isinstance(v, datetime):
            v = v.isoformat()
        return v
        
    return lambda self: { c: get_dado(self, c) for c in campos }


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

    venda:          'Mapped[Venda | None]'         = db.relationship('Venda', back_populates='imovel', uselist=False)
    imagens:        'Mapped[list[Imagem]]'  = db.relationship('Imagem', back_populates='imovel')

    dados = extrair_dados('id', 'nome', 'descricao', 'cidade', 'bairro', 'area', 'quartos', 'apartamento', 'quintal')


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

    dados = extrair_dados('id', 'preco', 'tipo')


class VendaRealizada(Venda):
    '''Uma venda que foi realizada'''

    __mapper_args__ = {
        'polymorphic_identity': 'realizada'
    }

    cliente_id:     Mapped[int]             = Column(ForeignKey(Cliente.id))
    cliente:        Mapped[Cliente]         = db.relationship(Cliente)

    data:           Mapped[datetime]        = Column(DateTime)

    dados = extrair_dados('id', 'preco', 'tipo', 'cliente_id', 'data')


class VendaAlugel(Venda):
    '''Venda através de alugeis'''

    __mapper_args__ = {
        'polymorphic_identity': 'alugel'
    }

    alugado:        Mapped[bool]            = Column(Boolean)
    alugeis:        'Mapped[list[Alugel]]'  = db.relationship('Alugel', back_populates='venda')

    dados = extrair_dados('id', 'preco', 'tipo', 'alugado')

    def alugel_atual(self):
        agora = datetime.now(timezone.utc)

        for alugel in self.alugeis:
            if alugel.data_fim >= agora:
                return alugel
        
        return None


class Alugel(db.Model):
    '''Um alugel realizado'''

    id:             Mapped[int]             = Column(Integer, primary_key=True)

    venda_id:       Mapped[int]             = Column(ForeignKey(VendaAlugel.id))
    venda:          Mapped[VendaAlugel]     = db.relationship(VendaAlugel, back_populates='alugeis')

    cliente_id:     Mapped[int]             = Column(ForeignKey(Cliente.id))
    cliente:        Mapped[Cliente]         = db.relationship(Cliente)

    data:           Mapped[datetime]        = Column(DateTime, nullable=False)
    data_fim:       Mapped[datetime]        = Column(DateTime, nullable=False)

    dados = extrair_dados('id', 'venda_id', 'cliente_id', 'data', 'data_fim')


class Imagem(db.Model):
    id:             Mapped[int]             = Column(Integer, primary_key=True)
    arquivo:        Mapped[str]             = Column(String(32), nullable=False, unique=True)

    imovel_id:      Mapped[int]             = Column(ForeignKey(Imovel.id))
    imovel:         Mapped[Imovel]          = db.relationship(Imovel, back_populates='imagens')
