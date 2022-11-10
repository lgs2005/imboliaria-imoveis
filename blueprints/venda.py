from datetime import datetime, timezone
from http.client import BAD_REQUEST, CONFLICT, UNAUTHORIZED
from flask import Blueprint, abort, jsonify
from flask_jwt_extended import jwt_required

from modelo import Cliente, Imovel, Venda, VendaAlugel, VendaRealizada, db
from utils import get_json_fields, admin_required

bp = Blueprint('venda', __name__, url_prefix='/api/venda')

# curl -H "Authorization: Bearer (jwt)" 127.0.0.1:5000/api/venda/1 -H "Content-Type: application/json" -d "{\"tipo\": \"venda\", \"preco\": 200}"
# venda alugel:
# curl -H "Authorization: Bearer (jwt)" 127.0.0.1:5000/api/venda/3 -H "Content-Type: application/json" -d "{\"tipo\": \"alugel\", \"preco\": 200}"
@bp.post('/<int:id>')
@admin_required
def cadastro_venda(id:int):
    '''Cadastra uma venda para um ímovel
    O ID no URL é o id do imóvel, apenas uma venda por imóvel
    Parâmetros:
        tipo: 'venda' ou 'alugel'
        preco: int
    
        ou

        tipo: 'realizada'
        preco: int
        cliente_id: int
    '''
    tipo = get_json_fields(str, 'tipo')
    preco = get_json_fields(int, 'preco')

    imovel = Imovel.query.get_or_404(id)
    venda = Venda.query.get(id)

    if venda != None:
        abort(CONFLICT)

    if tipo == 'venda':
        venda = Venda(
            preco=preco,
            imovel=imovel,
        )

    elif tipo == 'realizada':
        cliente_id = get_json_fields(int, 'cliente_id')[0]
        cliente = Cliente.query.get_or_404(cliente_id)

        venda = VendaRealizada(
            preco=preco,
            imovel=imovel,
            cliente=cliente,
            data=datetime.now(timezone.utc)
        )

    elif tipo == 'alugel':
        venda = VendaAlugel(
            preco=preco,
            imovel=imovel,
            alugado=False,
        )

    else:
        abort(BAD_REQUEST)

    db.session.add(venda)
    db.session.commit()

    return jsonify(venda.dados())


# curl 127.0.0.1:5000/api/venda/1
@bp.get('/<int:id>')
def dados_venda(id:int):
    '''Retorna os dados de uma venda'''
    return jsonify(Venda.query.get_or_404(id).dados())


# curl -H "Authorization: Bearer (jwt)" 127.0.0.1:5000/api/venda/1 -X DELETE
@bp.delete('/<int:id>')
@admin_required
def delete_venda(id:int):
    '''Remove uma venda do banco de dados'''
    venda = Venda.query.get_or_404(id)

    db.session.delete(venda)
    db.session.commit()

    return 'ok', 200


# curl -H "Authorization: Bearer (jwt)" 127.0.0.1:5000/api/venda/1/comprar -X POST
@bp.post('/<int:id>/comprar')
@jwt_required()
def comprar_venda(id:int):
    '''Permite aos usuários fazer uma compra fornecendo o id de uma venda
    Apenas para vendas do tipo 'venda'
    '''
    venda: Venda = Venda.query.get_or_404(id)

    if venda.tipo != 'venda':
        abort(CONFLICT)
    
    venda_realizada = VendaRealizada(
        preco=venda.preco,
        imovel=venda.imovel,
        cliente=Cliente.atual(),
        data=datetime.now(timezone.utc),
    )

    db.session.delete(venda)
    db.session.add(venda_realizada)
    db.session.commit()

    return jsonify(venda_realizada.dados())
