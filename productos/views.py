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
        imagen = request.json['imagen']
        nuevo_producto = Producto(nombre, descripcion, categoria, precio, cantidad, disponible, imagen)
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
            producto.nombre = request.json.get('nombre', producto.nombre)
            producto.descripcion = request.json.get('descripcion', producto.descripcion)
            producto.categoria = request.json.get('categoria', producto.categoria)
            producto.precio = request.json.get('precio', producto.precio)
            producto.cantidad = request.json.get('cantidad', producto.cantidad)
            producto.disponible = request.json.get('disponible', producto.disponible)
            producto.imagen = request.json.get('imagen', producto.imagen)
            db.session.commit()
            return jsonify({'data': Producto.Schema().dump(producto), 'success': True, 'message': 'Producto actualizado'})
        else:
            return jsonify({'data': None, 'success': False, 'message': 'Producto no encontrado'})
    except Exception as e:
        return jsonify({'data': str(e), 'success': False, 'message': 'Ocurrió un error en el servidor'})


@productos.route('/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
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


@productos.route('/cambiar_estado/<int:id_producto>', methods=['PATCH'])
def cambiar_estado_producto(id_producto):
    try:
        producto = Producto.query.get(id_producto)
        if producto is not None:
            producto.disponible = not producto.disponible
            db.session.commit()
            return jsonify({'data': Producto.Schema().dump(producto), 'success': True, 'message': 'Estado cambiado'})
        else:
            return jsonify({'data': None, 'success': False, 'message': 'Producto no encontrado'})
    except Exception as e:
        return jsonify({'data': str(e), 'success': False, 'message': 'Ocurrió un error en el servidor'})
