from django.apps import AppConfig


class ApiCadastroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_cadastro'

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import myapp.signals
