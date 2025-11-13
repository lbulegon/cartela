from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Carteira(models.Model):
    """Carteira do usuário para armazenar pontos e fundos"""
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='carteira',
        verbose_name='Usuário'
    )
    pontos = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Pontos'
    )
    fundos = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Fundos (R$)'
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Carteira'
        verbose_name_plural = 'Carteiras'
        ordering = ['-atualizado_em']

    def __str__(self):
        return f'Carteira de {self.usuario.username}'

    def adicionar_pontos(self, valor, descricao='', tipo='BONUS'):
        """Adiciona pontos à carteira e cria transação"""
        if valor <= 0:
            raise ValueError('O valor deve ser maior que zero')
        
        saldo_anterior_pontos = self.pontos
        saldo_anterior_fundos = self.fundos
        self.pontos += valor
        self.save()
        
        Transacao.objects.create(
            carteira=self,
            tipo=tipo,
            categoria='PONTOS',
            valor=valor,
            descricao=descricao or f'Adição de {valor} pontos',
            saldo_anterior_pontos=saldo_anterior_pontos,
            saldo_anterior_fundos=saldo_anterior_fundos
        )
        return self

    def adicionar_fundos(self, valor, descricao='', tipo='DEPOSITO'):
        """Adiciona fundos à carteira e cria transação"""
        if valor <= 0:
            raise ValueError('O valor deve ser maior que zero')
        
        saldo_anterior_pontos = self.pontos
        saldo_anterior_fundos = self.fundos
        self.fundos += valor
        self.save()
        
        Transacao.objects.create(
            carteira=self,
            tipo=tipo,
            categoria='FUNDOS',
            valor=valor,
            descricao=descricao or f'Adição de R$ {valor}',
            saldo_anterior_pontos=saldo_anterior_pontos,
            saldo_anterior_fundos=saldo_anterior_fundos
        )
        return self

    def debitar_pontos(self, valor, descricao=''):
        """Debita pontos da carteira e cria transação"""
        if valor <= 0:
            raise ValueError('O valor deve ser maior que zero')
        if self.pontos < valor:
            raise ValueError('Pontos insuficientes')
        
        saldo_anterior_pontos = self.pontos
        saldo_anterior_fundos = self.fundos
        self.pontos -= valor
        self.save()
        
        Transacao.objects.create(
            carteira=self,
            tipo='DEBITO',
            categoria='PONTOS',
            valor=-valor,
            descricao=descricao or f'Débito de {valor} pontos',
            saldo_anterior_pontos=saldo_anterior_pontos,
            saldo_anterior_fundos=saldo_anterior_fundos
        )
        return self

    def debitar_fundos(self, valor, descricao=''):
        """Debita fundos da carteira e cria transação"""
        if valor <= 0:
            raise ValueError('O valor deve ser maior que zero')
        if self.fundos < valor:
            raise ValueError('Fundos insuficientes')
        
        saldo_anterior_pontos = self.pontos
        saldo_anterior_fundos = self.fundos
        self.fundos -= valor
        self.save()
        
        Transacao.objects.create(
            carteira=self,
            tipo='DEBITO',
            categoria='FUNDOS',
            valor=-valor,
            descricao=descricao or f'Débito de R$ {valor}',
            saldo_anterior_pontos=saldo_anterior_pontos,
            saldo_anterior_fundos=saldo_anterior_fundos
        )
        return self


class Transacao(models.Model):
    """Histórico de transações da carteira"""
    
    TIPO_CHOICES = [
        ('DEPOSITO', 'Depósito'),
        ('BONUS', 'Bônus'),
        ('PREMIO', 'Prêmio'),
        ('DEBITO', 'Débito'),
        ('SAQUE', 'Saque'),
        ('APOSTA', 'Aposta'),
        ('GANHO', 'Ganho'),
    ]
    
    CATEGORIA_CHOICES = [
        ('PONTOS', 'Pontos'),
        ('FUNDOS', 'Fundos'),
    ]
    
    carteira = models.ForeignKey(
        Carteira,
        on_delete=models.CASCADE,
        related_name='transacoes',
        verbose_name='Carteira'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name='Tipo'
    )
    categoria = models.CharField(
        max_length=10,
        choices=CATEGORIA_CHOICES,
        verbose_name='Categoria'
    )
    valor = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Valor'
    )
    descricao = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Descrição'
    )
    saldo_anterior_pontos = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Saldo Anterior (Pontos)'
    )
    saldo_anterior_fundos = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Saldo Anterior (Fundos)'
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['-criado_em']),
            models.Index(fields=['carteira', '-criado_em']),
        ]

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.carteira.usuario.username} - {self.valor}'

    @property
    def valor_formatado(self):
        """Retorna o valor formatado com sinal"""
        if self.categoria == 'PONTOS':
            return f'{self.valor:+.2f} pontos'
        return f'R$ {self.valor:+.2f}'
