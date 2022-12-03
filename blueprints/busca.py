from flask import Blueprint, jsonify
from flask_sqlalchemy.pagination import Pagination

from modelo import Imovel, Venda
from utils import get_arg_fields, get_json_fields


bp = Blueprint('busca', __name__, url_prefix='/api/busca')


# curl 127.0.0.1:5000/api/busca/ -X GET -H "Content-Type: application/json" -d "{\"apt\": 0, \"quintal\": 0, \"preco_max\": 500, \"cidade\": \"canada\", \"bairro\": \"any\", \"tamanho_min\": 0, \"tamanho_max\": 5000, \"quartos_min\": 0}"
@bp.get('/')
def rota_busca():    
    '''Busca por vendas utilizando filtros
    Parâmetros:
        apt: int - 0 para false, qualquer outro para true
        quintal: int - 0 para false, qualquer outro para true
        preco_max: int
        cidade: str - 'any' para qualquer cidade
        bairro: str - 'any' para qualquer bairro
        quartos_min: int
    '''
    apt, quintal = get_arg_fields(bool, 'apt', 'quintal')
    preco_max = get_arg_fields(int, 'preco_max')
    cidade, bairro = get_arg_fields(str, 'cidade', 'bairro')
    quartos_min = get_arg_fields(int, 'quartos_min')

    query = Venda.query\
        .filter(Venda.tipo != 'realizada')\
        .filter(Venda.preco <= preco_max)\
        .join(Venda.imovel)

    if apt:
        query = query.filter(Imovel.apartamento == True)
    
    if quintal:
        query = query.filter(Imovel.quintal == True)

    if cidade != 'any':
        query = query.filter(Imovel.cidade == cidade)
    
    if bairro != 'any':
        query = query.filter(Imovel.bairro == bairro)

    query = query.filter(Imovel.quartos >= quartos_min)
    vendas: Pagination = query.paginate(max_per_page=20)
    
    response = {
        'total': vendas.pages,
        'dados': [
            v.dados()
            for v in vendas.items
        ]
    }

    return jsonify(response)
