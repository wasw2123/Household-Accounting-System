from django.contrib.auth import get_user_model

from app.notification.models import Notification

User = get_user_model()


def mark_notification_as_read(notification: Notification) -> Notification:
    notification.is_read = True
    notification.save(update_fields=["is_read"])
    return notification


def delete_notification(notification: Notification):
    notification.delete()
    return None
