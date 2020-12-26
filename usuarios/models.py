from database import db, ma, add_schema
from marshmallow_enum import EnumField
import enum
from datetime import datetime


@add_schema
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

    def __init__(self, nombres, apellidos, telefono, correo, contrasenha, estado):
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.correo = correo
        self.contrasenha = contrasenha
        self.estado = estado

    def __str__(self):
        return self.nombre + ' ' + self.apellidos

    def to_json(self):
        return dict(nombres=self.nombres, apellidos=self.apellidos)
