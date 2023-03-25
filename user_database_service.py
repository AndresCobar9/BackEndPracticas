import re
import string
from flask import jsonify, request
from sqlalchemy import create_engine, false, null
from sqlalchemy import exc

from sqlalchemy.orm import sessionmaker, joinedload
from user_database_setup import Base, LocalUser, Tareas

engine=create_engine('sqlite:///users.db')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)

## Obtener todos los usuarios
def get_info():
        try:
                session=DBSession()
                users = session.query(LocalUser).options(joinedload(LocalUser.tareas), joinedload(LocalUser.solicitudes)).all()
                session.close()
                return jsonify(users=[user.serialize() for user in users])
        except exc.SQLAlchemyError as e:
              print(e)
              return jsonify({'message': 'Error en la base de datos'}), 500
        



## Detectar si el correo electronico esta registrado
def if_user_exists(r_email):
        session=DBSession()
        q=session.query(LocalUser).filter(r_email == LocalUser.email).first()
        session.close()
        if q is None:
                return False
        else:
                return True

## Agregar usuario
def add_user(new_user):
        try:
                session=DBSession()
                session.add(new_user)
                session.flush()
                session.commit()
                session.close()
                return True
        except exc.SQLAlchemyError as e:
                return False
        
        ## Obtener un usuario su username
def get_user(r_username):
        session=DBSession()
        q=session.query(LocalUser).filter(r_username == LocalUser.username).options(joinedload(LocalUser.tareas), joinedload(LocalUser.solicitudes)).first()
        session.close()
        if q:
                resulted_user=q.serialize()
                return resulted_user
        else:
                return None
## Agregar una tarea a un usuario
def add_tarea(new_tarea, r_username):
        try:
                session=DBSession()
                q=session.query(LocalUser).filter(r_username == LocalUser.username).first()
                q.tareas.append(new_tarea)
                session.commit()
                session.close()
                return True
        except exc.SQLAlchemyError as e:
                return False
        
## Obtener informacion de una tarea
def get_tarea(r_id):
        session=DBSession()
        q=session.query(Tareas).filter(r_id == Tareas.id).first()
        try:
                session.close()
                return q.serialize()
        except:
                return None

## Agregar una publicacion
def add_publicacion(new_publicacion):
        try:
                session=DBSession()
                session.add(new_publicacion)
                session.flush()
                session.commit()
                session.close()
                return True
        except exc.SQLAlchemyError as e:
                return False
        