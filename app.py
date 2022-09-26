from init import app, db
from flask import render_template

import modelos


@app.route('/', methods=['GET'])
def rota_inicial():
    return render_template('index.html')


@app.route('/sobre', methods=['GET'])
def rota_pagina_sobre():
    return render_template('sobre.html')


@app.route('/contato', methods=['GET'])
def rota_pagina_contato():
    return render_template('contato.html')


# aiosofiajsoifjasoifjasioj

if __name__ == '__main__':
    db.create_all()
