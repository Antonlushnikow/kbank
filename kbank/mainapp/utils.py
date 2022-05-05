from .models import Notification
from authapp.models import KbankUser


def create_notification(request, body, scope=None):
    if scope == "all":
        users = KbankUser.objects.all()
    elif scope == "moderators":
        users = [user for user in KbankUser.objects.all() if user.is_privileged]
    else:
        users = [request.user]
    for user in users:
        obj = Notification.objects.create(user=user, body=body)
        obj.save()
