from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class Event(models.Model):
    """Evento esportivo (jogo)"""
    SPORT_CHOICES = [
        ("SOCCER", "Futebol"),
        ("BASKETBALL", "Basquete"),
        ("TENNIS", "Tênis"),
        ("VOLLEYBALL", "Vôlei"),
    ]
    
    STATUS_CHOICES = [
        ("SCHEDULED", "Agendado"),
        ("LIVE", "Ao vivo"),
        ("FINISHED", "Finalizado"),
        ("CANCELLED", "Cancelado"),
    ]
    
    sport = models.CharField(max_length=32, choices=SPORT_CHOICES, verbose_name="Esporte")
    external_id = models.CharField(max_length=128, blank=True, null=True, verbose_name="ID Externo")
    team_home = models.CharField(max_length=128, verbose_name="Time Casa")
    team_away = models.CharField(max_length=128, verbose_name="Time Visitante")
    start_time = models.DateTimeField(verbose_name="Horário de Início")
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="SCHEDULED", verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['sport', 'status']),
            models.Index(fields=['start_time']),
        ]
    
    def __str__(self):
        return f"{self.team_home} x {self.team_away}"


class MarketSelection(models.Model):
    """Cada quadrinho possível de uma cartela"""
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="selections",
        verbose_name="Evento"
    )
    selection_type = models.CharField(max_length=64, verbose_name="Tipo de Seleção")
    params = models.JSONField(default=dict, blank=True, verbose_name="Parâmetros")
    prob_base = models.FloatField(
        help_text="Probabilidade base (0.0-1.0)",
        validators=[MinValueValidator(0.0)],
        verbose_name="Probabilidade Base"
    )
    odd_justa = models.FloatField(
        validators=[MinValueValidator(1.0)],
        verbose_name="Odd Justa"
    )
    odd_publicada = models.FloatField(
        validators=[MinValueValidator(1.0)],
        verbose_name="Odd Publicada"
    )
    is_live = models.BooleanField(default=False, verbose_name="Ao Vivo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Seleção de Mercado"
        verbose_name_plural = "Seleções de Mercado"
        ordering = ['selection_type', 'updated_at']
        indexes = [
            models.Index(fields=['event', 'is_live']),
            models.Index(fields=['selection_type']),
        ]
    
    def __str__(self):
        return f"{self.event} - {self.selection_type} ({self.odd_publicada})"


class Influencer(models.Model):
    """Influenciador que cria cartelas especiais"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="influencer_profile",
        verbose_name="Usuário"
    )
    display_name = models.CharField(max_length=128, verbose_name="Nome de Exibição")
    bio = models.TextField(blank=True, verbose_name="Biografia")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Influenciador"
        verbose_name_plural = "Influenciadores"
    
    def __str__(self):
        return self.display_name


class CartelaTemplate(models.Model):
    """Template de cartela (modelo)"""
    TEMPLATE_TIPO_CHOICES = [
        ("PRE_MATCH", "Pré-jogo"),
        ("LIVE", "Ao vivo"),
        ("TURBO", "Turbo"),
        ("MISTERIOSA", "Misteriosa IA"),
        ("INFLUENCER", "Influenciador"),
    ]
    
    nome = models.CharField(max_length=128, verbose_name="Nome")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    tipo = models.CharField(max_length=32, choices=TEMPLATE_TIPO_CHOICES, verbose_name="Tipo")
    influencer = models.ForeignKey(
        Influencer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cartelas",
        verbose_name="Influenciador"
    )
    config = models.JSONField(default=dict, blank=True, verbose_name="Configuração")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Template de Cartela"
        verbose_name_plural = "Templates de Cartela"
        ordering = ['tipo', 'nome']
    
    def __str__(self):
        return self.nome


class CartelaTemplateItem(models.Model):
    """Define quais tipos de seleções podem entrar na cartela"""
    cartela_template = models.ForeignKey(
        CartelaTemplate,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Template"
    )
    allowed_selection_type = models.CharField(max_length=64, verbose_name="Tipo de Seleção Permitido")
    constraints = models.JSONField(default=dict, blank=True, verbose_name="Restrições")
    
    class Meta:
        verbose_name = "Item do Template"
        verbose_name_plural = "Itens do Template"
        unique_together = ['cartela_template', 'allowed_selection_type']
    
    def __str__(self):
        return f"{self.cartela_template} - {self.allowed_selection_type}"


class CartelaInstance(models.Model):
    """Instância de cartela marcada pelo usuário"""
    STATUS_CHOICES = [
        ("CRIADA", "Criada"),
        ("APOSTA_PENDENTE", "Aposta pendente"),
        ("APOSTA_CONFIRMADA", "Aposta confirmada"),
        ("SETTLED", "Liquidada"),
        ("CANCELADA", "Cancelada"),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cartelas",
        verbose_name="Usuário"
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="cartelas",
        verbose_name="Evento"
    )
    cartela_template = models.ForeignKey(
        CartelaTemplate,
        on_delete=models.PROTECT,
        related_name="instances",
        verbose_name="Template"
    )
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default="CRIADA",
        verbose_name="Status"
    )
    odd_final = models.FloatField(null=True, blank=True, verbose_name="Odd Final")
    premio_maximo = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Prêmio Máximo"
    )
    stake = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor Apostado"
    )
    snapshot_data = models.JSONField(default=dict, blank=True, verbose_name="Dados do Snapshot")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    locked_at = models.DateTimeField(null=True, blank=True, verbose_name="Travado em")
    
    class Meta:
        verbose_name = "Instância de Cartela"
        verbose_name_plural = "Instâncias de Cartela"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['event', 'status']),
        ]
    
    def __str__(self):
        return f"Cartela #{self.id} - {self.user.username}"


class CartelaInstanceItem(models.Model):
    """Ligação entre cartela marcada e seleções (quadrinhos)"""
    cartela_instance = models.ForeignKey(
        CartelaInstance,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Cartela"
    )
    market_selection = models.ForeignKey(
        MarketSelection,
        on_delete=models.PROTECT,
        related_name="cartela_items",
        verbose_name="Seleção"
    )
    odd_usada = models.FloatField(verbose_name="Odd Usada")
    
    class Meta:
        verbose_name = "Item da Cartela"
        verbose_name_plural = "Itens da Cartela"
        unique_together = ['cartela_instance', 'market_selection']
    
    def __str__(self):
        return f"{self.cartela_instance_id} - {self.market_selection_id}"


class Bet(models.Model):
    """Aposta ligada a uma cartela"""
    cartela = models.OneToOneField(
        CartelaInstance,
        on_delete=models.CASCADE,
        related_name="bet",
        verbose_name="Cartela"
    )
    stake = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor Apostado"
    )
    odd_final = models.FloatField(verbose_name="Odd Final")
    potential_return = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        verbose_name="Retorno Potencial"
    )
    is_won = models.BooleanField(null=True, blank=True, verbose_name="Ganhou?")
    settled_at = models.DateTimeField(null=True, blank=True, verbose_name="Liquidado em")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Aposta"
        verbose_name_plural = "Apostas"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Bet #{self.id} - Cartela #{self.cartela_id}"


class OddsSnapshot(models.Model):
    """Snapshot de odds para auditoria"""
    cartela = models.ForeignKey(
        CartelaInstance,
        on_delete=models.CASCADE,
        related_name="snapshots",
        verbose_name="Cartela"
    )
    data = models.JSONField(verbose_name="Dados")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Snapshot de Odds"
        verbose_name_plural = "Snapshots de Odds"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Snapshot #{self.id} - Cartela #{self.cartela_id}"


class RiskExposureMetrics(models.Model):
    """Métricas de exposição de risco"""
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="risk_metrics",
        verbose_name="Evento"
    )
    cartela_template = models.ForeignKey(
        CartelaTemplate,
        on_delete=models.CASCADE,
        related_name="risk_metrics",
        verbose_name="Template"
    )
    influencer = models.ForeignKey(
        Influencer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="risk_metrics",
        verbose_name="Influenciador"
    )
    volume_total = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        verbose_name="Volume Total"
    )
    payout_maximo = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        verbose_name="Payout Máximo"
    )
    margem_media = models.FloatField(default=0.0, verbose_name="Margem Média")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Métrica de Risco"
        verbose_name_plural = "Métricas de Risco"
        unique_together = ['event', 'cartela_template', 'influencer']
        indexes = [
            models.Index(fields=['event', 'cartela_template']),
        ]
    
    def __str__(self):
        return f"Risco - {self.event} - {self.cartela_template}"
