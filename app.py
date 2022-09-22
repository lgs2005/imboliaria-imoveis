from init import app, db

import modelos

@app.route('/', methods=['GET'])
def rota_inicial():
    return 'ok'


if __name__ == '__main__':
    db.create_all()
