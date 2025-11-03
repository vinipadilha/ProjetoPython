from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.resourcesapp.models import Recurso
from apps.trainings.models import Turma
from apps.accounts.services.current_user import get_usuario_from_request
from apps.accounts.roles import ROLE_ADMIN

@login_required
def listar_recursos(request, turma_id):
    """Lista todos os recursos de uma turma (admin)"""
    usuario = get_usuario_from_request(request)
    if not usuario or usuario.perfil_id != ROLE_ADMIN:
        return redirect('/aluno/turmas/')
    
    turma = get_object_or_404(Turma, pk=turma_id)
    recursos = Recurso.objects.filter(turma_id=turma_id).order_by('rec_nome')
    
    return render(request, 'admin/recursos/listar.html', {
        'turma': turma,
        'recursos': recursos
    })

@login_required
def criar_recurso(request, turma_id):
    """Cria um novo recurso para uma turma"""
    usuario = get_usuario_from_request(request)
    if not usuario or usuario.perfil_id != ROLE_ADMIN:
        return redirect('/aluno/turmas/')
    
    turma = get_object_or_404(Turma, pk=turma_id)
    
    if request.method == 'POST':
        nome = request.POST.get('rec_nome')
        tipo = request.POST.get('rec_tipo')
        descricao = request.POST.get('rec_descricao', '')
        arquivo_path = request.POST.get('rec_arquivo_path', '')
        acesso_previo = request.POST.get('rec_acesso_previo') == 'on'
        draft = request.POST.get('rec_draft') == 'on'
        
        if nome and tipo:
            recurso = Recurso.objects.create(
                turma=turma,
                rec_nome=nome,
                rec_tipo=tipo,
                rec_descricao=descricao if descricao else None,
                rec_arquivo_path=arquivo_path if arquivo_path else '',
                rec_acesso_previo=acesso_previo,
                rec_draft=draft,
                rec_cadastrado_em=timezone.now()
            )
            messages.success(request, 'Recurso criado com sucesso!')
            return redirect('admin_recursos_listar', turma_id=turma_id)
        else:
            messages.error(request, 'Nome e tipo são obrigatórios.')
    
    return render(request, 'admin/recursos/form.html', {
        'turma': turma,
        'recurso': None,
        'action': 'Criar'
    })

@login_required
def editar_recurso(request, turma_id, rec_id):
    """Edita um recurso existente"""
    usuario = get_usuario_from_request(request)
    if not usuario or usuario.perfil_id != ROLE_ADMIN:
        return redirect('/aluno/turmas/')
    
    turma = get_object_or_404(Turma, pk=turma_id)
    recurso = get_object_or_404(Recurso, pk=rec_id, turma_id=turma_id)
    
    if request.method == 'POST':
        nome = request.POST.get('rec_nome')
        tipo = request.POST.get('rec_tipo')
        descricao = request.POST.get('rec_descricao', '')
        arquivo_path = request.POST.get('rec_arquivo_path', '')
        acesso_previo = request.POST.get('rec_acesso_previo') == 'on'
        draft = request.POST.get('rec_draft') == 'on'
        
        if nome and tipo:
            recurso.rec_nome = nome
            recurso.rec_tipo = tipo
            recurso.rec_descricao = descricao if descricao else None
            recurso.rec_arquivo_path = arquivo_path if arquivo_path else ''
            recurso.rec_acesso_previo = acesso_previo
            recurso.rec_draft = draft
            recurso.save()
            messages.success(request, 'Recurso atualizado com sucesso!')
            return redirect('admin_recursos_listar', turma_id=turma_id)
        else:
            messages.error(request, 'Nome e tipo são obrigatórios.')
    
    return render(request, 'admin/recursos/form.html', {
        'turma': turma,
        'recurso': recurso,
        'action': 'Editar'
    })

@login_required
def excluir_recurso(request, turma_id, rec_id):
    """Exclui um recurso"""
    usuario = get_usuario_from_request(request)
    if not usuario or usuario.perfil_id != ROLE_ADMIN:
        return redirect('/aluno/turmas/')
    
    turma = get_object_or_404(Turma, pk=turma_id)
    recurso = get_object_or_404(Recurso, pk=rec_id, turma_id=turma_id)
    
    if request.method == 'POST':
        recurso.delete()
        messages.success(request, 'Recurso excluído com sucesso!')
        return redirect('admin_recursos_listar', turma_id=turma_id)
    
    return redirect('admin_recursos_listar', turma_id=turma_id)

