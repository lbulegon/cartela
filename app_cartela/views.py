from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
    return render(request, 'app_cartela/dashboard.html', {
        'user': request.user
    })
