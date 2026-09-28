from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "usuario.login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    # --- Modelos (se importan para que SQLAlchemy los registre) ---
    from app.models.usuario import Usuario
    from app.models.genero import Genero
    from app.models.juego import Juego
    from app.models.favorito import Favorito
    from app.models.resena import Resena
    from app.models.calificacion import Calificacion
    from app.models.captura import Captura

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # --- Controladores (Blueprints) ---
    from app.controllers.usuario_controller import usuario_bp
    from app.controllers.juego_controller import juego_bp
    from app.controllers.favorito_controller import favorito_bp
    from app.controllers.resena_controller import resena_bp
    from app.controllers.admin_controller import admin_bp

    app.register_blueprint(usuario_bp)
    app.register_blueprint(juego_bp)
    app.register_blueprint(favorito_bp)
    app.register_blueprint(resena_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    return app
