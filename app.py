from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import Lugar, Bien, Inventario, InventarioBien
from flask_cors import CORS


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/inventario'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"], "allow_headers": "*"}})

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

@app.route('/api/lugares', methods=['GET'])
def get_lugares():
    lugares = db.session.query(Lugar).all()
    return jsonify([{'edificio': lugar.edificio, 'area': lugar.area} for lugar in lugares])

@app.route('/api/lugares', methods=['POST'])
def add_lugar():
    data = request.get_json()
    nuevo_lugar = Lugar(
        edificio=data['edificio'],
        area=data['area']
    )
    db.session.add(nuevo_lugar)
    db.session.commit()
    return jsonify({'edificio': nuevo_lugar.edificio, 'area': nuevo_lugar.area}), 201

@app.route('/api/bienes', methods=['GET'])
def get_bienes():
    bienes = db.session.query(Bien).all()
    return jsonify([{
        'numero_activo': bien.numero_activo,
        'subnumero': bien.subnumero, 
        'descripcion': bien.descripcion,
        'material': bien.material,
        'color': bien.color,
        'marca': bien.marca,
        'modelo': bien.modelo,
        'serie': bien.serie,
        'estado': bien.estado,
        'id_lugar': bien.id_lugar,
        'imagen': bien.imagen
        } for bien in bienes])

@app.route('/api/bienes', methods=['POST'])
def add_bien():
    data = request.get_json()
    if isinstance(data, list):
        bienes_creados = []
        for bien_data in data:
            nuevo_bien = Bien(
                numero_activo=bien_data['numero_activo'],
                subnumero=bien_data['subnumero'],
                descripcion=bien_data['descripcion'],
                material=bien_data['material'],
                color=bien_data['color'],
                marca=bien_data['marca'],
                modelo=bien_data['modelo'],
                serie=bien_data['serie'],
                estado=bien_data['estado'],
                id_lugar=bien_data['id_lugar'],
                imagen=bien_data.get('imagen')
            )
            db.session.add(nuevo_bien)
            bienes_creados.append(nuevo_bien)
        db.session.commit()
        return jsonify([{'descripcion': bien.descripcion} for bien in bienes_creados]), 201
    else:
        nuevo_bien = Bien(
            numero_activo=data['numero_activo'],
            subnumero=data['subnumero'],
            descripcion=data['descripcion'],
            material=data['material'],
            color=data['color'],
            marca=data['marca'],
            modelo=data['modelo'],
            serie=data['serie'],
            estado=data['estado'],
            id_lugar=data['id_lugar'],
            imagen=data.get('imagen')
        )
        db.session.add(nuevo_bien)
        db.session.commit()
        return jsonify({'descripcion': nuevo_bien.descripcion}), 201

@app.route('/api/datos/bienes/<int:id>', methods=['PUT'])
def update_bien(id):
    data = request.get_json()
    bien = db.session.get(Bien, id)

    if bien is None:
        return jsonify({'error': 'Bien no encontrado'}), 404

    # Actualizar los campos del bien con los datos recibidos    
    bien.subnumero = data.get('subnumero', bien.subnumero)
    bien.descripcion = data.get('descripcion', bien.descripcion)
    bien.material = data.get('material', bien.material)
    bien.color = data.get('color', bien.color)
    bien.marca = data.get('marca', bien.marca)
    bien.modelo = data.get('modelo', bien.modelo)
    bien.serie = data.get('serie', bien.serie)
    bien.estado = data.get('estado', bien.estado)
    #bien.id_lugar = data.get('id_lugar', bien.id_lugar)
    #bien.imagen = data.get('imagen', bien.imagen)

    # Guardar los cambios en la base de datos
    db.session.commit()

    return jsonify({'descripcion': bien.descripcion}), 200

