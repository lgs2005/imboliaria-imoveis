from flask import Blueprint, render_template


bp = Blueprint('paginas', __name__)


@bp.get('/')
def page_default():
    return render_template('subtituto.html')


@bp.get('/contato')
def page_contato():
    return render_template('contato.html')


@bp.get('/sobre')
def page_sobre():
    return render_template('sobre.html')


@bp.get('/teste')
def page_teste():
    return render_template('testing.html')