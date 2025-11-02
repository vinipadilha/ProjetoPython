from django.urls import path
from apps.trainings.views import web

urlpatterns = [
    path('', web.listar_turmas, name='admin_turmas_listar'),
    path('criar/', web.criar_turma, name='admin_turmas_criar'),
    path('<int:tru_id>/editar/', web.editar_turma, name='admin_turmas_editar'),
    path('<int:tru_id>/excluir/', web.excluir_turma, name='admin_turmas_excluir'),
]
