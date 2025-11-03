from django.urls import path
from apps.resourcesapp.views import web

urlpatterns = [
    path('turma/<int:turma_id>/recursos/', web.listar_recursos, name='admin_recursos_listar'),
    path('turma/<int:turma_id>/recursos/criar/', web.criar_recurso, name='admin_recursos_criar'),
    path('turma/<int:turma_id>/recursos/<int:rec_id>/editar/', web.editar_recurso, name='admin_recursos_editar'),
    path('turma/<int:turma_id>/recursos/<int:rec_id>/excluir/', web.excluir_recurso, name='admin_recursos_excluir'),
]
