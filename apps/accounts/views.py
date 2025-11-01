from django.shortcuts import render
from django.utils import timezone
from apps.trainings.models import Turma
from apps.resourcesapp.models import Recurso
from apps.enrollments.models import Matricula

def turmas(request):
    aluno_id = 1 
    turmas = Turma.objects.filter(matriculas__aluno_id=aluno_id)
    return render(request, 'aluno/turmas.html', {'turmas': turmas})

def turma_recursos(request, turma_id):
    recursos = Recurso.objects.filter(turma_id=turma_id)
    return render(request, 'aluno/recursos.html', {'recursos': recursos})
