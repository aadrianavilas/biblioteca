from django.db.models import Q
from catalogo.models import Autor, EjemplarLibro, Genero, Libro
from django.db.models import Count
from django.db.models import Count, Case, When, IntegerField

# Consultas básicas
# 1. Todos los libros
libros = Libro.objects.all()
"""
SQL:
SELECT "catalogo_libro"."id",
       "catalogo_libro"."titulo",
       "catalogo_libro"."autor_id",
       "catalogo_libro"."resumen",
       "catalogo_libro"."isbn",
       "catalogo_libro"."idioma"
  FROM "catalogo_libro"
 ORDER BY "catalogo_libro"."titulo" ASC
 LIMIT 21

"""

# 2. Libros ordenados por título
libros = Libro.objects.order_by('titulo')
"""
SQL:
SELECT "catalogo_libro"."id",
       "catalogo_libro"."titulo",
       "catalogo_libro"."autor_id",
       "catalogo_libro"."resumen",
       "catalogo_libro"."isbn",
       "catalogo_libro"."idioma"
  FROM "catalogo_libro"
 ORDER BY "catalogo_libro"."titulo" ASC
 LIMIT 21

"""

# 3. Filtrado por autor
libros_de_autor = Libro.objects.filter(autor__apellido='García Márquez')
"""
SQL:
SELECT "catalogo_libro"."id",
       "catalogo_libro"."titulo",
       "catalogo_libro"."autor_id",
       "catalogo_libro"."resumen",
       "catalogo_libro"."isbn",
       "catalogo_libro"."idioma"
  FROM "catalogo_libro"
 INNER JOIN "catalogo_autor"
    ON ("catalogo_libro"."autor_id" = "catalogo_autor"."id")
 WHERE "catalogo_autor"."apellido" = 'García Márquez'
 ORDER BY "catalogo_libro"."titulo" ASC
 LIMIT 21
"""

# 4. Búsqueda por palabra clave en título o resumen
libros = Libro.objects.filter(Q(titulo__icontains='quijote') | Q(resumen__icontains='quijote'))
"""
SQL:
SELECT "catalogo_libro"."id",
       "catalogo_libro"."titulo",
       "catalogo_libro"."autor_id",
       "catalogo_libro"."resumen",
       "catalogo_libro"."isbn",
       "catalogo_libro"."idioma"
  FROM "catalogo_libro"
 WHERE (UPPER("catalogo_libro"."titulo"::text) LIKE UPPER('%quijote%') OR UPPER("catalogo_libro"."resumen"::text) LIKE UPPER('%quijote%'))
 ORDER BY "catalogo_libro"."titulo" ASC
 LIMIT 21
"""

# 5. Ejemplares disponibles
ejemplares_disponibles = EjemplarLibro.objects.filter(estado='d')
"""
SQL:
SELECT "catalogo_libro"."id",
       "catalogo_libro"."titulo",
       "catalogo_libro"."autor_id",
       "catalogo_libro"."resumen",
       "catalogo_libro"."isbn",
       "catalogo_libro"."idioma"
  FROM "catalogo_libro"
 WHERE "catalogo_libro"."id" = 3
 LIMIT 21
"""

# Consultas avanzadas
# 6. Contar libros por género
generos_con_conteo = Genero.objects.annotate(num_libros=Count('libro'))
"""
SQL:
SELECT "catalogo_genero"."id",
       "catalogo_genero"."nombre",
       COUNT("catalogo_libro_genero"."libro_id") AS "num_libros"
  FROM "catalogo_genero"
  LEFT OUTER JOIN "catalogo_libro_genero"
    ON ("catalogo_genero"."id" = "catalogo_libro_genero"."genero_id")
 GROUP BY "catalogo_genero"."id"
 LIMIT 21
"""

# 7. Autores con sus libros (evitando N+1 query)
autores_con_libros = Autor.objects.prefetch_related('libros')
"""
SELECT "catalogo_libro"."id",
       "catalogo_libro"."titulo",
       "catalogo_libro"."autor_id",
       "catalogo_libro"."resumen",
       "catalogo_libro"."isbn",
       "catalogo_libro"."idioma"
  FROM "catalogo_libro"
 WHERE "catalogo_libro"."autor_id" IN (4, 1, 2, 3, 5)
 ORDER BY "catalogo_libro"."titulo" ASC
"""

