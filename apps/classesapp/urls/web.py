from django.urls import path
from apps.trainings.views import web

urlpatterns = [
    path('', web.listar_turmas, name='admin_turmas_listar'),
    path('criar/', web.criar_turma, name='admin_turmas_criar'),
    path('<int:tru_id>/editar/', web.editar_turma, name='admin_turmas_editar'),
    path('<int:tru_id>/excluir/', web.excluir_turma, name='admin_turmas_excluir'),
    path('<int:tru_id>/dashboard/', web.dashboard_turma, name='admin_turma_dashboard'),
    path('<int:tru_id>/aluno/<int:usu_id>/remover/', web.remover_matricula, name='admin_remover_matricula'),
]
