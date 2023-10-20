from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        # Import here to avoid AppRegistryNotReady error
        from api.tasks import repeated_function

        # Call the function when the app is ready
        repeated_function.delay()
