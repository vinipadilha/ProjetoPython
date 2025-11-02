from django import forms
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.db import connection
from django.utils import timezone
from .models import Perfil, Usuario

class UsuarioAdminForm(forms.ModelForm):
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(),
        required=False,
        help_text='Deixe em branco para não alterar a senha.'
    )
    
    class Meta:
        model = Usuario
        fields = '__all__'

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('pef_id', 'pef_nome', 'pef_cadastrado_em')
    search_fields = ('pef_nome',)
    ordering = ('pef_nome',)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioAdminForm
    list_display = ('usu_nome', 'usu_email', 'perfil', 'usu_cadastrado_em')
    list_filter = ('perfil',)
    search_fields = ('usu_nome', 'usu_email')
    ordering = ('usu_nome',)
    
    fields = ('usu_email', 'usu_nome', 'usu_telefone', 'perfil', 'password', 'usu_cadastrado_em')
    readonly_fields = ('usu_cadastrado_em',)
    
    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('password')
        
        if change:
            senha_atual = password
            
            with connection.cursor() as cursor:
                if senha_atual and senha_atual.strip() != '':
                    senha_hasheada = make_password(senha_atual)
                    cursor.execute("""
                        UPDATE usuario 
                        SET usuEmail = %s, usuNome = %s, usuTelefone = %s, usuPefId = %s, usuSenha = %s
                        WHERE usuId = %s
                    """, [obj.usu_email, obj.usu_nome, obj.usu_telefone or None, obj.perfil_id, senha_hasheada, obj.usu_id])
                else:
                    cursor.execute("""
                        UPDATE usuario 
                        SET usuEmail = %s, usuNome = %s, usuTelefone = %s, usuPefId = %s
                        WHERE usuId = %s
                    """, [obj.usu_email, obj.usu_nome, obj.usu_telefone or None, obj.perfil_id, obj.usu_id])
        else:
            if not password:
                raise forms.ValidationError('A senha é obrigatória para novos usuários.')
            senha_hasheada = make_password(password)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuario (usuPefId, usuNome, usuEmail, usuTelefone, usuSenha, usuCadastradoEm, is_active, is_staff, is_superuser)
                    VALUES (%s, %s, %s, %s, %s, %s, 1, 0, 0)
                """, [obj.perfil_id, obj.usu_nome, obj.usu_email, obj.usu_telefone or None, senha_hasheada, timezone.now()])
                cursor.execute("SELECT LAST_INSERT_ID()")
                obj.usu_id = cursor.fetchone()[0]
