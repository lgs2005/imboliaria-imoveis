from flask import Blueprint, jsonify, request
from modelo import Imovel, db

from utils import admin_required, get_json_fields


bp = Blueprint('imovel', url_prefix='/api/imovel')

@bp.post('/')
@admin_required()
def cadastro_imovel():
    # validar
    get_json_fields(str, 'nome', 'descricao', 'cidade', 'bairro')
    get_json_fields(int, 'area', 'quartos')
    get_json_fields(bool, 'apartamento', 'quintal')
    
    imovel = Imovel(**request.get_json())

    db.session.add(imovel)
    db.session.commit()

    return jsonify(imovel.dados())

@bp.get('/<int:id>')
def get_imovel(id:int):
    return jsonify(Imovel.query.get_or_404(id).dados())

@bp.delete('/<int:id>')
@admin_required()
def delete_imovel(id:int):
    db.session.delete(Imovel.query.get_or_404(id))
    db.session.commit()

    return 'OK', 200