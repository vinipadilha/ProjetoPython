from django.urls import path
from apps.accounts.views import web

# URLs para a raiz (sem prefixo)
urlpatterns = [
    path('pos-login/', web.pos_login, name='pos_login'),
    path('dashboard/', web.dashboard, name='dashboard'),
]

# URLs para alunos (com prefixo /aluno/)
aluno_urlpatterns = [
    path('turmas/', web.turmas, name='aluno_turmas'),
    path('turma/<int:turma_id>/recursos/', web.turma_recursos, name='aluno_recursos'),
]
