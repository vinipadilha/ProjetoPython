from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, usu_email, usu_nome, perfil, usu_senha=None, **extra_fields):
        if not usu_email:
            raise ValueError('O usuário deve ter um email')
        email = self.normalize_email(usu_email)
        user = self.model(usu_email=email, usu_nome=usu_nome, perfil=perfil, **extra_fields)
        user.set_password(usu_senha)
        user.save(using=self._db)
        return user

    def create_superuser(self, usu_email, usu_nome, perfil, usu_senha=None, **extra_fields):
        user = self.create_user(usu_email, usu_nome, perfil, usu_senha, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Perfil(models.Model):
    pef_id = models.AutoField(db_column='pefId', primary_key=True)
    pef_nome = models.CharField(db_column='pefNome', max_length=100)
    pef_cadastrado_em = models.DateTimeField(db_column='pefCadastradoEm', auto_now_add=True)

    class Meta:
        db_table = 'perfil'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['pef_nome']

    def __str__(self):
        return self.pef_nome

class Usuario(AbstractBaseUser, PermissionsMixin):
    usu_id = models.AutoField(db_column='usuId', primary_key=True)
    perfil = models.ForeignKey(
        Perfil,
        on_delete=models.PROTECT,
        db_column='usuPefId',
        related_name='usuarios'
    )
    usu_nome = models.CharField(db_column='usuNome', max_length=200)
    usu_email = models.EmailField(db_column='usuEmail', max_length=200, unique=True)
    usu_telefone = models.CharField(db_column='usuTelefone', max_length=32, blank=True, null=True)
    usu_cadastrado_em = models.DateTimeField(db_column='usuCadastradoEm', auto_now_add=True)
    
    password = models.CharField(db_column='usuSenha', max_length=128)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'usu_email'
    REQUIRED_FIELDS = ['usu_nome', 'perfil']

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['usu_nome']

    def __str__(self):
        return self.usu_nome
    
    @property
    def is_admin(self):
        if hasattr(self, 'perfil'):
            return self.perfil.pef_nome.lower() == 'administrador' or self.perfil.pef_id == 1
        return self.is_staff or self.is_superuser
    
    @property
    def is_aluno(self):
        if hasattr(self, 'perfil'):
            return self.perfil.pef_nome.lower() == 'aluno' or self.perfil.pef_id == 2
        return False

class Aluno(models.Model):
    alu_id = models.AutoField(db_column='aluId', primary_key=True)
    alu_nome = models.CharField(db_column='aluNome', max_length=160)
    alu_email = models.CharField(db_column='aluEmail', max_length=190, unique=True)
    alu_telefone = models.CharField(db_column='aluTelefone', max_length=32, blank=True, null=True)
    alu_cadastrado_em = models.DateTimeField(db_column='aluCadastradoEm')

    class Meta:
        managed = False
        db_table = 'aluno'
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['alu_nome']

    def __str__(self):
        return self.alu_nome
