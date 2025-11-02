from django.db import models
from .roles import ROLE_ADMIN, ROLE_STUDENT

class Perfil(models.Model):
    pef_id = models.AutoField(db_column='pefId', primary_key=True)
    pef_nome = models.CharField(db_column='pefNome', max_length=100)
    pef_cadastrado_em = models.DateTimeField(db_column='pefCadastradoEm')

    class Meta:
        managed = False
        db_table = 'perfil'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return self.pef_nome


class Usuario(models.Model):
    usu_id = models.AutoField(db_column='usuId', primary_key=True)
    perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='usuPefId', related_name='usuarios')
    usu_nome = models.CharField(db_column='usuNome', max_length=200)
    usu_email = models.CharField(db_column='usuEmail', max_length=200, unique=True)
    usu_telefone = models.CharField(db_column='usuTelefone', max_length=32, null=True, blank=True)
    usu_cadastrado_em = models.DateTimeField(db_column='usuCadastradoEm')
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'usuario'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['usu_nome']
    
    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields')
        if update_fields and 'last_login' in update_fields:
            from django.db import connection
            from django.utils import timezone
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE usuario 
                        SET last_login = %s 
                        WHERE usuId = %s
                    """, [timezone.now(), self.usu_id])
                return
            except Exception:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.usu_nome

    @property
    def is_admin(self):
        return self.perfil_id == ROLE_ADMIN

    @property
    def is_student(self):
        return self.perfil_id == ROLE_STUDENT
    
    def check_password(self, raw_password):
        from django.db import connection
        from django.contrib.auth.hashers import check_password
        with connection.cursor() as cursor:
            cursor.execute("SELECT usuSenha FROM usuario WHERE usuId = %s", [self.usu_id])
            row = cursor.fetchone()
            if row:
                hashed_password = row[0]
                return check_password(raw_password, hashed_password)
        return False
    
    def set_password(self, raw_password):
        from django.db import connection
        from django.contrib.auth.hashers import make_password
        hashed_password = make_password(raw_password)
        with connection.cursor() as cursor:
            cursor.execute("UPDATE usuario SET usuSenha = %s WHERE usuId = %s", [hashed_password, self.usu_id])
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_username(self):
        return self.usu_email
    
    @property
    def username(self):
        return self.usu_email
    
    @property
    def email(self):
        return self.usu_email
    
    @property
    def is_active(self):
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SHOW COLUMNS FROM usuario LIKE 'is_active'")
                has_column = cursor.fetchone()
                if has_column:
                    cursor.execute("SELECT is_active FROM usuario WHERE usuId = %s", [self.usu_id])
                    row = cursor.fetchone()
                    return bool(row[0]) if row and row[0] is not None else True
        except Exception:
            pass
        return True
    
    @property
    def is_staff(self):
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SHOW COLUMNS FROM usuario LIKE 'is_staff'")
                has_column = cursor.fetchone()
                if has_column:
                    cursor.execute("SELECT is_staff FROM usuario WHERE usuId = %s", [self.usu_id])
                    row = cursor.fetchone()
                    return bool(row[0]) if row and row[0] is not None else False
        except Exception:
            pass
        return self.perfil_id == ROLE_ADMIN if hasattr(self, 'perfil_id') else False
    
    @property
    def is_superuser(self):
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SHOW COLUMNS FROM usuario LIKE 'is_superuser'")
                has_column = cursor.fetchone()
                if has_column:
                    cursor.execute("SELECT is_superuser FROM usuario WHERE usuId = %s", [self.usu_id])
                    row = cursor.fetchone()
                    return bool(row[0]) if row and row[0] is not None else False
        except Exception:
            pass
        return self.perfil_id == ROLE_ADMIN if hasattr(self, 'perfil_id') else False
    
    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return False
    
    def has_module_perms(self, app_label):
        if self.is_superuser or self.is_staff:
            return True
        return False
    
    def get_all_permissions(self, obj=None):
        if self.is_superuser:
            from django.contrib.contenttypes.models import ContentType
            from django.contrib.auth.models import Permission
            return Permission.objects.all().values_list('content_type__app_label', 'codename').order_by()
        return set()
    
    def get_user_permissions(self, obj=None):
        return set()
    
    def get_group_permissions(self, obj=None):
        return set()
