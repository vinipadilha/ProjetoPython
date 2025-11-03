from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db import connection
from apps.trainings.models import Treinamento, Turma
from apps.accounts.models import Usuario
from apps.enrollments.models import Matricula
from apps.resourcesapp.models import Recurso
from apps.accounts.services.current_user import get_usuario_from_request
from apps.accounts.roles import ROLE_ADMIN, ROLE_STUDENT

def is_admin(user):
    # Verifica se é uma instância de Usuario do nosso modelo customizado
    try:
        from apps.accounts.models import Usuario
        if isinstance(user, Usuario):
            return user.perfil_id == ROLE_ADMIN
        # Se não for Usuario, tenta verificar propriedades padrão
        if hasattr(user, 'is_admin'):
            return user.is_admin
        return getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False)
    except Exception:
        # Fallback seguro
        return getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False)

@login_required
@user_passes_test(is_admin)
def listar_treinamentos(request):
    treinamentos = Treinamento.objects.all().order_by('-tre_cadastrado_em')
    return render(request, 'admin/treinamentos/listar.html', {
        'treinamentos': treinamentos
    })

@login_required
@user_passes_test(is_admin)
def criar_treinamento(request):
    if request.method == 'POST':
        nome = request.POST.get('tre_nome')
        descricao = request.POST.get('tre_descricao', '')
        
        if nome:
            treinamento = Treinamento.objects.create(
                tre_nome=nome,
                tre_descricao=descricao,
                tre_cadastrado_em=timezone.now()
            )
            messages.success(request, 'Treinamento criado com sucesso!')
            return redirect('admin_treinamentos_listar')
        else:
            messages.error(request, 'O nome do treinamento é obrigatório.')
    
    return render(request, 'admin/treinamentos/form.html', {
        'treinamento': None,
        'action': 'Criar'
    })

@login_required
@user_passes_test(is_admin)
def editar_treinamento(request, tre_id):
    treinamento = get_object_or_404(Treinamento, pk=tre_id)
    
    if request.method == 'POST':
        nome = request.POST.get('tre_nome')
        descricao = request.POST.get('tre_descricao', '')
        
        if nome:
            treinamento.tre_nome = nome
            treinamento.tre_descricao = descricao
            treinamento.save()
            messages.success(request, 'Treinamento atualizado com sucesso!')
            return redirect('admin_treinamentos_listar')
        else:
            messages.error(request, 'O nome do treinamento é obrigatório.')
    
    return render(request, 'admin/treinamentos/form.html', {
        'treinamento': treinamento,
        'action': 'Editar'
    })

@login_required
@user_passes_test(is_admin)
def excluir_treinamento(request, tre_id):
    treinamento = get_object_or_404(Treinamento, pk=tre_id)
    
    if request.method == 'POST':
        treinamento.delete()
        messages.success(request, 'Treinamento excluído com sucesso!')
        return redirect('admin_treinamentos_listar')
    
    return redirect('admin_treinamentos_listar')

@login_required
def listar_turmas(request):
    # Verifica se é admin usando o context processor
    usuario = get_usuario_from_request(request)
    if not usuario or usuario.perfil_id != ROLE_ADMIN:
        return redirect('/aluno/turmas/')
    
    turmas = Turma.objects.select_related('treinamento').all().order_by('-tru_data_inicio')
    return render(request, 'admin/turmas/listar.html', {
        'turmas': turmas
    })

@login_required
@user_passes_test(is_admin)
def criar_turma(request):
    treinamentos = Treinamento.objects.all().order_by('tre_nome')
    
    if request.method == 'POST':
        nome = request.POST.get('tru_nome')
        treinamento_id = request.POST.get('treinamento')
        data_inicio = request.POST.get('tru_data_inicio')
        data_conclusao = request.POST.get('tru_data_conclusao', None)
        link_acesso = request.POST.get('tru_link_acesso', '')
        
        if nome and treinamento_id and data_inicio:
            treinamento = get_object_or_404(Treinamento, pk=treinamento_id)
            turma = Turma.objects.create(
                tru_nome=nome,
                treinamento=treinamento,
                tru_data_inicio=data_inicio,
                tru_data_conclusao=data_conclusao if data_conclusao else None,
                tru_link_acesso=link_acesso if link_acesso else None,
                tru_cadastrado_em=timezone.now()
            )
            messages.success(request, 'Turma criada com sucesso!')
            return redirect('admin_turmas_listar')
        else:
            messages.error(request, 'Nome, treinamento e data de início são obrigatórios.')
    
    return render(request, 'admin/turmas/form.html', {
        'turma': None,
        'treinamentos': treinamentos,
        'action': 'Criar'
    })

