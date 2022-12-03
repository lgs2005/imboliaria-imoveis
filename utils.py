import functools
import json
from http.client import BAD_REQUEST, UNAUTHORIZED
from operator import itemgetter
from typing import Any, TypeVar

from flask import abort, request, jsonify
from flask_jwt_extended import jwt_required

from modelo import Cliente

FieldsType = TypeVar('FieldsType')


def get_json_fields(typing: 'type[FieldsType]', *fields: str) -> 'tuple[FieldsType, ...]':
    json = request.get_json()

    if not isinstance(json, dict):
        abort(BAD_REQUEST)

    for field in fields:
        if (field not in json) or (type(json[field]) != typing):
            abort(BAD_REQUEST)

    return itemgetter(*fields)(json)

def get_arg_fields(typing: 'type[FieldsType]', *fields: str) -> 'tuple[FieldsType, ...]':
    for field in fields:
        if (field not in request.args):
            abort(BAD_REQUEST)

    if typing == str:
        return itemgetter(*fields)(request.args)
    else:
        data = {}
     
        for field in fields:
            try:
                data[field] = json.loads(request.args[field])
                if type(data[field]) != typing:
                    abort(BAD_REQUEST)
            except ValueError:
                abort(BAD_REQUEST)

        return itemgetter(*fields)(data)

def res_erro(mensagem: str):
    return jsonify({
        'ok': False,
        'erro': mensagem
    })


def res_sucesso(dados: Any):
    return jsonify({
        'ok': True,
        'dados': dados
    })

def admin_required(f):
    @jwt_required()
    @functools.wraps(f)
    def wrapper(*args, **kwargs):

        if not Cliente.atual().admin:
            abort(UNAUTHORIZED)

        return f(*args, **kwargs)

    return wrapper