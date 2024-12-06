from django.apps import AppConfig

class MainConfig(AppConfig):  # Replace "Main" with your app name
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        import main.signals  # Ensure your signals are imported

