from django.urls import path
from . import views

app_name = 'app_cartela'

urlpatterns = [
    # Autenticação do jogador
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.register_view, name='register'),
    path('recuperar-senha/', views.password_reset_request_view, name='password_reset_request'),
    path('recuperar-senha/<str:uidb64>/<str:token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    
    # Login administrativo
    path('empresa/login/', views.admin_login_view, name='admin_login'),
    
    # Logout
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('empresa/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # Funcionalidades do jogador
    path('carteira/', views.carteira_view, name='carteira'),
    path('deposito/', views.deposito_view, name='deposito'),
    path('bonus/', views.bonus_view, name='bonus'),
    path('evento/<int:event_id>/', views.evento_view, name='evento'),
    path('cartela/<int:cartela_id>/', views.cartela_detail_view, name='cartela_detail'),
]

