from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.models.usuario import Usuario

usuario_bp = Blueprint("usuario", __name__)


@usuario_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("juego.index"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirmar = request.form.get("confirmar_password", "")

        if not nombre or not email or not password:
            flash("Todos los campos son obligatorios.", "danger")
        elif password != confirmar:
            flash("Las contraseñas no coinciden.", "danger")
        elif Usuario.query.filter_by(email=email).first():
            flash("Ya existe una cuenta con ese correo.", "danger")
        else:
            nuevo_usuario = Usuario(nombre=nombre, email=email)
            nuevo_usuario.set_password(password)
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash("Cuenta creada correctamente. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("usuario.login"))

    return render_template("registro.html")


@usuario_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("juego.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_password(password):
            login_user(usuario)
            flash(f"¡Bienvenido, {usuario.nombre}!", "success")
            siguiente = request.args.get("next")
            return redirect(siguiente or url_for("juego.index"))
        flash("Correo o contraseña incorrectos.", "danger")

    return render_template("login.html")


@usuario_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("juego.index"))


@usuario_bp.route("/perfil")
@login_required
def perfil():
    return render_template("perfil.html", usuario=current_user)