@login_required
@user_passes_test(is_admin)
def editar_turma(request, tru_id):
    turma = get_object_or_404(Turma, pk=tru_id)
    treinamentos = Treinamento.objects.all().order_by('tre_nome')
    
    if request.method == 'POST':
        nome = request.POST.get('tru_nome')
        treinamento_id = request.POST.get('treinamento')
        data_inicio = request.POST.get('tru_data_inicio')
        data_conclusao = request.POST.get('tru_data_conclusao', None)
        link_acesso = request.POST.get('tru_link_acesso', '')
        
        if nome and treinamento_id and data_inicio:
            treinamento = get_object_or_404(Treinamento, pk=treinamento_id)
            turma.tru_nome = nome
            turma.treinamento = treinamento
            turma.tru_data_inicio = data_inicio
            turma.tru_data_conclusao = data_conclusao if data_conclusao else None
            turma.tru_link_acesso = link_acesso if link_acesso else None
            turma.save()
            messages.success(request, 'Turma atualizada com sucesso!')
            return redirect('admin_turmas_listar')
        else:
            messages.error(request, 'Nome, treinamento e data de início são obrigatórios.')
    
    return render(request, 'admin/turmas/form.html', {
        'turma': turma,
        'treinamentos': treinamentos,
        'action': 'Editar'
    })

@login_required
@user_passes_test(is_admin)
def excluir_turma(request, tru_id):
    turma = get_object_or_404(Turma, pk=tru_id)
    
    if request.method == 'POST':
        turma.delete()
        messages.success(request, 'Turma excluída com sucesso!')
        return redirect('admin_turmas_listar')
    
    return redirect('admin_turmas_listar')

@login_required
def dashboard_turma(request, tru_id):
    """Dashboard da turma mostrando alunos matriculados e recursos"""
    usuario = get_usuario_from_request(request)
    if not usuario or usuario.perfil_id != ROLE_ADMIN:
        return redirect('/aluno/turmas/')
    
    turma = get_object_or_404(Turma.objects.select_related('treinamento'), pk=tru_id)
    
    # Alunos matriculados nesta turma
    alunos_matriculados = Usuario.objects.filter(
        matriculas__turma_id=tru_id
    ).select_related('perfil').order_by('usu_nome')
    
    # Todos os alunos (para o select de adicionar)
    todos_alunos = Usuario.objects.filter(
        perfil_id=ROLE_STUDENT
    ).exclude(
        matriculas__turma_id=tru_id
    ).order_by('usu_nome')
    
    # Recursos da turma
    recursos = Recurso.objects.filter(turma_id=tru_id).order_by('rec_nome')
    
    # Processar adição de aluno
    if request.method == 'POST' and 'adicionar_aluno' in request.POST:
        aluno_id = request.POST.get('aluno_id')
        if aluno_id:
            try:
                aluno = get_object_or_404(Usuario, pk=aluno_id, perfil_id=ROLE_STUDENT)
                # Verifica se já está matriculado
                if not Matricula.objects.filter(turma_id=tru_id, usuario_id=aluno_id).exists():
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO matricula (matTruId, matUsuId, matCadastradoEm)
                            VALUES (%s, %s, %s)
                        """, [tru_id, aluno_id, timezone.now()])
                    messages.success(request, f'Aluno {aluno.usu_nome} matriculado com sucesso!')
                    return redirect('admin_turma_dashboard', tru_id=tru_id)
                else:
                    messages.error(request, 'Este aluno já está matriculado nesta turma.')
            except Exception as e:
                messages.error(request, f'Erro ao matricular aluno: {str(e)}')
    
    return render(request, 'admin/turmas/dashboard.html', {
        'turma': turma,
        'alunos_matriculados': alunos_matriculados,
        'todos_alunos': todos_alunos,
        'recursos': recursos
    })

@login_required
def remover_matricula(request, tru_id, usu_id):
    """Remove um aluno de uma turma"""
    usuario = get_usuario_from_request(request)
    if not usuario or usuario.perfil_id != ROLE_ADMIN:
        return redirect('/aluno/turmas/')
    
    turma = get_object_or_404(Turma, pk=tru_id)
    aluno = get_object_or_404(Usuario, pk=usu_id)
    
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM matricula 
                    WHERE matTruId = %s AND matUsuId = %s
                """, [tru_id, usu_id])
            messages.success(request, f'Aluno {aluno.usu_nome} removido da turma com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao remover aluno: {str(e)}')
    
    return redirect('admin_turma_dashboard', tru_id=tru_id)

