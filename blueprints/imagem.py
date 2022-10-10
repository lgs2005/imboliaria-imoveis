from http.client import NOT_FOUND
from flask import abort, Blueprint
from flask_jwt_extended import jwt_required

from imagedb import get_send_file_response, img_exists


bp = Blueprint('img', __name__, url_prefix='/img')


@bp.post('/<int:id>/add')
@jwt_required()
def rota_adicionar_imagem(id:int):
    # arquivo tbm
    pass


@bp.get('/<int:id>/list')
def rota_listar_imagens(id:int):
    pass


@bp.get('/<string:name>')
def rota_servir_imagem(name:str):
    if img_exists(name):
        abort(NOT_FOUND)
    
    return get_send_file_response(name)