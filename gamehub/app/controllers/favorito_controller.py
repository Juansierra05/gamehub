from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models.favorito import Favorito
from app.models.juego import Juego

favorito_bp = Blueprint("favorito", __name__)


@favorito_bp.route("/favoritos")
@login_required
def index():
    favoritos = Favorito.query.filter_by(usuario_id=current_user.id).all()
    return render_template("favoritos.html", favoritos=favoritos)


@favorito_bp.route("/favoritos/agregar/<int:juego_id>", methods=["POST"])
@login_required
def agregar(juego_id):
    Juego.query.get_or_404(juego_id)
    existente = Favorito.query.filter_by(usuario_id=current_user.id, juego_id=juego_id).first()
    if not existente:
        db.session.add(Favorito(usuario_id=current_user.id, juego_id=juego_id))
        db.session.commit()
        flash("Juego agregado a favoritos.", "success")
    return redirect(url_for("juego.detalle", juego_id=juego_id))


@favorito_bp.route("/favoritos/quitar/<int:juego_id>", methods=["POST"])
@login_required
def quitar(juego_id):
    favorito = Favorito.query.filter_by(usuario_id=current_user.id, juego_id=juego_id).first()
    if favorito:
        db.session.delete(favorito)
        db.session.commit()
        flash("Juego eliminado de favoritos.", "info")
    return redirect(url_for("favorito.index"))
