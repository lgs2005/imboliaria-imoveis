from http.client import BAD_REQUEST
from operator import itemgetter
from typing import Any, TypeVar

from flask import abort, request, jsonify

FieldsType = TypeVar('FieldsType')


def get_json_fields(typing: type[FieldsType], *fields: str) -> tuple[FieldsType, ...]:
    json = request.get_json()

    if not isinstance(json, dict):
        abort(BAD_REQUEST)

    for field in fields:
        if (field not in json) or (type(json[field]) != typing):
            abort(BAD_REQUEST)

    return itemgetter(*fields)(json)


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

