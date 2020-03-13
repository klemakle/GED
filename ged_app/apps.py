from django.apps import AppConfig


class GedAppConfig(AppConfig):
    name = 'ged_app'
    
    def ready(self):
        import ged_app.signals