from django.db import models
from apps.trainings.models import Turma
from apps.accounts.models import Usuario

class Matricula(models.Model):
    mat_id = models.AutoField(db_column='matId', primary_key=True)
    turma = models.ForeignKey(
        Turma,
        models.DO_NOTHING,
        db_column='matTruId',
        related_name='matriculas'
    )
    usuario = models.ForeignKey(
        Usuario,
        models.DO_NOTHING,
        db_column='matUsuId',
        related_name='matriculas'
    )
    mat_cadastrado_em = models.DateTimeField(db_column='matCadastradoEm')

    class Meta:
        managed = False
        db_table = 'matricula'
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        constraints = [
            models.UniqueConstraint(fields=['turma', 'usuario'], name='uq_matricula_tru_usuario')
        ]

    def __str__(self):
        return f'{self.usuario.usu_nome} → {self.turma.tru_nome}'
