from django.contrib import admin

from catalogo.models import Autor, EjemplarLibro, Genero, Libro

# Register your models here.
admin.site.register(Genero)
admin.site.register(Autor)
admin.site.register(Libro)
admin.site.register(EjemplarLibro)
