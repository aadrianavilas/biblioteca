from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Count, Q
from .models import Libro, Autor, EjemplarLibro, Genero

def index(request):
    """Vista para la página de inicio del sitio."""
    # Generar contadores para algunos de los objetos principales
    num_libros = Libro.objects.count()
    num_ejemplares = EjemplarLibro.objects.count()
    num_ejemplares_disponibles = EjemplarLibro.objects.filter(estado='d').count()
    num_autores = Autor.objects.count()
    # Libros que contienen 'novela' en el título
    num_libros_novela = Libro.objects.filter(titulo__icontains='novela').count()
    context = {
        'num_libros': num_libros,
        'num_ejemplares': num_ejemplares,
        'num_ejemplares_disponibles': num_ejemplares_disponibles,
        'num_autores': num_autores,
        'num_libros_novela': num_libros_novela,
    }
    return render(request, 'index.html', context=context)


class LibroListView(generic.ListView):
    model = Libro
    paginate_by = 10
    template_name='lista_libro.html'
    def get_queryset(self):

        # Filtrar por términos de búsqueda si hay alguno
        query = self.request.GET.get('q')
        if query:
            return Libro.objects.filter(
            Q(titulo__icontains=query) |
            Q(autor__nombre__icontains=query) |
            Q(autor__apellido__icontains=query)
            ).select_related('autor')
        
            # Devolver todos los libros
        return Libro.objects.select_related('autor')
    
    def get_context_data(self, **kwargs):
    # Llamar a la implementación base para obtener el contexto
        context = super().get_context_data(**kwargs)

        # Agregar estadísticas de libros al contexto
        context['generos_populares'] = Genero.objects.annotate(
        num_libros=Count('libros_genero')
        ).order_by('-num_libros')[:5]

        context['nombre_buscador']='Libro'
        context['placeholder_buscador']='titulo,nombre...'
        return context
    

class LibroDetailView(generic.DetailView):
    model = Libro
    template_name='libro_detalle.html'
    def get_queryset(self):
        # Optimizar consulta cargando relacionados
        return Libro.objects.select_related('autor').prefetch_related('genero', 'ejemplares')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Añadir información de disponibilidad de ejemplares
        libro = self.get_object()
        context['ejemplares_disponibles'] = libro.ejemplares.filter(estado='d').count()

        # Libros relacionados (mismo autor o géneros)
        context['libros_relacionados'] = Libro.objects.filter(
        Q(autor=libro.autor) | Q(genero__in=libro.genero.all())
        ).exclude(id=libro.id).distinct()[:5]
        return context
    

class AutorListView(generic.ListView):
    model=Autor
    paginate_by=10
    template_name='lista_autores.html'

    def get_queryset(self):
        #Autores con más libros
        
        query = self.request.GET.get('q')
        if query:
            return Autor.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(fecha_nacimiento__icontains=query)
            )
        return Autor.objects.prefetch_related('libros')
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)

        context['autor_mas_libros']=Autor.objects.prefetch_related('libros').annotate(
            cant=Count('libros')
        ).order_by('-cant').first()     

        context['total_autores']=Autor.objects.count()
        context['nombre_buscador']='Autor'
        context['placeholder_buscador']='nombre,apellido'

        return context
    

class AutorDetailView(generic.DetailView):
    model=Autor
    template_name='autor_detalle.html'
    def get_queryset(self):
        return Autor.objects.prefetch_related('libros')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        autor=self.get_object()
        context['cant_ejemplares']=autor.libros.annotate(
            cantidad=Count('ejemplares')
        )

        context['ejemplares_disponibles']=autor.libros.filter(ejemplares__estado='d')
        return context
    

class GeneroListView(generic.ListView):
    model=Genero
    template_name='lista_genero.html'
    paginate_by=12

    def get_queryset(self):
        query=self.request.GET.get('q')
        if query:
            return Genero.objects.filter(nombre__icontains=query)
        return Genero.objects.prefetch_related('libros_genero')
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        context['generos_populares']=Genero.objects.prefetch_related('libros_genero').annotate(
            cantidad_libros=Count('libros_genero')
        ).order_by('-cantidad_libros')[:3]

        context['total_generos']=Genero.objects.count()

        context['nombre_buscador']='Genero'
        context['placeholder_buscador']='nombre'

        return context
    
class GeneroDetailView(generic.DetailView):
    model=Genero
    template_name='generos_libros.html'

    def get_queryset(self):
        return Genero.objects.prefetch_related('libros_genero')
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        genero=self.get_object()
        context['cantidad_libros_genero']=genero.libros_genero.count()

        return context
