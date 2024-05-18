import os
import logging
from flask import Blueprint, jsonify, make_response
from src.commands.eventos.obtener_eventos import ObtenerEventosDeportivos
from src.commands.eventos.registrar_eventos import RegistrarEvento
from src.utils.seguridad_utils import DeportistaToken, token_required

VERSION = os.getenv('VERSION')

logger = logging.getLogger(__name__)
eventos_blueprint = Blueprint('eventos', __name__)


@eventos_blueprint.route('/listar', methods=['GET'])
@token_required
def obtener_eventos(usuario_token: DeportistaToken):
    logger.info('Obteniendo todos los eventos deportivos')
    result = ObtenerEventosDeportivos().execute()
    return make_response(jsonify(result), 200)

#El deportista registra un evento
@eventos_blueprint.route('/registrar/<id>', methods=['POST'])
@token_required
def registrar_eventos(usuario_token: DeportistaToken, id: str):
    logger.info(f'Registrar producto para {usuario_token.email}')
    if id is not None:
        info = {
            'email': usuario_token.email,
            'id_evento': id,
        }
        result = RegistrarEvento(usuario_token, info).execute()
    return make_response(jsonify(result), 200)