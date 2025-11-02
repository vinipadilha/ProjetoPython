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

    class Meta:
        managed = False
        db_table = 'usuario'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['usu_nome']

    def __str__(self):
        return self.usu_nome

    @property
    def is_admin(self):
        return self.perfil_id == ROLE_ADMIN

    @property
    def is_student(self):
        return self.perfil_id == ROLE_STUDENT
