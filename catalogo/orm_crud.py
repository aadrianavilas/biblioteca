from catalogo.models import Autor

#Create (Crear)
# Método 1: Crear y guardar
autor = Autor(nombre="Gabriel", apellido="García Márquez")
autor.save()

# Método 2: Crear con create()
autor = Autor.objects.create(nombre="Gabriel", apellido="García Márquez")

"""
SQL:
INSERT INTO myapp_autor (nombre, apellido)
VALUES ('Gabriel', 'García Márquez');
"""

#Read (Leer)
# Obtener todos los registros
autores = Autor.objects.all()

# Obtener un registro por su clave primaria
autor = Autor.objects.get(pk=1)

# Obtener el primer registro que cumpla con ciertos criterios
autor = Autor.objects.filter(apellido="García Márquez").first()

"""
SQL:
SELECT * FROM myapp_autor;
SELECT * FROM myapp_autor WHERE id = 1;
SELECT * FROM myapp_autor WHERE apellido = 'García Márquez' LIMIT 1;
"""

#Update (Actualizar)
# Método 1: Obtener, modificar y guardar
autor = Autor.objects.get(pk=1)
autor.nombre = "Gabriel José"
autor.save()

# Método 2: Actualizar directamente
Autor.objects.filter(pk=1).update(nombre="Gabriel José")

"""
SQL:
UPDATE myapp_autor SET nombre = 'Gabriel José' WHERE id = 1;
"""

#Delete (Eliminar)
# Método 1: Obtener y eliminar
autor = Autor.objects.get(pk=1)
autor.delete()

# Método 2: Eliminar directamente
Autor.objects.filter(apellido="García Márquez").delete()

"""
SQL:
DELETE FROM myapp_autor WHERE id = 1;
DELETE FROM myapp_autor WHERE apellido = 'García Márquez';
"""