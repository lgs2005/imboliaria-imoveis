from http.client import BAD_REQUEST
from flask import Blueprint, jsonify, request, abort
from modelo import Imovel, db

from utils import admin_required, get_json_fields


bp = Blueprint('imovel', __name__, url_prefix='/api/imovel')


@bp.post('/')
@admin_required
def cadastro_imovel():
    nome, descricao, cidade, bairro = get_json_fields(str, 'nome', 'descricao', 'cidade', 'bairro')
    area, quartos = get_json_fields(int, 'area', 'quartos')
    apartamento, quintal = get_json_fields(bool, 'apartamento', 'quintal')
    
    imovel = Imovel(nome=nome, descricao=descricao, cidade=cidade, bairro=bairro,
        area=area, quartos=quartos, apartamento=apartamento, quintal=quintal)

    db.session.add(imovel)
    db.session.commit()

    return jsonify(imovel.dados())


@bp.patch('/<int:id>')
@admin_required
def alterar_imovel():
    imovel: Imovel = Imovel.query.get_or_404(id)
    dados = request.get_json()

    if not isinstance(dados, dict):
        abort(BAD_REQUEST)

    def update(f, t):
        if (f in dados) and (type(dados[f]) == t):
            imovel.__setattr__(f, dados[f])

    update('nome', str)
    update('descricao', str)
    update('cidade', str)
    update('bairro', str)
    update('area', int)
    update('quartos', int)
    update('apartamento', bool)
    update('quintal', bool)

    db.session.commit()
    return jsonify(imovel.dados())


@bp.get('/<int:id>')
def get_imovel(id:int):
    return jsonify(Imovel.query.get_or_404(id).dados())


@bp.delete('/<int:id>')
@admin_required
def delete_imovel(id:int):
    db.session.delete(Imovel.query.get_or_404(id))
    db.session.commit()
    return 'OK', 200