# 8. Libro con su autor (evitando N+1 query)
libros_con_autor = Libro.objects.select_related('autor')
"""
SQL:
SELECT "catalogo_libro"."id",
       "catalogo_libro"."titulo",
       "catalogo_libro"."autor_id",
       "catalogo_libro"."resumen",
       "catalogo_libro"."isbn",
       "catalogo_libro"."idioma",
       "catalogo_autor"."id",
       "catalogo_autor"."nombre",
       "catalogo_autor"."apellido",
       "catalogo_autor"."fecha_nacimiento",
       "catalogo_autor"."fecha_fallecimiento",
       "catalogo_autor"."biografia"
  FROM "catalogo_libro"
  LEFT OUTER JOIN "catalogo_autor"
    ON ("catalogo_libro"."autor_id" = "catalogo_autor"."id")
 ORDER BY "catalogo_libro"."titulo" ASC
 LIMIT 21
"""

# 9. Contar ejemplares por estado
libro_stats = Libro.objects.annotate(
    ejemplares_disponibles=Count(
        Case(
            When(ejemplares__estado='d', then=1),
            output_field=IntegerField()
            )
        ),
    ejemplares_prestados=Count(
        Case(
        When(ejemplares__estado='p', then=1),
        output_field=IntegerField()
            )
        )
)

"""
SQL:
SELECT "catalogo_libro"."id",
       "catalogo_libro"."titulo",
       "catalogo_libro"."autor_id",
       "catalogo_libro"."resumen",
       "catalogo_libro"."isbn",
       "catalogo_libro"."idioma",
       COUNT(CASE WHEN "catalogo_ejemplarlibro"."estado" = 'd' THEN 1 ELSE NULL END) AS "ejemplares_disponibles",
       COUNT(CASE WHEN "catalogo_ejemplarlibro"."estado" = 'p' THEN 1 ELSE NULL END) AS "ejemplares_prestados"
  FROM "catalogo_libro"
  LEFT OUTER JOIN "catalogo_ejemplarlibro"
    ON ("catalogo_libro"."id" = "catalogo_ejemplarlibro"."libro_id")
 GROUP BY "catalogo_libro"."id"
 LIMIT 21

"""

# 10. Consulta compleja: libros que no tienen ejemplares disponibles
libros_sin_disponibles = Libro.objects.exclude(ejemplares__estado='d').distinct()

""""
SQL:
SELECT DISTINCT "catalogo_libro"."id",
       "catalogo_libro"."titulo",
       "catalogo_libro"."autor_id",
       "catalogo_libro"."resumen",
       "catalogo_libro"."isbn",
       "catalogo_libro"."idioma"
  FROM "catalogo_libro"
 WHERE NOT (EXISTS(
                    SELECT 1 AS "a" 
                    FROM "catalogo_ejemplarlibro" U1 
                    WHERE (U1."estado" = 'd' AND U1."libro_id" = ("catalogo_libro"."id")) LIMIT 1))
 ORDER BY "catalogo_libro"."titulo" ASC
 LIMIT 21

"""

# 11. Libros con múltiples filtros combinados
libros = Libro.objects.filter(
    Q(autor__apellido='Cervantes') &
    (Q(genero__nombre='Novela') | Q(genero__nombre='Clásico')) &
    ~Q(ejemplares__estado='m')
    ).distinct()


"""
SQL:
SELECT DISTINCT "catalogo_libro"."id",
       "catalogo_libro"."titulo",
       "catalogo_libro"."autor_id",
       "catalogo_libro"."resumen",
       "catalogo_libro"."isbn",
       "catalogo_libro"."idioma"
  FROM "catalogo_libro"
 INNER JOIN "catalogo_autor"
    ON ("catalogo_libro"."autor_id" = "catalogo_autor"."id")
 INNER JOIN "catalogo_libro_genero"
    ON ("catalogo_libro"."id" = "catalogo_libro_genero"."libro_id")
 INNER JOIN "catalogo_genero"
    ON ("catalogo_libro_genero"."genero_id" = "catalogo_genero"."id")
 WHERE ("catalogo_autor"."apellido" = 'Cervantes' 
 AND ("catalogo_genero"."nombre" = 'Novela' OR "catalogo_genero"."nombre" = 'Clásico') 
 AND NOT (EXISTS(
                SELECT 1 AS "a" 
                FROM "catalogo_ejemplarlibro" U1 
                WHERE (U1."estado" = 'm' AND U1."libro_id" = ("catalogo_libro"."id")) LIMIT 1)))
 ORDER BY "catalogo_libro"."titulo" ASC
 LIMIT 21

"""