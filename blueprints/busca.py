from flask import Blueprint, jsonify

from modelo import Imovel, Venda
from utils import get_json_fields


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
        tamanho_min: int
        tamanho_max: int
        quartos_min: int
    '''
    apt, quintal = get_json_fields(int, 'apt', 'quintal')
    preco_max = get_json_fields(int, 'preco_max')
    cidade, bairro = get_json_fields(str, 'cidade', 'bairro')
    tamanho_min, tamanho_max = get_json_fields(int, 'tamanho_min', 'tamanho_max')
    quartos_min = get_json_fields(int, 'quartos_min')

    query = Venda.query\
        .filter(Venda.tipo != 'realizada')\
        .filter(Venda.preco <= preco_max)\
        .join(Venda.imovel)

    if apt != 0:
        query = query.filter(Imovel.apartamento  == (apt == 1))
    
    if quintal != 0:
        query = query.filter(Imovel.quintal == (quintal == 1))

    if cidade != 'any':
        query = query.filter_by(cidade=cidade)
    
    if bairro != 'any':
        query = query.filter_by(bairro=bairro)

    query = query.filter(Imovel.area >= tamanho_min)
    query = query.filter(Imovel.area <= tamanho_max)
    query = query.filter(Imovel.quartos >= quartos_min)

    vendas = query.all()
    
    return jsonify([v.dados() for v in vendas])
