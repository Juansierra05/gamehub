# 🎮 GameHub — Plataforma de gestión y catálogo de videojuegos

Proyecto académico construido con **arquitectura MVC** usando Python + Flask + SQLite.

## Estructura MVC

```
gamehub/
├── run.py                     # Punto de entrada
├── config.py                  # Configuración
├── seed.py                    # Datos de ejemplo
├── requirements.txt
└── app/
    ├── __init__.py             # Application factory
    ├── models/                 # MODELO
    │   ├── usuario.py
    │   ├── juego.py
    │   ├── genero.py
    │   ├── favorito.py
    │   ├── calificacion.py
    │   └── resena.py
    ├── controllers/            # CONTROLADOR (Blueprints de Flask)
    │   ├── usuario_controller.py
    │   ├── juego_controller.py
    │   ├── favorito_controller.py
    │   ├── resena_controller.py
    │   └── admin_controller.py
    ├── templates/               # VISTA (Jinja2)
    │   ├── base.html, index.html, catalogo.html, detalle_juego.html
    │   ├── login.html, registro.html, perfil.html, favoritos.html
    │   └── admin/ (panel, juegos, form_juego, generos, usuarios)
    └── static/
        └── css/style.css
```

## Instalación

```bash
cd gamehub
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed.py                # Crea la BD y datos de ejemplo
python run.py
```

Abre tu navegador en **http://127.0.0.1:5000**

## Credenciales de prueba (creadas por seed.py)

| Rol       | Correo                | Contraseña   |
|-----------|------------------------|-------------|
| Admin     | admin@gamehub.com      | admin123    |
| Usuario   | jugador@gamehub.com    | jugador123  |

## Funcionalidades

- Registro e inicio de sesión (Flask-Login, contraseñas hasheadas)
- Catálogo de videojuegos con búsqueda y filtro por género
- Página de detalle con reseñas y calificaciones (1-5 estrellas)
- Sistema de favoritos por usuario
- Panel de administrador con CRUD completo de juegos y géneros,
  y listado de usuarios registrados
- Control de acceso: rutas protegidas con `@login_required` y `@admin_required`

## Cómo explicar el MVC en tu sustentación

- **Modelo** (`app/models/`): clases SQLAlchemy que representan las tablas
  (Usuario, Juego, Genero, Favorito, Calificacion, Resena) y sus relaciones.
- **Vista** (`app/templates/`): plantillas Jinja2 que solo reciben datos
  del controlador y los muestran; no contienen lógica de negocio.
- **Controlador** (`app/controllers/`): Blueprints de Flask que reciben
  las peticiones HTTP, consultan/actualizan el Modelo, y deciden qué Vista renderizar.
