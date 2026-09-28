from flask import Blueprint, render_template, request
from flask_login import current_user

from app.models.juego import Juego
from app.models.genero import Genero
from app.models.favorito import Favorito
from app.models.resena import Resena
from app.models.usuario import Usuario

juego_bp = Blueprint("juego", __name__)


@juego_bp.route("/")
def index():
    destacados = Juego.query.order_by(Juego.fecha_creacion.desc()).limit(6).all()
    todos_los_juegos = Juego.query.all()
    mejor_calificados = sorted()[:4]
    banner_juego = mejor_calificados[0] if mejor_calificados else (destacados[0] if destacados else None)
        [j for j in todos_los_juegos if j.total_calificaciones > 0],
        key=lambda j: j.promedio_calificacion,
        reverse=True
    generos = Genero.query.all()
    total_juegos = Juego.query.count()
    total_resenas = Resena.query.count()
    total_usuarios = Usuario.query.count()
    return render_template(
        "index.html",
        destacados=destacados,
        generos=generos,
        total_juegos=total_juegos,
        total_resenas=total_resenas,
        total_usuarios=total_usuarios,
        mejor_calificados=mejor_calificados,
        banner_juego =banner_juego,
    )

@juego_bp.route("/catalogo")
def catalogo():
    query = Juego.query
    genero_id = request.args.get("genero", type=int)
    busqueda = request.args.get("q", "").strip()

    if genero_id:
        query = query.filter_by(genero_id=genero_id)
    if busqueda:
        query = query.filter(Juego.titulo.ilike(f"%{busqueda}%"))

    juegos = query.order_by(Juego.titulo.asc()).all()
    generos = Genero.query.all()
    return render_template(
        "catalogo.html",
        juegos=juegos,
        generos=generos,
        genero_id=genero_id,
        busqueda=busqueda,
    )


@juego_bp.route("/juego/<int:juego_id>")
def detalle(juego_id):
    juego = Juego.query.get_or_404(juego_id)
    resenas = Resena.query.filter_by(juego_id=juego_id).order_by(Resena.fecha.desc()).all()

    es_favorito = False
    if current_user.is_authenticated:
        es_favorito = Favorito.query.filter_by(
            usuario_id=current_user.id, juego_id=juego_id
        ).first() is not None

    similares = Juego.query.filter(
        Juego.genero_id == juego.genero_id,
        Juego.id != juego.id
    ).limit(4).all() if juego.genero_id else []
    return render_template("detalle_juego.html", juego=juego, resenas=resenas, es_favorito=es_favorito, similares=similares)
