from django.urls import path
from apps.trainings.views import web

urlpatterns = [
    path('treinamentos/', web.listar_treinamentos, name='admin_treinamentos_listar'),
]
