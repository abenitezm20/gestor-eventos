import logging

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.db import db_session
from src.models.deporte import Deporte
from src.models.deportista import Deportista
from src.models.evento_deportista import EventoDeportista
from src.models.eventos import Eventos
from src.utils.seguridad_utils import DeportistaToken
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class RegistrarEvento(BaseCommand):
    def __init__(self, usuario_token: DeportistaToken, info: dict):
        '''
        Constructor para el comando RegistrarEvento
        '''
        self.usuario_token: DeportistaToken = usuario_token
        self.info = info

        if str_none_or_empty(info.get('email')):
            logger.error("email no puede ser vacio o nulo")
            raise BadRequest

    def execute(self):
        logger.info('registrando los eventos')

        with db_session() as session:
            deportista: Deportista = session.query(Deportista).filter_by(email=self.usuario_token.email).first()
            
            if deportista is None:
                logger.error("Deportista no encontrado")
                raise BadRequest
            else:
                logger.info(f'Deportista encontrado {deportista.email}')
                eventoDeportista = EventoDeportista(
                    id_deportista=deportista.id,
                    id_evento=self.info.get('id_evento')
                )
                session.add(eventoDeportista)
                session.commit()
                response = {
                    'message': 'success'
                }

            return response
