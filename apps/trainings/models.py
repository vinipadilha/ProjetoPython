from django.db import models

class Treinamento(models.Model):
    tre_id = models.AutoField(db_column='treId', primary_key=True)
    tre_nome = models.CharField(db_column='treNome', max_length=160)
    tre_descricao = models.TextField(db_column='treDescricao', blank=True, null=True)
    tre_cadastrado_em = models.DateTimeField(db_column='treCadastradoEm')

    class Meta:
        managed = False
        db_table = 'treinamento'
        verbose_name = 'Treinamento'
        verbose_name_plural = 'Treinamentos'
        ordering = ['tre_nome']

    def __str__(self):
        return self.tre_nome


class Turma(models.Model):
    tru_id = models.AutoField(db_column='truId', primary_key=True)
    treinamento = models.ForeignKey(
        Treinamento,
        models.DO_NOTHING,              # o CASCADE está no banco; aqui não precisa replicar
        db_column='truTreId',
        related_name='turmas'
    )
    tru_nome = models.CharField(db_column='truNome', max_length=160)
    tru_data_inicio = models.DateTimeField(db_column='truDataInicio')
    tru_data_conclusao = models.DateTimeField(db_column='truDataConclusao', blank=True, null=True)
    tru_link_acesso = models.CharField(db_column='truLinkAcesso', max_length=255, blank=True, null=True)
    tru_cadastrado_em = models.DateTimeField(db_column='truCadastradoEm')

    class Meta:
        managed = False
        db_table = 'turma'
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ['-tru_data_inicio']

    def __str__(self):
        return f'{self.tru_nome} ({self.treinamento.tre_nome})'
