
from django.apps import AppConfig

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        from django.contrib.sessions.models import Session
        from django.db.utils import OperationalError, ProgrammingError

        try:
            Session.objects.all().delete()
        except (OperationalError, ProgrammingError):
            pass