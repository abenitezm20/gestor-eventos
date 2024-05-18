from .db import Base
from sqlalchemy import Column, String, DateTime
from src.models.model import Model
from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship
from src.models.model import Model


class Eventos(Model, Base):
    __tablename__ = "eventos"
    id_deporte = Column(UUID(as_uuid=True), ForeignKey('deporte.id'), primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(1000))
    fecha = Column(DateTime)
    lugar = Column(String(50))
    pais = Column(String(50))

    deporte: Mapped['Deporte'] = relationship("Deporte")

    def __init__(self, id_deporte, nombre, descripcion, fecha, lugar, pais):
        Model.__init__(self)
        self.id_deporte = id_deporte
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha = fecha
        self.lugar = lugar
        self.pais = pais