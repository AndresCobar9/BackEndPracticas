## Imports
from datetime import datetime, timedelta
from socket import socket
from xmlrpc.client import boolean ## Sockets de comunicacion
from flask import Flask, jsonify, request, session  ## Import especifico de Flask
from flask_cors import CORS ## Import que permite el CORS origins de Flask
from flask_socketio import SocketIO
from sqlalchemy import false, true ## Modulo Socket Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (create_access_token)
from flask_jwt_extended import JWTManager
from user_database_setup import LocalUser, Tareas
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
    r_password=bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    result=""
    
    if user_database_service.if_user_exists(r_email):
        result="user already exists"
        print(result)
        return jsonify({'result': result})

    new_user=LocalUser(name=r_name, username=r_username, email=r_email, password=r_password, gender = r_gender , role = 'user', isactive = True, created=datetime.utcnow())
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

    if response_user:
        if bcrypt.check_password_hash(response_user.password, password):
            
            identity={
                'username': response_user.username,
                'name': response_user.name,
                'userrole': response_user.role,
                'isactive': response_user.isactive
            }

            # Crear el token JWT con una duración de 1 hora
            exp_time = datetime.utcnow() + timedelta(hours=1)
            payload = {
                'exp': exp_time,
                'sub': response_user.id,
                'identity': identity
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            
            # Devolver el token JWT en la respuesta
            return jsonify({'token': token, 'exp': exp_time.strftime('%Y-%m-%d %H:%M:%S'), 'identity': identity})
        else:
            result=jsonify({'error': 'Invalid username or password'})
    return result

##  ----------------------------------------------------- Obtener todos los usuarios -----------------------------------------------------

@app.route('/user/userslist', methods=['GET'])
def users():
    response_user=user_database_service.get_info()
    print(response_user)
    return response_user

##  ----------------------------------------------------- Agregar una tarea mediante el usuario -----------------------------------------------------

@app.route('/user/addtarea/<string:username>', methods=['POST'])
def addtarea(username):
    print(username)
    r_titulo=request.get_json()['titulo']
    r_descripcion=request.get_json()['descripcion']
    r_creado=datetime.utcnow()
    r_entrega=request.get_json()['entrega']
    r_estado=False

    new_tarea=Tareas(titulo=r_titulo, descripcion=r_descripcion, created=r_creado, entrega=r_entrega, isactive=r_estado)
    added=user_database_service.add_tarea(new_tarea, username)  
    return jsonify({'result': added})

##  ----------------------------------------------------- Obtener una tarea mediante su ID -----------------------------------------------------
@app.route('/user/gettarea/<int:id>', methods=['GET'])
def gettarea(id):
    response_tarea=user_database_service.get_tarea(id)
    return jsonify(response_tarea)


##  ----------------------------------------------------- Obtener Informacion de 1 Usario mediante username -----------------------------------------------------
@app.route('/user/get/<string:username>', methods=['GET'])
def getuser(username):
    
    response_user=user_database_service.get_user(username)
    return jsonify(response_user)

##  ----------------------------------------------------- Agregar una Publicacion -----------------------------------------------------
@app.route('/user/addpublicacion', methods=['POST'])
def addpublicacion():
    r_titulo=request.get_json()['titulo']
    r_descripcion=request.get_json()['descripcion']
    r_creado=datetime.utcnow()
    r_area=request.get_json()['area']
    new_tarea=Tareas(titulo=r_titulo, descripcion=r_descripcion, created=r_creado,area=r_area)
    added=user_database_service.add_publicacion(new_tarea)  
    return jsonify({'result': added})


##  ----------------------------------------------------- Informacion del servidor -----------------------------------------------------
if __name__ == "__main__":
    app.run(host="localhost", port = '3000', debug = False)


