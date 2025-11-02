from django.contrib.auth.backends import ModelBackend
from .models import Usuario

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('usu_email')
        try:
            user = Usuario.objects.get(usu_email=username)
        except Usuario.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None

