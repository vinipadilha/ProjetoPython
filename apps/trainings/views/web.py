from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from apps.trainings.models import Treinamento, Turma

def is_admin(user):
    if hasattr(user, 'is_admin'):
        return user.is_admin
    return user.is_staff or user.is_superuser

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
@user_passes_test(is_admin)
def listar_turmas(request):
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

