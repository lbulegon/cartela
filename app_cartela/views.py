from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from decimal import Decimal, InvalidOperation
from .models import Carteira, Transacao


def login_view(request):
    """View para fazer login do usuário"""
    if request.user.is_authenticated:
        return redirect('app_cartela:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}!')
                next_url = request.GET.get('next', 'app_cartela:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
    
    return render(request, 'app_cartela/login.html')


@login_required
def logout_view(request):
    """View para fazer logout do usuário"""
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('app_cartela:login')


@login_required
def dashboard_view(request):
    """View do dashboard após login"""
    carteira, created = Carteira.objects.get_or_create(usuario=request.user)
    
    # Últimas 5 transações
    ultimas_transacoes = carteira.transacoes.all()[:5]
    
    return render(request, 'app_cartela/dashboard.html', {
        'user': request.user,
        'carteira': carteira,
        'ultimas_transacoes': ultimas_transacoes
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
    
    usuarios = User.objects.all().order_by('username')
    return render(request, 'app_cartela/bonus.html', {
        'usuarios': usuarios,
        'tipos': Transacao.TIPO_CHOICES
    })
