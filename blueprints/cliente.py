from datetime import datetime, timedelta, timezone
from http.client import UNAUTHORIZED

from flask import abort, jsonify, Response, make_response, Blueprint
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt, get_jwt_identity, unset_jwt_cookies, JWTManager
from flask_bcrypt import generate_password_hash, check_password_hash

from modelo import Cliente, db
from utils import get_json_fields, res_erro, res_sucesso


bp = Blueprint('cliente', __name__, url_prefix='/api/cliente')


@bp.post('/registrar')
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
        senha=generate_password_hash(senha).decode('UTF-8')
    )

    db.session.add(novo_cliente)
    db.session.commit()

    token = create_access_token(novo_cliente.id)
    resposta = res_sucesso(novo_cliente.dados())

    set_access_cookies(resposta, token)
    return resposta


@bp.post('/login')
def rota_logar_cliente():
    email, senha = get_json_fields(str, 'email', 'senha')
    cliente: Cliente = Cliente.query.filter_by(email=email).first_or_404()

    if not check_password_hash(cliente.senha, senha):
        abort(UNAUTHORIZED)
    
    token = create_access_token(cliente.id)
    resposta = jsonify(cliente.dados())
    
    set_access_cookies(resposta, token)
    return resposta


@bp.get('/')
@jwt_required()
def rota_retornar_cliente():
    return jsonify(Cliente.atual().dados())


@bp.post('/logout')
def rota_deslogar_cliente():
    response = make_response(None, 200)
    unset_jwt_cookies(response)
    return response

jwt = JWTManager()

@jwt.user_lookup_loader
def user_lookup_loader(jwt_header, jwt_data):
    return Cliente.query.get(jwt_data['sub'])


@bp.after_app_request
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