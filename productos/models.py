from database import db, ma
from marshmallow_enum import EnumField
import enum
from datetime import datetime


# Serializador de objetos
def add_schema(**kwgs):
    def decorator(cls):
        class Meta:
            model = cls
        schema = type("Schema", (ma.SQLAlchemyAutoSchema,), {"Meta": Meta, **kwgs})
        cls.Schema = schema
        return cls
    return decorator


class ProductoCategorias(enum.Enum):
    MODA = 1
    DEPORTE = 2
    SALUD = 3
    BELLEZA = 4
    HERRAMIENTAS = 5
    TECNOLOGIA = 6


@add_schema(categoria=EnumField(ProductoCategorias, by_value=True))
class Producto(db.Model):

    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    categoria = db.Column(db.Enum(ProductoCategorias))
    precio = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    disponible = db.Column(db.BOOLEAN, default=0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, nombre, descripcion, categoria, precio, cantidad, disponible):
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.precio = precio
        self.cantidad = cantidad
        self.disponible = disponible

    def __str__(self):
        return self.nombre
