## Imports
from datetime import datetime, timedelta
import json
from socket import socket
from xmlrpc.client import boolean ## Sockets de comunicacion
from flask import Flask, Response, jsonify, request, session  ## Import especifico de Flask
from flask_cors import CORS ## Import que permite el CORS origins de Flask
from flask_socketio import SocketIO
from sqlalchemy import false, true ## Modulo Socket Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (create_access_token)
from flask_jwt_extended import JWTManager
from user_database_setup import LocalUser, Publicaciones, Solicitudes, Tareas
import jwt
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager
## importa Endpoints
import user_database_service


## Definicion de la aplicacion
app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":'*'}})
socket = SocketIO(app,cors_allowed_origins="*") ## Definimos Cors
bcrypt=Bcrypt(app)
SECRET_KEY = 'SanJoseKEY'
app.config['JWT_SECRET_KEY'] = SECRET_KEY # clave secreta para firmar los tokens JWT
jwt_manager = JWTManager(app) # inicialización de JWTManager


##  ----------------------------------------------------- Registar Usuario -----------------------------------------------------

@app.route('/user/register', methods=['POST'])
def register():

    r_name=request.get_json()['name']
    r_username=request.get_json()['username']
    r_email=request.get_json()['email']
    r_gender=request.get_json()['gender']
    r_area=request.get_json()['area']
    r_password=bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    result=""
    
    
    if user_database_service.if_user_exists(r_email):
        result="user already exists"
        print(result)
        return jsonify({'result': result})

    new_user=LocalUser(name=r_name,area=r_area, username=r_username, email=r_email, password=r_password, gender = r_gender , role = 'Usuario', isactive = True, created=datetime.utcnow())
    added=user_database_service.add_user(new_user)
    if added is True:
        result="user successfully added"
        print(result)
    else:
        result="unable to add"
        print(result)
    return jsonify({'result': result})


