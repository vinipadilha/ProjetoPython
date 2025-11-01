from django.contrib import admin
from .models import Treinamento, Turma

@admin.register(Treinamento)
class TreinamentoAdmin(admin.ModelAdmin):
    list_display = ('tre_nome', 'tre_cadastrado_em')
    search_fields = ('tre_nome',)

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('tru_nome', 'treinamento', 'tru_data_inicio', 'tru_data_conclusao')
    list_filter = ('treinamento',)
    search_fields = ('tru_nome',)
