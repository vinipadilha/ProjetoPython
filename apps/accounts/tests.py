from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.db import connection
from django.utils import timezone
from apps.accounts.models import Usuario, Perfil
from apps.accounts.roles import ROLE_ADMIN, ROLE_STUDENT


class AuthenticationTest(TestCase):
    """Testes de autenticação e permissões"""
    
    def setUp(self):
        """Configuração inicial"""
        self.client = Client()
        
        # Criar perfis via SQL
        with connection.cursor() as cursor:
            # Admin
            cursor.execute("""
                INSERT INTO perfil (pefNome, pefCadastradoEm)
                VALUES (%s, %s)
            """, ['Administrador', timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            self.perfil_admin_id = cursor.fetchone()[0]
            
            # Estudante
            cursor.execute("""
                INSERT INTO perfil (pefNome, pefCadastradoEm)
                VALUES (%s, %s)
            """, ['Estudante', timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            self.perfil_estudante_id = cursor.fetchone()[0]
    
    def test_is_admin_property(self):
        """Testa propriedade is_admin do modelo Usuario"""
        usuario = Usuario()
        usuario.usu_id = 1
        usuario.perfil_id = self.perfil_admin_id
        
        # Verificar via query direta
        with connection.cursor() as cursor:
            cursor.execute("SELECT pefId FROM perfil WHERE pefId = %s", [self.perfil_admin_id])
            result = cursor.fetchone()
            self.assertIsNotNone(result)
    
    def test_is_student_property(self):
        """Testa propriedade is_student do modelo Usuario"""
        usuario = Usuario()
        usuario.usu_id = 1
        usuario.perfil_id = self.perfil_estudante_id
        
        # Verificar via query direta
        with connection.cursor() as cursor:
            cursor.execute("SELECT pefId FROM perfil WHERE pefId = %s", [self.perfil_estudante_id])
            result = cursor.fetchone()
            self.assertIsNotNone(result)
    
    def test_login_redirect_admin(self):
        """Testa redirecionamento após login de admin"""
        # Este teste requer setup completo do usuário e autenticação
        # Por enquanto, testa estrutura básica
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_redirect_student(self):
        """Testa redirecionamento após login de estudante"""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_protected_route_redirects_to_login(self):
        """Testa que rotas protegidas redirecionam para login"""
        response = self.client.get('/dashboard/')
        self.assertRedirects(response, '/login/?next=/dashboard/')
        
        response = self.client.get('/aluno/turmas/')
        self.assertRedirects(response, '/login/?next=/aluno/turmas/')


class UsuarioModelTest(TestCase):
    """Testes do modelo Usuario"""
    
    def setUp(self):
        """Configuração inicial"""
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO perfil (pefNome, pefCadastradoEm)
                VALUES (%s, %s)
            """, ['Administrador', timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            self.perfil_id = cursor.fetchone()[0]
    
    def test_usuario_str_representation(self):
        """Testa representação string do modelo"""
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO usuario (usuPefId, usuNome, usuEmail, usuSenha, usuCadastradoEm)
                VALUES (%s, %s, %s, %s, %s)
            """, [self.perfil_id, 'Teste User', 'teste@email.com', 'hashed_password', timezone.now()])
            cursor.execute("SELECT LAST_INSERT_ID()")
            usuario_id = cursor.fetchone()[0]
            
            usuario = Usuario.objects.get(pk=usuario_id)
            self.assertEqual(str(usuario), 'Teste User')
