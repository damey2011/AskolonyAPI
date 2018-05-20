from Notification.models import NotificationCass
from AskolonyAPI.celery import app


@app.task(bind=True)
def createNotification(self, owner, actor, verb, action_object=None, target=None):
    try:
        NotificationCass.create(note_type="NM",
                                owner=owner,
                                actor=actor,
                                verb=verb,
                                target=target
                                )
    except Exception as e:
        self.retry(countdown=30, exc=2, max_retries=2)
