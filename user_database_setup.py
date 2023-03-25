
from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class LocalUser(Base):
    __tablename__ = 'local_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    role = Column(String(250), nullable=False)
    gender = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password = Column(String, nullable=False)
    created = Column(String, nullable=False)
    isactive = Column(Boolean, nullable = False)
    tareas = relationship("Tareas", back_populates="local_user", foreign_keys="Tareas.user_id")
    solicitudes = relationship("Solicitudes", back_populates="local_user", foreign_keys="Solicitudes.user_id")
    def serialize(self):
        return {
            
            'name': self.name,
            'role': self.role,
            'gender': self.gender,
            'username': self.username,
            'email': self.email,
            'password':self.password,
            'created': self.created,
            'autorizado': self.isactive,
            'tareas': [tarea.serialize() for tarea in self.tareas],
            'solicitudes': [solicitud.serialize() for solicitud in self.solicitudes]
        }
    

class Tareas(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(250), nullable=False)
    descripcion = Column(String(250), nullable=False)
    created = Column(String, nullable=False)
    entrega = Column(String, nullable=False)
    isactive = Column(Boolean, nullable = False)
    user_id = Column(Integer, ForeignKey('local_users.id'))
    local_user = relationship(LocalUser, back_populates="tareas")
    
    def serialize(self):
        return {
            
            'id':self.id,
            'titulo': self.titulo,
            'description': self.descripcion,
            'entrega': self.entrega,
            'created': self.created,
            'completado': self.isactive

        }

class Solicitudes(Base):
    __tablename__ = 'solicitudes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    asunto = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    created = Column(String, nullable=False)
    isactive = Column(Boolean, nullable = False)
    user_id = Column(Integer, ForeignKey('local_users.id'))
    local_user = relationship(LocalUser, back_populates="solicitudes")
    def serialize(self):
        return {
            
            'asunto': self.asunto,
            'description': self.description,
            'created': self.created,
            'autorizado': self.isactive
            
        }
	

class Publicaciones(Base):
    __tablename__ = 'publicaciones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(250), nullable=False)
    descripcion = Column(String(250), nullable=False)
    created = Column(String, nullable=False)
    area = Column(String, nullable=False)
    def serialize(self):
        return {
            'id':self.id,
            'titulo': self.titulo,
            'description': self.descripcion,
            'created': self.created,
            'area': self.area
        }
	
engine=create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)
