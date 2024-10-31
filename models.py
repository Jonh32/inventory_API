from sqlalchemy import Column, Integer, Date, Boolean, String, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Inventario(Base):
    __tablename__ = 'inventario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    estatus = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Inventario(id={self.id}, fecha={self.fecha}, estatus={self.estatus})>"
    
class Lugar(Base):
    __tablename__ = 'lugar'

    id = Column(Integer, primary_key=True, autoincrement=True)
    edificio = Column(String(100), nullable=False)
    area = Column(String(200), nullable=False)

    def __repr__(self):
        return f"<Lugar(id={self.id}, edificio={self.edificio}, area={self.area})>"

class Bien(Base):
    __tablename__ = 'bien'

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_activo = Column(Integer, nullable=False)
    subnumero = Column(Integer, nullable=False)
    descripcion = Column(String(200), nullable=False)
    material = Column(String(100), nullable=False)
    color = Column(String(100), nullable=False)
    marca = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    serie = Column(String(100), nullable=False)
    estado = Column(String(100), nullable=False)
    id_lugar = Column(Integer, ForeignKey('lugar.id'), nullable=False, default=1)
    imagen = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Bien(id={self.id}, numero_activo={self.numero_activo}, descripcion={self.descripcion}, id_lugar={self.id_lugar})>"
    
class InventarioBien(Base):
    __tablename__ = 'inventario_bien'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_inventario = Column(Integer, ForeignKey('inventario.id'), nullable=False)
    id_bien = Column(Integer, ForeignKey('bien.id'), nullable=False)
    localizado = Column(Integer, nullable=False, default=False)

    def __repr__(self):
        return f"<InventarioBien(id={self.id}, id_inventario={self.id_inventario}, id_bien={self.id_bien}, localizado={self.localizado})>"