# biblioteca/urls.py
from django.urls import path
from . import views

app_name = 'biblioteca'

urlpatterns = [
    path('', views.lista_livros, name='lista_livros'),
    path('livro/novo/', views.novo_livro, name='novo_livro'),

    path('emprestimo/novo/', views.novo_emprestimo, name='novo_emprestimo'),
    path('emprestimos/', views.lista_emprestimos, name='lista_emprestimos'),
    path('emprestimo/<int:pk>/devolver/', views.devolver_emprestimo,
         name='devolver_emprestimo'),

    path('livro/<int:livro_id>/resenha/nova/', views.nova_resenha,
         name='nova_resenha'),
    path('livro/<int:livro_id>/resenhas/', views.lista_resenhas,
         name='lista_resenhas'),
]