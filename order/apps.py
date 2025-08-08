from django.apps import AppConfig

class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order'

    def ready(self):
        """
        This method is called when the app is ready.
        We import our signals here to register them.
        """
        import order.signals
