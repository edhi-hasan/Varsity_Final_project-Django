from django.apps import AppConfig


class BloodologyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bloodology'

    def ready(self):
        import bloodology.signals 