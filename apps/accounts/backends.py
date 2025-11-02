from django.contrib.auth.backends import ModelBackend
from .models import Usuario

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username or kwargs.get('username') or kwargs.get('usu_email')
        if not email or not password:
            return None
        
        try:
            user = Usuario.objects.select_related('perfil').get(usu_email=email)
        except Usuario.DoesNotExist:
            return None
        
        if not user.check_password(password):
            return None
        
        if not self.user_can_authenticate(user):
            return None
        
        return user

    def user_can_authenticate(self, user):
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SHOW COLUMNS FROM usuario LIKE 'is_active'")
                has_column = cursor.fetchone()
                if has_column:
                    cursor.execute("SELECT is_active FROM usuario WHERE usuId = %s", [user.usu_id])
                    row = cursor.fetchone()
                    is_active = bool(row[0]) if row and row[0] is not None else True
                    return is_active
        except Exception:
            pass
        return True

    def get_user(self, user_id):
        try:
            return Usuario.objects.select_related('perfil').get(pk=user_id)
        except Usuario.DoesNotExist:
            return None

