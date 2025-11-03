from django.utils import timezone
from datetime import date

def recursos_visiveis(turma, recursos_iterable):
    agora = timezone.now().date()  # Converte para date para comparar com DateField
    visiveis = []
    
    # Converte tru_data_inicio para date se for datetime
    data_inicio = turma.tru_data_inicio
    if hasattr(data_inicio, 'date'):
        data_inicio = data_inicio.date()
    elif isinstance(data_inicio, date):
        data_inicio = data_inicio
    
    if data_inicio > agora:
        # Antes do início da turma: só recursos com acesso prévio
        for r in recursos_iterable:
            if getattr(r, 'rec_acesso_previo', False):
                visiveis.append(r)
    else:
        # Após o início da turma: recursos que não estão em draft
        for r in recursos_iterable:
            if not getattr(r, 'rec_draft', False):
                visiveis.append(r)
    return visiveis
