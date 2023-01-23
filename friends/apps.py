from django.apps import AppConfig


class FriendsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'friends'

    def ready(self):
        # Implicity connect signal handlers decorated with @receiver
        from . import signals
        