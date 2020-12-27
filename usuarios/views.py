from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from utilities import db
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


@usuarios.route('/<id_usuario>')
@jwt_required
def obtener_datos_usuario(id_usuario):
    try:
        token = get_jwt_identity()
        print(token)
        usuario = Usuario.query.get(id_usuario)
        if usuario is not None:
            return jsonify({'data': Usuario.Schema().dump(usuario), 'success': True, 'message': 'Datos del usuario'})
        else:
            return jsonify({'data': None, 'success': False, 'message': 'Usuario no encontrado'})
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
        token = create_access_token(identity={'id': nuevo_usuario.id, 'correo': nuevo_usuario.correo})

        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify(
            {
                'data': {'usuario': Usuario.Schema().dump(nuevo_usuario), 'token': token},
                'success': True,
                'message': 'Usuario registrado'
            })
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
                token = create_access_token(identity={'id': usuario.id, 'correo': usuario.correo})
                return jsonify(
                    {
                        'data': {'usuario': Usuario.Schema().dump(usuario), 'token': token},
                        'success': True,
                        'message': 'Usuario registrado'
                    })
            else:
                return jsonify({'data': None, 'success': False, 'message': 'La contraseña es incorrecta'})
        else:
            return jsonify({'data': '', 'success': False, 'message': 'El correo no pertenece a un usuario existente'})
    except Exception as e:
        return jsonify({'data': str(e), 'success': False, 'message': 'Ocurrió un error en el servidor'})
