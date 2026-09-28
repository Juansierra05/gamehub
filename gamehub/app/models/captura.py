from app import db


class Captura(db.Model):
    __tablename__ = "capturas"

    id = db.Column(db.Integer, primary_key=True)
    juego_id = db.Column(db.Integer, db.ForeignKey("juegos.id"), nullable=False)
    url = db.Column(db.String(255), nullable=False)