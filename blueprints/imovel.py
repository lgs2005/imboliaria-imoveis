from http.client import BAD_REQUEST
from flask import Blueprint, jsonify, request, abort
from modelo import Imovel, db

from utils import admin_required, get_json_fields


bp = Blueprint('imovel', __name__, url_prefix='/api/imovel')

# curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE0ODUzNiwianRpIjoiNzA0OTcxZmItNDRjMS00MTE1LTlmYjItYjdjYTliNzI2MmNkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY3MTQ4NTM2LCJjc3JmIjoiMWY0ODVhNGQtOTlmYy00ZWEzLTg4YWYtMzAzOWUyNmNlNDc0IiwiZXhwIjoxNjY3MTUyMTM2fQ.IAazJ_7F2qLK9MhC13y2hRssdGgd2urxOsEBa62Ukn0" 127.0.0.1:5000/api/imovel/ -H "Content-Type: application/json" -d "{\"nome\": \"teste\", \"descricao\": \"teste\", \"cidade\": \"canada\", \"bairro\": \"warnow\", \"area\": 5, \"quartos\": 20, \"apartamento\": false, \"quintal\": true}"
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

# curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE0ODUzNiwianRpIjoiNzA0OTcxZmItNDRjMS00MTE1LTlmYjItYjdjYTliNzI2MmNkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY3MTQ4NTM2LCJjc3JmIjoiMWY0ODVhNGQtOTlmYy00ZWEzLTg4YWYtMzAzOWUyNmNlNDc0IiwiZXhwIjoxNjY3MTUyMTM2fQ.IAazJ_7F2qLK9MhC13y2hRssdGgd2urxOsEBa62Ukn0" 127.0.0.1:5000/api/imovel/1 -H "Content-Type: application/json" -d "{\"apartamento\": true}" -X PATCH
@bp.patch('/<int:id>')
@admin_required
def alterar_imovel(id:int):
    imovel: Imovel = Imovel.query.get_or_404(id)
    dados = request.get_json()

    if not isinstance(dados, dict):
        abort(BAD_REQUEST)

    def update(f, t):
        if (f in dados):
            if (type(dados[f]) != t):
                abort(BAD_REQUEST)

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


# curl 127.0.0.1:5000/api/imovel/1
@bp.get('/<int:id>')
def get_imovel(id:int):
    return jsonify(Imovel.query.get_or_404(id).dados())


# curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE0ODUzNiwianRpIjoiNzA0OTcxZmItNDRjMS00MTE1LTlmYjItYjdjYTliNzI2MmNkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY3MTQ4NTM2LCJjc3JmIjoiMWY0ODVhNGQtOTlmYy00ZWEzLTg4YWYtMzAzOWUyNmNlNDc0IiwiZXhwIjoxNjY3MTUyMTM2fQ.IAazJ_7F2qLK9MhC13y2hRssdGgd2urxOsEBa62Ukn0" 127.0.0.1:5000/api/imovel/2 -X DELETE
@bp.delete('/<int:id>')
@admin_required
def delete_imovel(id:int):
    db.session.delete(Imovel.query.get_or_404(id))
    db.session.commit()
    return 'OK', 200