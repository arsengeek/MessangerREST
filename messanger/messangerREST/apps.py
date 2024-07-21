from django.apps import AppConfig


class MassengerrestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messangerREST'
    
class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messangerREST'

    def ready(self):
        import messangerREST.signals