import os
from http.client import BAD_REQUEST, NOT_FOUND
from flask import abort, Blueprint, request, send_file, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

import imagedb
from modelo import Imagem, Imovel, db

bp = Blueprint('img', __name__, url_prefix='/img')


@bp.post('/add')
#@jwt_required()
def rota_adicionar_imagem():
    if 'file' not in request.files:
        abort(BAD_REQUEST)

    #imovel: Imovel = Imovel.query.get_or_404(id)
    img = request.files['file']
    img_name = imagedb.new_entry()

    ext = img.filename.split('.', maxsplit=1)[1]
    filename = secure_filename(f'{img_name}.{ext}')

    img.save(imagedb.img_path(filename))

    # cadastro = Imagem(
    #     imovel=imovel,
    #     arquivo=img_name,
    # )

    # db.session.add(cadastro)
    # db.session.commit()

    return img_name


@bp.get('/<int:id>/list')
def rota_listar_imagens(id:int):
    imovel: Imovel = Imovel.query.get_or_404(id)

    return jsonify([ img.arquivo for img in imovel.imagens ])


@bp.get('/<string:name>')
def rota_servir_imagem(name:str):
    if not imagedb.img_exists(name):
        abort(NOT_FOUND)
    
    return send_file(imagedb.img_path(name))