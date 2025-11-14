from datetime import timedelta
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import (
    Event, MarketSelection, CartelaTemplate, CartelaInstance,
    CartelaInstanceItem, Bet, RiskExposureMetrics,
)


def _calculate_odd_final_basic(selections):
    """
    Versão simplificada: multiplica as odd_publicada de cada seleção.
    
    Aqui depois você pluga:
    - odd_justa
    - fator de correlação
    - margem dinâmica
    - ajustes do Risk Engine externo
    """
    odd = 1.0
    for s in selections:
        odd *= float(s.odd_publicada)
    return odd


def _update_risk_exposure(event, cartela_template, influencer, stake, potential_return):
    """
    Atualiza métricas de exposição de risco básicas.
    Versão bem simples; depois você pode evoluir com mais lógica.
    """
    metrics, _ = RiskExposureMetrics.objects.get_or_create(
        event=event,
        cartela_template=cartela_template,
        influencer=influencer,
        defaults={
            'volume_total': Decimal('0'),
            'payout_maximo': Decimal('0'),
        }
    )
    metrics.volume_total += Decimal(str(stake))
    metrics.payout_maximo += Decimal(str(potential_return))
    # margem_media pode ser calculada a partir das odds, por enquanto deixa 0 ou fixa
    metrics.save(update_fields=["volume_total", "payout_maximo", "updated_at"])


@transaction.atomic
def generate_cartela_quote(user, event_id, cartela_template_id, selection_ids, stake):
    """
    Cria CartelaInstance em estado APOSTA_PENDENTE e retorna odd_final + prêmio + validade.
    """
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        raise ValidationError("Evento não encontrado.")
    
    try:
        template = CartelaTemplate.objects.get(id=cartela_template_id, ativo=True)
    except CartelaTemplate.DoesNotExist:
        raise ValidationError("Template de cartela não encontrado ou inativo.")
    
    selections = list(
        MarketSelection.objects.filter(
            id__in=selection_ids,
            event=event,
        )
    )
    
    if len(selections) != len(selection_ids):
        raise ValidationError("Uma ou mais seleções são inválidas para este evento.")
    
    if "min_items" in template.config:
        if len(selections) < template.config["min_items"]:
            raise ValidationError("Cartela abaixo do mínimo de seleções.")
    
    if "max_items" in template.config:
        if len(selections) > template.config["max_items"]:
            raise ValidationError("Cartela acima do máximo de seleções.")
    
    odd_final = _calculate_odd_final_basic(selections)
    stake_dec = Decimal(str(stake))
    potential_return = stake_dec * Decimal(str(odd_final))
    
    # TODO: chamar Risk Engine para validar limites, ajustar margem, etc.
    # Exemplo simplificado: sem travas de risco.
    
    valid_until = timezone.now() + timedelta(minutes=5)
    
    cartela = CartelaInstance.objects.create(
        user=user,
        event=event,
        cartela_template=template,
        status="APOSTA_PENDENTE",
        odd_final=odd_final,
        premio_maximo=potential_return,
        stake=stake_dec,
        snapshot_data={
            "selection_ids": selection_ids,
            "odd_final_raw": odd_final,
            "stake": str(stake),
        },
    )
    
    for s in selections:
        CartelaInstanceItem.objects.create(
            cartela_instance=cartela,
            market_selection=s,
            odd_usada=float(s.odd_publicada),
        )
    
    # Atualiza exposição básica
    _update_risk_exposure(
        event=event,
        cartela_template=template,
        influencer=template.influencer,
        stake=stake_dec,
        potential_return=potential_return,
    )
    
    risk_flags = {
        "limited": False,
        "adjusted_margin": 0.0,  # depois você troca pelo valor real vindo do Risk Engine
    }
    
    return cartela, odd_final, potential_return, valid_until, risk_flags


@transaction.atomic
def confirm_bet(user, cartela_id):
    """
    Confirma a aposta (Bet) ligada a uma CartelaInstance.
    - valida que a cartela pertence ao usuário
    - valida que ainda está em APOSTA_PENDENTE e não expirou
    - TODO: chama serviço de carteira para debitar
    """
    try:
        cartela = CartelaInstance.objects.select_for_update().get(
            id=cartela_id,
            user=user
        )
    except CartelaInstance.DoesNotExist:
        raise ValidationError("Cartela não encontrada para este usuário.")
    
    if cartela.status != "APOSTA_PENDENTE":
        raise ValidationError("Esta cartela não está em estado de aposta pendente.")
    
    # Validade simples baseada no created_at (ou usar valid_until no snapshot_data)
    created_plus_5 = cartela.created_at + timedelta(minutes=5)
    if timezone.now() > created_plus_5:
        raise ValidationError("Cotação expirada. Gere uma nova cartela.")
    
    if cartela.stake <= 0:
        raise ValidationError("Valor da aposta (stake) inválido.")
    
    # TODO: integrar com Wallet Service para:
    # - verificar saldo
    # - debitar saldo do usuário
    # - registrar transação financeira
    
    bet = Bet.objects.create(
        cartela=cartela,
        stake=cartela.stake,
        odd_final=cartela.odd_final,
        potential_return=cartela.premio_maximo,
    )
    
    cartela.status = "APOSTA_CONFIRMADA"
    cartela.locked_at = timezone.now()
    cartela.save(update_fields=["status", "locked_at"])
    
    return bet

