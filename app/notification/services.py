from django.contrib.auth import get_user_model

from app.notification.selectors import get_notification_detail, get_notification_list
from app.notification.serializers import NotificationSerializer

User = get_user_model()


def get_notification_list_data(*, user: User):
    notification_list = get_notification_list(user=user)
    serializer = NotificationSerializer(notification_list, many=True)
    return serializer.data


def retrieve_notification(*, user: User, noti_pk: int):
    notification = get_notification_detail(user=user, noti_pk=noti_pk)
    notification.is_read = True
    notification.save(update_fields=["is_read"])
    serializer = NotificationSerializer(notification, many=False)
    return serializer.data


def delete_notification(*, user: User, noti_pk: int):
    notification = get_notification_detail(user=user, noti_pk=noti_pk)
    notification.delete()
    return None
