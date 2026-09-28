from flask import Blueprint, redirect, url_for, request, flash
from flask_login import login_required, current_user

from app import db
from app.models.resena import Resena
from app.models.calificacion import Calificacion
from app.models.juego import Juego

resena_bp = Blueprint("resena", __name__)


@resena_bp.route("/juego/<int:juego_id>/resena", methods=["POST"])
@login_required
def agregar_resena(juego_id):
    Juego.query.get_or_404(juego_id)
    comentario = request.form.get("comentario", "").strip()
    puntuacion = request.form.get("puntuacion", type=int)

    if comentario:
        db.session.add(Resena(usuario_id=current_user.id, juego_id=juego_id, comentario=comentario))

    if puntuacion and 1 <= puntuacion <= 5:
        existente = Calificacion.query.filter_by(usuario_id=current_user.id, juego_id=juego_id).first()
        if existente:
            existente.puntuacion = puntuacion
        else:
            db.session.add(Calificacion(usuario_id=current_user.id, juego_id=juego_id, puntuacion=puntuacion))

    db.session.commit()
    flash("¡Gracias por tu reseña!", "success")
    return redirect(url_for("juego.detalle", juego_id=juego_id))


@resena_bp.route("/resena/<int:resena_id>/eliminar", methods=["POST"])
@login_required
def eliminar_resena(resena_id):
    resena = Resena.query.get_or_404(resena_id)
    if resena.usuario_id != current_user.id and not current_user.es_admin:
        flash("No tienes permiso para eliminar esta reseña.", "danger")
    else:
        juego_id = resena.juego_id
        db.session.delete(resena)
        db.session.commit()
        flash("Reseña eliminada.", "info")
        return redirect(url_for("juego.detalle", juego_id=juego_id))
    return redirect(url_for("juego.index"))
