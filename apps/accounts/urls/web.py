from django.urls import path
from apps.accounts.views import web

# URLs para a raiz (sem prefixo)
urlpatterns = [
    path('pos-login/', web.pos_login, name='pos_login'),
    path('dashboard/', web.dashboard, name='dashboard'),
    path('usuarios/', web.listar_usuarios, name='admin_usuarios_listar'),
    path('usuarios/criar/', web.criar_usuario, name='admin_usuarios_criar'),
    path('usuarios/<int:usu_id>/editar/', web.editar_usuario, name='admin_usuarios_editar'),
    path('usuarios/<int:usu_id>/excluir/', web.excluir_usuario, name='admin_usuarios_excluir'),
]

# URLs para alunos (com prefixo /aluno/)
aluno_urlpatterns = [
    path('turmas/', web.turmas, name='aluno_turmas'),
    path('turma/<int:turma_id>/recursos/', web.turma_recursos, name='aluno_recursos'),
]
