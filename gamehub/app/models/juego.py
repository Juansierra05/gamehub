from datetime import datetime
from app import db


class Juego(db.Model):
    __tablename__ = "juegos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    desarrollador = db.Column(db.String(120), nullable=True)
    anio_lanzamiento = db.Column(db.Integer, nullable=True)
    plataforma = db.Column(db.String(80), nullable=True)
    imagen_url = db.Column(db.String(255), nullable=True)
    duracion_horas = db.Column(db.Integer, nullable=True)
    genero_id = db.Column(db.Integer, db.ForeignKey("generos.id"), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    favoritos = db.relationship("Favorito", backref="juego", lazy=True, cascade="all, delete-orphan")
    resenas = db.relationship("Resena", backref="juego", lazy=True, cascade="all, delete-orphan")
    calificaciones = db.relationship("Calificacion", backref="juego", lazy=True, cascade="all, delete-orphan")
    capturas = db.relationship("Captura", backref="juego", lazy=True, cascade="all, delete-orphan")

    @property
    def promedio_calificacion(self):
        if not self.calificaciones:
            return 0
        return round(sum(c.puntuacion for c in self.calificaciones) / len(self.calificaciones), 1)

    @property
    def total_calificaciones(self):
        return len(self.calificaciones)

    def __repr__(self):
        return f"<Juego {self.titulo}>"
