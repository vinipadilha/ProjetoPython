from django.contrib import admin
from .models import Recurso

@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('rec_nome', 'turma', 'rec_tipo', 'rec_acesso_previo', 'rec_draft', 'rec_cadastrado_em')
    list_filter = ('rec_tipo', 'rec_acesso_previo', 'rec_draft', 'turma')
    search_fields = ('rec_nome',)
