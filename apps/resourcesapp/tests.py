from django.test import TestCase
from django.utils import timezone
from datetime import date, timedelta
from apps.resourcesapp.services.access_rules import recursos_visiveis
from apps.trainings.models import Turma, Treinamento


class AccessRulesTest(TestCase):
    """Testes para regras de acesso a recursos"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        # Criar treinamento via SQL direto (já que managed=False)
        from django.db import connection
        with connection.cursor() as cursor:
            # Criar treinamento
            cursor.execute("""
                INSERT INTO treinamento (treNome, treDescricao, treCadastradoEm)
                VALUES (%s, %s, %s)
            """, ['Treinamento Teste', 'Descrição teste', timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            self.treinamento_id = cursor.fetchone()[0]
    
    def test_recursos_visiveis_antes_data_inicio_com_acesso_previo(self):
        """Testa que recursos com acesso prévio aparecem antes da data de início"""
        # Criar turma com data futura
        data_futura = date.today() + timedelta(days=10)
        
        turma = Turma()
        turma.tru_id = 1
        turma.treinamento = Treinamento()
        turma.treinamento.tre_id = self.treinamento_id
        turma.tru_data_inicio = data_futura
        
        # Criar recurso com acesso prévio
        class RecursoMock:
            def __init__(self):
                self.rec_id = 1
                self.rec_acesso_previo = True
                self.rec_draft = False
        
        recursos = [RecursoMock()]
        visiveis = recursos_visiveis(turma, recursos)
        
        self.assertEqual(len(visiveis), 1)
        self.assertEqual(visiveis[0].rec_id, 1)
    
    def test_recursos_visiveis_antes_data_inicio_sem_acesso_previo(self):
        """Testa que recursos sem acesso prévio NÃO aparecem antes da data de início"""
        data_futura = date.today() + timedelta(days=10)
        
        turma = Turma()
        turma.tru_id = 1
        turma.treinamento = Treinamento()
        turma.treinamento.tre_id = self.treinamento_id
        turma.tru_data_inicio = data_futura
        
        class RecursoMock:
            def __init__(self):
                self.rec_id = 1
                self.rec_acesso_previo = False
                self.rec_draft = False
        
        recursos = [RecursoMock()]
        visiveis = recursos_visiveis(turma, recursos)
        
        self.assertEqual(len(visiveis), 0)
    
    def test_recursos_draft_nao_aparecem_antes_data_inicio(self):
        """Testa que recursos em draft NUNCA aparecem, mesmo com acesso prévio"""
        data_futura = date.today() + timedelta(days=10)
        
        turma = Turma()
        turma.tru_id = 1
        turma.treinamento = Treinamento()
        turma.treinamento.tre_id = self.treinamento_id
        turma.tru_data_inicio = data_futura
        
        class RecursoMock:
            def __init__(self):
                self.rec_id = 1
                self.rec_acesso_previo = True
                self.rec_draft = True  # Rascunho
        
        recursos = [RecursoMock()]
        visiveis = recursos_visiveis(turma, recursos)
        
        self.assertEqual(len(visiveis), 0)
    
    def test_recursos_visiveis_apos_data_inicio_sem_draft(self):
        """Testa que recursos sem draft aparecem após a data de início"""
        data_passada = date.today() - timedelta(days=10)
        
        turma = Turma()
        turma.tru_id = 1
        turma.treinamento = Treinamento()
        turma.treinamento.tre_id = self.treinamento_id
        turma.tru_data_inicio = data_passada
        
        class RecursoMock:
            def __init__(self):
                self.rec_id = 1
                self.rec_acesso_previo = False
                self.rec_draft = False
        
        recursos = [RecursoMock()]
        visiveis = recursos_visiveis(turma, recursos)
        
        self.assertEqual(len(visiveis), 1)
    
    def test_recursos_draft_nao_aparecem_apos_data_inicio(self):
        """Testa que recursos em draft não aparecem mesmo após a data de início"""
        data_passada = date.today() - timedelta(days=10)
        
        turma = Turma()
        turma.tru_id = 1
        turma.treinamento = Treinamento()
        turma.treinamento.tre_id = self.treinamento_id
        turma.tru_data_inicio = data_passada
        
        class RecursoMock:
            def __init__(self):
                self.rec_id = 1
                self.rec_acesso_previo = False
                self.rec_draft = True  # Rascunho
        
        recursos = [RecursoMock()]
        visiveis = recursos_visiveis(turma, recursos)
        
        self.assertEqual(len(visiveis), 0)
    
    def test_multiplos_recursos_filtrados_corretamente(self):
        """Testa filtragem com múltiplos recursos"""
        data_futura = date.today() + timedelta(days=10)
        
        turma = Turma()
        turma.tru_id = 1
        turma.treinamento = Treinamento()
        turma.treinamento.tre_id = self.treinamento_id
        turma.tru_data_inicio = data_futura
        
        class RecursoMock:
            def __init__(self, rec_id, acesso_previo, draft):
                self.rec_id = rec_id
                self.rec_acesso_previo = acesso_previo
                self.rec_draft = draft
        
        recursos = [
            RecursoMock(1, True, False),   # Deve aparecer
            RecursoMock(2, False, False), # Não deve aparecer
            RecursoMock(3, True, True),   # Não deve aparecer (draft)
            RecursoMock(4, False, True),  # Não deve aparecer
        ]
        
        visiveis = recursos_visiveis(turma, recursos)
        
        self.assertEqual(len(visiveis), 1)
        self.assertEqual(visiveis[0].rec_id, 1)
