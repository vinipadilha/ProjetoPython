from django.contrib import admin
from .models import Matricula

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'turma', 'mat_cadastrado_em')
    list_filter = ('turma',)
    search_fields = ('aluno__alu_nome', 'turma__tru_nome')
