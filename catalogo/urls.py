from django.urls import path
from catalogo.views import index,LibroListView,LibroDetailView,AutorListView,AutorDetailView,GeneroListView,GeneroDetailView

urlpatterns = [
    path('',index,name='index'),
    path('libro/listView/',LibroListView.as_view(),name='libro_list_view'),
    path('libroDetails/<int:pk>/',LibroDetailView.as_view(),name='libro-detail'),
    path('listAutores/',AutorListView.as_view(),name='list_autores'),
    path('AutorDetails/<int:pk>',AutorDetailView.as_view(),name='autor-detail'),
    path('listGeneros/',GeneroListView.as_view(),name='list_generos'),
    path('GeneroDetail/<int:pk>',GeneroDetailView.as_view(),name='genero-detail')
]