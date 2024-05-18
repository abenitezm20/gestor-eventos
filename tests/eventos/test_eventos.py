import json
import pytest
import logging
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.deportista import Deportista, GeneroEnum, TipoIdentificacionEnum

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

                response = test_client.get('/gestor-eventos/eventos/listar', headers=headers, follow_redirects=True)

                assert response.status_code == 200

                session.delete(deportista_random)
                session.commit()
