from django.test import TestCase
from django.db import connection
from django.utils import timezone
from datetime import date
from apps.enrollments.models import Matricula
from apps.trainings.models import Turma, Treinamento
from apps.accounts.models import Usuario, Perfil


class MatriculaTest(TestCase):
    """Testes de matrícula"""
    
    def setUp(self):
        """Configuração inicial"""
        with connection.cursor() as cursor:
            # Criar perfil estudante
            cursor.execute("""
                INSERT INTO perfil (pefNome, pefCadastradoEm)
                VALUES (%s, %s)
            """, ['Estudante', timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            self.perfil_id = cursor.fetchone()[0]
            
            # Criar usuário
            cursor.execute("""
                INSERT INTO usuario (usuPefId, usuNome, usuEmail, usuSenha, usuCadastradoEm)
                VALUES (%s, %s, %s, %s, %s)
            """, [self.perfil_id, 'Estudante Teste', 'estudante@teste.com', 'hash', timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            self.usuario_id = cursor.fetchone()[0]
            
            # Criar treinamento
            cursor.execute("""
                INSERT INTO treinamento (treNome, treDescricao, treCadastradoEm)
                VALUES (%s, %s, %s)
            """, ['Treinamento Teste', 'Desc', timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            self.treinamento_id = cursor.fetchone()[0]
            
            # Criar turma
            cursor.execute("""
                INSERT INTO turma (truTreId, truNome, truDataInicio, truCadastradoEm)
                VALUES (%s, %s, %s, %s)
            """, [self.treinamento_id, 'Turma Teste', date.today(), timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            self.turma_id = cursor.fetchone()[0]
    
    def test_matricula_creation(self):
        """Testa criação de matrícula"""
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO matricula (matTruId, matUsuId, matCadastradoEm)
                VALUES (%s, %s, %s)
            """, [self.turma_id, self.usuario_id, timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            mat_id = cursor.fetchone()[0]
            
            matricula = Matricula.objects.select_related('turma', 'usuario').get(pk=mat_id)
            self.assertEqual(matricula.turma.tru_id, self.turma_id)
            self.assertEqual(matricula.usuario.usu_id, self.usuario_id)
    
    def test_matricula_str_representation(self):
        """Testa representação string da matrícula"""
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO matricula (matTruId, matUsuId, matCadastradoEm)
                VALUES (%s, %s, %s)
            """, [self.turma_id, self.usuario_id, timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            mat_id = cursor.fetchone()[0]
            
            matricula = Matricula.objects.select_related('turma', 'usuario').get(pk=mat_id)
            expected_str = f'{matricula.usuario.usu_nome} → {matricula.turma.tru_nome}'
            self.assertEqual(str(matricula), expected_str)
    
    def test_turmas_por_usuario(self):
        """Testa filtro de turmas por usuário matriculado"""
        with connection.cursor() as cursor:
            # Criar segunda turma
            cursor.execute("""
                INSERT INTO turma (truTreId, truNome, truDataInicio, truCadastradoEm)
                VALUES (%s, %s, %s, %s)
            """, [self.treinamento_id, 'Turma 2', date.today(), timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            turma2_id = cursor.fetchone()[0]
            
            # Matricular apenas na primeira turma
            cursor.execute("""
                INSERT INTO matricula (matTruId, matUsuId, matCadastradoEm)
                VALUES (%s, %s, %s)
            """, [self.turma_id, self.usuario_id, timezone.now()])
            
            # Verificar que apenas a turma matriculada aparece
            turmas = Turma.objects.filter(matriculas__usuario_id=self.usuario_id)
            self.assertEqual(turmas.count(), 1)
            self.assertEqual(turmas.first().tru_id, self.turma_id)
