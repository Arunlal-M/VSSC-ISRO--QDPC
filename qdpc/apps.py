from django.apps import AppConfig


class QdpcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qdpc'

    def ready(self):
        import qdpc.signals
        # print("🔥 Signal file loaded")
