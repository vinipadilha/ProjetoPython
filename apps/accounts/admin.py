from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Perfil, Usuario, Aluno

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('pef_id', 'pef_nome', 'pef_cadastrado_em')
    search_fields = ('pef_nome',)
    ordering = ('pef_nome',)

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('usu_nome', 'usu_email', 'perfil', 'usu_cadastrado_em', 'is_active')
    list_filter = ('perfil', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('usu_nome', 'usu_email')
    ordering = ('usu_nome',)
    
    fieldsets = (
        (None, {'fields': ('usu_email', 'password')}),
        ('Informações Pessoais', {'fields': ('usu_nome', 'usu_telefone', 'perfil')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('usu_cadastrado_em',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('usu_email', 'usu_nome', 'perfil', 'password'),
        }),
    )

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('alu_id', 'alu_nome', 'alu_email', 'alu_telefone', 'alu_cadastrado_em')
    search_fields = ('alu_nome', 'alu_email')
    ordering = ('alu_nome',)
