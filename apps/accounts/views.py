from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .services.current_user import get_usuario_from_request
from .roles import ROLE_ADMIN

@login_required
def pos_login(request):
    u = get_usuario_from_request(request)
    if u:
        request.session['role_id'] = u.perfil_id
        request.session['role_name'] = u.perfil.pef_nome

    if u and u.perfil_id == ROLE_ADMIN:
        return redirect('/admin/')
    return redirect('/aluno/turmas/')
