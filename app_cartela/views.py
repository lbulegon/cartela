from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from decimal import Decimal, InvalidOperation
from .models import Carteira, Transacao


def login_view(request):
    """View para fazer login do jogador/cliente"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('app_cartela:admin_dashboard')
        return redirect('app_cartela:dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            # Busca o usuário pelo email
            from django.contrib.auth.models import User
            try:
                user = User.objects.get(email=email)
                # Autentica usando o username do usuário encontrado
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Bem-vindo, {user.username}!')
                    # Redireciona baseado no tipo de usuário
                    if user.is_staff:
                        return redirect('app_cartela:admin_dashboard')
                    next_url = request.GET.get('next', 'app_cartela:dashboard')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Email ou senha incorretos.')
            except User.DoesNotExist:
                messages.error(request, 'Email ou senha incorretos.')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
    
    return render(request, 'app_cartela/login.html')


def admin_login_view(request):
    """View para fazer login administrativo da empresa"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('app_cartela:admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    messages.success(request, f'Bem-vindo, {user.username}!')
                    next_url = request.GET.get('next', 'app_cartela:admin_dashboard')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta área.')
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
    
    return render(request, 'app_cartela/admin_login.html')


@login_required
def logout_view(request):
    """View para fazer logout do usuário"""
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('app_cartela:login')


@login_required
def dashboard_view(request):
    """View do dashboard do jogador/cliente"""
    from betting.models import Bet, CartelaInstance
    
    carteira, created = Carteira.objects.get_or_create(usuario=request.user)
    
    # Últimas 5 transações
    ultimas_transacoes = carteira.transacoes.all()[:5]
    
    # Últimas apostas do usuário
    ultimas_apostas = Bet.objects.filter(
        cartela__user=request.user
    ).select_related(
        'cartela',
        'cartela__event',
        'cartela__cartela_template'
    ).order_by('-created_at')[:5]
    
    # Cartelas pendentes (em APOSTA_PENDENTE)
    cartelas_pendentes = CartelaInstance.objects.filter(
        user=request.user,
        status='APOSTA_PENDENTE'
    ).select_related('event', 'cartela_template').order_by('-created_at')[:5]
    
    return render(request, 'app_cartela/jogador_dashboard.html', {
        'user': request.user,
        'carteira': carteira,
        'ultimas_transacoes': ultimas_transacoes,
        'ultimas_apostas': ultimas_apostas,
        'cartelas_pendentes': cartelas_pendentes,
    })


