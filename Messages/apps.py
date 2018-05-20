from django.apps import AppConfig


class MessagesConfig(AppConfig):
    name = 'Messages'

    def ready(self):
        import Messages.signals