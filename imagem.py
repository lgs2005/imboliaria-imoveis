from http.client import NOT_FOUND
from flask import abort
from flask_jwt_extended import jwt_required

from init import app
from imagedb import new_entry, get_send_file_response, img_exists
from utils import get_json_fields


@app.post('/api/img/<int:id>/add')
@jwt_required()
def rota_adicionar_imagem(id:int):
    # arquivo tbm
    pass


@app.get('/api/img/<int:id>/list')
def rota_listar_imagens(id:int):
    pass


@app.get('/img/<str:name>')
def rota_servir_imagem(name:str):
    if img_exists(name):
        abort(NOT_FOUND)
    
    return get_send_file_response(name)