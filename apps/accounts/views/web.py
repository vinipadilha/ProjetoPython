from django.shortcuts import render, get_object_or_404
from apps.trainings.models import Turma
from apps.resourcesapp.models import Recurso
from apps.resourcesapp.services.access_rules import recursos_visiveis

def turmas(request):
    aluno_id = 1
    turmas = Turma.objects.filter(matriculas__aluno_id=aluno_id)
    return render(request, 'aluno/turmas.html', {'turmas': turmas})

def turma_recursos(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id)
    recursos_qs = Recurso.objects.filter(turma_id=turma_id).order_by('rec_nome')
    recursos = recursos_visiveis(turma, list(recursos_qs))
    return render(request, 'aluno/recursos.html', {'turma': turma, 'recursos': recursos})
