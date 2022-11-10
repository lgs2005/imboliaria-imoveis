from datetime import datetime, timedelta, timezone
from http.client import UNAUTHORIZED

from flask import abort, jsonify, Response, make_response, Blueprint
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt, get_jwt_identity, unset_jwt_cookies, JWTManager
from flask_bcrypt import generate_password_hash, check_password_hash

from modelo import Cliente, db
from utils import get_json_fields, res_erro, res_sucesso


bp = Blueprint('cliente', __name__, url_prefix='/api/cliente')


# curl -H "Content-Type: application/json" -d "{\"nome\": \"teste\", \"email\": \"email123@hotmail.com\", \"cpf\": \"12345678913\", \"telefone\": \"047158963289\", \"senha\": \"teste\"}" 127.0.0.1:5000/api/cliente/registrar
@bp.post('/registrar')
def route_registrar_cliente():
    '''Registra um novo cliente.
    Parâmetros:
        nome: str
        email: str
        cpf: str
        telefone: str
        senha: str
    '''
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


# curl -H "Content-Type: application/json" -d "{\"email\": \"email123@hotmail.com\", \"senha\": \"teste\"}" 127.0.0.1:5000/api/cliente/login
# usar -v para ver os headers
# jwt no header 'Set-Cookie'
# Set-Cookie: access_token_cookie=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE0ODUzNiwianRpIjoiNzA0OTcxZmItNDRjMS00MTE1LTlmYjItYjdjYTliNzI2MmNkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY3MTQ4NTM2LCJjc3JmIjoiMWY0ODVhNGQtOTlmYy00ZWEzLTg4YWYtMzAzOWUyNmNlNDc0IiwiZXhwIjoxNjY3MTUyMTM2fQ.IAazJ_7F2qLK9MhC13y2hRssdGgd2urxOsEBa62Ukn0; HttpOnly; Path=/
# jwt: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE0ODUzNiwianRpIjoiNzA0OTcxZmItNDRjMS00MTE1LTlmYjItYjdjYTliNzI2MmNkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY3MTQ4NTM2LCJjc3JmIjoiMWY0ODVhNGQtOTlmYy00ZWEzLTg4YWYtMzAzOWUyNmNlNDc0IiwiZXhwIjoxNjY3MTUyMTM2fQ.IAazJ_7F2qLK9MhC13y2hRssdGgd2urxOsEBa62Ukn0
@bp.post('/login')
def rota_logar_cliente():
    '''Faz login de um criente já registrado
    Parâmetos:
        email: str
        senha: str
    '''
    email, senha = get_json_fields(str, 'email', 'senha')
    cliente: Cliente = Cliente.query.filter_by(email=email).first_or_404()

    if not check_password_hash(cliente.senha, senha):
        abort(UNAUTHORIZED)
    
    token = create_access_token(cliente.id)
    resposta = jsonify(cliente.dados())
    
    set_access_cookies(resposta, token)
    return resposta


# curl -H "Authorization: Bearer (JWT)" 127.0.0.1:5000/api/cliente/
@bp.get('/')
@jwt_required()
def rota_retornar_cliente():
    '''Retorna os dados do cliente atual'''
    return jsonify(Cliente.atual().dados())


# curl 127.0.0.1:5000/api/cliente/1
@bp.get('/<int:id>')
def rota_dados_cliente(id:int):
    '''Retorna os dados de um cliente qualquer'''
    return jsonify(Cliente.query.get_or_404(id).dados())


# nem funciona pelo curl, apenas serve para uso em browsers
@bp.post('/logout')
@jwt_required()
def rota_deslogar_cliente():
    '''Remove os cookies de login em browsers'''
    response = make_response(None, 200)
    unset_jwt_cookies(response)
    return response


# curl -H "Authorization: Bearer (jwt)" 127.0.0.1:5000/api/cliente/toggle-admin -X POST
@bp.post('/toggle-admin')
@jwt_required()
def rota_toggle_admin():
    '''Torna o cliente admin ou não
    APENAS PARA TESTES!
    '''
    cliente = Cliente.atual()
    cliente.admin = not cliente.admin
    db.session.commit()
    return f'admin: {cliente.admin}', 200



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