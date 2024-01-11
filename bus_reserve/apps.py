from django.apps import AppConfig


class BusReserveConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bus_reserve"

    def ready(self) -> None:
        import bus_reserve.signals
