from .services.current_user import get_usuario_from_request

def current_usuario(request):
    usuario = get_usuario_from_request(request)
    
    return {
        'usuario': usuario,
        'role_id': request.session.get('role_id'),
        'role_name': request.session.get('role_name'),
    }

