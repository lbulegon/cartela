from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Carteira


@receiver(post_save, sender=User)
def criar_carteira_usuario(sender, instance, created, **kwargs):
    """Cria automaticamente uma carteira quando um novo usuário é criado"""
    if created:
        Carteira.objects.get_or_create(usuario=instance)

