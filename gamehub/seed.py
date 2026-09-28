"""
Script para poblar la base de datos con datos de ejemplo.
Ejecutar: python seed.py
"""
from app import create_app, db
from app.models.usuario import Usuario
from app.models.genero import Genero
from app.models.juego import Juego

app = create_app()

with app.app_context():
    # --- Usuario administrador ---
    if not Usuario.query.filter_by(email="admin@gamehub.com").first():
        admin = Usuario(nombre="Administrador", email="admin@gamehub.com", es_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)

    # --- Usuario de prueba ---
    if not Usuario.query.filter_by(email="jugador@gamehub.com").first():
        jugador = Usuario(nombre="Jugador Demo", email="jugador@gamehub.com", es_admin=False)
        jugador.set_password("jugador123")
        db.session.add(jugador)

    db.session.commit()

    # --- Géneros ---
    nombres_generos = ["Acción", "RPG", "Aventura", "Deportes", "Estrategia", "Terror"]
    generos = {}
    for nombre in nombres_generos:
        genero = Genero.query.filter_by(nombre=nombre).first()
        if not genero:
            genero = Genero(nombre=nombre)
            db.session.add(genero)
            db.session.flush()
        generos[nombre] = genero

    db.session.commit()

    # --- Juegos de ejemplo ---
    juegos_demo = [
        {
            "titulo": "Elden Ring",
            "descripcion": "Un vasto mundo de fantasía oscura creado por FromSoftware y George R. R. Martin.",
            "desarrollador": "FromSoftware",
            "anio_lanzamiento": 2022,
            "plataforma": "PC / PS5 / Xbox",
            "genero": "RPG",
        },
        {
            "titulo": "Hades",
            "descripcion": "Un roguelike de acción donde escapas del inframundo griego.",
            "desarrollador": "Supergiant Games",
            "anio_lanzamiento": 2020,
            "plataforma": "PC / Switch",
            "genero": "Acción",
        },
        {
            "titulo": "The Legend of Zelda: Tears of the Kingdom",
            "descripcion": "La secuela de Breath of the Wild, con nuevas mecánicas de construcción.",
            "desarrollador": "Nintendo",
            "anio_lanzamiento": 2023,
            "plataforma": "Switch",
            "genero": "Aventura",
        },
        {
            "titulo": "FIFA 24",
            "descripcion": "El simulador de fútbol más popular del mundo.",
            "desarrollador": "EA Sports",
            "anio_lanzamiento": 2023,
            "plataforma": "PC / PS5 / Xbox",
            "genero": "Deportes",
        },
        {
            "titulo": "Civilization VI",
            "descripcion": "Construye un imperio que perdure a través de los siglos.",
            "desarrollador": "Firaxis Games",
            "anio_lanzamiento": 2016,
            "plataforma": "PC",
            "genero": "Estrategia",
        },
        {
            "titulo": "Resident Evil 4 Remake",
            "descripcion": "El regreso del clásico survival horror totalmente renovado.",
            "desarrollador": "Capcom",
            "anio_lanzamiento": 2023,
            "plataforma": "PC / PS5 / Xbox",
            "genero": "Terror",
        },
    ]

    for datos in juegos_demo:
        if not Juego.query.filter_by(titulo=datos["titulo"]).first():
            juego = Juego(
                titulo=datos["titulo"],
                descripcion=datos["descripcion"],
                desarrollador=datos["desarrollador"],
                anio_lanzamiento=datos["anio_lanzamiento"],
                plataforma=datos["plataforma"],
                genero_id=generos[datos["genero"]].id,
            )
            db.session.add(juego)

    db.session.commit()
    print("✅ Base de datos poblada correctamente.")
    print("   Admin: admin@gamehub.com / admin123")
    print("   Usuario: jugador@gamehub.com / jugador123")
