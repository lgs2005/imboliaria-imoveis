import os
from datetime import datetime

from modelo import Alugel, Cliente, Imovel, Venda, VendaAlugel,VendaRealizada, db
from flask import Flask

from testes.tester import Tester

tester = Tester()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Testes importantes para verificar o
# funcionamento da estrutura e a
# integridade do banco de dados


@tester.test('criar banco de dados')
def criar_db():
    app.app_context().push()

    if os.path.exists(app.instance_path + '/testes.db'):
        os.remove(app.instance_path + '/testes.db')

    db.init_app(app)
    db.session.execute('PRAGMA FOREIGN_KEYS=ON')
    db.create_all()


@tester.test('inserir e buscar objetos')
def inserir_objetos():

    cliente = Cliente(
        nome='Teste',
        email='teste@teste.com',
        cpf='00011122233',
        telefone='047912345678',
        senha='$$$hash$$$$456$$???$?$?$??$',
    )

    imovel1 = Imovel(
        nome='imovel1',
        descricao='[]',
        cidade='sao jose dos pinhais',
        bairro='aquarinha',
        area=200,
        quartos=2,
        apartamento=False,
        quintal=True,
    )

    imovel2 = Imovel(
        nome='imovel2',
        descricao='[]',
        cidade='sao jose dos pinhais',
        bairro='aquarinha',
        area=200,
        quartos=2,
        apartamento=False,
        quintal=True,
    )

    imovel3 = Imovel(
        nome='imovel3',
        descricao='[]',
        cidade='sao jose dos pinhais',
        bairro='aquarinha',
        area=200,
        quartos=2,
        apartamento=False,
        quintal=True,
    )

    venda_normal = Venda(
        imovel=imovel1,
        preco=2_000_000,  # centavos, 2_000_000 = 20_000
    )

    venda_realizada = VendaRealizada(
        imovel=imovel2,
        cliente=cliente,
        preco=2_000_000,
        data=datetime.utcnow(),
    )

    venda_alugel = VendaAlugel(
        imovel=imovel3,
        preco=2_000,
        alugado=False,
    )

    alugel1 = Alugel(
        venda=venda_alugel,
        cliente=cliente,
        data=datetime.utcnow(),
        data_fim=datetime.utcnow()
    )

    alugel2 = Alugel(
        venda=venda_alugel,
        cliente=cliente,
        data=datetime.utcnow(),
        data_fim=datetime.utcnow()
    )


    db.session.add_all([cliente, imovel1, imovel2, imovel3, venda_normal,
                       venda_realizada, venda_alugel, alugel1, alugel2])
    db.session.commit()

    imovel2_busca = Imovel.query.filter_by(nome='imovel2').first()
    venda_realizada_busca = VendaRealizada.query.filter_by(imovel=imovel2_busca).first()

    assert venda_realizada_busca != None, 'venda nao encontrada por imovel'
    assert venda_realizada_busca.cliente != None, 'nao carregou cliente'

    imovel3_busca = Imovel.query.filter_by(nome='imovel3').first()

    assert imovel3_busca.venda.tipo == 'alugel', 'nao salvou venda correta'
    assert len(imovel3_busca.venda.alugeis) == 2, 'alugeis nao listados'

    vendas = Venda.query.all()

    assert len(vendas) == 3, 'nao carregou todas as vendas'


@tester.test('apenas uma venda por imovel', erro=True)
def uma_venda_por_imovel():
    imovel = Imovel(
        nome='imovel_teste',
        descricao='[]',
        cidade='sao jose dos pinhais',
        bairro='aquarinha',
        area=200,
        quartos=2,
        apartamento=False,
        quintal=True,
    )

    venda1 = Venda(
        imovel=imovel,
        preco=200,
    )

    venda2 = Venda( # ! ERRO: apenas uma venda por imovel
        imovel=imovel,
        preco=400,
    )

    db.session.add_all([imovel, venda1, venda2])
    db.session.commit()


@tester.test('alugel apenas em VendaAlugel', erro=True)
def alugel_venda_alugel():
    cliente = Cliente(
        nome='Teste',
        email='teste@teste.com',
        cpf='00011122233',
        telefone='047912345678',
        senha='$$$hash$$$$456$$???$?$?$??$',
    )

    imovel = Imovel(
        nome='imovel_teste',
        descricao='[]',
        cidade='sao jose dos pinhais',
        bairro='aquarinha',
        area=200,
        quartos=2,
        apartamento=False,
        quintal=True,
    )

    venda = Venda(
        imovel=imovel,
        preco=200,
    )

    alugel = Alugel( # ! ERRO: alugel apenas em VendaAlugel
        venda=venda,
        cliente=cliente,
        data=datetime.utcnow(),
        data_fim=datetime.utcnow(),
    )

    db.session.add_all([cliente, imovel, venda, alugel])
    db.session.commit()
