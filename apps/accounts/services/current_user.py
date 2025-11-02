from apps.accounts.models import Usuario

def get_usuario_from_request(request):
    if not request.user.is_authenticated:
        return None
    return (Usuario.objects
            .select_related('perfil')
            .filter(usu_email=request.user.email)
            .first())
