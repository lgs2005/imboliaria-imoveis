from flask import render_template

from init import app
from database import db

# imports para registrar no aplicativo
import database
import cliente

@app.route('/', methods=['GET'])
def rota_inicial():
    return render_template('index.html')


@app.route('/sobre', methods=['GET'])
def rota_pagina_sobre():
    return render_template('sobre.html')


@app.route('/contato', methods=['GET'])
def rota_pagina_contato():
    return render_template('contato.html')


if __name__ == '__main__':
    db.create_all()

    # # cliente = Cliente(
    # #     nome='lucas',
    # #     email='email',
    # #     cpf='01158932521',
    # #     telefone='047992176139',
    # #     senha='ok'
    # # )

    # cliente = Cliente.query.get(1)

    # imovel = Imovel(
    #     nome='teste',
    #     descricao='teste',
    #     local='teste',
    #     area=200
    # )

    # # venda = Venda(
    # #     imovel=imovel,
    # #     preco=200,
    # # )

    # # venda = VendaAlugel(
    # #     imovel=imovel,
    # #     preco=2000,
    # #     alugado=False,
    # # )

    # venda = VendaLeilao(
    #     imovel=imovel,
    #     preco=2000,
    #     data_fim=datetime.now(),
    # )

    # aposta1 = Aposta(
    #     leilao=venda,
    #     cliente=cliente,
    #     valor=5000,
    #     data=datetime.now(),
    # )

    # aposta2 = Aposta(
    #     leilao=venda,
    #     cliente=cliente,
    #     valor=8000,
    #     data=datetime.now(),
    # )


    # # alugel = Alugel(
    # #     venda=venda,
    # #     cliente=cliente,
    # #     data=datetime.utcnow(),
    # #     data_fim=datetime.now(timezone.utc) + timedelta(days=30)
    # # )

    # # alugel2 = Alugel(
    # #     venda=venda,
    # #     cliente=cliente,
    # #     data=datetime.utcnow(),
    # #     data_fim=datetime.now(timezone.utc) + timedelta(days=30)
    # # )


    # db.session.add_all([imovel, venda, aposta1, aposta2])
    # db.session.commit()

    # print(venda)
    # print(venda.apostas)
    # print(aposta1.leilao)