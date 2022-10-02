from datetime import datetime, timedelta, timezone
from http.client import UNAUTHORIZED

from flask import abort, jsonify, Response, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt, get_jwt_identity, unset_jwt_cookies

from init import app, bcrypt, cliente_atual, jwt
from database import Cliente, db
from utils import get_json_fields, res_erro, res_sucesso


@app.post('/api/cliente/registrar')
def route_registrar_cliente():
    nome, email, cpf, telefone, senha = get_json_fields(
        str, 'nome', 'email', 'cpf', 'telefone', 'senha')
    
    if Cliente.query.filter_by(email=email).first() != None:
        return res_erro('e-mail ja cadastrado')
    
    if Cliente.query.filter_by(cpf=cpf).first() != None:
        return res_erro('cpf ja cadastrado')
    
    if Cliente.query.filter_by(telefone=telefone).first() != None:
        return res_erro('telefone ja cadastrado')
    
    novo_cliente = Cliente(
        nome=nome,
        email=email,
        cpf=cpf,
        telefone=telefone,
        senha=bcrypt.generate_password_hash(senha).decode('UTF-8')
    )

    db.session.add(novo_cliente)
    db.session.commit()

    token = create_access_token(novo_cliente.id)
    resposta = res_sucesso(novo_cliente.dados())

    set_access_cookies(resposta, token)
    return resposta


@app.post('/api/cliente/login')
def rota_logar_cliente():
    email, senha = get_json_fields(str, 'email', 'senha')
    cliente: Cliente = Cliente.query.filter_by(email=email).first_or_404()

    if not bcrypt.check_password_hash(cliente.senha, senha):
        abort(UNAUTHORIZED)
    
    token = create_access_token(cliente.id)
    resposta = jsonify(cliente.dados())
    
    set_access_cookies(resposta, token)
    return resposta


@app.get('/api/cliente')
@jwt_required()
def rota_retornar_cliente():
    return jsonify(cliente_atual.dados())


@app.post('/api/cliente/logout')
def rota_deslogar_cliente():
    response = make_response(None, 200)
    unset_jwt_cookies(response)
    return response


@jwt.user_lookup_loader
def user_lookup_loader(jwt_header, jwt_data):
    return Cliente.query.get(jwt_data['sub'])


@app.after_request
def refresh_jwt_token(response: Response):
    try:
        expire_timestamp = get_jwt()['exp']
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))

        if target_timestamp > expire_timestamp:
            token = create_access_token(get_jwt_identity())
            set_access_cookies(response, token)

        return response
    except (RuntimeError, KeyError):
        return response