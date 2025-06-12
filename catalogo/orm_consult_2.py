from catalogo.models import Autor, Genero, Libro
from django.db.models import Count, Sum, Avg, Min, Max, F, Q
from django.db.models import Subquery, OuterRef, Count

#Consultas Básicas
#Filtros Simples

# Filtrar por condición exacta
autores = Autor.objects.filter(apellido="García Márquez")
# Filtrar por múltiples condiciones (AND)
autores = Autor.objects.filter(apellido="García Márquez", nombre="Gabriel")
# Excluir registros
autores = Autor.objects.exclude(apellido="García Márquez")
# Limitar resultados
autores = Autor.objects.all()[:5] # Primeros 5 resultados
autores = Autor.objects.all()[5:10] # Resultados del 6 al 10

"""
SQL:
SELECT * FROM myapp_autor WHERE apellido = 'García Márquez';
SELECT * FROM myapp_autor WHERE apellido = 'García Márquez' AND nombre = 'Gabriel';
SELECT * FROM myapp_autor WHERE apellido != 'García Márquez';
SELECT * FROM myapp_autor LIMIT 5;
SELECT * FROM myapp_autor LIMIT 5 OFFSET 5;
"""

#Ordenamiento
# Ordenar por un campo (ascendente)
autores = Autor.objects.order_by('apellido')
# Ordenar por un campo (descendente)
autores = Autor.objects.order_by('-fecha_nacimiento')
# Ordenar por múltiples campos
autores = Autor.objects.order_by('apellido', 'nombre')

"""
SQL:
SELECT * FROM myapp_autor ORDER BY apellido ASC;
SELECT * FROM myapp_autor ORDER BY fecha_nacimiento DESC;
SELECT * FROM myapp_autor ORDER BY apellido ASC, nombre ASC;
"""

#Operadores de Consulta (Field Lookups)
# Contiene
libros = Libro.objects.filter(titulo__contains='don')
# Contiene (case-insensitive)
libros = Libro.objects.filter(titulo__icontains='don')
# Empieza con
libros = Libro.objects.filter(titulo__startswith='El')
# Termina con
libros = Libro.objects.filter(titulo__endswith='Quijote')
# Mayor que
libros = Libro.objects.filter(publicado__gt='2000-01-01')
# Menor que
libros = Libro.objects.filter(publicado__lt='2000-01-01')
# En una lista
libros = Libro.objects.filter(id__in=[1, 2, 3])
# Rango
libros = Libro.objects.filter(publicado__range=('2000-01-01', '2010-12-31'))
# Isnull
autores = Autor.objects.filter(fecha_nacimiento__isnull=True)

"""
SQL:
SELECT * FROM myapp_libro WHERE titulo LIKE '%don%';
SELECT * FROM myapp_libro WHERE UPPER(titulo) LIKE UPPER('%don%');
SELECT * FROM myapp_libro WHERE titulo LIKE 'El%';
SELECT * FROM myapp_libro WHERE titulo LIKE '%Quijote';
SELECT * FROM myapp_libro WHERE publicado > '2000-01-01';
SELECT * FROM myapp_libro WHERE publicado < '2000-01-01';
SELECT * FROM myapp_libro WHERE id IN (1, 2, 3);
SELECT * FROM myapp_libro WHERE publicado BETWEEN '2000-01-01' AND '2010-12-31';
SELECT * FROM myapp_autor WHERE fecha_nacimiento IS NULL;
"""

#Consultas Q para Operaciones OR y Operaciones Complejas

# OR
libros = Libro.objects.filter(Q(titulo__contains='don') | Q(titulo__contains='quijote'))
"""
SQL:
    SELECT *
  FROM "catalogo_libro"
 WHERE ("catalogo_libro"."titulo"::text LIKE '%don%' OR "catalogo_libro"."titulo"::text LIKE '%quijote%')
 ORDER BY "catalogo_libro"."titulo" ASC
"""

# AND
libros = Libro.objects.filter(Q(titulo__contains='Cien') & Q(autor__fecha_nacimiento__year=1927))
"""
SQL:
SELECT *
  FROM "catalogo_libro"
 INNER JOIN "catalogo_autor"
    ON ("catalogo_libro"."autor_id" = "catalogo_autor"."id")
 WHERE ("catalogo_libro"."titulo"::text LIKE '%Cien%' AND "catalogo_autor"."fecha_nacimiento" BETWEEN '1927-01-01'::date AND '1927-12-31'::date)
 ORDER BY "catalogo_libro"."titulo" ASC

"""

