from datetime import datetime, timezone
from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR, UNAUTHORIZED
from flask import Blueprint, abort, jsonify

from modelo import Imovel, Venda, VendaAlugel, VendaRealizada, db
from utils import get_json_fields, admin_required

bp = Blueprint('venda', url_prefix='/api/venda')


@bp.post('/<int:id>')
@admin_required()
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
        # TODO: ver se cliente existe
        cliente_id = get_json_fields(int, 'cliente')[0]

        venda = VendaRealizada(
            tipo=tipo,
            preco=preco,
            imovel=imovel,
            cliente_id=cliente_id,
            data=datetime.now(timezone.utc)
        )

    elif tipo == 'alugel':
        venda = VendaAlugel(
            tipo=tipo,
            preco=preco,
            imovel=imovel,
            alugado=False,
        )

    elif tipo == 'leilao':
        # mais tarde
        abort(INTERNAL_SERVER_ERROR)

    else:
        abort(BAD_REQUEST)

    db.session.add(venda)
    db.session.commit()

    return jsonify(venda.dados())