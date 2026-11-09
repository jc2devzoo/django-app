# biblioteca/admin.py
from django.contrib import admin
from .models import Livro, Emprestimo, Resenha, Profile


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'cdu', 'cdi', 'genero')
    search_fields = ('titulo', 'autor', 'cdu', 'cdi')


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('livro', 'usuario', 'data_emprestimo',
                    'data_devolucao_prevista', 'status')
    list_filter = ('status',)
    search_fields = ('livro__titulo', 'usuario__username')

    def has_delete_permission(self, request, obj=None):
        return False  # empréstimos nunca são apagados


@admin.register(Resenha)
class ResenhaAdmin(admin.ModelAdmin):
    list_display = ('livro', 'usuario', 'nota', 'criado_em')
    list_filter = ('nota',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo')
    list_filter = ('tipo',)
# Register your models here.
