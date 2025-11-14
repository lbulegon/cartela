from django.urls import path
from .views import (
    CartelaTemplatesByEventAPIView,
    MarketSelectionsByEventTemplateAPIView,
    CartelaQuoteAPIView,
    BetConfirmAPIView,
    MyBetsListAPIView,
    CartelaDetailAPIView,
)

app_name = "betting"

urlpatterns = [
    # Cartelas
    path(
        "cartelas/event/<int:event_id>/templates/",
        CartelaTemplatesByEventAPIView.as_view(),
        name="cartela-templates-by-event",
    ),
    path(
        "cartelas/event/<int:event_id>/selections/",
        MarketSelectionsByEventTemplateAPIView.as_view(),
        name="cartela-selections-by-event-template",
    ),
    path(
        "cartelas/quote/",
        CartelaQuoteAPIView.as_view(),
        name="cartela-quote",
    ),
    path(
        "cartelas/<int:cartela_id>/",
        CartelaDetailAPIView.as_view(),
        name="cartela-detail",
    ),
    # Bets
    path(
        "bets/confirm/",
        BetConfirmAPIView.as_view(),
        name="bet-confirm",
    ),
    path(
        "bets/my/",
        MyBetsListAPIView.as_view(),
        name="bets-my",
    ),
]

