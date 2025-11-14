from django.contrib import admin
from .models import (
    Event, MarketSelection, Influencer, CartelaTemplate,
    CartelaTemplateItem, CartelaInstance, CartelaInstanceItem,
    Bet, OddsSnapshot, RiskExposureMetrics
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['team_home', 'team_away', 'sport', 'start_time', 'status']
    list_filter = ['sport', 'status', 'start_time']
    search_fields = ['team_home', 'team_away']
    date_hierarchy = 'start_time'


@admin.register(MarketSelection)
class MarketSelectionAdmin(admin.ModelAdmin):
    list_display = ['event', 'selection_type', 'odd_publicada', 'is_live', 'updated_at']
    list_filter = ['selection_type', 'is_live', 'event__sport']
    search_fields = ['event__team_home', 'event__team_away', 'selection_type']
    raw_id_fields = ['event']


@admin.register(Influencer)
class InfluencerAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'user', 'is_active']
    search_fields = ['display_name', 'user__username']


@admin.register(CartelaTemplate)
class CartelaTemplateAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'influencer', 'ativo']
    list_filter = ['tipo', 'ativo']
    search_fields = ['nome', 'descricao']


@admin.register(CartelaTemplateItem)
class CartelaTemplateItemAdmin(admin.ModelAdmin):
    list_display = ['cartela_template', 'allowed_selection_type']
    list_filter = ['cartela_template']


@admin.register(CartelaInstance)
class CartelaInstanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'status', 'stake', 'premio_maximo', 'created_at']
    list_filter = ['status', 'cartela_template__tipo', 'created_at']
    search_fields = ['user__username', 'event__team_home', 'event__team_away']
    raw_id_fields = ['user', 'event', 'cartela_template']
    readonly_fields = ['created_at', 'locked_at']


@admin.register(CartelaInstanceItem)
class CartelaInstanceItemAdmin(admin.ModelAdmin):
    list_display = ['cartela_instance', 'market_selection', 'odd_usada']
    raw_id_fields = ['cartela_instance', 'market_selection']


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ['id', 'cartela', 'stake', 'odd_final', 'potential_return', 'is_won', 'created_at']
    list_filter = ['is_won', 'created_at']
    raw_id_fields = ['cartela']
    readonly_fields = ['created_at', 'settled_at']


@admin.register(OddsSnapshot)
class OddsSnapshotAdmin(admin.ModelAdmin):
    list_display = ['cartela', 'created_at']
    raw_id_fields = ['cartela']
    readonly_fields = ['created_at']


@admin.register(RiskExposureMetrics)
class RiskExposureMetricsAdmin(admin.ModelAdmin):
    list_display = ['event', 'cartela_template', 'volume_total', 'payout_maximo', 'updated_at']
    list_filter = ['cartela_template__tipo']
    raw_id_fields = ['event', 'cartela_template', 'influencer']