@app.route('/api/datos/cambiarplace/bienes/<int:id>', methods=['PUT'])
def change_idLugar_bien(id):
    data = request.get_json()
    bien = db.session.get(Bien, id)

    if bien is None:
        return jsonify({'error': 'Bien no encontrado'}), 404

    # Actualizar los campos del bien con los datos recibidos    
    bien.id_lugar = data.get('id_lugar', bien.id_lugar)

    # Guardar los cambios en la base de datos
    db.session.commit()

    return jsonify({'descripcion': bien.descripcion}), 200

@app.route('/api/bienes/<int:id>', methods=['PUT'])
def update_image_from_bien(id):
    try:
        # Obtener los datos enviados en la solicitud PUT
        data = request.get_json()

        # Buscar el bien por su ID
        bien = db.session.get(Bien, id)

        if bien is None:
            return jsonify({"error": "Bien no encontrado"}), 404

        # Actualizar la imagen del bien
        bien.imagen = data.get('imagen')

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({"message": "Imagen actualizada con éxito"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/inventarios', methods=['GET'])
def get_inventarios():
    inventarios = db.session.query(Inventario).all()
    return jsonify([{'fecha': inventario.fecha.strftime('%Y-%m-%d'), 'estatus': inventario.estatus} for inventario in inventarios])

@app.route('/api/inventarios', methods=['POST'])
def add_inventario():
    data = request.get_json()
    if isinstance(data, list):
        inventarios_creados = []
        for inventario_data in data:
            nuevo_inventario = Inventario(
                fecha=inventario_data['fecha'],
                estatus=inventario_data['estatus']
            )
            db.session.add(nuevo_inventario)
            inventarios_creados.append(nuevo_inventario)
        db.session.commit()
        return jsonify([{'fecha': inventario.fecha.strftime('%Y-%m-%d'), 'estatus': inventario.estatus} for inventario in inventarios_creados]), 201
    else:
        nuevo_inventario = Inventario(
            fecha=data['fecha'],
            estatus=data['estatus']
        )
        db.session.add(nuevo_inventario)
        db.session.commit()
        return jsonify({'fecha': nuevo_inventario.fecha.strftime('%Y-%m-%d'), 'estatus': nuevo_inventario.estatus}), 201

@app.route('/api/inventario_bien', methods=['GET'])
def get_inventarios_bien():
    inventarios_bien = db.session.query(InventarioBien).all()
    return jsonify([{'localizado': inventario.localizado, 'id_bien': inventario.id_bien, 'id_inventario': inventario.id_inventario} for inventario in inventarios_bien])

@app.route('/api/inventario_bien', methods=['POST'])
def add_inventario_bienes():
    data = request.get_json()
    if isinstance(data, list):
        inventarios_bienes_creados = []
        for inventario_bien_data in data:
            nuevo_inventario_bien = InventarioBien(
                id_inventario=inventario_bien_data['id_inventario'],
                id_bien=inventario_bien_data['id_bien'],
                localizado=inventario_bien_data.get('localizado', 0)  # Default is 0 if not provided
            )
            db.session.add(nuevo_inventario_bien)
            inventarios_bienes_creados.append(nuevo_inventario_bien)
        db.session.commit()
        return jsonify([
            {
                'id_inventario': inventario_bien.id_inventario,
                'id_bien': inventario_bien.id_bien,
                'localizado': inventario_bien.localizado
            }
            for inventario_bien in inventarios_bienes_creados
        ]), 201
    else:
        nuevo_inventario_bien = InventarioBien(
            id_inventario=data['id_inventario'],
            id_bien=data['id_bien'],
            localizado=data.get('localizado', 0)  # Default is 0 if not provided
        )
        db.session.add(nuevo_inventario_bien)
        db.session.commit()
        return jsonify({
            'id_inventario': nuevo_inventario_bien.id_inventario,
            'id_bien': nuevo_inventario_bien.id_bien,
            'localizado': nuevo_inventario_bien.localizado
        }), 201

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
