from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from apps.trainings.models import Turma
from apps.resourcesapp.models import Recurso
from apps.resourcesapp.services.access_rules import recursos_visiveis

def turmas_json(request, aluno_id):
    turmas = Turma.objects.filter(matriculas__aluno_id=aluno_id).values(
        'tru_id', 'tru_nome', 'tru_data_inicio', 'tru_data_conclusao'
    )
    return JsonResponse({'turmas': list(turmas)})

def recursos_json(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id)
    recursos_qs = Recurso.objects.filter(turma_id=turma_id)
    recursos = recursos_visiveis(turma, list(recursos_qs))
    data = [
        {
            'rec_id': r.rec_id,
            'rec_nome': r.rec_nome,
            'rec_tipo': r.rec_tipo,
            'rec_arquivo_path': r.rec_arquivo_path,
        } for r in recursos
    ]
    return JsonResponse({'recursos': data})
