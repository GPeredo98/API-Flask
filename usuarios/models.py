from database import db, add_schema
from datetime import datetime


@add_schema()
class Usuario(db.Model):

    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    correo = db.Column(db.String(200), nullable=False, unique=True)
    contrasenha = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.BOOLEAN, default=1)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now())
    imagen = db.Column(db.Text)

    def __init__(self, nombres, apellidos, telefono, correo, contrasenha, estado, imagen):
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.correo = correo
        self.contrasenha = contrasenha
        self.estado = estado
        self.imagen = imagen

    def __str__(self):
        return self.nombre + ' ' + self.apellidos

    def to_json(self):
        return dict(nombres=self.nombres, apellidos=self.apellidos)
