from django.apps import AppConfig


class GaragesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'garages'

    def ready(self):
        import garages.signals