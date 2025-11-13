from django.contrib import admin
from .models import Carteira, Transacao


@admin.register(Carteira)
class CarteiraAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'pontos', 'fundos', 'atualizado_em']
    list_filter = ['criado_em', 'atualizado_em']
    search_fields = ['usuario__username', 'usuario__email']
    readonly_fields = ['criado_em', 'atualizado_em']
    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('usuario',)
        }),
        ('Saldo', {
            'fields': ('pontos', 'fundos')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ['carteira', 'tipo', 'categoria', 'valor', 'criado_em']
    list_filter = ['tipo', 'categoria', 'criado_em']
    search_fields = ['carteira__usuario__username', 'descricao']
    readonly_fields = ['criado_em']
    date_hierarchy = 'criado_em'
    fieldsets = (
        ('Informações da Transação', {
            'fields': ('carteira', 'tipo', 'categoria', 'valor', 'descricao')
        }),
        ('Saldos Anteriores', {
            'fields': ('saldo_anterior_pontos', 'saldo_anterior_fundos'),
            'classes': ('collapse',)
        }),
        ('Data', {
            'fields': ('criado_em',)
        }),
    )
