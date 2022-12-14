from http.client import BAD_REQUEST, NOT_FOUND
from flask import abort, Blueprint, request, send_file, jsonify
from werkzeug.utils import secure_filename

import imagedb
from modelo import Imagem, Imovel, db
from utils import admin_required

bp = Blueprint('img', __name__, url_prefix='/img')


@bp.post('/<int:id>/add')
@admin_required
def rota_adicionar_imagem(id:int):
    '''Salva uma imagem e a relaciona com o imóvel do ID especificado'''
    if 'file' not in request.files:
        abort(BAD_REQUEST)

    imovel: Imovel = Imovel.query.get_or_404(id)
    img = request.files['file']
    
    if '.' not in img.filename:
        abort(BAD_REQUEST)

    ext = img.filename.rsplit('.', 1)[1].lower()

    if ext not in ['png', 'jpg', 'jpeg', 'gif']:
        abort(BAD_REQUEST)

    img_name = imagedb.new_entry()
    filename = secure_filename(f'{img_name}.{ext}')

    img.save(imagedb.img_path(filename))

    cadastro = Imagem(
        imovel=imovel,
        arquivo=filename,
    )

    db.session.add(cadastro)
    db.session.commit()

    return filename


@bp.get('/<int:id>/list')
def rota_listar_imagens(id:int):
    '''Lista todas as imagens de um imóvel'''
    imovel: Imovel = Imovel.query.get_or_404(id)

    return jsonify([ img.arquivo for img in imovel.imagens ])


@bp.get('/<string:name>')
def rota_servir_imagem(name:str):
    '''Retorna o arquivo de imagem salvo com este nome'''
    if not imagedb.img_exists(name):
        abort(NOT_FOUND)
    
    return send_file(imagedb.img_path(name))