# NOT
libros = Libro.objects.filter(~Q(autor__apellido='Cervantes'))

"""
SQL:
SELECT *
  FROM "catalogo_libro"
  LEFT OUTER JOIN "catalogo_autor"
    ON ("catalogo_libro"."autor_id" = "catalogo_autor"."id")
 WHERE NOT ("catalogo_autor"."apellido" = 'Cervantes' AND "catalogo_autor"."apellido" IS NOT NULL)
 ORDER BY "catalogo_libro"."titulo" ASC
"""


# Agregaciones básicas
# Contar todos los libros
total_libros = Libro.objects.count()
"""
SQL:
SELECT COUNT(*) AS "__count"
  FROM "catalogo_libro"
"""

# Anotar el número de libros por autor
autores_con_conteo = Autor.objects.annotate(num_libros=Count('libros'))
for autor in autores_con_conteo:
    print(f"{autor.nombre} {autor.apellido}: {autor.num_libros} libros")

"""
SQL:
    SELECT "catalogo_autor"."id",
       "catalogo_autor"."nombre",
       "catalogo_autor"."apellido",
       "catalogo_autor"."fecha_nacimiento",
       "catalogo_autor"."fecha_fallecimiento",
       "catalogo_autor"."biografia",
       COUNT("catalogo_libro"."id") AS "num_libros"
  FROM "catalogo_autor"
  LEFT OUTER JOIN "catalogo_libro"
    ON ("catalogo_autor"."id" = "catalogo_libro"."autor_id")
 GROUP BY "catalogo_autor"."id"
"""

# Ordenar por campo anotado
autores_populares = Autor.objects.annotate(
num_libros=Count('libros')
).order_by('-num_libros')[:5] # Top 5 autores con más libros
""""
SQL:
SELECT "catalogo_autor"."id",
       "catalogo_autor"."nombre",
       "catalogo_autor"."apellido",
       "catalogo_autor"."fecha_nacimiento",
       "catalogo_autor"."fecha_fallecimiento",
       "catalogo_autor"."biografia",
       COUNT("catalogo_libro"."id") AS "num_libros"
  FROM "catalogo_autor"
  LEFT OUTER JOIN "catalogo_libro"
    ON ("catalogo_autor"."id" = "catalogo_libro"."autor_id")
 GROUP BY "catalogo_autor"."id"
 ORDER BY 7 DESC
"""

# Filtrar por campo anotado
autores_prolificos = Autor.objects.annotate(
num_libros=Count('libros')
).filter(num_libros__gt=5) # Autores con más de 5 libros


"""
SQL:
SELECT "catalogo_autor"."id",
       "catalogo_autor"."nombre",
       "catalogo_autor"."apellido",
       "catalogo_autor"."fecha_nacimiento",
       "catalogo_autor"."fecha_fallecimiento",
       "catalogo_autor"."biografia",
       COUNT("catalogo_libro"."id") AS "num_libros"
  FROM "catalogo_autor"
  LEFT OUTER JOIN "catalogo_libro"
    ON ("catalogo_autor"."id" = "catalogo_libro"."autor_id")
 GROUP BY "catalogo_autor"."id"
HAVING COUNT("catalogo_libro"."id") > 5
"""


libros = Libro.objects.all()
for libro in libros:
    print(libro.autor.nombre) # Consulta adicional por cada libro

# Con select_related (para ForeignKey y OneToOneField) - Solo 1 consulta
libros = Libro.objects.select_related('autor')
for libro in libros:
    print(libro.autor.nombre) # No genera consultas adicionales

"""
SQL con select_related:
SELECT *
  FROM "catalogo_libro"
  LEFT OUTER JOIN "catalogo_autor"
    ON ("catalogo_libro"."autor_id" = "catalogo_autor"."id")
 ORDER BY "catalogo_libro"."titulo" ASC
"""

