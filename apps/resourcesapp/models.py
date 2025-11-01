from django.db import models
from apps.trainings.models import Turma

class Recurso(models.Model):
    rec_id = models.AutoField(db_column='recId', primary_key=True)
    turma = models.ForeignKey(
        Turma,
        models.DO_NOTHING,
        db_column='recTruId',
        related_name='recursos'
    )
    rec_tipo = models.CharField(db_column='recTipo', max_length=10)
    rec_acesso_previo = models.BooleanField(db_column='recAcessoPrevio')
    rec_draft = models.BooleanField(db_column='recDraft')
    rec_nome = models.CharField(db_column='recNome', max_length=160)
    rec_descricao = models.TextField(db_column='recDescricao', blank=True, null=True)
    rec_arquivo_path = models.CharField(db_column='recArquivoPath', max_length=512)
    rec_cadastrado_em = models.DateTimeField(db_column='recCadastradoEm')

    class Meta:
        managed = False
        db_table = 'recurso'
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'
        ordering = ['rec_nome']

    def __str__(self):
        return self.rec_nome
