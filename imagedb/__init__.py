# from you are import s2
import os
from uuid import uuid4

from flask import send_file

from modelo import Imagem


this_folder = os.path.dirname(os.path.abspath(__name__))


def img_exists(name: str):
    return os.path.exists(img_path(name))


def img_path(name: str):
    return os.path.join(this_folder, name)


def new_entry() -> str:
    while True:
        new_id = uuid4().hex
        if not img_exists(new_id):
            return new_id


def get_send_file_response(img: Imagem):
    return send_file(img_path(img.arquivo))