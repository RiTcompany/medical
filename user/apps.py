import os
from threading import Thread, Lock
from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    _scheduler_started = False
    _lock = Lock()

    def ready(self) -> None:
        import sys
        from user.scheduler import run_scheduler
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') == 'true':
            with self._lock:
                print("Starting scheduler...")
                scheduler_thread = Thread(target=run_scheduler, daemon=True)
                scheduler_thread.start()
                self._scheduler_started = True
