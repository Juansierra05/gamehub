from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user

from app import db
from app.models.juego import Juego
from app.models.captura import Captura
from app.models.genero import Genero
from app.models.usuario import Usuario

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    def decorado(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorado


@admin_bp.route("/")
@login_required
@admin_required
def panel():
    total_juegos = Juego.query.count()
    total_usuarios = Usuario.query.count()
    total_generos = Genero.query.count()
    return render_template(
        "admin/panel.html",
        total_juegos=total_juegos,
        total_usuarios=total_usuarios,
        total_generos=total_generos,
    )


@admin_bp.route("/juegos")
@login_required
@admin_required
def listar_juegos():
    juegos = Juego.query.order_by(Juego.titulo.asc()).all()
    return render_template("admin/juegos.html", juegos=juegos)


@admin_bp.route("/juegos/nuevo", methods=["GET", "POST"])
@login_required
@admin_required
def nuevo_juego():
    generos = Genero.query.all()
    if request.method == "POST":
        juego = Juego(
            titulo=request.form.get("titulo", "").strip(),
            descripcion=request.form.get("descripcion", "").strip(),
            desarrollador=request.form.get("desarrollador", "").strip(),
            anio_lanzamiento=request.form.get("anio_lanzamiento", type=int),
            plataforma=request.form.get("plataforma", "").strip(),
            duracion_horas=request.form.get("duracion_horas" , type=int),
            imagen_url=request.form.get("imagen_url", "").strip(),
            genero_id=request.form.get("genero_id", type=int),
        )
        db.session.add(juego)
        db.session.flush()  # para que juego.id ya exista
        for url in request.form.get("capturas_urls", "").splitlines():
            url = url.strip()
            if url:
                db.session.add(Captura(juego_id=juego.id, url=url))
        db.session.commit()
        flash("Juego creado correctamente.", "success")
        return redirect(url_for("admin.listar_juegos"))
    return render_template("admin/form_juego.html", generos=generos, juego=None)


@admin_bp.route("/juegos/<int:juego_id>/editar", methods=["GET", "POST"])
@login_required
@admin_required
def editar_juego(juego_id):
    juego = Juego.query.get_or_404(juego_id)
    generos = Genero.query.all()
    if request.method == "POST":
        juego.titulo = request.form.get("titulo", "").strip()
        juego.descripcion = request.form.get("descripcion", "").strip()
        juego.desarrollador = request.form.get("desarrollador", "").strip()
        juego.anio_lanzamiento = request.form.get("anio_lanzamiento", type=int)
        juego.plataforma = request.form.get("plataforma", "").strip()
        juego.duracion_horas = request.form.get("duracion_horas",type=int)
        juego.imagen_url = request.form.get("imagen_url", "").strip()
        juego.genero_id = request.form.get("genero_id", type=int)
        Captura.query.filter_by(juego_id=juego.id).delete()
        for url in request.form.get("capturas_urls", "").splitlines():
            url = url.strip()
            if url:
                db.session.add(Captura(juego_id=juego.id, url=url))
        db.session.commit()
        flash("Juego actualizado correctamente.", "success")
        return redirect(url_for("admin.listar_juegos"))
    return render_template("admin/form_juego.html", generos=generos, juego=juego)


@admin_bp.route("/juegos/<int:juego_id>/eliminar", methods=["POST"])
@login_required
@admin_required
def eliminar_juego(juego_id):
    juego = Juego.query.get_or_404(juego_id)
    db.session.delete(juego)
    db.session.commit()
    flash("Juego eliminado correctamente.", "info")
    return redirect(url_for("admin.listar_juegos"))


@admin_bp.route("/generos", methods=["GET", "POST"])
@login_required
@admin_required
def generos():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        if nombre and not Genero.query.filter_by(nombre=nombre).first():
            db.session.add(Genero(nombre=nombre))
            db.session.commit()
            flash("Género agregado.", "success")
        else:
            flash("Ese género ya existe o el nombre es inválido.", "danger")
        return redirect(url_for("admin.generos"))
    lista_generos = Genero.query.all()
    return render_template("admin/generos.html", generos=lista_generos)


@admin_bp.route("/generos/<int:genero_id>/eliminar", methods=["POST"])
@login_required
@admin_required
def eliminar_genero(genero_id):
    genero = Genero.query.get_or_404(genero_id)
    db.session.delete(genero)
    db.session.commit()
    flash("Género eliminado.", "info")
    return redirect(url_for("admin.generos"))


@admin_bp.route("/usuarios")
@login_required
@admin_required
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template("admin/usuarios.html", usuarios=usuarios)
