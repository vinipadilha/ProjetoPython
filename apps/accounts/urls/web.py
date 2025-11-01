from django.urls import path
from apps.accounts.views import web

urlpatterns = [
    path('turmas/', web.turmas, name='aluno_turmas'),
    path('turma/<int:turma_id>/recursos/', web.turma_recursos, name='aluno_recursos'),
]
