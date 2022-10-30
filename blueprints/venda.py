from datetime import datetime, timezone
from http.client import BAD_REQUEST, CONFLICT, UNAUTHORIZED
from flask import Blueprint, abort, jsonify
from flask_jwt_extended import jwt_required

from modelo import Cliente, Imovel, Venda, VendaAlugel, VendaRealizada, db
from utils import get_json_fields, admin_required

bp = Blueprint('venda', __name__, url_prefix='/api/venda')


@bp.post('/<int:id>')
@admin_required
def cadastro_venda(id:int):
    tipo = get_json_fields(str, 'tipo')[0]
    preco = get_json_fields(int, 'preco')[0]

    imovel = Imovel.query.get_or_404(id)
    venda = Venda.query.get(id)

    if venda != None:
        abort(UNAUTHORIZED)

    if tipo == 'venda':
        venda = Venda(
            tipo=tipo,
            preco=preco,
            imovel=imovel,
        )

    elif tipo == 'realizada':
        cliente_id = get_json_fields(int, 'cliente_id')[0]
        cliente = Cliente.query.get_or_404(cliente_id)

        venda = VendaRealizada(
            tipo=tipo,
            preco=preco,
            imovel=imovel,
            cliente=cliente,
            data=datetime.now(timezone.utc)
        )

    elif tipo == 'alugel':
        venda = VendaAlugel(
            tipo=tipo,
            preco=preco,
            imovel=imovel,
            alugado=False,
        )

    else:
        abort(BAD_REQUEST)

    db.session.add(venda)
    db.session.commit()

    return jsonify(venda.dados())


@bp.get('/<int:id>')
def dados_venda(id:int):
    return jsonify(Venda.query.get_or_404(id).dados())


@bp.delete('/<int:id>')
@admin_required
def delete_venda(id:int):
    venda = Venda.query.get_or_404(id)

    db.session.delete(venda)
    db.session.commit()

    return 'ok', 200


@bp.post('/<int:id>/comprar')
@jwt_required()
def comprar_venda(id:int):
    venda: Venda = Venda.query.get_or_404(id)

    if venda.tipo != 'venda':
        abort(CONFLICT)
    
    venda_realizada = VendaRealizada(
        tipo=venda.tipo,
        preco=venda.preco,
        imovel=venda.imovel,
        cliente=Cliente.atual(),
    )

    db.session.remove(venda)
    db.session.add(venda_realizada)
    db.session.commit()

    return jsonify(venda_realizada.dados())
