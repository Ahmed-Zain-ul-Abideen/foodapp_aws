from django.apps import AppConfig
import os

class WebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webApp'

    def ready(self):
        from . import jobs
        if os.environ.get('RUN_MAIN', None) != 'true':
            jobs.start_scheduler()
