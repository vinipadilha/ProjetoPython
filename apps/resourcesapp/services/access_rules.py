from django.utils import timezone

def recursos_visiveis(turma, recursos_iterable):
    agora = timezone.now()
    visiveis = []
    if turma.tru_data_inicio > agora:
        for r in recursos_iterable:
            if getattr(r, 'rec_acesso_previo', False):
                visiveis.append(r)
    else:
        for r in recursos_iterable:
            if not getattr(r, 'rec_draft', False):
                visiveis.append(r)
    return visiveis
