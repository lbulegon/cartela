from django.apps import AppConfig


class AppCartelaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_cartela'
    
    def ready(self):
        import app_cartela.signals  # Importa os signals