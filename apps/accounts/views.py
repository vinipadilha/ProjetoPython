from django.shortcuts import render, get_object_or_404
from apps.trainings.models import Turma
from apps.resourcesapp.models import Recurso
from apps.enrollments.models import Matricula
from django.utils import timezone


def turmas(request):
    aluno_id = 1
    turmas = Turma.objects.filter(matriculas__aluno_id=aluno_id)

    return render(request, 'aluno/turmas.html', {
        'turmas': turmas
    })

def turma_recursos(request, turma_id):
    aluno_id = 1
    turma = get_object_or_404(Turma, pk=turma_id)
    
    recursos = Recurso.objects.filter(turma_id=turma_id)

    recursos_visiveis = []
    for r in recursos:
        if turma.tru_data_inicio > timezone.now():
            if r.rec_acesso_previo:
                recursos_visiveis.append(r)
        else:
            if not r.rec_draft:
                recursos_visiveis.append(r)

    return render(request, 'aluno/recursos.html', {
        'turma': turma,
        'recursos': recursos_visiveis
    })
