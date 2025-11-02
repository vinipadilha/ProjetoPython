from django.contrib import admin
from .models import Matricula

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'turma', 'mat_cadastrado_em')
    list_filter = ('turma',)
    search_fields = ('usuario__usu_nome', 'turma__tru_nome')
