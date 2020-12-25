from flask import Blueprint, jsonify, request

from database import db
from productos.models import Producto

productos = Blueprint('productos', __name__)


@productos.route('/lista')
def obtener_productos():
    try:
        lista_productos = Producto.query.all()
        return jsonify(
            {'data': Producto.Schema(many=True).dump(lista_productos), 'success': True, 'message': 'Productos obtenidos'})
    except Exception as e:
        return jsonify({'data': str(e), 'success': False, 'message': 'Ocurrió un error en el servidor'})


@productos.route('/<int:id_producto>')
def obtener_producto(id_producto):
    try:
        producto = Producto.query.get(id_producto)
        if producto is not None:
            return jsonify({'data': Producto.Schema().dump(producto), 'success': True, 'message': 'Producto obtenido'})
        else:
            return jsonify({'data': None, 'success': False, 'message': 'Producto no encontrado'})
    except Exception as e:
        return jsonify({'data': str(e), 'success': False, 'message': 'Ocurrió un error en el servidor'})


@productos.route('/', methods=['POST'])
def agregar_producto():
    try:
        nombre = request.json['nombre']
        descripcion = request.json['descripcion']
        categoria = request.json['categoria']
        precio = request.json['precio']
        cantidad = request.json['cantidad']
        disponible = request.json['disponible']
        nuevo_producto = Producto(nombre, descripcion, categoria, precio, cantidad, disponible)
        db.session.add(nuevo_producto)
        db.session.commit()
        return jsonify({'data': Producto.Schema().dump(nuevo_producto), 'success': True, 'message': 'Producto agregado'})
    except Exception as e:
        return jsonify({'data': str(e), 'success': False, 'message': 'Ocurrió un error en el servidor'})


@productos.route('/<int:id_producto>', methods=['PUT'])
def editar_producto(id_producto):
    try:
        producto = Producto.query.get(id_producto)

        if producto is not None:
            producto.nombre = request.json['nombre'] if 'nombre' in request.json else producto.nombre
            producto.descripcion = request.json['descripcion'] if 'descripcion' in request.json else producto.descripcion
            producto.categoria = request.json['categoria'] if 'categoria' in request.json else producto.categoria
            producto.precio = request.json['precio'] if 'precio' in request.json else producto.precio
            producto.cantidad = request.json['cantidad'] if 'cantidad' in request.json else producto.cantidad
            producto.disponible = request.json['disponible'] if 'disponible' in request.json else producto.disponible
            db.session.commit()
            return jsonify({'data': Producto.Schema().dump(producto), 'success': True, 'message': 'Producto actualizado'})
        else:
            return jsonify({'data': None, 'success': False, 'message': 'Producto no encontrado'})
    except Exception as e:
        return jsonify({'data': str(e), 'success': False, 'message': 'Ocurrió un error en el servidor'})


@productos.route('/<int:id_producto>', methods=['DELETE'])
def delete_product(id_producto):
    try:
        producto = Producto.query.get(id_producto)
        if producto is not None:
            db.session.delete(producto)
            db.session.commit()
            return jsonify({'data': Producto.Schema().dump(producto), 'success': True, 'message': 'Producto eliminado'})
        else:
            return jsonify({'data': None, 'success': False, 'message': 'Producto no encontrado'})
    except Exception as e:
        return jsonify({'data': str(e), 'success': False, 'message': 'Ocurrió un error en el servidor'})
