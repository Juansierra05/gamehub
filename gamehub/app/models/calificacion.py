from datetime import datetime
from app import db


class Calificacion(db.Model):
    __tablename__ = "calificaciones"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    juego_id = db.Column(db.Integer, db.ForeignKey("juegos.id"), nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)  # 1 a 5
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("usuario_id", "juego_id", name="uq_usuario_juego_calificacion"),)
