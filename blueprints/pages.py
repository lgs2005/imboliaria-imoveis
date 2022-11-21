from flask import Blueprint, render_template, request
from modelo import Imovel


bp = Blueprint('paginas', __name__)


@bp.get('/')
def page_default():
    return f'<a href="http://{request.host}/index">imoveis</a> (Lucas e Amadeus)'


@bp.get('/index')
def page_index():
    return render_template('index.html')


@bp.get('/contato')
def page_contato():
    return render_template('contato.html')


@bp.get('/sobre')
def page_sobre():
    return render_template('sobre.html')


@bp.get('/teste')
def page_teste():
    return render_template('testing.html')


@bp.get('/imovel/<int:id>')
def page_imovel(id:int):
    return render_template('imovel.html', imovel=Imovel.query.get_or_404(id))