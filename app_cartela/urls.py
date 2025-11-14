from django.urls import path
from . import views

app_name = 'app_cartela'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('carteira/', views.carteira_view, name='carteira'),
    path('deposito/', views.deposito_view, name='deposito'),
    path('bonus/', views.bonus_view, name='bonus'),
    path('evento/<int:event_id>/', views.evento_view, name='evento'),
    path('cartela/<int:cartela_id>/', views.cartela_detail_view, name='cartela_detail'),
]

