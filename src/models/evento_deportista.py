from .db import Base
from sqlalchemy import Column, String, DateTime
from src.models.model import Model
from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship
from src.models.model import Model


class EventoDeportista(Model, Base):
    __tablename__ = "evento_deportista"
    id_evento = Column(UUID(as_uuid=True), ForeignKey('eventos.id'), primary_key=True)
    id_deportista = Column(UUID(as_uuid=True), ForeignKey('deportista.id'), primary_key=True)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)

    deportista: Mapped['Deportista'] = relationship("Deportista")
    eventos: Mapped['Eventos'] = relationship("Eventos")

    def __init__(self, id_evento, id_deportista):
        Model.__init__(self)
        self.id_evento = id_evento
        self.id_deportista = id_deportista