@login_required
def admin_dashboard_view(request):
    """View do dashboard administrativo da empresa"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('app_cartela:dashboard')
    
    from betting.models import (
        Event, Bet, CartelaInstance, RiskExposureMetrics,
        CartelaTemplate, MarketSelection, Influencer
    )
    from app_cartela.models import Carteira, Transacao
    from django.contrib.auth.models import User
    from django.db.models import Sum, Count, Q, Avg
    from django.utils import timezone
    from datetime import timedelta
    
    # Estatísticas gerais
    total_usuarios = User.objects.count()
    usuarios_hoje = User.objects.filter(
        date_joined__date=timezone.now().date()
    ).count()
    
    total_eventos = Event.objects.count()
    eventos_hoje = Event.objects.filter(
        start_time__date=timezone.now().date()
    ).count()
    eventos_ao_vivo = Event.objects.filter(status='LIVE').count()
    eventos_agendados = Event.objects.filter(status='SCHEDULED').count()
    
    # Estatísticas de cartelas
    total_cartelas = CartelaInstance.objects.count()
    cartelas_pendentes_count = CartelaInstance.objects.filter(
        status='APOSTA_PENDENTE'
    ).count()
    cartelas_confirmadas = CartelaInstance.objects.filter(
        status='APOSTA_CONFIRMADA'
    ).count()
    total_templates = CartelaTemplate.objects.filter(ativo=True).count()
    
    # Estatísticas de seleções/quadrinhos
    total_selecoes = MarketSelection.objects.count()
    selecoes_ao_vivo = MarketSelection.objects.filter(is_live=True).count()
    
    # Estatísticas de apostas
    total_apostas = Bet.objects.count()
    apostas_hoje = Bet.objects.filter(
        created_at__date=timezone.now().date()
    ).count()
    apostas_pendentes = Bet.objects.filter(is_won__isnull=True).count()
    apostas_ganhas = Bet.objects.filter(is_won=True).count()
    apostas_perdidas = Bet.objects.filter(is_won=False).count()
    
    # Volume financeiro
    volume_total = Bet.objects.aggregate(
        total=Sum('stake')
    )['total'] or 0
    
    volume_hoje = Bet.objects.filter(
        created_at__date=timezone.now().date()
    ).aggregate(
        total=Sum('stake')
    )['total'] or 0
    
    payout_total = Bet.objects.filter(is_won=True).aggregate(
        total=Sum('potential_return')
    )['total'] or 0
    
    # Carteiras
    total_carteiras = Carteira.objects.count()
    saldo_total_pontos = Carteira.objects.aggregate(
        total=Sum('pontos')
    )['total'] or 0
    saldo_total_fundos = Carteira.objects.aggregate(
        total=Sum('fundos')
    )['total'] or 0
    
    # Transações
    total_transacoes = Transacao.objects.count()
    transacoes_hoje = Transacao.objects.filter(
        criado_em__date=timezone.now().date()
    ).count()
    
    # Métricas de risco
    risco_alto = RiskExposureMetrics.objects.filter(
        payout_maximo__gt=10000
    ).count()
    risco_medio = RiskExposureMetrics.objects.filter(
        payout_maximo__gt=5000,
        payout_maximo__lte=10000
    ).count()
    
    # Influenciadores
    total_influenciadores = Influencer.objects.filter(is_active=True).count()
    
    # Eventos recentes
    eventos_recentes = Event.objects.filter(
        status__in=['SCHEDULED', 'LIVE']
    ).order_by('start_time')[:10]
    
    # Apostas recentes
    apostas_recentes = Bet.objects.select_related(
        'cartela',
        'cartela__user',
        'cartela__event',
        'cartela__cartela_template'
    ).order_by('-created_at')[:10]
    
    # Cartelas pendentes
    cartelas_pendentes = CartelaInstance.objects.filter(
        status='APOSTA_PENDENTE'
    ).select_related('user', 'event', 'cartela_template').order_by('-created_at')[:10]
    
    # Templates de cartela
    templates_ativos = CartelaTemplate.objects.filter(ativo=True).order_by('tipo', 'nome')
    
    return render(request, 'app_cartela/admin_dashboard.html', {
        'user': request.user,
        # Usuários
        'total_usuarios': total_usuarios,
        'usuarios_hoje': usuarios_hoje,
        # Eventos
        'total_eventos': total_eventos,
        'eventos_hoje': eventos_hoje,
        'eventos_ao_vivo': eventos_ao_vivo,
        'eventos_agendados': eventos_agendados,
        # Cartelas
        'total_cartelas': total_cartelas,
        'cartelas_pendentes_count': cartelas_pendentes_count,
        'cartelas_confirmadas': cartelas_confirmadas,
        'total_templates': total_templates,
        'total_selecoes': total_selecoes,
        'selecoes_ao_vivo': selecoes_ao_vivo,
        # Apostas
        'total_apostas': total_apostas,
        'apostas_hoje': apostas_hoje,
        'apostas_pendentes': apostas_pendentes,
        'apostas_ganhas': apostas_ganhas,
        'apostas_perdidas': apostas_perdidas,
        # Financeiro
        'volume_total': volume_total,
        'volume_hoje': volume_hoje,
        'payout_total': payout_total,
        # Carteiras
        'total_carteiras': total_carteiras,
        'saldo_total_pontos': saldo_total_pontos,
        'saldo_total_fundos': saldo_total_fundos,
        # Transações
        'total_transacoes': total_transacoes,
        'transacoes_hoje': transacoes_hoje,
        # Risco
        'risco_alto': risco_alto,
        'risco_medio': risco_medio,
        # Influenciadores
        'total_influenciadores': total_influenciadores,
        # Listas
        'eventos_recentes': eventos_recentes,
        'apostas_recentes': apostas_recentes,
        'cartelas_pendentes': cartelas_pendentes,
        'templates_ativos': templates_ativos,
    })


@login_required
def carteira_view(request):
    """View para visualizar a carteira completa"""
    carteira, created = Carteira.objects.get_or_create(usuario=request.user)
    
    # Filtros
    tipo_filter = request.GET.get('tipo', '')
    categoria_filter = request.GET.get('categoria', '')
    
    # Query das transações
    transacoes = carteira.transacoes.all()
    
    if tipo_filter:
        transacoes = transacoes.filter(tipo=tipo_filter)
    if categoria_filter:
        transacoes = transacoes.filter(categoria=categoria_filter)
    
    # Paginação
    paginator = Paginator(transacoes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'app_cartela/carteira.html', {
        'carteira': carteira,
        'page_obj': page_obj,
        'tipo_filter': tipo_filter,
        'categoria_filter': categoria_filter,
        'tipos': Transacao.TIPO_CHOICES,
        'categorias': Transacao.CATEGORIA_CHOICES,
    })


@login_required
def deposito_view(request):
    """View para realizar depósito"""
    carteira, created = Carteira.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        valor_str = request.POST.get('valor', '').replace(',', '.')
        try:
            valor = Decimal(valor_str)
            if valor <= 0:
                messages.error(request, 'O valor deve ser maior que zero.')
            else:
                carteira.adicionar_fundos(valor, descricao='Depósito realizado', tipo='DEPOSITO')
                messages.success(request, f'Depósito de R$ {valor:.2f} realizado com sucesso!')
                return redirect('app_cartela:carteira')
        except (ValueError, InvalidOperation):
            messages.error(request, 'Valor inválido.')
    
    return render(request, 'app_cartela/deposito.html', {
        'carteira': carteira
    })


@login_required
def bonus_view(request):
    """View para adicionar bônus (apenas para administradores)"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado.')
        return redirect('app_cartela:dashboard')
    
    carteira, created = Carteira.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        valor_str = request.POST.get('valor', '').replace(',', '.')
        descricao = request.POST.get('descricao', '')
        tipo_bonus = request.POST.get('tipo', 'BONUS')  # BONUS ou PREMIO
        
        try:
            from django.contrib.auth.models import User
            usuario = get_object_or_404(User, id=usuario_id)
            carteira_usuario, _ = Carteira.objects.get_or_create(usuario=usuario)
            valor = Decimal(valor_str)
            
            if valor <= 0:
                messages.error(request, 'O valor deve ser maior que zero.')
            else:
                if request.POST.get('categoria') == 'PONTOS':
                    carteira_usuario.adicionar_pontos(valor, descricao=descricao, tipo=tipo_bonus)
                    messages.success(request, f'{tipo_bonus} de {valor:.2f} pontos adicionado para {usuario.username}!')
                else:
                    carteira_usuario.adicionar_fundos(valor, descricao=descricao, tipo=tipo_bonus)
                    messages.success(request, f'{tipo_bonus} de R$ {valor:.2f} adicionado para {usuario.username}!')
                return redirect('app_cartela:bonus')
        except (ValueError, InvalidOperation):
            messages.error(request, 'Valor inválido.')
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')
    
    from django.contrib.auth.models import User
    usuarios = User.objects.all().order_by('username')
    return render(request, 'app_cartela/bonus.html', {
        'usuarios': usuarios,
        'tipos': Transacao.TIPO_CHOICES
    })


@login_required
def evento_view(request, event_id):
    """View para visualizar um evento e seus templates de cartela"""
    from betting.models import Event, CartelaTemplate, MarketSelection
    
    evento = get_object_or_404(Event, id=event_id)
    templates = CartelaTemplate.objects.filter(ativo=True)
    
    # Seleções disponíveis (pode filtrar por template depois)
    selecoes = MarketSelection.objects.filter(event=evento)
    
    return render(request, 'app_cartela/evento.html', {
        'evento': evento,
        'templates': templates,
        'selecoes': selecoes,
    })


@login_required
def cartela_detail_view(request, cartela_id):
    """View para visualizar detalhes de uma cartela"""
    from betting.models import CartelaInstance
    
    cartela = get_object_or_404(
        CartelaInstance.objects.select_related('event', 'cartela_template', 'user')
        .prefetch_related('items', 'items__market_selection'),
        id=cartela_id,
        user=request.user
    )
    
    return render(request, 'app_cartela/cartela_detail.html', {
        'cartela': cartela,
    })
