
from datetime import date

from catalogo.models import Autor, EjemplarLibro, Genero, Libro

Autor.objects.create(
    nombre="Gabriel",
    apellido="García Márquez",
    fecha_nacimiento=date(1927, 3, 6),
    fecha_fallecimiento=date(2014, 4, 17),
    biografia="Escritor, periodista y Nobel colombiano, fue una figura central del realismo mágico, conocido por retratar la historia y mitología latinoamericana con una narrativa poética, mágica y política."
)

Autor.objects.create(
    nombre="Jane",
    apellido="Austen",
    fecha_nacimiento=date(1775, 12, 16),
    fecha_fallecimiento=date(1817, 7, 18),
    biografia="Escritora inglesa del período georgiano, célebre por sus novelas románticas que exploraban con ironía la dependencia económica de las mujeres y las dinámicas sociales de su época."
)

Autor.objects.create(
    nombre="Franz",
    apellido="Kafka",
    fecha_nacimiento=date(1883, 7, 3),
    fecha_fallecimiento=date(1924, 6, 3),
    biografia="Autor austrohúngaro de origen judío, cuyas obras exploran el absurdo, la burocracia, la alienación y la angustia existencial en un estilo único y opresivo."
)

Autor.objects.create(
    nombre="George",
    apellido="Orwell",
    fecha_nacimiento=date(1903, 6, 25),
    fecha_fallecimiento=date(1950, 1, 21),
    biografia="Escritor y periodista británico conocido por sus obras de crítica política, especialmente contra los totalitarismos, el control estatal y la manipulación ideológica."
)

Autor.objects.create(
    nombre="Isabel",
    apellido="Allende",
    fecha_nacimiento=date(1942, 8, 2),
    fecha_fallecimiento=None,
    biografia="Escritora chilena considerada una de las voces más leídas del mundo hispano, fusiona lo político, histórico y lo mágico con énfasis en protagonistas femeninas."
)

Autor.objects.create(
    nombre="Haruki",
    apellido="Murakami",
    fecha_nacimiento=date(1949, 1, 12),
    fecha_fallecimiento=None,
    biografia="Novelista japonés contemporáneo, famoso por mezclar lo cotidiano con lo surreal, sus temas exploran la soledad, el amor y la identidad en una atmósfera onírica."
)



Genero.objects.create(nombre="Realismo mágico")
Genero.objects.create(nombre="Novela")
Genero.objects.create(nombre="Romance")
Genero.objects.create(nombre="Comedia")
Genero.objects.create(nombre="Drama")
Genero.objects.create(nombre="Fantasía")
Genero.objects.create(nombre="Ficción")
Genero.objects.create(nombre="Distopía")
Genero.objects.create(nombre="Drama familiar")
Genero.objects.create(nombre="Surrealismo")
Genero.objects.create(nombre="Satírica")




# Libro 1 - Gabriel García Márquez (id=1), Realismo mágico (id=1)
libro1 = Libro.objects.create(
    titulo="Cien años de soledad",
    autor_id=1,
    resumen="Relata la saga de la familia Buendía en el mítico pueblo de Macondo, donde lo mágico y lo trágico se entrelazan.",
    isbn="978030747472",
    idioma="Español"
)

# Libro 2 - Jane Austen (id=2), Romance (id=3)
libro2 = Libro.objects.create(
    titulo="Orgullo y prejuicio",
    autor_id=2,
    resumen="Elizabeth Bennet y el señor Darcy enfrentan malentendidos y clases sociales en esta crítica a la Inglaterra del siglo XIX.",
    isbn="978014143951",
    idioma="Español"
)


# Libro 3 - Franz Kafka (id=3), Surrealismo (id=10)
libro3 = Libro.objects.create(
    titulo="La metamorfosis",
    autor_id=3,
    resumen="Gregor Samsa despierta convertido en un insecto gigante, lo que provoca su exclusión y decadencia familiar.",
    isbn="978849105212",
    idioma="Español"
)


# Libro 4 - George Orwell (id=4), Distopía (id=8)
libro4 = Libro.objects.create(
    titulo="1984",
    autor_id=4,
    resumen="En un futuro distópico, un régimen totalitario vigila cada aspecto de la vida humana y controla la verdad misma.",
    isbn="978045152493",
    idioma="Español"
)


# Libro 5 - Isabel Allende (id=5), Drama familiar (id=9)
libro5 = Libro.objects.create(
    titulo="La casa de los espíritus",
    autor_id=5,
    resumen="Saga familiar en Chile marcada por la dictadura, los secretos y la conexión espiritual entre generaciones.",
    isbn="978150111701",
    idioma="Español"
)


