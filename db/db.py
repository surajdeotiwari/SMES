from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, BLOB, LargeBinary, Date
from sqlalchemy.orm import DeclarativeBase,relationship, backref
from flask_login import UserMixin
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    user_type = Column(String)
    phone = Column(Integer)
    photo = Column(LargeBinary)
    file = Column(String)
    mimetype = Column(String)
    is_active = Column(db.Boolean, default=True)
    is_authenticated = Column(db.Boolean, default=True)
    def is_active(self):
        return self.is_active
    def get_id(self):
        return self.id
    def is_authenticated(self):
        return self.is_authenticated
class Devices(db.Model):
    __tablename__ = 'devices'
    device_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref=backref("devices", lazy=True))
    device_name = Column(String)
    device_location = Column(String)
    wifi_name = Column(String)
    password = Column(String)
class Data(db.Model):
    __tablename__  = 'data'
    reqid = Column(Integer, primary_key=True,autoincrement=True)
    time = Column(Date)
    date = Column(String)
    voltage = Column(Float)
    current = Column(Float)
    frequency = Column(Float)
    power = Column(Float)
    energy = Column(Float)
    device_id = Column(Integer, ForeignKey('devices.device_id'))
    device = relationship("Devices", backref=backref("data", lazy=True))
