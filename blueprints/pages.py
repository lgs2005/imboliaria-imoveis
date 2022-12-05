from flask import Blueprint, render_template, request, g
from flask_jwt_extended import jwt_required

from modelo import Imovel, Cliente
from utils import admin_required


bp = Blueprint('paginas', __name__)


@bp.get('/')
def page_default():
    return f'<a href="http://{request.host}/inicio">imoveis</a> (Lucas e Amadeus)'


@bp.get('/inicio')
def page_index():
    return render_template('inicio.html')


@bp.get('/imovel/<int:id>')
def page_imovel(id:int):
    return render_template('imovel.html', imovel=Imovel.query.get_or_404(id))


@bp.get('/editar')
@admin_required
def page_cadastrar_imovel():
    return render_template('editar_imovel.html')


@bp.get('/editar/<int:id>')
@admin_required
def page_editar_imovel(id:int):
    return render_template('editar_imovel.html', imovel=Imovel.query.get_or_404(id))


@bp.get('/busca')
def page_busca_imoveis():
    return render_template('busca.html')


@bp.before_request
@jwt_required(optional=True)
def add_admin_to_context():
    try:
        cliente = Cliente.atual()
        g.user = cliente
        g.admin = cliente.admin
    except Exception:
        g.admin = False