from flask import Blueprint
from modelos import Usuario

cadastro = Blueprint('usuario')

@cadastro.post('/registrar')
def route_registrar_usuario():
	usuario = Usuario(
		id=0,
		cpf='',
	)

	usuario.id