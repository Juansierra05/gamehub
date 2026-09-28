from datetime import datetime
from app import db


class Resena(db.Model):
    __tablename__ = "resenas"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    juego_id = db.Column(db.Integer, db.ForeignKey("juegos.id"), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
