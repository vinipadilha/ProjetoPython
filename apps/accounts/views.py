from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from apps.trainings.models import Turma
from apps.resourcesapp.models import Recurso
from apps.enrollments.models import Matricula
from apps.accounts.models import Aluno
from apps.resourcesapp.services.access_rules import recursos_visiveis

def _aluno_atual(request):
    return Aluno.objects.filter(alu_email=request.user.email).first()

@login_required
def turmas(request):
    aluno = _aluno_atual(request)
    turmas = Turma.objects.none()
    if aluno:
        turmas = Turma.objects.filter(matriculas__aluno_id=aluno.alu_id)
    return render(request, 'aluno/turmas.html', {'turmas': turmas, 'aluno': aluno})

@login_required
def turma_recursos(request, turma_id):
    aluno = _aluno_atual(request)
    turma = get_object_or_404(Turma, pk=turma_id)
    recursos_qs = Recurso.objects.filter(turma_id=turma_id).order_by('rec_nome')
    recursos = recursos_visiveis(turma, list(recursos_qs))
    return render(request, 'aluno/recursos.html', {'turma': turma, 'recursos': recursos, 'aluno': aluno})
