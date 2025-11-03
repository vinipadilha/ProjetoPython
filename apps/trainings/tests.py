from django.test import TestCase
from django.db import connection
from django.utils import timezone
from datetime import date, timedelta
from apps.trainings.models import Treinamento, Turma


class TreinamentoModelTest(TestCase):
    """Testes do modelo Treinamento"""
    
    def test_treinamento_creation(self):
        """Testa criação de treinamento via SQL"""
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO treinamento (treNome, treDescricao, treCadastradoEm)
                VALUES (%s, %s, %s)
            """, ['Treinamento Teste', 'Descrição', timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            tre_id = cursor.fetchone()[0]
            
            treinamento = Treinamento.objects.get(pk=tre_id)
            self.assertEqual(treinamento.tre_nome, 'Treinamento Teste')
            self.assertEqual(treinamento.tre_descricao, 'Descrição')
    
    def test_treinamento_str_representation(self):
        """Testa representação string do modelo"""
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO treinamento (treNome, treDescricao, treCadastradoEm)
                VALUES (%s, %s, %s)
            """, ['Treinamento ABC', 'Desc', timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            tre_id = cursor.fetchone()[0]
            
            treinamento = Treinamento.objects.get(pk=tre_id)
            self.assertEqual(str(treinamento), 'Treinamento ABC')


class TurmaModelTest(TestCase):
    """Testes do modelo Turma"""
    
    def setUp(self):
        """Configuração inicial"""
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO treinamento (treNome, treDescricao, treCadastradoEm)
                VALUES (%s, %s, %s)
            """, ['Treinamento Base', 'Desc', timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            self.treinamento_id = cursor.fetchone()[0]
    
    def test_turma_creation(self):
        """Testa criação de turma"""
        data_inicio = date.today()
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO turma (truTreId, truNome, truDataInicio, truCadastradoEm)
                VALUES (%s, %s, %s, %s)
            """, [self.treinamento_id, 'Turma Teste', data_inicio, timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            turma_id = cursor.fetchone()[0]
            
            turma = Turma.objects.select_related('treinamento').get(pk=turma_id)
            self.assertEqual(turma.tru_nome, 'Turma Teste')
            self.assertEqual(turma.treinamento.tre_id, self.treinamento_id)
    
    def test_turma_str_representation(self):
        """Testa representação string do modelo"""
        data_inicio = date.today()
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO turma (truTreId, truNome, truDataInicio, truCadastradoEm)
                VALUES (%s, %s, %s, %s)
            """, [self.treinamento_id, 'Turma XYZ', data_inicio, timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            turma_id = cursor.fetchone()[0]
            
            turma = Turma.objects.select_related('treinamento').get(pk=turma_id)
            expected_str = f'{turma.tru_nome} ({turma.treinamento.tre_nome})'
            self.assertEqual(str(turma), expected_str)
    
    def test_turma_with_conclusion_date(self):
        """Testa turma com data de conclusão"""
        data_inicio = date.today()
        data_conclusao = date.today() + timedelta(days=30)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO turma (truTreId, truNome, truDataInicio, truDataConclusao, truCadastradoEm)
                VALUES (%s, %s, %s, %s, %s)
            """, [self.treinamento_id, 'Turma Completa', data_inicio, data_conclusao, timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            turma_id = cursor.fetchone()[0]
            
            turma = Turma.objects.get(pk=turma_id)
            self.assertEqual(turma.tru_data_conclusao, data_conclusao)
