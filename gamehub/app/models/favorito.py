from datetime import datetime
from app import db


class Favorito(db.Model):
    __tablename__ = "favoritos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    juego_id = db.Column(db.Integer, db.ForeignKey("juegos.id"), nullable=False)
    fecha_agregado = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("usuario_id", "juego_id", name="uq_usuario_juego_favorito"),)
