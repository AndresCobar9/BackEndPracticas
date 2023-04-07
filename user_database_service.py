import re
import string
from flask import jsonify, request
from sqlalchemy import create_engine, false, null
from sqlalchemy import exc

from sqlalchemy.orm import sessionmaker, joinedload
from user_database_setup import Base, LocalUser, Publicaciones, Solicitudes, Tareas

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
## Obtener todas las tareas
def get_tareas():
        session=DBSession()
        q=session.query(Tareas).all()
        try:
                session.close()
                return jsonify(tareas=[tarea.serialize() for tarea in q])
        except exc.SQLAlchemyError as e:
                print(e)
                return None
        
## Obtener todas las tareas de un usuario
def get_tareasuser(r_username):
        session=DBSession()
        q=session.query(LocalUser).filter(r_username == LocalUser.username).first()
        try:
                session.close()
                return jsonify(tareas=[tarea.serialize() for tarea in q.tareas])
        except exc.SQLAlchemyError as e:
                print(e)
                return None
## borrar tarea
def delete_tarea(r_id):
        try:
                session=DBSession()
                q=session.query(Tareas).filter(r_id == Tareas.id).first()
                session.delete(q)
                session.commit()
                session.close()
                return True
        except exc.SQLAlchemyError as e:
                return False
        
        
## Agregar una publicacion
def add_publicacion(new_publicacion):
        try:
                session=DBSession(Publicaciones)
                session.add(new_publicacion)
                session.flush()
                session.commit()
                session.close()
                return True
        except exc.SQLAlchemyError as e:
                return False

## Obtener todas las publicaciones 
def get_publicaciones():
        session=DBSession()
        q=session.query(Publicaciones).all()
        try:
                session.close()
                return jsonify(publicaciones=[publicacion.serialize() for publicacion in q])
        except exc.SQLAlchemyError as e:
                print(e)
                return None     
        
                
        
## Obtener todas las publicaciones por area
def get_publicacionesarea(area):
        session=DBSession()
        q=session.query(Publicaciones).filter(Publicaciones.area == area).all()
        try:
                session.close()
                return jsonify(publicaciones=[publicacion.serialize() for publicacion in q])
        except:
                return None
## borrar publicacion   
def delete_publicacion(r_id):
        try:
                session=DBSession()
                q=session.query(Publicaciones).filter(r_id == Publicaciones.id).first()
                session.delete(q)
                session.commit()
                session.close()
                return True
        except exc.SQLAlchemyError as e:
                return False
        
## Obtener todas las solicitudes
def get_solicitudes():
        session=DBSession()
        q=session.query(Solicitudes).filter(Solicitudes).all()
        try:
                session.close()
                return jsonify(solicitudes=[solicitud.serialize() for solicitud in q])
        except:
                return None
## Obtener una solicitud     
def get_solicitud(r_id):
        session=DBSession()
        q=session.query(Solicitudes).filter(r_id == Solicitudes.id).first()
        try:
                session.close()
                return q.serialize()
        except:
                return None
        
## Agregar una solicitud
def add_solicitud(new_solicitud, r_username):
        try:
                session=DBSession()
                q=session.query(LocalUser).filter(r_username == LocalUser.username).first()
                q.solicitudes.append(new_solicitud)
                session.commit()
                session.close()
                return True
        except exc.SQLAlchemyError as e:
                return False
        
## borrar solicitud
def delete_solicitud(r_id):
        try:
                session=DBSession()
                q=session.query(Solicitudes).filter(r_id == Solicitudes.id).first()
                session.delete(q)
                session.commit()
                session.close()
                return True
        except exc.SQLAlchemyError as e:
                return False
