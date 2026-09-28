import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "gamehub-clave-secreta-cambiar-en-produccion"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "gamehub.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
