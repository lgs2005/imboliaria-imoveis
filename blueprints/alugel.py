from datetime import datetime, timezone
from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND
from flask import Blueprint, abort, jsonify
from flask_jwt_extended import jwt_required

from modelo import Alugel, Cliente, VendaAlugel, db
from utils import admin_required, get_json_fields

bp = Blueprint('alugel', __name__, url_prefix='/api/alugel')


# curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE0ODUzNiwianRpIjoiNzA0OTcxZmItNDRjMS00MTE1LTlmYjItYjdjYTliNzI2MmNkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY3MTQ4NTM2LCJjc3JmIjoiMWY0ODVhNGQtOTlmYy00ZWEzLTg4YWYtMzAzOWUyNmNlNDc0IiwiZXhwIjoxNjY3MTUyMTM2fQ.IAazJ_7F2qLK9MhC13y2hRssdGgd2urxOsEBa62Ukn0" 127.0.0.1:5000/api/alugel/3/alugar -H "Content-Type: application/json" -d "{\"data_fim\": \"2078-08-01T03:00:00.000Z\"}
@bp.post('/<int:id>/alugar')
@jwt_required()
def adicionar_alugel(id:int):
    '''Faz o alugel de um imóvel que está sendo vendido em uma venda do tipo 'alugel'
    ID no URL = ID da venda
    Parâmetros:
        data_fim: str - uma data no formato ISO
    '''
    venda: VendaAlugel = VendaAlugel.query.get_or_404(id)

    if venda.alugado:
        abort(CONFLICT)

    iso_data_fim = get_json_fields(str, 'data_fim')

    try:
        data_fim = datetime.fromisoformat(iso_data_fim)
    except ValueError:
        abort(BAD_REQUEST)
    
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


# curl 127.0.0.1:5000/api/alugel/3/todos
@bp.get('/<int:id>/todos')
def listar_alugel(id:int):
    '''Lista todos os alugeis de uma venda tipo 'alugel' '''
    return jsonify([a.dados() for a in VendaAlugel.query.get_or_404(id).alugeis])

# curl 127.0.0.1:5000/api/alugel/3/atual
@bp.get('/<int:id>/atual')
def alugel_atual(id:int):
    '''Retorna o alugel atual de uma venda tipo 'alugel' '''
    atual = VendaAlugel.query.get_or_404(id).alugel_atual()

    if atual == None:
        abort(NOT_FOUND)

    return jsonify(atual.dados())

# curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE0ODUzNiwianRpIjoiNzA0OTcxZmItNDRjMS00MTE1LTlmYjItYjdjYTliNzI2MmNkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY3MTQ4NTM2LCJjc3JmIjoiMWY0ODVhNGQtOTlmYy00ZWEzLTg4YWYtMzAzOWUyNmNlNDc0IiwiZXhwIjoxNjY3MTUyMTM2fQ.IAazJ_7F2qLK9MhC13y2hRssdGgd2urxOsEBa62Ukn0" 127.0.0.1:5000/api/alugel/3/devolver -X POST
# este comando ira funcionar após 3 da manha de 1 de agosto de 2078 no horario de brasilia
# (altere as datas para testar)
@bp.post('/<int:id>/devolver')
@admin_required
def devolver_alugel(id:int):
    '''Marca uma venda tipo 'alugel' como não alugada se o tempo do último alugel já passou'''
    venda: VendaAlugel = VendaAlugel.query.get_or_404(id)
    
    if venda.alugel_atual() != None:
        abort(CONFLICT)

    venda.alugado = False
    db.session.commit()
    return jsonify(venda.dados())


