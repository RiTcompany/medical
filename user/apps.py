import os
from threading import Thread, Lock
from django.apps import AppConfig
from django.contrib.auth import get_user_model


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    _scheduler_started = False
    _lock = Lock()


    def ready(self) -> None:
        import sys
        import user.signals
        from user.scheduler import run_scheduler
        from client.models import Client
        from notification.firebase_service import initialize_firebase
        User = get_user_model()
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') == 'true':
            with self._lock:
                try:
                    users = User.objects.all()
                    for user in users:
                        if not user.client.all().exists():
                            Client.objects.create(user=user)
                            print(f'Client for user: {user} successfully created')
                except:
                    pass
                print("Starting scheduler...")
                scheduler_thread = Thread(target=run_scheduler, daemon=True)
                scheduler_thread.start()
                self._scheduler_started = True
                initialize_firebase()
