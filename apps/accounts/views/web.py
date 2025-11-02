from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.trainings.models import Turma, Treinamento
from apps.resourcesapp.models import Recurso
from apps.resourcesapp.services.access_rules import recursos_visiveis
from apps.accounts.models import Usuario
from apps.enrollments.models import Matricula
from apps.accounts.services.current_user import get_usuario_from_request
from apps.accounts.roles import ROLE_ADMIN

@login_required
def pos_login(request):
    u = get_usuario_from_request(request)
    if u:
        request.session['role_id'] = u.perfil_id
        request.session['role_name'] = u.perfil.pef_nome

    if u and u.perfil_id == ROLE_ADMIN:
        return redirect('/dashboard/')
    return redirect('/aluno/turmas/')

@login_required
def dashboard(request):
    u = get_usuario_from_request(request)
    if not u or u.perfil_id != ROLE_ADMIN:
        return redirect('/aluno/turmas/')
    
    stats = {
        'total_treinamentos': Treinamento.objects.count(),
        'total_turmas': Turma.objects.count(),
        'total_usuarios': Usuario.objects.count(),
        'total_matriculas': Matricula.objects.count(),
        'turmas_recentes': Turma.objects.select_related('treinamento').order_by('-tru_data_inicio')[:5],
        'treinamentos_recentes': Treinamento.objects.order_by('-tre_cadastrado_em')[:5],
    }
    
    return render(request, 'admin/dashboard.html', {'usuario': u, 'stats': stats})

@login_required
def turmas(request):
    usuario = get_usuario_from_request(request)
    if not usuario:
        return redirect('/login/')
    
    turmas = Turma.objects.filter(matriculas__usuario_id=usuario.usu_id).select_related('treinamento').order_by('-tru_data_inicio')
    return render(request, 'aluno/listar.html', {'turmas': turmas, 'usuario': usuario})

@login_required
def turma_recursos(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id)
    recursos_qs = Recurso.objects.filter(turma_id=turma_id).order_by('rec_nome')
    recursos = recursos_visiveis(turma, list(recursos_qs))
    return render(request, 'aluno/recursos.html', {'turma': turma, 'recursos': recursos})
