from rest_framework import serializers
from django.conf import settings
from .models import (
    Event, MarketSelection, CartelaTemplate,
    CartelaInstance, CartelaInstanceItem, Bet,
)


class CartelaTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartelaTemplate
        fields = [
            "id",
            "nome",
            "descricao",
            "tipo",
            "config",
        ]


class MarketSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketSelection
        fields = [
            "id",
            "selection_type",
            "params",
            "prob_base",
            "odd_justa",
            "odd_publicada",
            "is_live",
        ]


class CartelaQuoteRequestSerializer(serializers.Serializer):
    event_id = serializers.IntegerField()
    cartela_template_id = serializers.IntegerField()
    selection_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    stake = serializers.DecimalField(max_digits=18, decimal_places=2)


class CartelaQuoteResponseSerializer(serializers.Serializer):
    cartela_id = serializers.IntegerField()
    odd_final = serializers.FloatField()
    premio_maximo = serializers.DecimalField(max_digits=18, decimal_places=2)
    valid_until = serializers.DateTimeField()
    risk_flags = serializers.DictField()


class BetConfirmRequestSerializer(serializers.Serializer):
    cartela_id = serializers.IntegerField()


class BetSerializer(serializers.ModelSerializer):
    cartela = serializers.PrimaryKeyRelatedField(read_only=True)
    event = serializers.SerializerMethodField()
    cartela_tipo = serializers.SerializerMethodField()
    
    class Meta:
        model = Bet
        fields = [
            "id",
            "cartela",
            "event",
            "cartela_tipo",
            "stake",
            "odd_final",
            "potential_return",
            "is_won",
            "created_at",
            "settled_at",
        ]
    
    def get_event(self, obj):
        event = obj.cartela.event
        return {
            "id": event.id,
            "sport": event.sport,
            "team_home": event.team_home,
            "team_away": event.team_away,
            "start_time": event.start_time,
        }
    
    def get_cartela_tipo(self, obj):
        return obj.cartela.cartela_template.tipo


class CartelaInstanceItemSerializer(serializers.ModelSerializer):
    selection = serializers.SerializerMethodField()
    
    class Meta:
        model = CartelaInstanceItem
        fields = ["id", "selection", "odd_usada"]
    
    def get_selection(self, obj):
        ms = obj.market_selection
        return {
            "id": ms.id,
            "selection_type": ms.selection_type,
            "params": ms.params,
            "odd_publicada": ms.odd_publicada,
        }


class CartelaInstanceDetailSerializer(serializers.ModelSerializer):
    items = CartelaInstanceItemSerializer(many=True, read_only=True)
    event = serializers.SerializerMethodField()
    cartela_template_nome = serializers.CharField(
        source="cartela_template.nome",
        read_only=True
    )
    
    class Meta:
        model = CartelaInstance
        fields = [
            "id",
            "user",
            "event",
            "cartela_template_nome",
            "status",
            "odd_final",
            "premio_maximo",
            "stake",
            "snapshot_data",
            "created_at",
            "items",
        ]
        read_only_fields = ["user"]
    
    def get_event(self, obj):
        e = obj.event
        return {
            "id": e.id,
            "sport": e.sport,
            "team_home": e.team_home,
            "team_away": e.team_away,
            "start_time": e.start_time,
        }

