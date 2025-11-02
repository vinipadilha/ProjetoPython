from django.urls import path
from apps.trainings.views import web

urlpatterns = [
    path('', web.listar_treinamentos, name='admin_treinamentos_listar'),
    path('criar/', web.criar_treinamento, name='admin_treinamentos_criar'),
    path('<int:tre_id>/editar/', web.editar_treinamento, name='admin_treinamentos_editar'),
    path('<int:tre_id>/excluir/', web.excluir_treinamento, name='admin_treinamentos_excluir'),
]
