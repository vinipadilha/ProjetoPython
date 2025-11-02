from apps.accounts.models import Usuario

def get_usuario_from_request(request):
    if not request.user.is_authenticated:
        return None
    
    if isinstance(request.user, Usuario):
        return Usuario.objects.select_related('perfil').filter(pk=request.user.usu_id).first()
    
    if hasattr(request.user, 'usu_email'):
        return Usuario.objects.select_related('perfil').filter(usu_email=request.user.usu_email).first()
    
    if hasattr(request.user, 'email'):
        return Usuario.objects.select_related('perfil').filter(usu_email=request.user.email).first()
    
    return None
