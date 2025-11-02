from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
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