# Con prefetch_related (para ManyToManyField o consultas "inversas") - 2 consultas
libros = Libro.objects.prefetch_related('genero')
for libro in libros:
    for categoria in libro.genero.all(): # No genera consultas adicionales
        print(categoria.nombre)

"""
SQL:
SELECT ("catalogo_libro_genero"."libro_id") AS "_prefetch_related_val_libro_id",
       "catalogo_genero"."id",
       "catalogo_genero"."nombre"
  FROM "catalogo_genero"
 INNER JOIN "catalogo_libro_genero"
    ON ("catalogo_genero"."id" = "catalogo_libro_genero"."genero_id")
 WHERE "catalogo_libro_genero"."libro_id" IN (2, 1, 3, 4)

"""

#Combinar ambos para optimizar múltiples tipos de relaciones
libros = Libro.objects.select_related('autor').prefetch_related('genero')

""""
SQL con prefetch_related y select_related:
SELECT ("catalogo_libro_genero"."libro_id") AS "_prefetch_related_val_libro_id",
       "catalogo_genero"."id",
       "catalogo_genero"."nombre"
  FROM "catalogo_genero"
 INNER JOIN "catalogo_libro_genero"
    ON ("catalogo_genero"."id" = "catalogo_libro_genero"."genero_id")
 WHERE "catalogo_libro_genero"."libro_id" IN (2, 1, 3, 4)

"""

libros_con_conteo = Libro.objects.annotate(num_ejemplares=Count('ejemplares'),ejemplares_disponibles=Count('ejemplares', filter=Q(ejemplares__estado='d')))
"""
SQL:
SELECT "catalogo_libro"."id",
       "catalogo_libro"."titulo",
       "catalogo_libro"."autor_id",
       "catalogo_libro"."resumen",
       "catalogo_libro"."isbn",
       "catalogo_libro"."idioma",
       COUNT("catalogo_ejemplarlibro"."id") AS "num_ejemplares",
       COUNT("catalogo_ejemplarlibro"."id") FILTER (WHERE ("catalogo_ejemplarlibro"."estado" = 'd')) AS "ejemplares_disponibles"
  FROM "catalogo_libro"
  LEFT OUTER JOIN "catalogo_ejemplarlibro"
    ON ("catalogo_libro"."id" = "catalogo_ejemplarlibro"."libro_id")
 GROUP BY "catalogo_libro"."id"
"""

# Uso de only para seleccionar solo ciertos campos
autores_basico = Autor.objects.only('nombre', 'apellido')
"""
SELECT "catalogo_autor"."id",
       "catalogo_autor"."nombre",
       "catalogo_autor"."apellido"
  FROM "catalogo_autor"
 ORDER BY "catalogo_autor"."apellido" ASC,
          "catalogo_autor"."nombre" ASC
"""

# Uso de defer para excluir campos grandes
libros_sin_resumen = Libro.objects.defer('resumen')

"""
SELECT "catalogo_libro"."id",
       "catalogo_libro"."titulo",
       "catalogo_libro"."autor_id",
       "catalogo_libro"."isbn",
       "catalogo_libro"."idioma"
  FROM "catalogo_libro"
 ORDER BY "catalogo_libro"."titulo" ASC
 LIMIT 21
"""

#Subconsultas con Subquery y OuterRef

# Obtener el último libro de cada autor
ultimo_libro = Libro.objects.filter(
autor=OuterRef('pk')
).order_by('-publicado').values('titulo')[:1]
autores = Autor.objects.annotate(
ultimo_libro=Subquery(ultimo_libro)
)
# Contar libros por categoría
categoria_count = Libro.objects.filter(
categorias=OuterRef('pk')
).values('categorias').annotate(c=Count('*')).values('c')
categorias = Genero.objects.annotate(
num_libros=Subquery(categoria_count)
)

"""
SQL:
SELECT myapp_autor.*,
(SELECT titulo
FROM myapp_libro
WHERE myapp_libro.autor_id = myapp_autor.id
ORDER BY publicado DESC
LIMIT 1) AS ultimo_libro
FROM myapp_autor;


SELECT myapp_categoria.*,
(SELECT COUNT(*)
FROM myapp_libro_categorias
WHERE myapp_libro_categorias.categoria_id = myapp_categoria.id) AS num_libros
FROM myapp_categoria;
"""

#