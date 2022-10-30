from datetime import datetime, timezone
from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND
from flask import Blueprint, abort, jsonify
from flask_jwt_extended import jwt_required

from modelo import Alugel, Cliente, VendaAlugel, db
from utils import admin_required, get_json_fields

bp = Blueprint('alugel', __name__, url_prefix='/api/alugel')


@bp.post('/<int:id>/alugar')
@jwt_required()
def adicionar_alugel(id:int):
    venda: VendaAlugel = VendaAlugel.query.get_or_404(id)

    if venda.alugado:
        abort(CONFLICT)

    iso_data_fim = get_json_fields(str, 'data_fim')[0]
    data_fim = datetime.fromisoformat(iso_data_fim)
    data_now = datetime.now(timezone.utc)

    if data_fim <= data_now:
        abort(BAD_REQUEST)

    alugel = Alugel(
        venda=venda,
        cliente=Cliente.atual(),
        data=data_now,
        data_fim=data_fim,
    )

    venda.alugado = True
    db.session.add(alugel)
    db.session.commit()

    return jsonify(alugel.dados())


@bp.get('/<int:id>/todos')
def listar_alugel(id:int):
    return jsonify([a.dados() for a in VendaAlugel.query.get_or_404(id).alugeis])


@bp.get('/<int:id>/atual')
def alugel_atual(id:int):
    atual = VendaAlugel.get_or_404(id).alugel_atual()

    if atual == None:
        abort(NOT_FOUND)

    return jsonify(atual.dados())


@bp.post('/<int:id>/devolver')
@admin_required
def devolver_alugel(id:int):
    venda: VendaAlugel = VendaAlugel.query.get_or_404(id)
    
    if venda.alugel_atual() != None:
        abort(CONFLICT)

    venda.alugado = False
    db.session.commit()
    return jsonify(venda.dados())