# Libro 6 - Haruki Murakami (id=6), Fantasía (id=6), Surrealismo (id=10)
libro6 = Libro.objects.create(
    titulo="Kafka en la orilla",
    autor_id=6,
    resumen="Un joven fugitivo y un anciano con poderes sobrenaturales se cruzan en una historia que entrelaza sueños, profecías y realidades paralelas.",
    isbn="978030727526",
    idioma="Español"
)


# Libro 7 - Gabriel García Márquez (id=1), Romance (id=3)
libro7 = Libro.objects.create(
    titulo="El amor en los tiempos del cólera",
    autor_id=1,
    resumen="Una historia de amor que se desarrolla a lo largo de más de medio siglo, donde dos amantes esperan pacientemente la oportunidad de estar juntos pese a las adversidades y el paso del tiempo.",
    isbn="978030738973",
    idioma="Español"
)


# Libro 8 - Gabriel García Márquez (id=1), Realismo mágico (id=1), Drama (id=5)
libro8 = Libro.objects.create(
    titulo="Crónica de una muerte anunciada",
    autor_id=1,
    resumen="Relato que reconstruye los eventos y circunstancias que rodean el asesinato anunciado de Santiago Nasar en un pequeño pueblo, explorando la inevitabilidad y complicidad social.",
    isbn="97803073897",
    idioma="Español"
)

libro1.genero.add(1, 2)           # Realismo mágico, Novela
libro2.genero.add(2, 3, 4, 5)     # Novela, Romance, Comedia, Drama
libro3.genero.add(2, 6)           # Novela, Fantasía
libro4.genero.add(8, 11, 7)       # Distopía, Satírica, Ficción
libro5.genero.add(1, 2, 9)        # Realismo mágico, Novela, Drama familiar
libro6.genero.add(10, 1, 7)       # Surrealismo, Realismo mágico, Ficción
libro7.genero.add(1, 2, 3)        # Realismo mágico, Novela, Romance
libro8.genero.add(1, 2)           # Realismo mágico, Novela



EjemplarLibro.objects.create(
    id='34b66c18-f383-4fe3-ab59-40e01fb31294',
    fecha_adquisicion='2025-05-14',
    fecha_devolucion='2025-05-31',
    estado='p',
    libro_id=4
)

EjemplarLibro.objects.create(
    id='00fe4d08-30d5-4ff8-b313-5d4732183060',
    fecha_adquisicion='2025-05-16',
    fecha_devolucion='2025-08-05',
    estado='r',
    libro_id=1
)

EjemplarLibro.objects.create(
    id='82523d35-5a91-488c-8aab-a97625d4d209',
    fecha_adquisicion='2025-05-16',
    fecha_devolucion=None,
    estado='p',
    libro_id=8
)

EjemplarLibro.objects.create(
    id='dfab3987-92ee-4658-8c2c-e1815a1b9e68',
    fecha_adquisicion=None,
    fecha_devolucion=None,
    estado='m',
    libro_id=8
)

EjemplarLibro.objects.create(
    id='d16e3e01-a59d-41df-bec0-daefeac452da',
    fecha_adquisicion='2025-06-06',
    fecha_devolucion='2025-06-26',
    estado='r',
    libro_id=7
)

EjemplarLibro.objects.create(
    id='3acf4ed7-967c-43ad-949f-c48a7c634228',
    fecha_adquisicion='2025-06-24',
    fecha_devolucion=None,
    estado='r',
    libro_id=6
)

EjemplarLibro.objects.create(
    id='9972aa59-195b-47af-ba2f-6258baf33d65',
    fecha_adquisicion='2025-06-14',
    fecha_devolucion='2025-07-10',
    estado='p',
    libro_id=5
)

EjemplarLibro.objects.create(
    id='21e3a658-ba7a-4d32-a1a1-503e21b9d3d5',
    fecha_adquisicion=None,
    fecha_devolucion=None,
    estado='p',
    libro_id=3
)

EjemplarLibro.objects.create(
    id='18f2cac0-45f4-4fb1-9dca-4f45c7439859',
    fecha_adquisicion=None,
    fecha_devolucion=None,
    estado='d',
    libro_id=2
)

EjemplarLibro.objects.create(
    id='22bcc501-6882-4921-b03d-eb3eca7ad8af',
    fecha_adquisicion=None,
    fecha_devolucion=None,
    estado='d',
    libro_id=1
)
