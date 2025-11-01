from django.db import models

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
