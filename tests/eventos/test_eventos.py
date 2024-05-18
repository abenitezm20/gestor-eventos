import json
import pytest
import logging
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.deporte import Deporte
from src.models.deportista import Deportista, GeneroEnum, TipoIdentificacionEnum
from src.models.evento_deportista import EventoDeportista
from src.models.eventos import Eventos
from sqlalchemy import delete

fake = Faker()
logger = logging.getLogger(__name__)

class TestEventos():

    @patch('requests.post')
    def test_listarEventos(self, mock_post):
        with db_session() as session:
            with app.test_client() as test_client:

                # Crear Deportista
                info_deportista = {
                    'nombre': fake.name(),
                    'apellido': fake.name(),
                    'tipo_identificacion': fake.random_element(elements=(
                        tipo_identificacion.value for tipo_identificacion in TipoIdentificacionEnum)),
                    'numero_identificacion': fake.random_int(min=1000000, max=999999999),
                    'email': fake.email(),
                    'genero': fake.random_element(elements=(genero.value for genero in GeneroEnum)),
                    'edad': fake.random_int(min=18, max=100),
                    'peso': fake.pyfloat(3, 1, positive=True),
                    'altura': fake.random_int(min=140, max=200),
                    'pais_nacimiento': fake.country(),
                    'ciudad_nacimiento': fake.city(),
                    'pais_residencia': fake.country(),
                    'ciudad_residencia': fake.city(),
                    'antiguedad_residencia': fake.random_int(min=0, max=10),
                    'contrasena': fake.password(),
                    'deportes' : [ {"atletismo": 1}, {"ciclismo": 0}]
                }
                deportista_random = Deportista(**info_deportista)
                session.add(deportista_random)
                session.commit()

                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    'token_valido': True, 
                    'email': deportista_random.email,
                    'tipo_usuario': 'deportista',
                    'subscripcion': "Premium",
                    }
                mock_post.return_value = mock_response

                headers = {'Authorization': 'Bearer 123'}
                
                info_deporte = {
                    'nombre': fake.name(),
                }
                deporte_random = Deporte(**info_deporte)
                session.add(deporte_random)
                session.commit()
                deporte_id = deporte_random.id
                
                info_evento = {
                    'id_deporte': deporte_id,
                    'nombre': fake.name(),
                    'descripcion': fake.text(),
                    'fecha': fake.date_time(),
                    'pais': fake.country(),
                    'lugar': fake.city()
                }
                evento_random = Eventos(**info_evento)
                session.add(evento_random)
                session.commit()

                response = test_client.get('/gestor-eventos/eventos/listar', headers=headers, follow_redirects=True)

                assert response.status_code == 200

                session.delete(evento_random)
                session.delete(deporte_random)
                session.delete(deportista_random)
                session.commit()

    @patch('requests.post')
    def test_RegistrarEventos(self, mock_post):
        with db_session() as session:
            with app.test_client() as test_client:

                # Crear Deportista
                info_deportista = {
                    'nombre': fake.name(),
                    'apellido': fake.name(),
                    'tipo_identificacion': fake.random_element(elements=(
                        tipo_identificacion.value for tipo_identificacion in TipoIdentificacionEnum)),
                    'numero_identificacion': fake.random_int(min=1000000, max=999999999),
                    'email': fake.email(),
                    'genero': fake.random_element(elements=(genero.value for genero in GeneroEnum)),
                    'edad': fake.random_int(min=18, max=100),
                    'peso': fake.pyfloat(3, 1, positive=True),
                    'altura': fake.random_int(min=140, max=200),
                    'pais_nacimiento': fake.country(),
                    'ciudad_nacimiento': fake.city(),
                    'pais_residencia': fake.country(),
                    'ciudad_residencia': fake.city(),
                    'antiguedad_residencia': fake.random_int(min=0, max=10),
                    'contrasena': fake.password(),
                    'deportes' : [ {"atletismo": 1}, {"ciclismo": 0}]
                }
                deportista_random = Deportista(**info_deportista)
                session.add(deportista_random)
                session.commit()

                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    'token_valido': True, 
                    'email': deportista_random.email,
                    'tipo_usuario': 'deportista',
                    'subscripcion': "Premium",
                    }
                mock_post.return_value = mock_response

                headers = {'Authorization': 'Bearer 123'}
                
                info_deporte = {
                    'nombre': fake.name(),
                }
                deporte_random = Deporte(**info_deporte)
                session.add(deporte_random)
                session.commit()
                deporte_id = deporte_random.id
                
                info_evento = {
                    'id_deporte': deporte_id,
                    'nombre': fake.name(),
                    'descripcion': fake.text(),
                    'fecha': fake.date_time(),
                    'pais': fake.country(),
                    'lugar': fake.city()
                }
                evento_random = Eventos(**info_evento)
                session.add(evento_random)
                session.commit()
                evento_id = evento_random.id

                response = test_client.post('/gestor-eventos/eventos/registrar/'+str(evento_id), headers=headers, follow_redirects=True)
                assert response.status_code == 200

                
                delEventoDeportista = delete(EventoDeportista).where(EventoDeportista.id_evento == evento_id)
                session.execute(delEventoDeportista)
                session.commit()

                session.delete(evento_random)
                session.delete(deporte_random)
                session.delete(deportista_random)
                session.commit()


    @patch('requests.post')
    def test_listarEventosRegistrados(self, mock_post):
        with db_session() as session:
            with app.test_client() as test_client:

                # Crear Deportista
                info_deportista = {
                    'nombre': fake.name(),
                    'apellido': fake.name(),
                    'tipo_identificacion': fake.random_element(elements=(
                        tipo_identificacion.value for tipo_identificacion in TipoIdentificacionEnum)),
                    'numero_identificacion': fake.random_int(min=1000000, max=999999999),
                    'email': fake.email(),
                    'genero': fake.random_element(elements=(genero.value for genero in GeneroEnum)),
                    'edad': fake.random_int(min=18, max=100),
                    'peso': fake.pyfloat(3, 1, positive=True),
                    'altura': fake.random_int(min=140, max=200),
                    'pais_nacimiento': fake.country(),
                    'ciudad_nacimiento': fake.city(),
                    'pais_residencia': fake.country(),
                    'ciudad_residencia': fake.city(),
                    'antiguedad_residencia': fake.random_int(min=0, max=10),
                    'contrasena': fake.password(),
                    'deportes' : [ {"atletismo": 1}, {"ciclismo": 0}]
                }
                deportista_random = Deportista(**info_deportista)
                session.add(deportista_random)
                session.commit()

                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    'token_valido': True, 
                    'email': deportista_random.email,
                    'tipo_usuario': 'deportista',
                    'subscripcion': "Premium",
                    }
                mock_post.return_value = mock_response

                headers = {'Authorization': 'Bearer 123'}
                
                info_deporte = {
                    'nombre': fake.name(),
                }
                deporte_random = Deporte(**info_deporte)
                session.add(deporte_random)
                session.commit()
                deporte_id = deporte_random.id
                
                #se crea el evento
                info_evento = {
                    'id_deporte': deporte_id,
                    'nombre': fake.name(),
                    'descripcion': fake.text(),
                    'fecha': fake.date_time(),
                    'pais': fake.country(),
                    'lugar': fake.city()
                }
                evento_random = Eventos(**info_evento)
                session.add(evento_random)
                session.commit()
                evento_id = evento_random.id

                #Se asocia el evento al deportista
                info_evento_deportista = {
                    'id_deportista': deportista_random.id,
                    'id_evento': evento_id
                }
                evento_deportista_random = EventoDeportista(**info_evento_deportista)
                session.add(evento_deportista_random)
                session.commit()

                response = test_client.get('/gestor-eventos/eventos/agendados', headers=headers, follow_redirects=True)
                assert response.status_code == 200

                session.delete(evento_deportista_random)
                session.delete(evento_random)
                session.delete(deporte_random)
                session.delete(deportista_random)
                session.commit()
