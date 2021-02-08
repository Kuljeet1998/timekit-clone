from django.apps import AppConfig


class KitConfig(AppConfig):
    name = 'kit'

    def ready(self):
        import kit.signals