##  ----------------------------------------------------- Login -----------------------------------------------------
@app.route('/user/login', methods=['POST'])
def login():
    username=request.get_json()['username']
    password=request.get_json()['password']
    result=""
    
    response_user=user_database_service.get_user(username)
    print(response_user)
    if response_user:
        if bcrypt.check_password_hash(response_user['password'], password):
            
            identity={
                'username': response_user['username'],
                'name': response_user['name'],
                'userrole': response_user['role'],
                'area': response_user['area'],
                'isactive': response_user['isactive']
            }

            # Crear el token JWT con una duración de 1 hora
            exp_time = datetime.utcnow() + timedelta(hours=1)
            payload = {
                'exp': exp_time,
                'sub': response_user['id'],
                'identity': identity
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            
            # Devolver el token JWT en la respuesta
            return jsonify({'token': token, 'exp': exp_time.strftime('%Y-%m-%d %H:%M:%S'), 'identity': identity})
        else:
            result=jsonify({'error': 'Invalid username or password'})
    return result

##  ----------------------------------------------------- Actualizar usuario -----------------------------------------------------
@app.route('/user/update/<int:id>', methods=['PUT'])
def updateuser(id):
    updateObject = request.get_json()
    print(updateObject)
    res=user_database_service.update_user(id,updateObject)
    return res

@app.route('/user/updatepassword/<string:UserID>', methods=['PUT'])
def UpdatePassword(UserID):
   
    r_password=bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    res=user_database_service.update_password(UserID,r_password)
    return res


##  ----------------------------------------------------- Obtener todos los usuarios -----------------------------------------------------

@app.route('/user/userslist', methods=['GET'])
def users():
    response_user=user_database_service.get_info()
    print(response_user)
    return response_user

##  ----------------------------------------------------- Obtener Informacion de 1 Usario mediante username -----------------------------------------------------
@app.route('/user/get/<string:username>', methods=['GET'])
def getuser(username):
    
    response_user=user_database_service.get_user(username)
    return jsonify(response_user)

##  ----------------------------------------------------- Obtener Informacion de 1 Usario mediante id -----------------------------------------------------
@app.route('/user/getid/<string:id>', methods=['GET'])
def getuserid(id):
    
    response_user=user_database_service.get_userid(id)
    return jsonify(response_user)


##  ----------------------------------------------------- Agregar una tarea mediante el  id -----------------------------------------------------

@app.route('/user/addtarea/<string:id>', methods=['POST'])
def addtarea(id):
    print(id)
    r_titulo=request.get_json()['Tarea']
    r_descripcion=request.get_json()['Descripcion']
    r_creado=datetime.utcnow()
    r_entrega=request.get_json()['Fecha']
    r_estado=False

    new_tarea=Tareas(titulo=r_titulo, descripcion=r_descripcion, created=r_creado, entrega=r_entrega, isactive=r_estado)
    added=user_database_service.add_tarea(new_tarea, id)  
    return jsonify({'result': added})


##                                                      TAREAS


##  ----------------------------------------------------- Obtener una tarea mediante su ID -----------------------------------------------------
@app.route('/user/gettarea/<int:id>', methods=['GET'])
def gettarea(id):
    response_tarea=user_database_service.get_tarea(id)
    return jsonify(response_tarea)

##  ----------------------------------------------------- Cambiar de estado tarea mediante su ID -----------------------------------------------------
@app.route('/user/updatetarea/<int:id>', methods=['PUT'])
def changetarea(id):
    r_estado=request.get_json()['estado']
    print(r_estado)
    response_tarea=user_database_service.change_tarea(id, r_estado)
    return jsonify(response_tarea)


@app.route('/user/deletetarea/<int:id>', methods=['DELETE'])
def deletetarea(id):
    response_tarea=user_database_service.delete_tarea(id)
    return jsonify(response_tarea)

## ----------------------------------------------------- Obtener todas las tareas -----------------------------------------------------
@app.route('/user/gettareas', methods=['GET'])
def gettareas():
    response_tarea=user_database_service.get_tareas()
    return jsonify(response_tarea)

## ----------------------------------------------------- Obtener todas las tareas de un usuario -----------------------------------------------------
@app.route('/user/gettareas/<string:username>', methods=['GET'])
def gettareasuser(username):
    response_tarea=user_database_service.get_tareasuser(username)
    return jsonify(response_tarea)

##  ----------------------------------------------------- Agregar una Publicacion -----------------------------------------------------
@app.route('/user/addpublicacion', methods=['POST'])
def addpublicacion():
    r_titulo=request.get_json()['titulo']
    r_descripcion=request.get_json()['descripcion']
    r_creado=datetime.utcnow()
    r_area=request.get_json()['area']
    r_autor=request.get_json()['autor']
    new_tarea=Publicaciones(titulo=r_titulo, descripcion=r_descripcion, created=r_creado,area=r_area, autor = r_autor)
    added=user_database_service.add_publicacion(new_tarea)  
    return jsonify({'result': added})


## ----------------------------------------------------- Obtener todas las publicaciones -----------------------------------------------------
@app.route('/user/getpublicaciones', methods=['GET'])
def getpublicaciones():
    response_tarea=user_database_service.get_publicaciones()
    return jsonify(response_tarea)

## ----------------------------------------------------- Obtener una publicacion mediante su area -----------------------------------------------------
@app.route('/user/getpublicacion/<string:area>', methods=['GET'])
def getpublicacion(area):
    response_tarea = user_database_service.get_publicacionesarea(area)
    
    if response_tarea is None:
        return Response(json.dumps({"error": "No se encontraron publicaciones o hubo un error en la consulta"}), status=404, mimetype='application/json')
    else:
        return Response(json.dumps({"publicaciones": response_tarea}), status=200, mimetype='application/json')

##  ----------------------------------------------------- Borrar publicacion -----------------------------------------------------
@app.route('/user/deletepublicacion/<int:id>', methods=['DELETE'])
def deletepublicacion(id):
    response_tarea=user_database_service.delete_publicacion(id)
    return jsonify(response_tarea)

## ----------------------------------------------------- Agregar una solicitud -----------------------------------------------------

@app.route('/user/addsolicitud', methods=['POST'])
def addsolicitud():
    r_username=request.get_json()['Solicitante']
    r_asunto=request.get_json()['Asunto']
    r_descripcion=request.get_json()['Descripcion']
    r_creado=datetime.utcnow()
    new_tarea=Solicitudes(asunto=r_asunto, description=r_descripcion, created=r_creado,isactive = True)
    added=user_database_service.add_solicitud(new_tarea, r_username)  
    return jsonify({'result': added})

## Obtener todas las solicitudes de un usuario por id
@app.route('/user/getsolicitudes/<int:id>', methods=['GET'])
def getsolicitudesuser(id):
    response_tarea=user_database_service.get_solicitudesuser(id)
    return jsonify(response_tarea)


## ----------------------------------------------------- Obtener todas las solicitudes -----------------------------------------------------
@app.route('/user/getsolicitudes', methods=['GET'])
def getsolicitudes():
    response_tarea=user_database_service.get_solicitudes()
    return jsonify(response_tarea)




## ----------------------------------------------------- Obtener una solicitud mediante su id -----------------------------------------------------
@app.route('/user/getsolicitud/<int:id>', methods=['GET'])
def getsolicitud(id):
    response_tarea=user_database_service.get_solicitud(id)
    return jsonify(response_tarea)

##  ----------------------------------------------------- Cambiar de estado de Solicitud mediante su ID -----------------------------------------------------
@app.route('/user/updatesolicitud/<int:id>', methods=['PUT'])
def changesolicitud(id):
    r_estado=request.get_json()['estado']
    print(r_estado)
    response_tarea=user_database_service.change_solicitud(id, r_estado)
    return jsonify(response_tarea)


##  ----------------------------------------------------- Informacion del servidor -----------------------------------------------------
if __name__ == "__main__":
    app.run(host="localhost", port = '3000', debug = False)


