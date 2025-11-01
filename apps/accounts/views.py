from django.shortcuts import render, get_object_or_404
from apps.resourcesapp.services.access_rules import recursos_visiveis

def turma_recursos(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id)
    recursos_qs = Recurso.objects.filter(turma_id=turma_id).order_by('rec_nome')
    recursos = recursos_visiveis(turma, list(recursos_qs))
    return render(request, 'aluno/recursos.html', {'turma': turma, 'recursos': recursos})
