from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.db import connection
import os
from pathlib import Path
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
        
        arquivo_upload = request.FILES.get('rec_arquivo')
        arquivo_final_path = arquivo_path
        
        # Processa upload de arquivo se fornecido
        if arquivo_upload:
            # Define diretório baseado no tipo
            if tipo == 'VIDEO':
                upload_dir = settings.MEDIA_ROOT / 'videos' / f'turma_{turma_id}'
            else:
                upload_dir = settings.MEDIA_ROOT / 'recursos' / f'turma_{turma_id}'
            
            # Cria diretório se não existir
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            # Gera nome único para o arquivo
            from django.utils.text import slugify
            nome_arquivo = f"{slugify(nome)}_{timezone.now().strftime('%Y%m%d_%H%M%S')}{Path(arquivo_upload.name).suffix}"
            arquivo_path_full = upload_dir / nome_arquivo
            
            # Salva arquivo
            with open(arquivo_path_full, 'wb+') as destination:
                for chunk in arquivo_upload.chunks():
                    destination.write(chunk)
            
            # Define URL do arquivo
            if tipo == 'VIDEO':
                arquivo_final_path = f"/media/videos/turma_{turma_id}/{nome_arquivo}"
            else:
                arquivo_final_path = f"/media/recursos/turma_{turma_id}/{nome_arquivo}"
        elif not arquivo_path:
            messages.error(request, 'É necessário fornecer um arquivo ou uma URL.')
            return render(request, 'admin/recursos/form.html', {
                'turma': turma,
                'recurso': None,
                'action': 'Criar'
            })
        
        if nome and tipo:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO recurso (recTruId, recNome, recTipo, recDescricao, recArquivoPath, recAcessoPrevio, recDraft, recCadastradoEm)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [
                    turma_id,
                    nome,
                    tipo,
                    descricao if descricao else None,
                    arquivo_final_path,
                    1 if acesso_previo else 0,
                    1 if draft else 0,
                    timezone.now()
                ])
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
        
        arquivo_upload = request.FILES.get('rec_arquivo')
        arquivo_final_path = arquivo_path or recurso.rec_arquivo_path
        
        # Processa upload de arquivo se fornecido
        if arquivo_upload:
            # Remove arquivo antigo se existir e for um arquivo local
            if recurso.rec_arquivo_path and recurso.rec_arquivo_path.startswith('/media/'):
                arquivo_antigo = settings.MEDIA_ROOT / recurso.rec_arquivo_path.replace('/media/', '')
                if arquivo_antigo.exists():
                    try:
                        arquivo_antigo.unlink()
                    except Exception:
                        pass  # Ignora erros ao deletar arquivo antigo
            
            # Define diretório baseado no tipo
            if tipo == 'VIDEO':
                upload_dir = settings.MEDIA_ROOT / 'videos' / f'turma_{turma_id}'
            else:
                upload_dir = settings.MEDIA_ROOT / 'recursos' / f'turma_{turma_id}'
            
            # Cria diretório se não existir
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            # Gera nome único para o arquivo
            from django.utils.text import slugify
            nome_arquivo = f"{slugify(nome)}_{timezone.now().strftime('%Y%m%d_%H%M%S')}{Path(arquivo_upload.name).suffix}"
            arquivo_path_full = upload_dir / nome_arquivo
            
            # Salva arquivo
            with open(arquivo_path_full, 'wb+') as destination:
                for chunk in arquivo_upload.chunks():
                    destination.write(chunk)
            
            # Define URL do arquivo
            if tipo == 'VIDEO':
                arquivo_final_path = f"/media/videos/turma_{turma_id}/{nome_arquivo}"
            else:
                arquivo_final_path = f"/media/recursos/turma_{turma_id}/{nome_arquivo}"
        
        if nome and tipo:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE recurso 
                    SET recNome = %s, recTipo = %s, recDescricao = %s, recArquivoPath = %s, 
                        recAcessoPrevio = %s, recDraft = %s
                    WHERE recId = %s
                """, [
                    nome,
                    tipo,
                    descricao if descricao else None,
                    arquivo_final_path,
                    1 if acesso_previo else 0,
                    1 if draft else 0,
                    rec_id
                ])
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

