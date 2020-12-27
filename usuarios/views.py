from flask import Blueprint, jsonify, request

from database import db
from usuarios.models import Usuario
import bcrypt

usuarios = Blueprint('usuarios', __name__)


@usuarios.route('/lista')
def obtener_usuarios():
    try:
        lista_usuarios = Usuario.query.all()
        return jsonify(
            {'data': Usuario.Schema(many=True).dump(lista_usuarios), 'success': True, 'message': 'Usuarios obtenidos'})
    except Exception as e:
        return jsonify({'data': str(e), 'success': False, 'message': 'Ocurrió un error en el servidor'})


@usuarios.route('/registrar', methods=['POST'])
def registrar_usuario():
    try:
        nombres = request.json['nombres']
        apellidos = request.json['apellidos']
        telefono = request.json['telefono']
        correo = request.json['correo']
        estado = request.json['estado']
        imagen = request.json['imagen']

        contrasenha = request.json['contrasenha']
        contrasenha_hasheada = bcrypt.hashpw(contrasenha.encode('utf-8'), bcrypt.gensalt())

        nuevo_usuario = Usuario(nombres, apellidos, telefono, correo, contrasenha_hasheada, estado, imagen)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({'data': Usuario.Schema().dump(nuevo_usuario), 'success': True, 'message': 'Usuario registrado'})
    except Exception as e:
        return jsonify({'data': str(e), 'success': False, 'message': 'Ocurrió un error en el servidor'})


@usuarios.route('/login', methods=['POST'])
def login():
    try:
        correo = request.json['correo']
        contrasenha = request.json['contrasenha']

        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario is not None:
            if bcrypt.checkpw(contrasenha.encode('utf-8'), usuario.contrasenha.encode('utf-8')):
                return jsonify({'data': Usuario.Schema().dump(usuario), 'success': True, 'message': 'Bienvenido'})
            else:
                return jsonify({'data': None, 'success': False, 'message': 'La contraseña es incorrecta'})
        else:
            return jsonify({'data': '', 'success': False, 'message': 'El correo no pertenece a un usuario existente'})
    except Exception as e:
        return jsonify({'data': str(e), 'success': False, 'message': 'Ocurrió un error en el servidor'})
