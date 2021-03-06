from authapp.models import KbankUser


class PersonalNotification:
    """
    Класс для создания персональных уведомлений
    """

    def __init__(self, request, body, title, url, scope=None, users_group=None):
        self.request = request
        self.body = body
        self.title = title
        self.url = url
        self.scope = scope
        self.users_group = users_group

    def create(self):
        from mainapp.models import Notification

        if self.scope == "all":
            users = KbankUser.objects.all()
        elif self.scope == "moderators":
            users = [user for user in KbankUser.objects.all() if user.is_privileged]
        else:
            users = self.users_group if self.users_group else [self.request.user]
        for user in users:
            obj = Notification.objects.create(
                user=user, body=self.body, title=self.title, url=self.url
            )
            obj.save()


# Формы времени в разных числах/падежах
TIME_VARIANTS = {
    "days": ["день", "дня", "дней"],
    "hours": ["час", "часа", "часов"],
    "minutes": ["минута", "минуты", "минут"],
}


def plural_time(num, type_: str):
    if num % 10 == 1 and num % 100 != 11:
        index = 0
    elif 2 <= num % 10 <= 4 and (num % 100 < 10 or num % 100 >= 20):
        index = 1
    else:
        index = 2

    return f"{num} {TIME_VARIANTS[type_][index]}"
