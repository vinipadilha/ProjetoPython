from django.urls import path
from . import views

urlpatterns = [
    path('turmas/', views.turmas, name='aluno_turmas'),
    path('turma/<int:turma_id>/recursos/', views.turma_recursos, name='aluno_recursos'),
]
