from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db import connection
from django.utils import timezone
from apps.trainings.models import Turma, Treinamento
from apps.resourcesapp.models import Recurso
from apps.resourcesapp.services.access_rules import recursos_visiveis
from apps.accounts.models import Usuario, Perfil
from apps.enrollments.models import Matricula
from apps.accounts.services.current_user import get_usuario_from_request
from apps.accounts.roles import ROLE_ADMIN, ROLE_STUDENT

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
def listar_usuarios(request):
    """Lista todos os usuários (admin)"""
    usuario = get_usuario_from_request(request)
    if not usuario or usuario.perfil_id != ROLE_ADMIN:
        return redirect('/aluno/turmas/')
    
    usuarios = Usuario.objects.select_related('perfil').prefetch_related(
        'matriculas__turma__treinamento'
    ).all().order_by('usu_nome')
    
    return render(request, 'admin/usuarios/listar.html', {
        'usuarios': usuarios
    })

@login_required
def criar_usuario(request):
    """Cria um novo usuário"""
    usuario = get_usuario_from_request(request)
    if not usuario or usuario.perfil_id != ROLE_ADMIN:
        return redirect('/aluno/turmas/')
    
    perfis = Perfil.objects.all().order_by('pef_nome')
    
    if request.method == 'POST':
        nome = request.POST.get('usu_nome')
        email = request.POST.get('usu_email')
        telefone = request.POST.get('usu_telefone', '')
        perfil_id = request.POST.get('perfil')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        # Validações
        if not nome or not email or not perfil_id or not senha:
            messages.error(request, 'Nome, email, perfil e senha são obrigatórios.')
        elif senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
        elif len(senha) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
        else:
            # Verifica se o email já existe
            if Usuario.objects.filter(usu_email=email).exists():
                messages.error(request, 'Este email já está cadastrado.')
            else:
                try:
                    perfil = get_object_or_404(Perfil, pk=perfil_id)
                    senha_hasheada = make_password(senha)
                    
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO usuario (usuPefId, usuNome, usuEmail, usuTelefone, usuSenha, usuCadastradoEm, is_active, is_staff, is_superuser)
                            VALUES (%s, %s, %s, %s, %s, %s, 1, 0, 0)
                        """, [perfil_id, nome, email, telefone if telefone else None, senha_hasheada, timezone.now()])
                    
                    messages.success(request, 'Usuário criado com sucesso!')
                    return redirect('admin_usuarios_listar')
                except Exception as e:
                    messages.error(request, f'Erro ao criar usuário: {str(e)}')
    
    return render(request, 'admin/usuarios/form.html', {
        'usuario': None,
        'perfis': perfis,
        'action': 'Criar'
    })

@login_required
def editar_usuario(request, usu_id):
    """Edita um usuário existente"""
    usuario = get_usuario_from_request(request)
    if not usuario or usuario.perfil_id != ROLE_ADMIN:
        return redirect('/aluno/turmas/')
    
    usuario_obj = get_object_or_404(Usuario, pk=usu_id)
    perfis = Perfil.objects.all().order_by('pef_nome')
    
    if request.method == 'POST':
        nome = request.POST.get('usu_nome')
        email = request.POST.get('usu_email')
        telefone = request.POST.get('usu_telefone', '')
        perfil_id = request.POST.get('perfil')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        # Validações
        if not nome or not email or not perfil_id:
            messages.error(request, 'Nome, email e perfil são obrigatórios.')
        elif senha and senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
        elif senha and len(senha) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
        else:
            # Verifica se o email já existe (exceto o próprio usuário)
            if Usuario.objects.filter(usu_email=email).exclude(pk=usu_id).exists():
                messages.error(request, 'Este email já está cadastrado.')
            else:
                try:
                    perfil = get_object_or_404(Perfil, pk=perfil_id)
                    
                    with connection.cursor() as cursor:
                        if senha and senha.strip():
                            senha_hasheada = make_password(senha)
                            cursor.execute("""
                                UPDATE usuario 
                                SET usuEmail = %s, usuNome = %s, usuTelefone = %s, usuPefId = %s, usuSenha = %s
                                WHERE usuId = %s
                            """, [email, nome, telefone if telefone else None, perfil_id, senha_hasheada, usu_id])
                        else:
                            cursor.execute("""
                                UPDATE usuario 
                                SET usuEmail = %s, usuNome = %s, usuTelefone = %s, usuPefId = %s
                                WHERE usuId = %s
                            """, [email, nome, telefone if telefone else None, perfil_id, usu_id])
                    
                    messages.success(request, 'Usuário atualizado com sucesso!')
                    return redirect('admin_usuarios_listar')
                except Exception as e:
                    messages.error(request, f'Erro ao atualizar usuário: {str(e)}')
    
    return render(request, 'admin/usuarios/form.html', {
        'usuario': usuario_obj,
        'perfis': perfis,
        'action': 'Editar'
    })

@login_required
def excluir_usuario(request, usu_id):
    """Exclui um usuário"""
    usuario = get_usuario_from_request(request)
    if not usuario or usuario.perfil_id != ROLE_ADMIN:
        return redirect('/aluno/turmas/')
    
    usuario_obj = get_object_or_404(Usuario, pk=usu_id)
    
    if request.method == 'POST':
        try:
            # Não permite excluir o próprio usuário
            if usuario_obj.usu_id == usuario.usu_id:
                messages.error(request, 'Você não pode excluir seu próprio usuário.')
            else:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM usuario WHERE usuId = %s", [usu_id])
                messages.success(request, 'Usuário excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir usuário: {str(e)}')
        return redirect('admin_usuarios_listar')
    
    return redirect('admin_usuarios_listar')

@login_required
def turmas(request):
    usuario = get_usuario_from_request(request)
    if not usuario:
        return redirect('/login/')
    
    turmas = Turma.objects.filter(matriculas__usuario_id=usuario.usu_id).select_related('treinamento').order_by('-tru_data_inicio')
    return render(request, 'aluno/listar.html', {'turmas': turmas, 'usuario': usuario})

@login_required
def turma_recursos(request, turma_id):
    usuario = get_usuario_from_request(request)
    if not usuario:
        return redirect('/login/')
    
    turma = get_object_or_404(Turma.objects.select_related('treinamento'), pk=turma_id)
    
    # Verifica se o aluno está matriculado nesta turma
    if not Matricula.objects.filter(turma_id=turma_id, usuario_id=usuario.usu_id).exists():
        messages.error(request, 'Você não está matriculado nesta turma.')
        return redirect('aluno_turmas')
    
    recursos_qs = Recurso.objects.filter(turma_id=turma_id).order_by('rec_nome')
    recursos = recursos_visiveis(turma, list(recursos_qs))
    
    # Determina o status da turma para exibir mensagem adequada
    from datetime import date
    agora = timezone.now().date()
    data_inicio = turma.tru_data_inicio
    if hasattr(data_inicio, 'date'):
        data_inicio = data_inicio.date()
    elif isinstance(data_inicio, date):
        data_inicio = data_inicio
    
    turma_iniciada = data_inicio <= agora
    
    return render(request, 'aluno/recursos.html', {
        'turma': turma, 
        'recursos': recursos,
        'turma_iniciada': turma_iniciada,
        'data_inicio': data_inicio
    })
