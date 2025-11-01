from django.urls import path
from apps.accounts import api

urlpatterns = [
    path('aluno/<int:aluno_id>/turmas/', api.turmas_json, name='api_aluno_turmas'),
    path('turma/<int:turma_id>/recursos/', api.recursos_json, name='api_turma_recursos'),
]
