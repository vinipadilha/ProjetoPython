from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from apps.trainings.models import Treinamento

def is_admin(user):
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

