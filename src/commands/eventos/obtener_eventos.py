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


class ObtenerEventosDeportivos(BaseCommand):
    def __init__(self, usuario_token: DeportistaToken):
        '''
        Constructor para el comando ObtenerEventosDeportivos
        '''
        self.usuario_token: DeportistaToken = usuario_token

        if str_none_or_empty(self.usuario_token.email):
            logger.error("email no puede ser vacio o nulo")
            raise BadRequest

    def execute(self):
        logger.info('Obteniendo todos los eventos')

        with db_session() as session:
            
            deportista: Deportista = session.query(Deportista).filter_by(email=self.usuario_token.email).first()
            
            if deportista is None:
                logger.error("Deportista no encontrado")
                raise BadRequest
            else:
                eventos_bd = session.query(Eventos).all()

                if eventos_bd is None or len(eventos_bd) == 0:
                    logger.error("No existen eventos configurados")
                    return []

                respuesta = []

                eventos_agendados_bd = session.query(EventoDeportista).filter_by(id_deportista=deportista.id).all()
                evento: Eventos
                for evento in eventos_bd:
                    deporte: Deporte = session.query(Deporte).filter_by(id=evento.id_deporte).first()

                    resp_tmp = {
                        'id': evento.id,
                        'nombre': evento.nombre,
                        'descripcion': evento.descripcion,
                        'fecha': evento.fecha.strftime("%Y-%m-%dT%H:%M:%S"),
                        'lugar': evento.lugar,
                        'pais': evento.pais,
                        'deporte': deporte.nombre,
                        'registrado': 'no'
                    }


                    for evento_agendado in eventos_agendados_bd:
                        if evento_agendado.id_evento == evento.id:
                            resp_tmp['registrado'] = 'si'
                            break
                    respuesta.append(resp_tmp)

                return respuesta


class ObtenerEventosAgendados(BaseCommand):
    def __init__(self, usuario_token: DeportistaToken):
        '''
        Constructor para el comando ObtenerEventosDeportivos
        '''
        self.usuario_token: DeportistaToken = usuario_token

        if str_none_or_empty(self.usuario_token.email):
            logger.error("email no puede ser vacio o nulo")
            raise BadRequest

    def execute(self):
        logger.info('Obteniendo todos los eventos')

        with db_session() as session:
            deportista: Deportista = session.query(Deportista).filter_by(email=self.usuario_token.email).first()
            
            if deportista is None:
                logger.error("Deportista no encontrado")
                raise BadRequest
            else:
                logger.info(f'Deportista encontrado {deportista.email}')
            
                eventos_agendados_bd = session.query(EventoDeportista).filter_by(id_deportista=deportista.id).all()

                if eventos_agendados_bd is None or len(eventos_agendados_bd) == 0:
                    logger.error("No existen eventos agendados")
                    return []

                respuesta = []

                evento_agendado: EventoDeportista
                for evento_agendado in eventos_agendados_bd:
                    
                    #se generan los eventos
                    evento: Eventos = session.query(Eventos).filter_by(id=evento_agendado.id_evento).first()
                    
                    if evento is None:
                        logger.error("Evento no encontrado")
                        raise BadRequest
                    else:
                        deporte: Deporte = session.query(Deporte).filter_by(id=evento.id_deporte).first()

                        resp_tmp = {
                            'id': evento.id,
                            'nombre': evento.nombre,
                            'descripcion': evento.descripcion,
                            'fecha': evento.fecha,
                            'lugar': evento.lugar,
                            'pais': evento.pais,
                            'deporte': deporte.nombre,
                            'deportista': deportista.email
                        }
                        respuesta.append(resp_tmp)

                return respuesta
