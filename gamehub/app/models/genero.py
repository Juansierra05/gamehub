from app import db


class Genero(db.Model):
    __tablename__ = "generos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    juegos = db.relationship("Juego", backref="genero", lazy=True)

    def __repr__(self):
        return f"<Genero {self.nombre}>"
