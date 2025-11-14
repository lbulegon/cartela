from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import (
    Event, MarketSelection, CartelaTemplate, CartelaInstance, Bet,
)
from .serializers import (
    CartelaTemplateSerializer,
    MarketSelectionSerializer,
    CartelaQuoteRequestSerializer,
    CartelaQuoteResponseSerializer,
    BetConfirmRequestSerializer,
    BetSerializer,
    CartelaInstanceDetailSerializer,
)
from .services import generate_cartela_quote, confirm_bet


class CartelaTemplatesByEventAPIView(generics.ListAPIView):
    """
    GET /api/v1/cartelas/event/<event_id>/templates/
    Retorna os templates de cartelas disponíveis para o evento.
    """
    serializer_class = CartelaTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        event_id = self.kwargs["event_id"]
        # Se quiser filtrar por esporte, liga, etc., pode incrementar aqui.
        # Por enquanto, retornamos todos os templates ativos.
        return CartelaTemplate.objects.filter(ativo=True)


class MarketSelectionsByEventTemplateAPIView(generics.ListAPIView):
    """
    GET /api/v1/cartelas/event/<event_id>/selections/?template_id=...
    Retorna as seleções (quadrinhos) válidas para montar a cartela.
    """
    serializer_class = MarketSelectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        event_id = self.kwargs["event_id"]
        template_id = self.request.query_params.get("template_id")
        
        event = get_object_or_404(Event, id=event_id)
        qs = MarketSelection.objects.filter(event=event)
        
        # Aqui você pode restringir conforme regras do template (tipo, live, etc.)
        if template_id:
            # Exemplo bem simples: se template for turbo, filtra apenas is_live=True
            template = get_object_or_404(CartelaTemplate, id=template_id)
            if template.tipo in ("LIVE", "TURBO"):
                qs = qs.filter(is_live=True)
        
        return qs


class CartelaQuoteAPIView(APIView):
    """
    POST /api/v1/cartelas/quote/
    Gera a cotação de uma cartela com base nas seleções + stake.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = CartelaQuoteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        event_id = serializer.validated_data["event_id"]
        template_id = serializer.validated_data["cartela_template_id"]
        selection_ids = serializer.validated_data["selection_ids"]
        stake = serializer.validated_data["stake"]
        
        try:
            cartela, odd_final, potential_return, valid_until, risk_flags = generate_cartela_quote(
                user=request.user,
                event_id=event_id,
                cartela_template_id=template_id,
                selection_ids=selection_ids,
                stake=stake,
            )
            
            resp = CartelaQuoteResponseSerializer({
                "cartela_id": cartela.id,
                "odd_final": odd_final,
                "premio_maximo": potential_return,
                "valid_until": valid_until,
                "risk_flags": risk_flags,
            })
            
            return Response(resp.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class BetConfirmAPIView(APIView):
    """
    POST /api/v1/bets/confirm/
    Confirma a aposta ligada a uma cartela.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = BetConfirmRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cartela_id = serializer.validated_data["cartela_id"]
        
        try:
            bet = confirm_bet(user=request.user, cartela_id=cartela_id)
            resp = BetSerializer(bet)
            return Response(resp.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class MyBetsListAPIView(generics.ListAPIView):
    """
    GET /api/v1/bets/my/
    Lista as apostas do usuário logado.
    """
    serializer_class = BetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Bet.objects.filter(
            cartela__user=self.request.user
        ).select_related(
            "cartela",
            "cartela__event",
            "cartela__cartela_template"
        ).order_by("-created_at")


class CartelaDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/v1/cartelas/<cartela_id>/
    Detalhe da cartela (com quadrinhos marcados).
    """
    serializer_class = CartelaInstanceDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "cartela_id"
    
    def get_queryset(self):
        return CartelaInstance.objects.filter(
            user=self.request.user
        ).select_related(
            "event",
            "cartela_template"
        ).prefetch_related(
            "items",
            "items__market_selection"
        )
