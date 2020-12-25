from database import db, ma
import enum


class ProductoCategorias(enum.Enum):
    MODA = 1
    DEPORTE = 2
    SALUD = 3
    BELLEZA = 4
    HERRAMIENTAS = 5
    TECNOLOGIA = 6


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    categoria = db.Column(db.Enum(ProductoCategorias))
    precio = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)

    def __init__(self, nombre, descripcion, categoria, precio, cantidad):
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.precio = precio
        self.cantidad = cantidad

    def __str__(self):
        return self.nombre


class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'descripcion', 'categoria', 'precio', 'cantidad')


producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)
