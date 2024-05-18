import logging

from src.commands.base_command import BaseCommand
from src.models.db import db_session
from src.models.deporte import Deporte
from src.models.eventos import Eventos


logger = logging.getLogger(__name__)


class ObtenerEventosDeportivos(BaseCommand):
    def __init__(self):
        '''
        Constructor para el comando ObtenerEventosDeportivos
        '''

    def execute(self):
        logger.info('Obteniendo todos los eventos')

        with db_session() as session:
            eventos_bd = session.query(Eventos).all()

            if eventos_bd is None or len(eventos_bd) == 0:
                logger.error("No existen eventos configurados")
                return []

            respuesta = []

            evento: Eventos
            for evento in eventos_bd:
                deporte: Deporte = session.query(Deporte).filter_by(id=evento.id_deporte).first()

                resp_tmp = {
                    'id': evento.id,
                    'nombre': evento.nombre,
                    'descripcion': evento.descripcion,
                    'fecha': evento.fecha,
                    'lugar': evento.lugar,
                    'pais': evento.pais,
                    'deporte': deporte.nombre
                }
                respuesta.append(resp_tmp)

            return respuesta
